// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "MeowBar",
    platforms: [.macOS(.v13)],
    targets: [
        .executableTarget(
            name: "MeowBar",
            path: "Sources"
        )
    ]
)
