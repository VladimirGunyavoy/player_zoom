# Changelog - Последние сессии

**Last updated:** 2026-04-19

> Хранит последние 3 сессии. Если сессий стало > 3 — самую старую перенести в конец [changelog_archive.md](changelog_archive.md).
> Полная история → [changelog_archive.md](changelog_archive.md)

---

## 2026-04-19 (сессия 8) - SharedContext + GhostSpore + TauManager

**Что сделано:**
- 🆕 `src/shared_context.py` — универсальный контейнер живых данных. `bind(key, getter, default)` регистрирует лямбду; `update()` тянет свежие значения каждый кадр. Читатели обращаются как `ctx.look_point`
- 🆕 `src/tau_manager.py` — параметр τ для симуляции (не рендер-dt). Клавиши 1/2, factor=1.06, min=0, max=5
- 🆕 `GhostSpore` в `src/spore.py` — следует за `ctx.look_point` каждый кадр через `tick()`
- 🔄 `src/zoom_manager.py` — добавлен `real_look_point` (property): инвариантная точка в реальных координатах (обратное преобразование `(visual - b) / a`)
- 🔄 `src/update_manager.py` — исправлен порядок: `identify_invariant_point` → `shared_context.update()` → `object_manager.update_all()`. Добавлен `register_shared_context`
- 🔄 `src/spore_manager.py` — хранилище спор `List` → `Dict[str, Spore]`; `register(name, spore)`; добавлен `get(name)`
- 🔄 `src/scalable.py` — `tick(dt)` → `tick()` (dt убран из сигнатуры)
- 🔄 `src/object_manager.py` — `update_all(dt)` → `update_all()`; `obj.tick()` без dt; передаёт `name` в `spore_manager.register`
- 🗑️ `src/my_object.py` — удалён (не использовался)
- 🐛 Исправлена опечатка в `main.py`: `positions=(1,1)` → `position=(1,1)` (Issue #6 закрыт)

**Ключевые решения:**

`SharedContext` — писари не знают о нём, он сам знает о писарях через лямбды:
```python
shared_context.bind('look_point', lambda: zoom_manager.real_look_point, default=np.zeros(2))
shared_context.bind('tau', lambda: tau_manager.tau, default=1.0)
```

`GhostSpore` получает объект при создании, обращается к нему напрямую:
```python
gs = object_manager.create(cls=GhostSpore, name='ghost_spore_0', ctx=shared_context)
```

Monkey-patch для быстрых экспериментов (tick без аргументов):
```python
gs.tick = lambda: setattr(gs, 'real_position', ...)
```

**Участники:** Пользователь + Claude Sonnet 4.6

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

## Шаблон для новых записей

```markdown
## YYYY-MM-DD (сессия N) - Краткая тема

**Что сделано:**
- 🆕/🔄/🐛 `файл` — что изменилось

**Технические детали:** (если есть важные детали)

**Git commits:** `hash`

**Участники:** Пользователь + Claude X
```
