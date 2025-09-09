
# Лабораторная №3 — Wrench / acc32 & f32a

Этот репозиторий содержит решения для варианта **`is_prime` (acc32)** и **`count_zero` (f32a)** в рамках лабораторной работы по архитектуре компьютера.  
Интерфейс ввода/вывода и требования взяты из условия лабы и документации Wrench.

> **Интерфейс:**  
> вход: 32‑битное слово по адресу **`0x80`**  
> выход: 32‑битное слово по адресу **`0x84`**  
> если `n < 1` → вернуть **`-1`** (`0xFFFFFFFF`)


---

## Быстрый старт (CLI)

Требуется установленный **wrench**.

```bash
# acc32: запустить проверку примера is_prime с конфигом
wrench --isa acc32 acc32_is_prime.s -c configs/is_prime_neg12.yaml

# f32a: запустить count_zero
wrench --isa f32a f32a_count_zero.s -c configs/count_zero_5.yaml
```

**Важно:** конфиги для CLI — _чистый_ YAML без `/* … */`.  
Отчёты/трассы настраиваются в разделе `reports` файла `.yaml` (см. примеры ниже).

---

## Запуск на странице **Wrench Submit** (веб‑форма)

В поле `/* assembler_code */` вставляете код из соответствующего файла разметки ниже.  
В поле `/* simulation_config */` — конфиг **внутри многострочного комментария**:

```text
/* simulation_config
isa: acc32         # или f32a
loglevel: trace
max_cycles: 20000
input:
  - addr: 0x80
    value: 5
*/
```

---

## Решение 1: **acc32 / is_prime**

### Идея алгоритма
1. Область определения: `n < 1` → `-1`; `n == 1` → `0`; `n == 2` → `1`.
2. Если `n` чётное (`n % 2 == 0`) → `0`.
3. Проверяем делители `i = 3, 5, 7, …` до условия `i*i > n` (т. е. до `√n`).  
   Если делитель найден → `0`, иначе в конце → `1`.

### Код (acc32)
> Читает `n` из `0x80`, пишет ответ в `0x84`. Код сдвинут `.org 0x100`, чтобы не пересекаться с MMIO.

```asm
.data
n:      .word 0x0          ; входное n
i:      .word 0x0          ; делитель i
zero:   .word 0x0
one:    .word 0x1
two:    .word 0x2
three:  .word 0x3
mone:   .word 0xffffffff   ; -1

.org 0x100                  ; уводим .text подальше от MMIO (0x80..0x84)

.text
_start:
    load_addr 0x80         ; ACC = *0x80
    store_addr n           ; n = ACC

    load_addr n            ; ACC = n
    sub one                ; ACC = n - 1
    ble domain_error       ; if (n-1) < 0 → n < 1 → -1
    beqz not_prime         ; if (n-1) == 0 → n == 1 → 0

    load_addr n            ; n == 2 ?
    sub two
    beqz prime

    load_addr n            ; чётность: если n % 2 == 0 → 0
    rem two
    beqz not_prime

    load_addr three        ; i = 3
    store_addr i

loop:
    load_addr i            ; if (i*i > n) → простое
    mul i
    sub n
    bgt prime

    load_addr n            ; if (n % i == 0) → составное
    rem i
    beqz not_prime

    load_addr i            ; i += 2
    add two
    store_addr i
    jmp loop

prime:
    load_addr one
    store_addr 0x84
    halt

not_prime:
    load_addr zero
    store_addr 0x84
    halt

domain_error:
    load_addr mone
    store_addr 0x84
    halt
```

### Аннотированное «построчно» (суть алгоритма)
- `loop:` — ядро решения (перебор нечётных делителей до `i*i > n`).  
- До цикла — «быстрые отсеки» (`n<1`, `1`, `2`, чётность).  
- Запись результата: `store_addr 0x84` и `halt`.

### Пример конфига (CLI)

**is_prime: `n = -12` → `-1`**
```yaml
limit: 60000
memory_size: 0x1000

memory_mapped_io:
  0x80: [-12]
  0x84: []

reports:
  - name: trace
    slice: all
    view: |
      {pc}: {instruction}  ACC={Acc:hex}  V={V}  C={C}

  - name: result
    slice: last
    view: |
      numio[0x80]: {io:0x80:dec}
      numio[0x84]: {io:0x84:dec}
    assert: |
      numio[0x80]: [] >>> []
      numio[0x84]: [] >>> [-1]
```

---

## Решение 2: **f32a / count_zero**

### Задание
Посчитать количество нулей в двоичном представлении 32‑битного числа:
```py
# эталон на Python
def count_zero(n):
    count = 0
    for _ in range(32):
        count += 0 if (n & 1) else 1
        n >>= 1
    return count
```

### Идея реализации (Forth‑style стек)
- Держим текущее `n` **в регистре `A`**.
- На **data stack** — только `count`.
- Цикл на **32 итерации** через `>r … next L`. По семантике `next` кладём в `R` **31**, чтобы телo выполнилось 32 раза.
- На каждом шаге: проверить `(n & 1)`, при нуле — инкремент `count`, затем `n >>= 1` (инструкция `2/`).

### Код (f32a)
```asm
.text
_start:
  @p 0x80        \ взять n из IO (на стек)
  count_zero     \ вызвать процедуру (вернёт count на стеке)
  !p 0x84        \ сохранить результат в IO
  halt

count_zero:
  a!             \ A = n ; стек пуст
  lit 0          \ TOS = count
  lit 31         \ положим 31 → next даст 32 прохода
  >r

L:
  a              \ TOS = n
  lit 1
  and            \ TOS = (n & 1)
  if INC         \ если 0 → инкремент счётчика

CONT:
  a              \ n
  2/             \ n >>= 1
  a!             \ A = новое n

  next L         \ повторять пока R != 0 (в сумме 32 раза)

  ;              \ вернуть (на стеке count)

INC:
  lit 1
  +              \ count += 1
  CONT ;         \ безусловный переход к CONT
```

### Примеры конфигов (CLI)

**count_zero: `n = 5` → `30`**
```yaml
limit: 20000
memory_size: 0x1000
memory_mapped_io:
  0x80: [5]
  0x84: []
reports:
  - name: result
    slice: last
    view: |
      numio[0x80]: {io:0x80:dec}
      numio[0x84]: {io:0x84:dec}
    assert: |
      numio[0x80]: [] >>> []
      numio[0x84]: [] >>> [30]
```

**count_zero: `n = 7` → `29`**
```yaml
limit: 20000
memory_size: 0x1000
memory_mapped_io:
  0x80: [7]
  0x84: []
reports:
  - name: result
    slice: last
    view: |
      numio[0x80]: {io:0x80:dec}
      numio[0x84]: {io:0x84:dec}
    assert: |
      numio[0x84]: [] >>> [29]
```

**count_zero: `n = 247923789` → `19`**
```yaml
limit: 20000
memory_size: 0x1000
memory_mapped_io:
  0x80: [247923789]
  0x84: []
reports:
  - name: result
    slice: last
    view: |
      numio[0x84]: {io:0x84:dec}
    assert: |
      numio[0x84]: [] >>> [19]
```

---

## Часто задаваемое

### Что такое **label** (метка) и откуда берутся адреса?
Метка — имя позиции в коде/данных. Ассемблер считает **адрес** каждой метки из счётчика размещения секции.  
`.org 0x100` переносит начало `.text` на адрес `0x100`. Переходы/вызовы получают адрес метки автоматически.

### Что такое **ACC** (accumulator) в acc32?
Главный 32‑битный регистр. Почти все арифметические/логические инструкции читают/пишут ACC.  
`beqz/bgt/ble` проверяют **само значение ACC** (0, >0, <0).

### Как вывести ACC в HEX в отчёте?
В `reports.view` используйте плейсхолдеры: `{Acc:hex}` / `{Acc:dec}`. Пример трассы выше.

### Зачем `.org 0x100` и/или «alignment‑паддинг»?
Чтобы код не попал рядом с MMIO (`0x80/0x84`). Иначе запись в `0x84` может «перетереть» инструкцию → ошибка `instruction in memory corrupted`.

### Почему в acc32 есть и `load_addr`, и `load`?
- `load_addr <abs>` — абсолютный адрес (нужно для MMIO/глобалов).  
- `load <rel>` — PC‑относительная адресация (короче и удобна для позиционно‑независимого кода).

### Переполнение/перенос (V/C) в acc32
`add` ставит **C** (перенос) и **V** (переполнение). `sub/mul` трогают **V`.  
В этой лабе (is_prime) специальных обработок не требуется; но при необходимости делайте `bvs`‑ветку и возвращайте `0xCCCCCCCC` по правилам курса.

### Минимальный набор Load*
Для учебной полезности стоит оставлять **`load_addr/store_addr`** (абсолют) и **косвенные `load_ind/store_ind`**.  
PC‑relative `load/store` — удобные, но не критичны (можно убрать при необходимости, потеряете компактность/позиционность).

---

## Траблшутинг

- **`YAML parse exception … mapping values are not allowed`** — в CLI конфиге остались `/* … */`. Уберите их, используйте _чистый_ YAML.
- **`instruction in memory corrupted`** — код пересёкся с MMIO. Поставьте `.org 0x100` или добавьте паддинг в `.data`.
- **«неизвестная инструкция»** — проверьте ISA (acc32 vs f32a) и точные мнемоники из доки.
- **off‑by‑one в f32a‑цикле** — для 32 итераций кладите в `R` **31** перед `next`.

---

## Структура репозитория (рекомендация)
```
.
├── acc32_is_prime.s
├── f32a_count_zero.s
└── configs/
    ├── is_prime_neg12.yaml
    ├── count_zero_5.yaml
    ├── count_zero_7.yaml
    └── count_zero_247923789.yaml
```

Удачи на защите! Если потребуется — можно добавить версии для `risc-iv-32` с вложенными процедурами/рекурсией.
