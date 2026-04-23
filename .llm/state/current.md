# Current State - Текущее состояние проекта

**Last updated:** 2026-04-23 (сессия 10)

---

## ✅ Что работает

### Базовая функциональность:
- ✅ **Камера** (FirstPersonController) — WASD, Mouse look, Space/Shift, Alt курсор
- ✅ **Zoom система** — scroll/Q/E zoom, R reset, математически корректная с invariant point
- ✅ **Визуализация** — Frame (XYZ оси), клетчатый пол, Spore (Circle), GhostSpore
- ✅ **ScreenManager + Message** — динамический текст на экране через getter каждый кадр

### Архитектура (сессия 10):
- ✅ **`SporeManager.create()`** — прокси к ObjectManager для создания спор
- ✅ **`ObjectManager`** — знает `shared_context`, auto-inject `ctx` для Spore-субклассов, `register_tickable()`
- ✅ **`ParamManager`** — поддержка `min_val`/`max_val` с clamping в `tweak()`
- ✅ **`DoubleIntegrator`** — stateless `step(x0, v0, u, t)`, берёт `ctx`, `tick()` синхронизирует `a_max`
- ✅ **`GhostSporeFamily`** — сетка `n_tau × (2*n_u+1)` призрачных спор, рекурсивная эволюция через DI

### Параметры (актуальное):
- `1` + scroll — spore size
- `2` + scroll — tau
- `3` + scroll — a_max (min=0)
- `4` + scroll — n_tau (шаг 1, min=0)
- `5` + scroll — n_u (шаг 1, min=0)
- `scroll` — zoom

### Математика (src/math/):
- ✅ `DoubleIntegrator` — 1D, stateless step, a_max из SharedContext
- ✅ `SporeIntegrator` — 2D unicycle model (x, y, theta)

### Архитектура (сессия 9):
- ✅ **`src/` реорганизована** на `core/`, `spores/`, `math/`, `utils/`
- ✅ **`ParamManager`** — именованные параметры, exp/linear
- ✅ **`InputManager.bind()`** — mode='press' и mode='scroll'
- ✅ **`SharedContext`** — живые данные, bind/tick

---

## 🔄 Что в процессе

- 🔄 **`GhostSporeFamily`** — позиции работают, рёбра (линии между вершинами) не отрисованы

---

## ❌ Что сломано / не работает

- ❌ **colors.json** — файл отсутствует, warning в консоли (не критично, дефолты работают)

---

## 📁 Структура src/

```
src/
  core/
    color_manager.py
    window_manager.py
    input_manager.py
    update_manager.py
    scene_manager.py
    shared_context.py
    param_manager.py       ← min_val/max_val
    object_manager.py      ← shared_context, register_tickable
    scalable.py
    screen_manager.py
    zoom_manager.py

  spores/
    spore.py
    spore_manager.py       ← create() прокси
    ghost_spore_family.py  ← НОВЫЙ

  math/
    double_integrator.py   ← stateless, ctx-aware
    spore_integrator.py
```

---

## 🚀 Как запустить

```bash
python main.py        # обычный запуск
python run.py         # с автоперезапуском
```

---

**Статус:** 🟢 Стабилен
