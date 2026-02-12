import Foundation

enum CatState: String, Codable, CaseIterable {
    case idle
    case starting
    case thinking
    case working
    case error
    case complete
    case ending
    case compacting

    var displayName: String {
        switch self {
        case .idle: return "Sleeping"
        case .starting: return "Waking up"
        case .thinking: return "Typing"
        case .working: return "Running"
        case .error: return "Scared!"
        case .complete: return "Waiting for praise"
        case .ending: return "Bye bye"
        case .compacting: return "Thinking"
        }
    }

    var emoji: String {
        switch self {
        case .idle: return "\u{1F4A4}"      // zzz
        case .starting: return "\u{2600}"    // sun
        case .thinking: return "\u{2328}"    // keyboard
        case .working: return "\u{1F3C3}"    // running
        case .error: return "\u{26A0}"       // warning
        case .complete: return "\u{2728}"    // sparkles
        case .ending: return "\u{1F44B}"     // wave
        case .compacting: return "\u{1F4AD}" // thought bubble
        }
    }

    var statusColor: String {
        switch self {
        case .idle: return "gray"
        case .starting: return "yellow"
        case .thinking: return "blue"
        case .working: return "green"
        case .error: return "red"
        case .complete: return "gold"
        case .ending: return "purple"
        case .compacting: return "teal"
        }
    }

    /// Frame file prefix for this state
    var framePrefix: String {
        switch self {
        case .idle: return "idle"
        case .starting: return "wakeup"
        case .thinking: return "typing"
        case .working: return "running"
        case .error: return "scared"
        case .complete: return "celebrate"
        case .ending: return "wave"
        case .compacting: return "thinking"
        }
    }

    /// Number of animation frames for this state
    var frameCount: Int {
        switch self {
        case .idle: return 4
        case .starting: return 3
        case .thinking: return 4
        case .working: return 6
        case .error: return 3
        case .complete: return 4
        case .ending: return 4
        case .compacting: return 4
        }
    }

    /// Animation interval in seconds
    var animationInterval: TimeInterval {
        switch self {
        case .idle: return 1.0
        case .starting: return 0.3
        case .thinking: return 0.4
        case .working: return 0.15
        case .error: return 0.2
        case .complete: return 0.3
        case .ending: return 0.4
        case .compacting: return 0.5
        }
    }

    /// How long to auto-transition back to a default state (nil = stay until next event)
    var autoTransitionDuration: TimeInterval? {
        switch self {
        case .starting: return 2.0
        case .error: return 3.0
        case .ending: return 3.0
        default: return nil
        }
    }

    /// State to transition to after autoTransitionDuration
    var autoTransitionTarget: CatState {
        switch self {
        case .starting: return .thinking
        case .error: return .working
        case .ending: return .idle
        default: return .idle
        }
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

    enum CodingKeys: String, CodingKey {
        case state, timestamp
        case sessionId = "session_id"
        case lastEvent = "last_event"
        case toolName = "tool_name"
        case errorMessage = "error_message"
        case eventsLog = "events_log"
    }

    static let empty = MeowStateData(
        state: .idle,
        timestamp: "",
        sessionId: nil,
        lastEvent: nil,
        toolName: nil,
        errorMessage: nil,
        eventsLog: nil
    )
}
