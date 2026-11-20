package com.example.app.domain

import java.util.UUID
import kotlinx.coroutines.flow.Flow

data class Item(
    val id: String = UUID.randomUUID().toString(),
    val name: String,
)

interface ItemRepository {
    fun observeItems(): Flow<List<Item>>
    suspend fun add(item: Item)
}
