package com.example.app.features.items

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle

@Composable
fun ItemsRoute(viewModel: ItemsViewModel) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    ItemsScreen(state = state, onAdd = viewModel::add)
}

@Composable
fun ItemsScreen(state: ItemsUiState, onAdd: (String) -> Unit) {
    var name by rememberSaveable { mutableStateOf("") }
    Column(Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        if (state.items.isEmpty() && !state.isLoading) {
            // Sample only: real code uses string resources (strings.xml), never inline text.
            Text("No items yet", style = MaterialTheme.typography.bodyLarge)
        }
        LazyColumn(Modifier.weight(1f)) {
            items(state.items, key = { it.id }) { item -> Text(item.name) }
        }
        state.error?.let {
            // Sample only: map ItemsError to a localized message instead of printing the enum name.
            Text(it.name, color = MaterialTheme.colorScheme.error, modifier = Modifier.testTag("items.error"))
        }
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            OutlinedTextField(
                value = name,
                onValueChange = { name = it },
                modifier = Modifier.weight(1f).testTag("items.nameField"),
                singleLine = true,
            )
            Button(onClick = { onAdd(name); name = "" }, modifier = Modifier.testTag("items.addButton")) {
                Text("Add")
            }
        }
    }
}
