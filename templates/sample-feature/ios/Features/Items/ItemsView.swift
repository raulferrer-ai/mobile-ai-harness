import SwiftUI

struct ItemsView: View {
    @State private var viewModel: ItemsViewModel
    @State private var newName = ""

    init(viewModel: ItemsViewModel) {
        _viewModel = State(initialValue: viewModel)
    }

    var body: some View {
        NavigationStack {
            List(viewModel.items) { item in
                Text(item.name)
            }
            .overlay {
                if viewModel.items.isEmpty && !viewModel.isLoading {
                    ContentUnavailableView("items.empty.title", systemImage: "tray")
                }
            }
            .navigationTitle("items.title")
            .safeAreaInset(edge: .bottom) { addBar }
            .task { await viewModel.load() }
        }
    }

    private var addBar: some View {
        VStack(alignment: .leading, spacing: 8) {
            if let message = viewModel.errorMessage {
                Text(message)
                    .font(.footnote)
                    .foregroundStyle(.red)  // replace with a design-system token
                    .accessibilityIdentifier("items.error")
            }
            HStack {
                TextField("items.field.name", text: $newName)
                    .textFieldStyle(.roundedBorder)
                    .accessibilityIdentifier("items.nameField")
                Button("items.action.add") {
                    Task {
                        if await viewModel.add(name: newName) { newName = "" }
                    }
                }
                .accessibilityIdentifier("items.addButton")
            }
        }
        .padding()
        .background(.bar)
    }
}
