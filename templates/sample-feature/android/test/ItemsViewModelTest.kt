package com.example.app.features.items

import app.cash.turbine.test
import com.example.app.domain.Item
import com.example.app.domain.ItemRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.test.TestDispatcher
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.rules.TestWatcher
import org.junit.runner.Description

@OptIn(ExperimentalCoroutinesApi::class)
class MainDispatcherRule(
    private val dispatcher: TestDispatcher = UnconfinedTestDispatcher(),
) : TestWatcher() {
    override fun starting(description: Description) = Dispatchers.setMain(dispatcher)
    override fun finished(description: Description) = Dispatchers.resetMain()
}

class FakeItemRepository(private val failOnAdd: Boolean = false) : ItemRepository {
    private val items = MutableStateFlow<List<Item>>(emptyList())
    override fun observeItems(): Flow<List<Item>> = items
    override suspend fun add(item: Item) {
        if (failOnAdd) error("save failed")
        items.value = items.value + item
    }
}

class ItemsViewModelTest {
    @get:Rule val main = MainDispatcherRule()

    @Test fun addShowsTheItem() = runTest {
        val vm = ItemsViewModel(FakeItemRepository())
        vm.uiState.test {
            vm.add("First item")
            val state = expectMostRecentItem()
            assertEquals(listOf("First item"), state.items.map { it.name })
            assertEquals(null, state.error)
        }
    }

    @Test fun blankNameIsRejected() = runTest {
        val vm = ItemsViewModel(FakeItemRepository())
        vm.uiState.test {
            vm.add("   ")
            val state = expectMostRecentItem()
            assertTrue(state.items.isEmpty())
            assertEquals(ItemsError.EmptyName, state.error)
        }
    }

    @Test fun saveFailureShowsErrorAndKeepsListUnchanged() = runTest {
        val vm = ItemsViewModel(FakeItemRepository(failOnAdd = true))
        vm.uiState.test {
            vm.add("Second item")
            val state = expectMostRecentItem()
            assertTrue(state.items.isEmpty())
            assertEquals(ItemsError.SaveFailed, state.error)
        }
    }
}
