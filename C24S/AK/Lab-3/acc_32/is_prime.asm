; is_prime (acc32)
; Вход:  *0x80 = n
; Выход: *0x84 = 1 (prime) | 0 (composite) | 0xFFFFFFFF (-1, n < 1)

.data
; рабочие ячейки
n:      .word 0x0
i:      .word 0x0

; константы
zero:   .word 0x0
one:    .word 0x1
two:    .word 0x2
three:  .word 0x3
mone:   .word 0xffffffff

; --- опционально: прокладка, чтобы .text точно ушёл за 0x80 ---
; Если твой ассемблер не понимает .org, оставь .org закомментированной
; и добавь прокладку .word (см. ниже):
; pad:   .word 0,0,0,0,0,0,0,0,0,0    ; при необходимости — увеличить список

; переносим начало кода за IO-область
.org 0x100

.text
_start:
    ; n = *0x80  (прямой IO)
    load_addr 0x80
    store_addr n

    ; --- domain check: n < 1 → -1 ---
    load_addr n
    sub one                  ; acc = n - 1
    ble domain_error         ; acc < 0 ?  => n < 1
    beqz not_prime           ; acc == 0 ? => n == 1 -> 0

    ; n == 2 -> 1
    load_addr n
    sub two
    beqz prime

    ; чётность: n % 2 == 0 -> 0
    load_addr n
    rem two
    beqz not_prime

    ; i = 3
    load_addr three
    store_addr i

loop:
    ; если i*i > n -> prime
    load_addr i
    mul i                    ; acc = i*i
    sub n                    ; acc = i*i - n
    bgt prime                ; acc > 0 ? делителей нет

    ; если n % i == 0 -> composite
    load_addr n
    rem i
    beqz not_prime

    ; i += 2
    load_addr i
    add two
    store_addr i
    jmp loop

prime:
    load_addr one
    store_addr 0x84          ; прямой вывод в IO
    halt

not_prime:
    load_addr zero
    store_addr 0x84
    halt

domain_error:
    load_addr mone
    store_addr 0x84
    halt
