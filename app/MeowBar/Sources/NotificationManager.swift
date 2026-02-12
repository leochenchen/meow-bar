import Foundation
import UserNotifications

final class NotificationManager {
    static let shared = NotificationManager()

    private init() {}

    func requestPermission() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            if granted {
                print("[MeowBar] Notification permission granted")
            } else if let error = error {
                print("[MeowBar] Notification error: \(error)")
            } else {
                print("[MeowBar] Notification permission denied - enable in System Settings > Notifications > MeowBar")
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
        UNUserNotificationCenter.current().add(request) { error in
            if let error = error {
                print("[MeowBar] Failed to send notification: \(error)")
            }
        }
    }

    func sendStateNotification(state: CatState, errorMessage: String? = nil) {
        switch state {
        case .complete:
            send(title: "MeowBar", body: "Task complete! Cat is waiting for praise")
        case .error:
            let msg = errorMessage ?? "Something went wrong"
            send(title: "MeowBar", body: "Error: \(msg)")
        default:
            break
        }
    }
}
