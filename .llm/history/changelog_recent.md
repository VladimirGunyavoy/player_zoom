# Changelog - Последние сессии

**Last updated:** 2026-04-23

> Хранит последние 3 сессии. Если сессий стало > 3 — самую старую перенести в конец [changelog_archive.md](changelog_archive.md)
> Полная история → [changelog_archive.md](changelog_archive.md)

---

## 2026-04-23 (сессия 9) - Рефакторинг архитектуры: tick/register/ParamManager/структура src/

**Что сделано:**
- 🔄 `register(**kwargs)` — универсальный метод регистрации вместо отдельных `register_X()` в InputManager и UpdateManager
- 🔄 `tick()` — унифицированное имя per-frame метода у всех компонентов (было: `update`, `update_all`, `identify_invariant_point`). `UpdateManager.update_all()` теперь цикл по списку компонентов
- 🆕 `src/core/param_manager.py` — `ParamManager`: именованные float-параметры, `add(name, value, mode, factor, step)`, `tweak(name, sign)` с exp/linear режимами
- 🗑️ `src/tau_manager.py` — удалён, tau теперь `param_manager.add('tau', 0.5)`
- 🔄 `src/core/input_manager.py` — `bind(key, action, mode, description, value_getter)`: `mode='press'` и `mode='scroll'` (hold+scroll). Hold+scroll подавляет зум. `get_help()` генерирует подсказку с текущими значениями параметров
- 🔄 Биндинги переехали из `ObjectManager` в `InputManager`; `ObjectManager.bind/handle_input/get_help` удалены
- 🔄 `src/` реорганизована: `core/` (13 файлов, переиспользуемое), `spores/` (spore, spore_manager, trajectories), `math/`, `utils/`
- 🔄 `SceneSetup` → `SceneManager` (файл `scene_manager.py`, класс `SceneManager`)
- 🔄 Все внутренние импорты обновлены под новую структуру

**Ключевые решения:**

`register(**kwargs)` вместо отдельных методов:
```python
input_manager.register(scene_setup=scene_setup, zoom_manager=zoom_manager, ...)
```

hold+scroll: клавиша зажата → параметр, не зажата → зум:
```python
input_manager.bind('1', lambda sign: param_manager.tweak('tau', sign), mode='scroll',
                   description='tau', value_getter=lambda: param_manager.tau)
```

**Участники:** Пользователь + Claude Sonnet 4.6

---

## 2026-04-19 (сессия 8) - SharedContext + GhostSpore + TauManager

**Что сделано:**
- 🆕 `src/shared_context.py` — универсальный контейнер живых данных
- 🆕 `src/tau_manager.py` — параметр τ (клавиши 1/2, factor=1.06)
- 🆕 `GhostSpore` — следует за `ctx.look_point` каждый кадр
- 🔄 `zoom_manager.py` — добавлен `real_look_point` property
- 🔄 `spore_manager.py` — `List` → `Dict[str, Spore]`, добавлен `get(name)`
- 🐛 Исправлена опечатка `positions=` → `position=` (Issue #6)

**Участники:** Пользователь + Claude Sonnet 4.6

---

## 2026-04-19 (сессия 7) - ScreenManager + рефакторинг биндингов

**Что сделано:**
- 🆕 `src/screen_manager.py` — `ScreenManager` + `Message` (динамический текст)
- 🔄 `src/object_manager.py` — `bind()` требует `key` и `description`; `get_help()`
- 🔄 `src/input_manager.py` — `input_frozen` блокирует все биндинги

**Участники:** Пользователь + Claude Sonnet 4.6

---

## Шаблон для новых записей

```markdown
## YYYY-MM-DD (сессия N) - Краткая тема

**Что сделано:**
- 🆕/🔄/🐛/🗑️ `файл` — что изменилось

**Участники:** Пользователь + Claude X
```
