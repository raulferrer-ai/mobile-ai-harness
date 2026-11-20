import Testing
@testable import App   // replace `App` with your app module name

actor FakeItemRepository: ItemRepository {
    private var items: [Item]
    private let shouldFailSaving: Bool

    init(items: [Item] = [], shouldFailSaving: Bool = false) {
        self.items = items
        self.shouldFailSaving = shouldFailSaving
    }

    struct SaveFailed: Error {}

    func fetchItems() async throws -> [Item] { items }

    func add(_ item: Item) async throws {
        if shouldFailSaving { throw SaveFailed() }
        items.append(item)
    }
}

@MainActor
struct ItemsViewModelTests {
    @Test func loadShowsExistingItems() async {
        let viewModel = ItemsViewModel(repository: FakeItemRepository(items: [Item(name: "A")]))
        await viewModel.load()
        #expect(viewModel.items.count == 1)
        #expect(viewModel.errorMessage == nil)
    }

    @Test func addAppendsItem() async {
        let viewModel = ItemsViewModel(repository: FakeItemRepository())
        let saved = await viewModel.add(name: "First item")
        #expect(saved)
        #expect(viewModel.items.map(\.name) == ["First item"])
    }

    @Test(arguments: ["", "   ", "\n"])
    func addRejectsBlankName(name: String) async {
        let viewModel = ItemsViewModel(repository: FakeItemRepository())
        let saved = await viewModel.add(name: name)
        #expect(!saved)
        #expect(viewModel.items.isEmpty)
        #expect(viewModel.errorMessage != nil)
    }

    @Test func saveFailureShowsMessageAndKeepsListUnchanged() async {
        let viewModel = ItemsViewModel(repository: FakeItemRepository(shouldFailSaving: true))
        let saved = await viewModel.add(name: "Second item")
        #expect(!saved)
        #expect(viewModel.items.isEmpty)
        #expect(viewModel.errorMessage != nil)
    }
}
