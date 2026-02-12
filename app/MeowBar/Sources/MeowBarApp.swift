import AppKit

class AppDelegate: NSObject, NSApplicationDelegate {
    var statusBarController: StatusBarController?

    func applicationDidFinishLaunching(_ notification: Notification) {
        statusBarController = StatusBarController()
        print("[MeowBar] Started! Watching ~/.claude/meow-state.json")
    }
}

@main
enum MeowBarLauncher {
    static func main() {
        let app = NSApplication.shared
        app.setActivationPolicy(.accessory) // No dock icon

        let delegate = AppDelegate()
        app.delegate = delegate

        app.run()
    }
}
