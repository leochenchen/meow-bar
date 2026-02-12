import AppKit
import Foundation

final class StatusBarController {
    private let statusItem: NSStatusItem
    private var animationTimer: Timer?
    private var autoTransitionTimer: Timer?
    private var idleTimer: Timer?
    private var statusTextTimer: Timer?
    private var currentFrameIndex = 0
    private var currentState: CatState = .idle
    private var currentStateData: MeowStateData = .empty
    private var frames: [NSImage] = []
    private let stateWatcher = StateWatcher()
    private let framesDir: String

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
            button.imagePosition = .imageLeft
        }

        loadFrames(for: .idle)
        startAnimation()
        rebuildMenu()

        stateWatcher.onStateChange = { [weak self] state in
            self?.handleStateChange(state)
        }
        stateWatcher.start()

        updateStatusBarText()

        // Refresh duration display every 30s
        statusTextTimer = Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { [weak self] _ in
            self?.updateStatusBarText()
        }

        NotificationManager.shared.requestPermission()
        resetIdleTimer()
    }

    // MARK: - State Handling

    private func handleStateChange(_ stateData: MeowStateData) {
        let newState = stateData.state
        currentStateData = stateData

        guard newState != currentState else {
            updateStatusBarText()
            rebuildMenu()
            return
        }

        currentState = newState

        // Send macOS notification for important events
        NotificationManager.shared.sendStateNotification(
            state: newState,
            errorMessage: stateData.errorMessage
        )

        loadFrames(for: newState)
        startAnimation()
        updateStatusBarText()
        rebuildMenu()

        // Auto-transition (complete → idle after 6s)
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
        // Use yellow "waiting" frames when idle with active session
        let prefix: String
        let count: Int
        if state == .idle,
           let sid = currentStateData.sessionId, !sid.isEmpty {
            prefix = "waiting"
            count = 4
        } else {
            prefix = state.framePrefix
            count = state.frameCount
        }

        for i in 0..<count {
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

    // MARK: - Status Bar Text

    private func updateStatusBarText() {
        guard let button = statusItem.button else { return }
        var text = ""

        switch currentState {
        case .working:
            text = " fine, on it"
        case .complete:
            text = " done!"
        case .error:
            text = " oops"
        case .idle:
            if let sid = currentStateData.sessionId, !sid.isEmpty {
                text = " your turn"
            } else {
                text = ""
            }
        }

        let attrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.monospacedDigitSystemFont(ofSize: 11, weight: .regular),
            .baselineOffset: 1
        ]
        button.attributedTitle = NSAttributedString(string: text, attributes: attrs)
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

        // Feed the cat when complete!
        if currentState == .complete {
            menu.addItem(NSMenuItem.separator())
            let feedItem = NSMenuItem(
                title: "\u{1F356} Feed the cat",
                action: #selector(feedCat),
                keyEquivalent: ""
            )
            feedItem.target = self
            menu.addItem(feedItem)
        }

        menu.addItem(NSMenuItem.separator())

        let quitItem = NSMenuItem(title: "Quit MeowBar", action: #selector(quit), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)

        statusItem.menu = menu
    }

    // MARK: - Actions

    @objc private func feedCat() {
        // Feed the cat meat! Transition to idle (satisfied)
        currentState = .idle
        loadFrames(for: .idle)
        startAnimation()
        updateStatusBarText()
        rebuildMenu()
    }

    @objc private func quit() {
        NSApplication.shared.terminate(nil)
    }

    // MARK: - Helpers

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
