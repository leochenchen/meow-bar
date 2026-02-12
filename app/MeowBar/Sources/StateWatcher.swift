import Foundation

/// Watches ~/.claude/meow-state.json for changes using GCD file monitoring
final class StateWatcher {
    private let filePath: String
    private var fileDescriptor: Int32 = -1
    private var dispatchSource: DispatchSourceFileSystemObject?
    private var pollTimer: Timer?
    private var lastModified: Date?

    var onStateChange: ((MeowStateData) -> Void)?

    init() {
        let home = FileManager.default.homeDirectoryForCurrentUser.path
        filePath = "\(home)/.claude/meow-state.json"
    }

    func start() {
        // Ensure the directory and file exist
        let dir = (filePath as NSString).deletingLastPathComponent
        try? FileManager.default.createDirectory(atPath: dir, withIntermediateDirectories: true)
        if !FileManager.default.fileExists(atPath: filePath) {
            let initial = #"{"state":"idle","timestamp":"","events_log":[]}"#
            try? initial.write(toFile: filePath, atomically: true, encoding: .utf8)
        }

        // Read initial state
        readState()

        // Watch the directory (more reliable than watching the file directly since mv replaces inodes)
        let dirPath = (filePath as NSString).deletingLastPathComponent
        let fd = open(dirPath, O_EVTONLY)
        if fd >= 0 {
            fileDescriptor = fd
            let source = DispatchSource.makeFileSystemObjectSource(
                fileDescriptor: fd,
                eventMask: .write,
                queue: .main
            )
            source.setEventHandler { [weak self] in
                self?.readState()
            }
            source.setCancelHandler {
                close(fd)
            }
            source.resume()
            dispatchSource = source
        }

        // Fallback: poll every 1s in case FSEvents misses something
        pollTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.checkForChanges()
        }
    }

    func stop() {
        dispatchSource?.cancel()
        dispatchSource = nil
        pollTimer?.invalidate()
        pollTimer = nil
        if fileDescriptor >= 0 {
            // Already closed by cancel handler, but guard
            fileDescriptor = -1
        }
    }

    private func checkForChanges() {
        guard let attrs = try? FileManager.default.attributesOfItem(atPath: filePath),
              let modified = attrs[.modificationDate] as? Date else { return }

        if lastModified == nil || modified > lastModified! {
            lastModified = modified
            readState()
        }
    }

    private func readState() {
        guard let data = FileManager.default.contents(atPath: filePath) else { return }
        guard let state = try? JSONDecoder().decode(MeowStateData.self, from: data) else { return }

        // Update last modified
        if let attrs = try? FileManager.default.attributesOfItem(atPath: filePath) {
            lastModified = attrs[.modificationDate] as? Date
        }

        DispatchQueue.main.async { [weak self] in
            self?.onStateChange?(state)
        }
    }
}
