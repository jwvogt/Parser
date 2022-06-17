# While/Proc Parser

This was a project assigned during the Automata/Formal Langs class I took at UAB.
The task was to be able to parse programs in a simple "while/proc" programming language, and return an Abstract Syntax Tree that could be used to compile the program.

## While/Proc Grammar

```
(starting symbol P)
P -> S ";" P | S
S -> "proc" f "(" L ")" "{" P "}"
   | "if" C "{" P "}" "else" "{" P "}"
   | "while" C "{" P "}"
   | "print" C
   | C
L -> x "," X | x | Ɛ
X -> x "," X | x
C -> E | E "<" E | E "=" E
E -> T | T M
M -> "+" T M | "-" T M | Ɛ
T -> F | F N
N -> "*" F N | "/" F N | Ɛ
F -> A | A "^" F
A -> "(" C ")"
   | x B
   | f "(" R ")"
   | n
B -> ":" "=" C | Ɛ  ## this was added in order to left-factor A
R -> C "," Q | C | Ɛ
Q -> C "," Q | C
```
