# Review & Ideas - Потенциальные проблемы и улучшения

**Дата:** 2026-03-19 (ревью от Claude Opus 4.6)

---

## Реальные проблемы (стоит починить)

### 1. MyObject ломается при зуме — это не "потенциальный" баг, а гарантированный

Уже описан в issues.md, но недооценён. Вот что происходит:

```python
# my_object.py — update_position() пишет в self.position
self.position = (x, 0, z)

# scalable.py — apply_transform() читает self.real_position
self.position = self.real_position * a + b
```

`real_position` устанавливается **один раз** в `__init__` Scalable и больше не меняется. Значит при зуме MyObject прыгнет на трансформированную начальную позицию, а не на текущую.

**Как проверить:** запустить, подождать 5 секунд, нажать E. Шар прыгнет.

**Фикс — простой, одна строка в `update_position`:**
```python
def update_position(self, dt):
    self.angle += self.speed * dt
    if self.angle >= 2 * math.pi:
        self.angle -= 2 * math.pi
    x = self.radius * math.cos(self.angle)
    z = self.radius * math.sin(self.angle)
    self.real_position = np.array([x, 0, z])  # <-- вот это
    self.position = (x, 0, z)
```

Но это поднимает вопрос: а что если зум уже активен? Тогда position нужно пересчитывать через текущую трансформацию. Значит MyObject должен знать о текущих a/b. Два пути:

- **Путь А (простой):** после `update_position` вызывать `apply_transform` с текущими a/b. UpdateManager уже знает ZoomManager — добавить один вызов.
- **Путь Б (чистый):** MyObject хранит ссылку на ZoomManager и сам вызывает apply_transform после обновления позиции.

Рекомендую путь А — минимальные изменения, одна строка в UpdateManager.

---

### 2. identify_invariant_point() вызывается каждый кадр впустую

В `UpdateManager.update_all()`:
```python
if self.zoom_manager:
    self.zoom_manager.identify_invariant_point()  # результат не используется
```

Функция считает тригонометрию, выделяет numpy array, и результат выбрасывается. Это не критично по производительности, но это мёртвый код, который путает при чтении. Либо убрать, либо если нужен для отладки — сохранять в `self.invariant_point`.

---

### 3. SceneSetup.input_handler() — мёртвый код

```python
def input_handler(self, key: str) -> None:
    if self.input_manager_mode:
        return
    if key == 'q':
        application.quit()
```

Этот метод **нигде не вызывается**. InputManager обрабатывает все клавиши. А Q сейчас — это zoom out, не quit. Метод можно удалить.

Аналогично `enable_input_manager_mode()` — нигде не вызывается, `input_manager_mode` всегда False.

---

### 4. `import time` внутри `update()` в main.py

```python
def update():
    import time
    update_manager.update_all(time.dt)
```

Это **не** стандартный `time` модуль. Это `ursina.time` (магический объект Ursina). Работает только потому что Ursina подменяет `time` в глобальном scope при запуске. Код выглядит как баг, хотя технически работает. Лучше явно:

```python
from ursina import time as ursina_time

def update():
    update_manager.update_all(ursina_time.dt)
```

---

## Мелочи (не горит, но стоит знать)

### 5. sys.path.insert в main.py — лишний

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
```

Все импорты в main.py уже через `from src.xxx import`, что работает без модификации sys.path. Строка осталась от старой версии.

---

### 6. ScalableFloor — пустой класс

```python
class ScalableFloor(Scalable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
```

Делает то же что `Scalable`. Если планируется добавлять логику пола — ок, иначе можно просто использовать `Scalable`.

---

### 7. WindowManager.MONITORS — захардкожены под конкретную конфигурацию мониторов

```python
MONITORS = {
    "main": {"size": (1920, 1080), "position": (0, 0)},
    "left": {"size": (1800, 950), "position": (-1850, 250)},
    ...
}
```

Это нормально для песочницы, но если проект когда-нибудь уедет на другую машину — окно улетит за экран. Просто знать об этом.

---

### 8. Frame не является Scalable, но его дети — да

Frame наследует от Entity, а его оси — от Scalable. Они регистрируются в ZoomManager поштучно. Это работает, но есть нюанс: `frame.toggle_visibility()` устанавливает `enabled` через Frame, а ZoomManager обрабатывает детей отдельно. Пока это ок, но если появится потребность двигать весь фрейм целиком — будет путаница.

---

## Идеи улучшений (на будущее)

### A. Визуализация invariant point

Добавить маркер (маленькую сферу/крест) на полу в точке, куда смотрит камера. Это сразу покажет что zoom работает правильно и куда будет происходить масштабирование. Сделать toggle по клавише.

**Сложность:** ~20 строк.

---

### B. Smooth zoom

Сейчас зум дискретный — нажал E, всё мгновенно скачет на 12.5%. Можно добавить интерполяцию: хранить target_a и target_b, и в update() плавно приближаться к ним (lerp).

**Сложность:** ~30 строк в ZoomManager + изменение в UpdateManager.

---

### C. Зум колёсиком мыши

Сейчас E/Q. Колёсико мыши — интуитивнее и стандартнее. В Ursina это `scroll up` / `scroll down` в input handler.

**Сложность:** 4 строки в InputManager.

---

### D. Сохранение/загрузка состояния камеры

Клавиши для быстрого сохранения позиции камеры (например, Ctrl+1..5 для сохранения, 1..5 для загрузки). Удобно при исследовании сцены — можно быстро вернуться к интересной точке.

**Сложность:** ~40 строк.

---

## Чего я бы НЕ делал

- **Logging вместо print** — это песочница, print достаточно. Logging добавляет настройку без реальной пользы тут.
- **colors.json** — дефолтные цвета работают, warning в консоли не мешает. Файл создать можно, но это не приоритет.
- **Юнит-тесты** — математика зума проверена визуально, а тестировать Ursina entity'и — больше мороки чем пользы.
- **Рефакторинг InputManager в декларативную структуру** — при 10 клавишах if/elif читается лучше чем маппинг-словарь. Делать когда будет 30+.
- **try-except для arrow.obj** — файл есть, не удалится сам. Defensive programming ради defensive programming.

---

## Приоритеты (если делать)

| # | Что | Зачем | Строк |
|---|-----|-------|-------|
| 1 | Починить MyObject + zoom | Реальный баг | ~5 |
| 2 | Убрать мёртвый identify_invariant_point() в update | Чистота | 1 |
| 3 | Убрать мёртвый input_handler в SceneSetup | Чистота | ~15 удалить |
| 4 | Зум колёсиком | UX | 4 |
| 5 | Визуализация invariant point | Наглядность | ~20 |
| 6 | Smooth zoom | Приятность | ~30 |
