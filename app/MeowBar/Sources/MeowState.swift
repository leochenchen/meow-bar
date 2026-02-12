import Foundation

enum CatState: String, Codable, CaseIterable {
    case idle
    case working
    case complete
    case error

    var displayName: String {
        switch self {
        case .idle: return "Sleeping"
        case .working: return "Running"
        case .complete: return "Waiting for praise"
        case .error: return "Scared!"
        }
    }

    var emoji: String {
        switch self {
        case .idle: return "\u{1F4A4}"      // zzz
        case .working: return "\u{1F3C3}"    // running
        case .complete: return "\u{2728}"    // sparkles
        case .error: return "\u{26A0}"       // warning
        }
    }

    var framePrefix: String {
        switch self {
        case .idle: return "idle"
        case .working: return "running"
        case .complete: return "celebrate"
        case .error: return "scared"
        }
    }

    var frameCount: Int {
        switch self {
        case .idle: return 4
        case .working: return 6
        case .complete: return 4
        case .error: return 3
        }
    }

    var animationInterval: TimeInterval {
        switch self {
        case .idle: return 1.0
        case .working: return 0.15
        case .complete: return 0.3
        case .error: return 0.2
        }
    }

    /// Auto-transition back after this duration (nil = stay until next event)
    var autoTransitionDuration: TimeInterval? {
        switch self {
        case .complete: return 6.0
        default: return nil  // error stays as error until next event
        }
    }

    var autoTransitionTarget: CatState {
        return .idle
    }
}

struct EventEntry: Codable {
    let event: String
    let time: String
    let detail: String
}

struct MeowStateData: Codable {
    var state: CatState
    var timestamp: String
    var sessionId: String?
    var lastEvent: String?
    var toolName: String?
    var errorMessage: String?
    var eventsLog: [EventEntry]?
    // Stats
    var sessionStartTime: String?
    var toolCallCount: Int?
    var promptCount: Int?
    var errorCount: Int?

    enum CodingKeys: String, CodingKey {
        case state, timestamp
        case sessionId = "session_id"
        case lastEvent = "last_event"
        case toolName = "tool_name"
        case errorMessage = "error_message"
        case eventsLog = "events_log"
        case sessionStartTime = "session_start_time"
        case toolCallCount = "tool_call_count"
        case promptCount = "prompt_count"
        case errorCount = "error_count"
    }

    static let empty = MeowStateData(
        state: .idle,
        timestamp: "",
        sessionId: nil,
        lastEvent: nil,
        toolName: nil,
        errorMessage: nil,
        eventsLog: nil,
        sessionStartTime: nil,
        toolCallCount: nil,
        promptCount: nil,
        errorCount: nil
    )
}
