# Current State - Текущее состояние проекта

**Last updated:** 2026-04-23 (сессия 9)

---

## ✅ Что работает

### Базовая функциональность:
- ✅ **Камера** (FirstPersonController) — WASD, Mouse look, Space/Shift, Alt курсор
- ✅ **Zoom система** — scroll/Q/E zoom, R reset, математически корректная с invariant point
- ✅ **Визуализация** — Frame (XYZ оси), клетчатый пол, Spore (Circle), GhostSpore
- ✅ **ScreenManager + Message** — динамический текст на экране через getter каждый кадр

### Архитектура (сессия 9):
- ✅ **`src/` реорганизована** на `core/`, `spores/`, `math/`, `utils/`
- ✅ **`SceneSetup` → `SceneManager`** (файл `scene_manager.py`)
- ✅ **`register(**kwargs)`** — универсальная регистрация компонентов (вместо `register_X()` методов)
- ✅ **`tick()`** — единое имя для per-frame обновления у всех компонентов
- ✅ **`ParamManager`** — хранит именованные параметры (`add`, `tweak`), exp/linear режимы
- ✅ **`InputManager.bind()`** — биндинги с `mode='press'` и `mode='scroll'` (hold+scroll)
- ✅ **hold+scroll подавляет зум** — если зажата клавиша параметра, зум не срабатывает
- ✅ **Подсказка** в `get_help()` с текущими значениями параметров

### Управление (актуальное):
- `1` + scroll — tau
- `2` + scroll — spore size
- `scroll` — zoom (если нет зажатой клавиши параметра)
- `Q/E` — zoom in/out
- `R` — reset zoom
- `U` — toggle frame
- `Alt` — захват/освобождение курсора
- `F11` — fullscreen
- `H` — debug info
- `Esc` — выход

### Математика (src/math/):
- ✅ `DoubleIntegrator` — 1D double integrator, аналитическое интегрирование
- ✅ `SporeIntegrator` — обёртка для генерации траекторий

---

## 🔄 Что в процессе

*Нет задач в процессе.*

---

## ❌ Что сломано / не работает

- ❌ **colors.json** — файл отсутствует, warning в консоли (не критично, дефолты работают)

---

## 📁 Структура src/

```
src/
  core/         ← переиспользуемое в любом проекте
    color_manager.py
    window_manager.py
    input_manager.py
    update_manager.py
    scene_manager.py      ← (бывший scene_setup.py, класс SceneManager)
    shared_context.py
    param_manager.py
    object_manager.py
    scalable.py
    scalable_line.py
    scalable_surface.py
    frame.py
    screen_manager.py
    zoom_manager.py

  spores/       ← специфика этого проекта
    spore.py
    spore_manager.py
    trajectories.py

  math/         ← математика
  utils/        ← watcher.py, nb_logger.py
```

---

## 🚀 Как запустить

```bash
python main.py        # обычный запуск
python run.py         # с автоперезапуском
```

---

**Статус:** 🟢 Стабилен, все биндинги работают
