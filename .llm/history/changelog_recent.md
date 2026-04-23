# Changelog - Последние сессии

**Last updated:** 2026-04-23

> Хранит последние 3 сессии. Если сессий стало > 3 — самую старую перенести в конец [changelog_archive.md](changelog_archive.md)
> Полная история → [changelog_archive.md](changelog_archive.md)

---

## 2026-04-23 (сессия 10) - GhostSporeFamily + архитектура менеджеров

**Что сделано:**
- 🔄 `SporeManager` — добавлен `create(cls, name, **kwargs)` как прокси к ObjectManager; убрана зависимость ObjectManager → SporeManager
- 🔄 `ObjectManager` — принимает `shared_context`, auto-inject `ctx` для Spore-субклассов, добавлен `register_tickable()` для не-GameObject объектов с tick()
- 🔄 `ParamManager` — добавлены `min_val`/`max_val` с clamping; новые параметры `a_max` (кл. 3), `n_tau` (кл. 4), `n_u` (кл. 5)
- 🔄 `SharedContext` — `param_manager` забиндан как единая точка доступа к параметрам
- 🔄 `DoubleIntegrator` — рефакторинг: stateless `step(x0, v0, u, t)`, принимает SharedContext, `tick()` синхронизирует `a_max`, убрано внутреннее состояние позиции
- 🆕 `src/spores/ghost_spore_family.py` — `GhostSporeFamily`: сетка `n_tau × (2*n_u+1)` призрачных спор, рекурсивная эволюция через DI (шаг δτ = tau/n_tau), пересоздание только при смене n_tau/n_u, пересчёт позиций каждый tick
- 🔄 `main.py` — ghost_spore_1/2 заменены на семью; создание спор через spore_manager.create()
- 🔄 `AGENT_START.md` — добавлено правило: не удалять существующий код без явного запроса

**Ключевые архитектурные решения:**

SporeManager как прокси (ObjectManager — системный, не знает про SporeManager):
```python
spore_manager.create(GhostSpore, 'ghost_spore_0')  # вместо object_manager.create(...)
```

GhostSporeFamily — rebuild vs recompute:
- rebuild (новые Entity): только при смене n_tau / n_u
- recompute (позиции): каждый tick — дёшево

**Участники:** Пользователь + Claude Sonnet 4.6

---

## 2026-04-23 (сессия 9) - Рефакторинг архитектуры: tick/register/ParamManager/структура src/

**Что сделано:**
- 🔄 `register(**kwargs)` — универсальный метод регистрации вместо отдельных `register_X()` в InputManager и UpdateManager
- 🔄 `tick()` — унифицированное имя per-frame метода у всех компонентов
- 🆕 `src/core/param_manager.py` — `ParamManager`: именованные float-параметры, exp/linear режимы
- 🗑️ `src/tau_manager.py` — удалён, tau теперь `param_manager.add('tau', 0.5)`
- 🔄 `src/core/input_manager.py` — `bind()` с mode='press' и mode='scroll', hold+scroll подавляет зум
- 🔄 `src/` реорганизована: `core/`, `spores/`, `math/`, `utils/`
- 🔄 `SceneSetup` → `SceneManager`

**Участники:** Пользователь + Claude Sonnet 4.6

---

## 2026-04-19 (сессия 8) - SharedContext + GhostSpore + TauManager

**Что сделано:**
- 🆕 `src/shared_context.py` — универсальный контейнер живых данных
- 🆕 `src/tau_manager.py` — параметр τ
- 🆕 `GhostSpore` — следует за `ctx.look_point` каждый кадр
- 🔄 `zoom_manager.py` — добавлен `real_look_point` property
- 🔄 `spore_manager.py` — `List` → `Dict[str, Spore]`, добавлен `get(name)`
- 🐛 Исправлена опечатка `positions=` → `position=` (Issue #6)

**Участники:** Пользователь + Claude Sonnet 4.6

---

## Шаблон для новых записей

```markdown
## YYYY-MM-DD (сессия N) - Краткая тема

**Что сделано:**
- 🆕/🔄/🐛/🗑️ `файл` — что изменилось

**Участники:** Пользователь + Claude X
```
