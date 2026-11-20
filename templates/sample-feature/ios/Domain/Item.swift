import Foundation

nonisolated struct Item: Identifiable, Equatable, Sendable {
    let id: UUID
    var name: String

    init(id: UUID = UUID(), name: String) {
        self.id = id
        self.name = name
    }
}

nonisolated protocol ItemRepository: Sendable {
    func fetchItems() async throws -> [Item]
    func add(_ item: Item) async throws
}
