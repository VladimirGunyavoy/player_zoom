# Changelog Archive - История изменений

> Архив. Актуальные последние сессии → [changelog_recent.md](changelog_recent.md)

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

## 2026-03-19 (сессия 1) - Создание LLM контекста и git репозитория

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

**Git:**
- Создан отдельный репозиторий: https://github.com/VladimirGunyavoy/player_zoom.git
- Commits: `6e84f96` (initial), `a70c259` (gitignore)

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

**Созданные модули:** scalable.py, zoom_manager.py, scene_setup.py, frame.py, input_manager.py, update_manager.py, color_manager.py, window_manager.py, my_object.py, watcher.py

**Git commits:** `2b427d9 Initial commit`

**Участники:** Пользователь + Claude

---

## До 2026-03-16 - Экстракция из v16_picker

Player Zoom создан как независимая песочница, экстрагированная из v16_picker.

**Взято:** архитектура менеджеров, система зума с инвариантной точкой, Scalable pattern, watcher.
**Упрощено:** убран picking, сложная UI система, упрощены InputManager и UpdateManager.
