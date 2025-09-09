.text
_start:
  @p 0x80        \ взять n из IO
  count_zero     \ вызвать процедуру (вернёт count на стеке)
  !p 0x84        \ записать результат в IO
  halt

count_zero:
  a!             \ A = n, стек пуст
  lit 0          \ count = 0  (TOS = count)
  lit 31         \ !!! 31 итерация -> всего 32 прохода тела
  >r

L:
  a              \ n
  lit 1
  and            \ (n & 1)
  if INC         \ если 0 -> инкрементируем count

CONT:
  a              \ n
  2/             \ n >>= 1
  a!             \ сохранить в A

  next L         \ повторять, пока R != 0 (преддекремент)

  ;              \ вернуть (на стеке остаётся count)

INC:
  lit 1
  +              \ count += 1
  CONT ;         \ безусловный переход к CONT
