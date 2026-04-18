# Current State - Текущее состояние проекта

**Last updated:** 2026-04-19 (сессия 7)

---

## ✅ Что работает

### Базовая функциональность:
- ✅ **Камера** (FirstPersonController)
  - WASD движение
  - Mouse look
  - Space/Shift вертикаль
  - Alt для захвата/освобождения курсора

- ✅ **Zoom система**
  - E/Q и scroll up/down - zoom in/out
  - R - reset zoom
  - Математически корректная с сохранением invariant point
  - Масштабирование всех зарегистрированных объектов

- ✅ **Визуализация**
  - Координатная система (Frame) с осями XYZ
  - Клетчатый пол (ScalableFloor)
  - Spore — плоский круг (Circle mesh), zoom-aware маркер
  - SporeManager — управление размером спор (3/4)

- ✅ **Управление**
  - InputManager - централизованная обработка ввода
  - UpdateManager - координация update() всех компонентов
  - WindowManager - fullscreen (F11), мониторы
  - `U` - toggle frame visibility
  - Key binding system: `object_manager.bind(func, trigger, key, description)` — key и description обязательны
  - `input_frozen` блокирует все биндинги автоматически (проверка перед `object_manager.handle_input`)

- ✅ **Архитектура объектов**
  - `GameObject(Scalable)` - базовый класс с `tick(dt)` stub
  - `ObjectManager` - фабрика + реестр + биндинги клавиш + авторегистрация Spore в SporeManager
  - `ScreenManager` + `Message` — вывод текста на экран, динамический getter каждый кадр
  - `Frame` внутри `SceneSetup` (не отдельный объект)
  - Новый объект = `object_manager.create(MyClass, 'name', **kwargs)`

- ✅ **Математика (src/math/)**
  - `DoubleIntegrator` - 1D double integrator (x_ddot = u)
  - state = [x, x_dot], control = u (скаляр)
  - Точное аналитическое интегрирование (линейная система, без накопления ошибок)

- ✅ **Визуализация траекторий (сессия 5–6)**
  - `src/trajectories.py` — `generate_trajectories(start_state, pattern_length, tau, N, seed, pattern_index)`
  - `src/spore.py` — статичный маркер-quad, billboard=True, наследник MyObject
  - `src/spore_manager.py` — управление размером всех спор (клавиши 3/4, мультипликативно ×1.2)
  - `src/scalable_line.py` — линия между двумя точками, zoom-aware через override apply_transform
  - `PATTERN_INDICES` + `PATTERN_COLORS` в main.py — контроль какие паттерны и каким цветом
  - Маппинг state → Ursina: `pos=(x, 0, x_dot)` — phase portrait в плоскости xOz (x = позиция, z = скорость)

- ✅ **Инфраструктура**
  - ColorManager - управление цветами (с fallback на дефолты)
  - Watcher - автоперезапуск при изменении .py файлов
  - DI pattern - избежание циркулярных импортов

---

## 🔄 Что в процессе

*Нет задач в процессе.*

---

## ❌ Что сломано / не работает

- ❌ **colors.json** - файл отсутствует
  - Проект работает с дефолтными цветами
  - ColorManager ищет `config/json/colors.json` но не находит
  - Не критично, но warning в консоли

- ~~❌ **MyObject.real_position не обновляется при анимации**~~ ✅ Исправлено (сессия 3)

---

## 📊 Метрики

### Размер кодовой базы:
```
src/
├── scalable.py           ~45 lines  (+ GameObject)
├── frame.py              ~92 lines
├── scene_setup.py        ~125 lines (+ Frame внутри, toggle_frame)
├── zoom_manager.py       ~103 lines
├── color_manager.py      ~50 lines
├── window_manager.py     ~100 lines
├── input_manager.py      ~110 lines (упрощён)
├── update_manager.py     ~60 lines  (упрощён)
├── object_manager.py     ~50 lines  (новый)
├── my_object.py          ~80 lines
└── math/
    ├── __init__.py       ~2 lines
    └── double_integrator.py  ~100 lines

main.py                   ~130 lines (упрощён)
```

**Общий объем:** ~1000 строк кода (без комментариев)

### Зависимости:
- Python 3.12
- ursina (3D движок)
- numpy (математика)
- watchdog (watcher для auto-reload)

---

## 🎯 Текущая фокус-область

**Нет активной задачи.** Базовый функционал работает, проект стабилен.

---

## 📝 Недавние изменения

### 2026-03-19 (сессия 5):
- ✅ `src/trajectories.py` — генерация DiffDrive-траекторий по паттернам управления
- ✅ `src/spore.py` — статичный quad-маркер (наследник MyObject, billboard)
- ✅ `src/spore_manager.py` — управление размером всех спор (3/4, мультипликативно)
- ✅ `src/scalable_line.py` — scalable-линия, обновляет mesh-вершины при zoom
- ✅ MyObject принимает `model` через kwargs.pop (для override в подклассах)
- ✅ Фикс: Spore.real_position обновляется после установки pos

### 2026-03-19 (сессия 4):
- ✅ Mouse wheel zoom (scroll up/down = zoom in/out)
- ✅ `ObjectManager` — фабрика + реестр + binding system
- ✅ `GameObject(Scalable)` — базовый класс с `tick(dt)`
- ✅ `Frame` перенесён внутрь `SceneSetup`
- ✅ Key binding system: `bind(func, trigger=lambda key: ...)` вместо `on_input` в объектах
- ✅ `tick(dt)` вместо `update(dt)` — избежание конфликта с Ursina Entity.update()
- ✅ `src/math/double_integrator.py` — 2D double integrator (x_ddot=ux, y_ddot=uy), точное интегрирование

### 2026-03-19 (сессия 3):
- ✅ Фикс Issue #1: MyObject.real_position теперь обновляется при анимации
- ✅ UpdateManager: после обновления позиции MyObject применяется текущий zoom transform
- ✅ Добавлен комментарий к `import time` в main.py (ursina magic)
- ✅ Создан `llm/review_and_ideas.md` — ревью кодовой базы с потенциальными проблемами и идеями

### 2026-03-19 (сессия 2):
- ✅ Добавлена клавиша `U` для toggle frame visibility
- ✅ Фикс: скрытый Frame теперь получает zoom трансформации (убрана проверка `enabled` в `update_transform`)
- ✅ Создана документация InputManager: `llm/context/input_manager_guide.md`
- ✅ Обновлён backlog в `plan.md`

### 2026-03-19 (сессия 1):
- ✅ Создана полная структура `llm/` (14 файлов)
- ✅ Написаны все файлы контекста
- ✅ Проанализированы проблемы (5 issues)
- ✅ Документирована архитектура (7 решений)
- ✅ Обновлен README.md
- ✅ Создан отдельный git репозиторий
- ✅ Запушено на GitHub

---

## 🔮 Ближайшие планы

См. [`plan.md`](plan.md) для детального плана.

**Краткая версия:**
1. ~~Исправить Issue #1 (MyObject.real_position при анимации)~~ ✅
2. Исправить Issue #2 (создать config/json/colors.json)
3. Идеи в backlog → `plan.md`
4. См. `llm/review_and_ideas.md` для дополнительных идей

---

## ⚙️ Конфигурация разработки

### IDE: VSCode
- Используется Claude Code extension

### Python environment:
- Python 3.12
- Виртуальное окружение (предполагается)

### Git:
- Текущая ветка: `main`
- Последний коммит: "Добавлены классы для адаптивного управления..."
- Много незакоммиченных изменений (см. git status)

---

## 🚀 Как запустить проект

```bash
# Обычный запуск
python main.py

# С автоперезапуском (для разработки)
python run.py

# Установка зависимостей
pip install ursina numpy watchdog
```

---

**Статус:** 🟢 Проект стабилен, визуализация траекторий работает
