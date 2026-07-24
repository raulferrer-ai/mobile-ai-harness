# iOS stack reference (defaults)

Patterns for the default iOS stack in `ios/AGENTS.md`. If you change the stack, update this file in the same
change set (`docs/customizing.md`). Verify API details against current Apple documentation; samples are shapes, not gospel.

## Xcode project settings checklist
- Swift language version 6; `SWIFT_APPROACHABLE_CONCURRENCY = YES`; default actor isolation `MainActor` for the app target.
- Deployment target per `docs/stack.md`; String Catalogs on; user script sandboxing on.
- Test targets: unit (`<App>Tests`) and UI (`<App>UITests`). Share the scheme and set `IOS_PROJECT`/`IOS_SCHEME` in `harness.env`.
- Never commit `xcuserdata/`; shared schemes are fine.

## Layout
```text
<App>/
  App/            <App>App.swift (entry + composition root), RootView.swift
  Features/<Feature>/   <Feature>View.swift, <Feature>ViewModel.swift, small subviews
  Domain/Models, Domain/Repositories, Domain/Services
  Data/Repositories, Data/SwiftData (entities, container), Data/Notifications, Data/Photos
  DesignSystem/   Colors, Typography, Spacing, components
  Resources/      Assets.xcassets, Localizable.xcstrings
```

## Concurrency rules
- Views and view models: `@MainActor` (implicit with default MainActor isolation; be explicit on view models anyway).
- Pure domain types: `nonisolated`, value types, `Sendable`. Repository protocols are `async throws`.
- Prefer `.task { await viewModel.load() }` over `Task {}` in views; respect cancellation (`Task.checkCancellation()`).
- Shared mutable state lives in an `actor`. No `Task.detached` without a written reason.

## View model pattern
```swift
@MainActor
@Observable
final class ItemsViewModel {
    private(set) var items: [Item] = []
    private(set) var isLoading = false
    private(set) var errorMessage: String?

    private let repository: any ItemRepository

    init(repository: any ItemRepository) {
        self.repository = repository
    }

    func load() async {
        guard !isLoading else { return }
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }
        do {
            items = try await repository.fetchItems()
        } catch {
            errorMessage = String(localized: "items.error.load")  // calm, user-facing
        }
    }
}
```
Ownership in a view: `@State private var viewModel: ItemsViewModel`, created with its dependencies from the composition root.

## Repository boundary (SwiftData)
- Protocol in `Domain/Repositories`; implementation in `Data/Repositories` using `@Model` entities that never leave `Data/`.
- Map entity <-> domain model in the repository (`init(entity:)` / `toEntity()`).
- Create the `ModelContainer` once in `App/`; tests use an in-memory configuration (`isStoredInMemoryOnly: true`).
- Schema changes: use versioned schemas and migration plans from the first release; never edit shipped models in place.

## Composition root
```swift
@main
struct MyApp: App {
    private let container: AppContainer   // builds repositories, services, view model factories

    init() { container = AppContainer.live() }

    var body: some Scene {
        WindowGroup { RootView(container: container) }
    }
}
```
Tests and previews build `AppContainer` variants with fakes. No singletons.

## OS capabilities behind protocols
Notifications (`UNUserNotificationCenter`), photo library/camera, clock/calendar, permissions: wrap in a protocol in
`Domain/` (or `Data/` when purely technical) and fake it in tests. Always model denied/restricted/not-determined.

## Testing patterns
Unit (Swift Testing):
```swift
import Testing
@testable import App

@MainActor
struct ItemsViewModelTests {
    @Test func loadShowsItems() async {
        let repo = FakeItemRepository(items: [Item(name: "A")])
        let viewModel = ItemsViewModel(repository: repo)
        await viewModel.load()
        #expect(viewModel.items.count == 1)
        #expect(viewModel.errorMessage == nil)
    }

    @Test func loadFailureShowsCalmMessage() async {
        let repo = FakeItemRepository(error: FakeError.failed)
        let viewModel = ItemsViewModel(repository: repo)
        await viewModel.load()
        #expect(viewModel.items.isEmpty)
        #expect(viewModel.errorMessage != nil)
    }
}
```
UI (XCUITest): seed data through a launch argument handled in `#if DEBUG` code in `App/`, so flows never depend on
the camera, the photo library or the network. Set `accessibilityIdentifier`s; use `waitForExistence(timeout:)`, never `sleep`.

## Gotchas
- Swift 6 data-race errors usually mean a missing `Sendable`/isolation decision, not something to silence with `@unchecked Sendable`.
- Do not use `@Query` in feature views: it puts persistence in the UI layer.
- A `View` that owns a view model with `@State` must not recreate it in `body`.
- Simulator names change with Xcode versions: `make simulators`, then fix `IOS_DESTINATION` in `harness.env`.
- Info.plist usage strings (camera, photos, notifications context) are required before requesting those permissions.
