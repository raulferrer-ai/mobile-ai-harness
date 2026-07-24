# Android stack reference (defaults)

Patterns for the default Android stack in `android/AGENTS.md`. If you change the stack, update this file in the same
change set (`docs/customizing.md`). Verify API details against current Android documentation; samples are shapes, not gospel.

## Build checklist
- Gradle Kotlin DSL; every version in `gradle/libs.versions.toml`; wrapper committed (`gradlew` runs via `sh ./gradlew` in sensors).
- Versions baseline in `docs/stack.md`. Newer Compose releases require a newer `compileSdk` and AGP; AGP 9 changed how
  Kotlin is integrated, so read the AGP release notes instead of copying older plugin lines.
- Kotlin 2.4 removed `kotlinOptions {}`; configure with `kotlin { compilerOptions { ... } }`.
- Compose compiler is the Kotlin Gradle plugin `org.jetbrains.kotlin.plugin.compose`, versioned with Kotlin.
- Set `ANDROID_TEST_TASK` in `harness.env` if your module is not `:app`.

## Layout
```text
app/src/main/java/<package>/
  features/<feature>/    <Feature>Screen.kt, <Feature>UiState.kt, <Feature>ViewModel.kt, small composables
  domain/model, domain/repository, domain/usecase, domain/scheduling
  data/local (Room), data/repository, data/notifications, data/photos
  designsystem/          Color.kt, Type.kt, Spacing.kt, Theme.kt, components
  AppContainer.kt, <App>Application.kt, MainActivity.kt
app/src/test/ (JVM)   app/src/androidTest/ (instrumented)
```

## UDF pattern
```kotlin
data class ItemsUiState(
    val items: List<Item> = emptyList(),
    val isLoading: Boolean = true,
    val error: ItemsError? = null,
)

class ItemsViewModel(repository: ItemRepository) : ViewModel() {
    val uiState: StateFlow<ItemsUiState> = repository.observeItems()
        .map { ItemsUiState(items = it, isLoading = false) }
        .catch { emit(ItemsUiState(isLoading = false, error = ItemsError.LoadFailed)) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ItemsUiState())
}
```
Rethrow `CancellationException` in any `try/catch` around suspend calls. Events are plain ViewModel functions.

Screen (stateless composable + thin stateful wrapper):
```kotlin
@Composable
fun ItemsRoute(viewModel: ItemsViewModel) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    ItemsScreen(state = state)
}

@Composable
fun ItemsScreen(state: ItemsUiState) { /* renders state; previewable; no logic */ }
```

## Persistence (Room 3 default)
- Coordinates: `androidx.room3:room3-runtime` and `androidx.room3:room3-compiler` (KSP); Gradle plugin id `androidx.room3`
  with `room3 { schemaDirectory(...) }`. Package is `androidx.room3`. Room 3 is KSP-only; DAO functions must be `suspend` or return `Flow`.
- Room 2.x (`androidx.room`) remains valid (maintenance mode); the rules below do not change.
- Repository interface in `domain/repository` returns `Flow`/`suspend`; the Room implementation lives in `data/` and
  maps entities to domain models. Entities and DAOs never leave `data/`.
- Export schemas and write a migration for every schema change; test migrations. Do not use destructive migration in production.
- Builder and driver setup changed in Room 3: follow the current official Room 3 guide instead of older snippets.
- Small key-value settings: DataStore, behind an interface in `data/`.

## Composition root (manual DI)
`AppContainer(context)` builds database, repositories, use cases and services once (owned by the `Application`).
ViewModels get dependencies by constructor and are created with `viewModelFactory { initializer { ... } }`.
Switch to Hilt/Koin only through an ADR when the graph is large enough to justify it; keep constructor injection either way.

## OS capabilities
- Notifications: create a channel; request `POST_NOTIFICATIONS` at runtime on API 33+; show a useful state if denied.
- Scheduling: prefer WorkManager or inexact alarms unless the product needs exact times; for exact alarms check
  `AlarmManager.canScheduleExactAlarms()` and handle revoked access. Reschedule after reboot.
- Photos: Photo Picker (`ActivityResultContracts.PickVisualMedia`) and a camera intent with a `FileProvider`; honor EXIF orientation;
  downscale before storing.
- Wrap all of these in interfaces so tests can fake them.

## Testing patterns
```kotlin
class MainDispatcherRule(
    private val dispatcher: TestDispatcher = UnconfinedTestDispatcher(),
) : TestWatcher() {
    override fun starting(description: Description) = Dispatchers.setMain(dispatcher)
    override fun finished(description: Description) = Dispatchers.resetMain()
}

class ItemsViewModelTest {
    @get:Rule val main = MainDispatcherRule()

    @Test fun emitsItems() = runTest {
        val vm = ItemsViewModel(FakeItemRepository(listOf(Item("A"))))
        vm.uiState.test {
            val state = expectMostRecentItem()
            assertEquals(1, state.items.size)
        }
    }
}
```
- Prefer hand-written fakes over mocks. Use Turbine for Flow assertions.
- Compose UI tests: `createComposeRule()`, `Modifier.testTag(...)`, no `Thread.sleep`; use the test clock/idling.
- Instrumented DAO tests use an in-memory database.

## Gotchas
- `Eagerly` sharing keeps upstream flows alive forever; use `WhileSubscribed(5_000)` unless you have a reason.
- Do not collect flows in composables with plain `collectAsState()`: use lifecycle-aware collection.
- Do not pass Room entities or Android `Context` into domain types.
- Instrumented tests need an emulator/device; the default sensor runs JVM tests only (fast, CI-friendly).
