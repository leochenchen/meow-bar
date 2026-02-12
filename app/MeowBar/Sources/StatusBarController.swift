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
    private var statsEnabled: Bool {
        get { UserDefaults.standard.object(forKey: "statsEnabled") as? Bool ?? true }
        set { UserDefaults.standard.set(newValue, forKey: "statsEnabled") }
    }
    private var eventsEnabled: Bool {
        get { UserDefaults.standard.object(forKey: "eventsEnabled") as? Bool ?? true }
        set { UserDefaults.standard.set(newValue, forKey: "eventsEnabled") }
    }

    init() {
        let bundleFrames = Bundle.main.resourcePath.map { "\($0)/Frames" } ?? ""
        let homeFrames = FileManager.default.homeDirectoryForCurrentUser.path + "/.meow-bar/frames"
        if FileManager.default.fileExists(atPath: bundleFrames) {
            framesDir = bundleFrames
        } else {
            framesDir = homeFrames
        }

        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        if let button = statusItem.button {
            button.imagePosition = .imageOnly
        }

        loadFrames(for: .idle)
        startAnimation()
        rebuildMenu()

        stateWatcher.onStateChange = { [weak self] state in
            self?.handleStateChange(state)
        }
        stateWatcher.start()

        NotificationManager.shared.requestPermission()
        resetIdleTimer()
    }

    // MARK: - State Handling

    private func handleStateChange(_ stateData: MeowStateData) {
        let newState = stateData.state
        currentStateData = stateData

        guard newState != currentState else {
            rebuildMenu()
            return
        }

        currentState = newState

        // Send macOS notification for important events
        if notificationsEnabled {
            NotificationManager.shared.sendStateNotification(
                state: newState,
                errorMessage: stateData.errorMessage
            )
        }

        loadFrames(for: newState)
        startAnimation()
        rebuildMenu()

        // Auto-transition (complete → idle after 5s, error → idle after 3s)
        autoTransitionTimer?.invalidate()
        if let duration = newState.autoTransitionDuration {
            autoTransitionTimer = Timer.scheduledTimer(withTimeInterval: duration, repeats: false) { [weak self] _ in
                guard let self = self else { return }
                self.currentState = newState.autoTransitionTarget
                self.loadFrames(for: self.currentState)
                self.startAnimation()
                self.rebuildMenu()
            }
        }

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
                image.size = NSSize(width: 22, height: 22)
                image.isTemplate = false
                frames.append(image)
            }
        }

        if frames.isEmpty {
            let fallback = createTextIcon(state.emoji)
            frames = [fallback]
        }

        currentFrameIndex = 0
    }

    private func startAnimation() {
        animationTimer?.invalidate()
        guard !frames.isEmpty else { return }
        statusItem.button?.image = frames[0]
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

        // Session stats (toggleable)
        if statsEnabled {
            let statsHeader = NSMenuItem(title: "Session Stats", action: nil, keyEquivalent: "")
            statsHeader.isEnabled = false
            menu.addItem(statsHeader)

            // Duration
            if let startStr = currentStateData.sessionStartTime, !startStr.isEmpty {
                let duration = calcDuration(from: startStr)
                let item = NSMenuItem(title: "  Duration: \(duration)", action: nil, keyEquivalent: "")
                item.isEnabled = false
                menu.addItem(item)
            }

            // Prompts
            let prompts = currentStateData.promptCount ?? 0
            let promptItem = NSMenuItem(title: "  Prompts: \(prompts)", action: nil, keyEquivalent: "")
            promptItem.isEnabled = false
            menu.addItem(promptItem)

            // Tool calls
            let tools = currentStateData.toolCallCount ?? 0
            let toolItem = NSMenuItem(title: "  Tool calls: \(tools)", action: nil, keyEquivalent: "")
            toolItem.isEnabled = false
            menu.addItem(toolItem)

            // Errors
            let errors = currentStateData.errorCount ?? 0
            if errors > 0 {
                let errItem = NSMenuItem(title: "  Errors: \(errors)", action: nil, keyEquivalent: "")
                errItem.isEnabled = false
                menu.addItem(errItem)
            }

            menu.addItem(NSMenuItem.separator())
        }

        // Recent events (toggleable)
        if eventsEnabled, let events = currentStateData.eventsLog, !events.isEmpty {
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

        // Toggle options
        let statsToggle = NSMenuItem(
            title: "Show Stats",
            action: #selector(toggleStats),
            keyEquivalent: ""
        )
        statsToggle.target = self
        statsToggle.state = statsEnabled ? .on : .off
        menu.addItem(statsToggle)

        let eventsToggle = NSMenuItem(
            title: "Show Events",
            action: #selector(toggleEvents),
            keyEquivalent: ""
        )
        eventsToggle.target = self
        eventsToggle.state = eventsEnabled ? .on : .off
        menu.addItem(eventsToggle)

        let notifToggle = NSMenuItem(
            title: "Push Notifications",
            action: #selector(toggleNotifications),
            keyEquivalent: ""
        )
        notifToggle.target = self
        notifToggle.state = notificationsEnabled ? .on : .off
        menu.addItem(notifToggle)

        menu.addItem(NSMenuItem.separator())

        let quitItem = NSMenuItem(title: "Quit MeowBar", action: #selector(quit), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)

        statusItem.menu = menu
    }

    // MARK: - Actions

    @objc private func toggleStats() {
        statsEnabled.toggle()
        rebuildMenu()
    }

    @objc private func toggleEvents() {
        eventsEnabled.toggle()
        rebuildMenu()
    }

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
            return String(isoString.suffix(8))
        }
        let display = DateFormatter()
        display.dateFormat = "HH:mm:ss"
        return display.string(from: date)
    }

    private func calcDuration(from isoString: String) -> String {
        let formatter = ISO8601DateFormatter()
        guard let start = formatter.date(from: isoString) else { return "—" }
        let elapsed = Int(Date().timeIntervalSince(start))
        if elapsed < 60 { return "\(elapsed)s" }
        if elapsed < 3600 { return "\(elapsed / 60)m \(elapsed % 60)s" }
        return "\(elapsed / 3600)h \((elapsed % 3600) / 60)m"
    }

    private func createTextIcon(_ text: String) -> NSImage {
        let size = NSSize(width: 22, height: 22)
        let image = NSImage(size: size)
        image.lockFocus()
        let attrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 16)
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
