import Foundation
import Observation

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
            errorMessage = String(localized: "items.error.load")
        }
    }

    /// Returns true when the item was saved.
    @discardableResult
    func add(name: String) async -> Bool {
        let trimmed = name.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else {
            errorMessage = String(localized: "items.error.emptyName")
            return false
        }
        do {
            try await repository.add(Item(name: trimmed))
            items = try await repository.fetchItems()
            errorMessage = nil
            return true
        } catch {
            errorMessage = String(localized: "items.error.save")
            return false
        }
    }
}
