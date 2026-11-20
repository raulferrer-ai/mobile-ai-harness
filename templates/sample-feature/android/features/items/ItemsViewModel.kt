package com.example.app.features.items

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.app.domain.Item
import com.example.app.domain.ItemRepository
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

enum class ItemsError { LoadFailed, EmptyName, SaveFailed }

data class ItemsUiState(
    val items: List<Item> = emptyList(),
    val isLoading: Boolean = true,
    val error: ItemsError? = null,
)

class ItemsViewModel(private val repository: ItemRepository) : ViewModel() {
    private val actionError = MutableStateFlow<ItemsError?>(null)

    val uiState: StateFlow<ItemsUiState> =
        combine(repository.observeItems(), actionError) { items, error ->
            ItemsUiState(items = items, isLoading = false, error = error)
        }
            .catch { emit(ItemsUiState(isLoading = false, error = ItemsError.LoadFailed)) }
            .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ItemsUiState())

    fun add(name: String) {
        val trimmed = name.trim()
        if (trimmed.isEmpty()) {
            actionError.value = ItemsError.EmptyName
            return
        }
        viewModelScope.launch {
            try {
                repository.add(Item(name = trimmed))
                actionError.value = null
            } catch (e: CancellationException) {
                throw e
            } catch (e: Exception) {
                actionError.value = ItemsError.SaveFailed
            }
        }
    }
}
