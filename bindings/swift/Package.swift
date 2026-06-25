// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "MCHSBind",
    platforms: [
        .macOS(.v13),
        .iOS(.v16),
    ],
    products: [
        .library(name: "MCHSBind", targets: ["MCHSBind"]),
    ],
    targets: [
        .target(
            name: "MCHSBind",
            swiftSettings: [
                .enableUpcomingFeature("StrictConcurrency"),
            ]
        ),
        .executableTarget(
            name: "MCHSBindSmoke",
            dependencies: ["MCHSBind"]
        ),
    ]
)
