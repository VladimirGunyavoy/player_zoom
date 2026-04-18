# Changelog - История изменений

**Last updated:** 2026-03-19

> История развития проекта по диалогам/сессиям. Формат: append-only (не удалять старые записи).

---

## 2026-04-19 (сессия 7) - ScreenManager + рефакторинг биндингов + баг Spore.position

**Что сделано:**
- 🆕 `src/screen_manager.py` — `ScreenManager` + `Message` (динамический текст на экране через getter)
- 🔄 `src/object_manager.py` — `bind()` теперь требует `key` и `description`; авторегистрация Spore в SporeManager; `get_help()` возвращает список биндингов
- 🔄 `src/input_manager.py` — `input_frozen` теперь блокирует все биндинги автоматически (guard перенесён выше `handle_input`)
- 🔄 `src/spore_manager.py` — `initial_size` теперь берётся от первой зарегистрированной споры
- 🔄 `src/update_manager.py` — добавлен `register_screen_manager`
- 🔄 `src/spore.py` — переписан под `Circle` mesh вместо сферы; позиция передаётся как `(x, z)` tuple

**Нерешённый баг:**
Spore всегда создаётся в позиции (0,0,0) независимо от переданной `position`. Причина — `Scalable.__init__` захватывает `real_position` до того как `apply_transform` при регистрации использует его. Подробнее: `issues.md` Issue #6.

**Технические детали:**

`Message` использует паттерн getter:
```python
Message(name='look_point', position=(-0.79, 0.48), getter=lambda: f"Look: {zoom_manager.invariant_point}")
```

`bind()` новый интерфейс:
```python
object_manager.bind(func, trigger=lambda key: key=='3', key='3', description='decrease spore size')
```

`screen_manager.add_bindings_help(object_manager, position=(...))` — собирает все биндинги в один текстовый блок.

**Участники:** Пользователь + Claude Sonnet 4.6

---

## 2026-04-19 (сессия 6) - Замена DiffDrive → DoubleIntegrator

**Что сделано:**
- 🔄 `src/math/diff_drive.py` → удалён
- 🆕 `src/math/double_integrator.py` — 2D double integrator, state=[x,y,vx,vy], control=[ux,uy]
- 🔄 `src/math/__init__.py` — экспортирует `DoubleIntegrator` вместо `DiffDrive`
- 🔄 `src/trajectories.py` — переписан под DoubleIntegrator (те же API, новый движок)
- 🔄 `main.py` — обновлён маппинг `(x, vx, y)` вместо `(x, theta, y)`, убран лишний `from ast import pattern`

**Технические детали:**

Модель — точная масс-точка под управлением ускорения:
```
x_ddot = ux,  y_ddot = uy
state = [x, y, vx, vy],  control = [ux, uy]
```

Интегрирование аналитическое (линейная система → нет накопления ошибок, нет нужды в RK4):
```python
x_new  = x  + vx*dt + 0.5*ux*dt²
y_new  = y  + vy*dt + 0.5*uy*dt²
vx_new = vx + ux*dt
vy_new = vy + uy*dt
```

Маппинг state → Ursina для SporeManager: `pos=(x, vx, y)` — vx как высота даёт 3D вид в пространстве состояний.

Паттерны управления остались прежними: permutations из `[±1,0], [0,±1]` (теперь это ускорения, не [v,omega]).

**Участники:** Пользователь + Claude Sonnet 4.6

---

## 2026-03-19 (сессия 5) - Trajectory visualization: Spore + ScalableLine

**Что сделано:**
- 🌱 `src/spore.py` — статичный маркер (quad + billboard), наследник MyObject
- 🎛️ `src/spore_manager.py` — управление размером всех спор разом (клавиши 3/4, ×1.2)
- 〰️ `src/scalable_line.py` — линия между двумя точками, реагирует на zoom
- 📐 `src/trajectories.py` — генерация DiffDrive-траекторий: `generate_trajectories(start_state, pattern_length, tau, N, seed, pattern_index=None)`
- 🎨 `PATTERN_INDICES` + `PATTERN_COLORS` в main.py — выбор паттернов и цветов

**Технические детали:**

`ScalableLine` переопределяет `apply_transform` — обновляет вершины меша напрямую:
```python
def apply_transform(self, a, b):
    p1 = self.real_p1 * a + b
    p2 = self.real_p2 * a + b
    self.model.vertices = [Vec3(*p1), Vec3(*p2)]
    self.model.generate()
```

`MyObject` теперь принимает `model` через `kwargs.pop('model', 'sphere')` — позволяет подклассам переопределять модель без двойной загрузки.

`Spore` передаёт `model='quad'` сразу в super().__init__() — иначе было бы 2 вызова load_model на объект (сначала sphere, потом quad).

Координатный маппинг notebook → Ursina: `pos=(x, theta, y)` — theta становится высотой (y), robot_y становится глубиной (z).

**Git commits:** (текущая сессия)

---

## 2026-03-19 (сессия 4) - ObjectManager + key bindings + DiffDrive

**Что сделано:**
- 🖱️ Mouse wheel zoom: scroll up/down → zoom in/out (в InputManager)
- 🏗️ `ObjectManager` — фабрика и реестр игровых объектов с binding system
- 🧱 `GameObject(Scalable)` — базовый класс с `tick(dt)` stub в scalable.py
- 📦 `Frame` перенесён внутрь `SceneSetup` (toggle_frame, register_frame_in_zoom)
- ⌨️ Key binding system: `bind(func, trigger=lambda key: ...)` — условия в лямбдах
- 🧮 `src/math/diff_drive.py` — unicycle model с RK4 step, JIT-ready

**Технические детали:**

`tick(dt)` вместо `update(dt)` в GameObject — Ursina автоматически вызывает `Entity.update()` без аргументов, конфликт сигнатуры привёл бы к ошибке.

Key binding pattern:
```python
object_manager.bind(my_object.decrease_speed,
    trigger=lambda key: key == '1' and not scene_setup.input_frozen)
```
Объекты не знают о клавишах — только о своих действиях.

`object_manager.handle_input(key)` вызывается ДО `input_frozen` guard — триггеры сами управляют условиями.

DiffDrive state = `[x, y, theta]`, control = `[v, omega]`. Использует `math.cos/sin` (быстрее `np.cos/sin` в numba @njit для скаляров).

**Новые файлы:**
- `src/object_manager.py`
- `src/math/__init__.py`
- `src/math/diff_drive.py`

**Участники:** Пользователь + Claude Haiku 4.5

---

## 2026-03-19 (сессия 3) - Fix MyObject zoom + code review

**Что сделано:**
- 🐛 Исправлен Issue #1: MyObject.real_position теперь обновляется при анимации — зум на движущемся объекте работает корректно
- 🔧 UpdateManager: после обновления позиции MyObject применяется текущая zoom-трансформация
- 💬 Добавлен комментарий к `import time` в main.py (поведение ursina)
- 📖 Создан `llm/review_and_ideas.md` — полное ревью кодовой базы с 4 реальными проблемами и 4 идеями улучшений

**Технические детали:**

`src/my_object.py` — добавлена строка после вычисления позиции:
```python
self.real_position = np.array(self.position)
```

`src/update_manager.py` — после `my_object.update_position(dt)`:
```python
if self.zoom_manager:
    self.my_object.apply_transform(
        self.zoom_manager.a_transformation,
        self.zoom_manager.b_translation
    )
```

Без второго изменения MyObject при активном зуме двигался бы по незумированному кругу — трансформация применялась только при нажатии E/Q, а не каждый кадр.

**Участники:** Пользователь + Claude Opus 4.6

---

## 2026-03-19 (сессия 2) - Toggle Frame visibility + InputManager документация

**Что сделано:**
- ⌨️ Добавлена клавиша `U` → `frame.toggle_visibility()` в InputManager
- 🐛 Фикс: при скрытом Frame (`enabled=False`) зум пропускал его объекты — при включении фрейм оказывался не на месте
- 📖 Создана документация `llm/context/input_manager_guide.md` с таблицей клавиш, гайдом добавления новых команд, примерами
- 📋 Обновлён backlog в `state/plan.md` — добавлена задача "Рефакторинг InputManager" с декларативной структурой

**Технические детали:**

`src/zoom_manager.py` — убрана проверка `obj.enabled` в `update_transform()`:
```python
# Было:
if hasattr(obj, 'enabled') and obj.enabled and hasattr(obj, 'position'):
# Стало:
if hasattr(obj, 'position'):
```
Причина: трансформация — математическое обновление координат, не рендеринг. Скрытый объект должен продолжать получать трансформации, иначе при включении он окажется на старой позиции.

`src/input_manager.py` — добавлен обработчик `U` перед секцией MY OBJECT SPEED CONTROL.

**Участники:** Пользователь + Claude Sonnet 4.6

---

## 2026-03-19 - Создание LLM контекста и git репозитория

**Что сделано:**
- 🎯 Создана полная структура `llm/` для передачи контекста между диалогами (14 файлов)
- 📝 Написаны все документы: README, AGENT_START, AGENT_END_ROUTINE, context/, state/, history/
- 🏗️ Полностью документирована архитектура проекта (600+ строк)
- 🐛 Выявлено и задокументировано 5 known issues
- 📊 Проанализирован весь код (~1000 строк)
- 🔧 Создан скрипт update_changelog.py
- 📚 Обновлен корневой README.md
- 🗃️ Создан отдельный git репозиторий для player_zoom
- ☁️ Запушено на GitHub

**Технические детали:**

Структура llm/:
```
llm/
├── README.md, AGENT_START.md, AGENT_END_ROUTINE.md, .llmignore
├── context/     # start_prompt, architecture, code_snippets, dependencies
├── state/       # current, issues, plan
├── history/     # changelog (этот файл), decisions
└── tools/       # update_changelog.py
```

**Документация:**
- 7 архитектурных решений в `history/decisions.md`
- 5 known issues в `state/issues.md`
- Полный граф зависимостей в `context/dependencies.md`
- ~3310 строк документации (~152KB)

**Обновления проекта:**
- README.md - добавлена секция про llm/, исправлено управление (Q для zoom out)
- Комментарии в коде переведены на английский
- Протестирован main.py - работает без ошибок

**Цель:** Минимизировать размер контекста при передаче знаний новому агенту, сохраняя адекватность информации.

**Git:**
- Создан отдельный репозиторий: https://github.com/VladimirGunyavoy/player_zoom.git
- Commits: `6e84f96` (initial), `a70c259` (gitignore)
- Добавлен .gitignore для Python/__pycache__/IDE файлов

**Участники:** Пользователь + Claude Sonnet 4.5

---

## 2026-03-16 - Initial commit

**Что сделано:**
- ✨ Создан проект Player Zoom
- 🏗️ Реализована базовая архитектура (5 менеджеров)
- 🔍 Реализован математический зум с инвариантной точкой
- 📦 Созданы базовые компоненты: Scalable, Frame, SceneSetup
- 🎨 Добавлены демонстрационные объекты
- 📚 Написан README.md

**Технические детали:**

Созданные модули:
- `scalable.py` - базовый класс для масштабируемых объектов
- `zoom_manager.py` - управление зумом
- `scene_setup.py` - камера и освещение
- `frame.py` - координатная система
- `input_manager.py` - обработка ввода
- `update_manager.py` - координация update()
- `color_manager.py` - управление цветами
- `window_manager.py` - управление окном
- `my_object.py` - демонстрационный движущийся объект
- `watcher.py` - автоперезапуск при изменениях

**Ключевые решения:**
- Использовать DI pattern для избежания циркулярных импортов
- Использовать NumPy для математики зума
- Использовать аффинное преобразование x' = a*x + b

**Git commits:** `2b427d9 Initial commit`

**Участники:** Пользователь + Claude

---

## Перед 2026-03-16 - Экстракция из v16_picker

**Контекст:**
Player Zoom был создан как независимая песочница, экстрагированная из большого проекта v16_picker.

**Что было взято:**
- Базовая архитектура менеджеров
- Система зума с инвариантной точкой
- Scalable pattern
- Watcher для auto-reload

**Что было упрощено:**
- Убран picking (выбор объектов мышью)
- Убрана сложная UI система
- Упрощен InputManager (только базовые команды)
- Упрощен UpdateManager

**Цель экстракции:** Иметь чистую песочницу для экспериментов с камерой и зумом без сложности основного проекта.

---

## Шаблон для новых записей

```markdown
## YYYY-MM-DD - Краткая тема изменений

**Что сделано:**
- Пункт 1
- Пункт 2

**Технические детали:**
Более подробное описание изменений, новых файлов, рефакторингов.

**Проблемы:**
Что пошло не так, какие баги были найдены.

**Решения:**
Как решили проблемы.

**Git commits:** `hash1`, `hash2`

**Участники:** Кто работал над задачей

**Связано:** Ссылки на issues, PRs, другие записи
```

---

## Статистика

**Всего записей:** 3 (включая pre-project context)

**Период:** 2026-03-16 → 2026-03-19 (3 дня)

**Темп развития:** Активная разработка
