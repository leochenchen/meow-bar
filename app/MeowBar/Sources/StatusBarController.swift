import AppKit
import Foundation

final class StatusBarController {
    private let statusItem: NSStatusItem
    private var animationTimer: Timer?
    private var autoTransitionTimer: Timer?
    private var idleTimer: Timer?
    private var currentFrameIndex = 0
    private var currentState: CatState = .idle
    private var currentStateData: MeowStateData = .empty
    private var frames: [NSImage] = []
    private let stateWatcher = StateWatcher()
    private let framesDir: String

    // User preferences
    private var notificationsEnabled: Bool {
        get { UserDefaults.standard.object(forKey: "notificationsEnabled") as? Bool ?? true }
        set { UserDefaults.standard.set(newValue, forKey: "notificationsEnabled") }
    }

    init() {
        // Resolve frames directory: check bundle first, then known install paths
        let bundleFrames = Bundle.main.resourcePath.map { "\($0)/Frames" } ?? ""
        let homeFrames = FileManager.default.homeDirectoryForCurrentUser.path + "/.meow-bar/frames"
        if FileManager.default.fileExists(atPath: bundleFrames) {
            framesDir = bundleFrames
        } else if FileManager.default.fileExists(atPath: homeFrames) {
            framesDir = homeFrames
        } else {
            framesDir = homeFrames
        }

        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)

        if let button = statusItem.button {
            button.imagePosition = .imageOnly
        }

        // Load initial frames and start animation
        loadFrames(for: .idle)
        startAnimation()

        // Build menu
        rebuildMenu()

        // Start watching state file
        stateWatcher.onStateChange = { [weak self] state in
            self?.handleStateChange(state)
        }
        stateWatcher.start()

        // Request notification permission
        NotificationManager.shared.requestPermission()

        // Start idle detection timer
        resetIdleTimer()
    }

    // MARK: - State Handling

    private func handleStateChange(_ stateData: MeowStateData) {
        let newState = stateData.state
        currentStateData = stateData

        guard newState != currentState else {
            // Still update the menu even if state hasn't changed
            rebuildMenu()
            return
        }

        currentState = newState

        // Send notification for important state changes
        if notificationsEnabled {
            NotificationManager.shared.sendStateNotification(
                state: newState,
                errorMessage: stateData.errorMessage
            )
        }

        // Update animation
        loadFrames(for: newState)
        startAnimation()

        // Rebuild menu with new info
        rebuildMenu()

        // Handle auto-transitions
        autoTransitionTimer?.invalidate()
        if let duration = newState.autoTransitionDuration {
            autoTransitionTimer = Timer.scheduledTimer(withTimeInterval: duration, repeats: false) { [weak self] _ in
                guard let self = self else { return }
                let target = newState.autoTransitionTarget
                self.currentState = target
                self.loadFrames(for: target)
                self.startAnimation()
                self.rebuildMenu()
            }
        }

        // Reset idle detection
        resetIdleTimer()
    }

    // MARK: - Animation

    private func loadFrames(for state: CatState) {
        frames = []
        let prefix = state.framePrefix

        for i in 0..<state.frameCount {
            let name = "\(prefix)-\(i)"
            let path = "\(framesDir)/\(name).png"
            if let image = NSImage(contentsOfFile: path) {
                image.size = NSSize(width: 18, height: 18)
                image.isTemplate = false // Keep colors!
                frames.append(image)
            }
        }

        // Fallback: if no frames loaded, create a text-based icon
        if frames.isEmpty {
            let fallback = createTextIcon(state.emoji)
            frames = [fallback]
        }

        currentFrameIndex = 0
    }

    private func startAnimation() {
        animationTimer?.invalidate()

        guard !frames.isEmpty else { return }

        // Show first frame immediately
        statusItem.button?.image = frames[0]

        // If only one frame, no need to animate
        guard frames.count > 1 else { return }

        let interval = currentState.animationInterval
        animationTimer = Timer.scheduledTimer(withTimeInterval: interval, repeats: true) { [weak self] _ in
            guard let self = self, !self.frames.isEmpty else { return }
            self.currentFrameIndex = (self.currentFrameIndex + 1) % self.frames.count
            self.statusItem.button?.image = self.frames[self.currentFrameIndex]
        }
    }

    // MARK: - Idle Detection

    private func resetIdleTimer() {
        idleTimer?.invalidate()
        idleTimer = Timer.scheduledTimer(withTimeInterval: 120, repeats: false) { [weak self] _ in
            guard let self = self, self.currentState != .idle else { return }
            self.currentState = .idle
            self.loadFrames(for: .idle)
            self.startAnimation()
            self.rebuildMenu()
        }
    }

    // MARK: - Menu

    private func rebuildMenu() {
        let menu = NSMenu()

        // Status header
        let headerTitle = "\(currentState.emoji)  \(currentState.displayName)"
        let header = NSMenuItem(title: headerTitle, action: nil, keyEquivalent: "")
        header.isEnabled = false
        menu.addItem(header)

        // Session info
        if let sid = currentStateData.sessionId, !sid.isEmpty {
            let sessionItem = NSMenuItem(
                title: "Session: \(String(sid.prefix(12)))...",
                action: nil, keyEquivalent: ""
            )
            sessionItem.isEnabled = false
            menu.addItem(sessionItem)
        }

        // Last tool
        if let tool = currentStateData.toolName, !tool.isEmpty, tool != "null" {
            let toolItem = NSMenuItem(title: "Last tool: \(tool)", action: nil, keyEquivalent: "")
            toolItem.isEnabled = false
            menu.addItem(toolItem)
        }

        // Error message
        if currentState == .error, let err = currentStateData.errorMessage, !err.isEmpty {
            menu.addItem(NSMenuItem.separator())
            let errItem = NSMenuItem(title: "\u{26A0} \(err)", action: nil, keyEquivalent: "")
            errItem.isEnabled = false
            menu.addItem(errItem)
        }

        menu.addItem(NSMenuItem.separator())

        // Recent events
        if let events = currentStateData.eventsLog, !events.isEmpty {
            let eventsHeader = NSMenuItem(title: "Recent Events", action: nil, keyEquivalent: "")
            eventsHeader.isEnabled = false
            menu.addItem(eventsHeader)

            for event in events.suffix(5) {
                let timeStr = formatTime(event.time)
                let detail = event.detail.isEmpty ? event.event : "\(event.event): \(event.detail)"
                let item = NSMenuItem(title: "  \(timeStr) \(detail)", action: nil, keyEquivalent: "")
                item.isEnabled = false
                if let font = NSFont.monospacedSystemFont(ofSize: 11, weight: .regular) as NSFont? {
                    item.attributedTitle = NSAttributedString(
                        string: "  \(timeStr) \(detail)",
                        attributes: [.font: font]
                    )
                }
                menu.addItem(item)
            }

            menu.addItem(NSMenuItem.separator())
        }

        // Notification toggle
        let notifItem = NSMenuItem(
            title: "Notifications",
            action: #selector(toggleNotifications),
            keyEquivalent: ""
        )
        notifItem.target = self
        notifItem.state = notificationsEnabled ? .on : .off
        menu.addItem(notifItem)

        menu.addItem(NSMenuItem.separator())

        // Quit
        let quitItem = NSMenuItem(title: "Quit MeowBar", action: #selector(quit), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)

        statusItem.menu = menu
    }

    // MARK: - Actions

    @objc private func toggleNotifications() {
        notificationsEnabled.toggle()
        rebuildMenu()
    }

    @objc private func quit() {
        NSApplication.shared.terminate(nil)
    }

    // MARK: - Helpers

    private func formatTime(_ isoString: String) -> String {
        let formatter = ISO8601DateFormatter()
        guard let date = formatter.date(from: isoString) else {
            return isoString.suffix(8).description
        }
        let display = DateFormatter()
        display.dateFormat = "HH:mm:ss"
        return display.string(from: date)
    }

    private func createTextIcon(_ text: String) -> NSImage {
        let size = NSSize(width: 18, height: 18)
        let image = NSImage(size: size)
        image.lockFocus()

        let attrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 14)
        ]
        let str = NSAttributedString(string: text, attributes: attrs)
        let strSize = str.size()
        let point = NSPoint(
            x: (size.width - strSize.width) / 2,
            y: (size.height - strSize.height) / 2
        )
        str.draw(at: point)

        image.unlockFocus()
        image.isTemplate = false
        return image
    }
}
