import Foundation
import UserNotifications

final class NotificationManager {
    static let shared = NotificationManager()

    private init() {}

    func requestPermission() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound]) { granted, _ in
            if granted {
                print("[MeowBar] Notification permission granted")
            }
        }
    }

    func send(title: String, body: String) {
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default

        let request = UNNotificationRequest(
            identifier: UUID().uuidString,
            content: content,
            trigger: nil
        )
        UNUserNotificationCenter.current().add(request)
    }

    func sendStateNotification(state: CatState, errorMessage: String? = nil) {
        switch state {
        case .complete:
            send(title: "MeowBar \u{1F431}", body: "Task complete! Your cat is waiting for praise \u{2728}")
        case .error:
            let msg = errorMessage ?? "Something went wrong"
            send(title: "MeowBar \u{1F640}", body: "Error: \(msg)")
        case .ending:
            send(title: "MeowBar \u{1F44B}", body: "Session ended. Your cat is going to sleep...")
        default:
            break
        }
    }
}
