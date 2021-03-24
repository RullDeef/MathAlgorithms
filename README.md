# Algorithms executor

Advanced Markov Algorifms and Turing Machine executor.

---

## Installation

Using setuptools:

```
python setup.py install
```

Package is supplied with tests, which you can run by:

```
python setup.py pytest
```

---

## Normal Algorifms format

```
// comment starts with '//'

// context definition
a in V              // V strongly contains 'a'
for b, c in V       // iterators for input alphabet
A, B, C not in V    // meta symbols

// normal algorifm definition
Aa -> aaA           // meta 'A' duplicates symbol 'a'
Ab -> bA            // 'b' iterates over input alphabet, 'A' jumps over each symbol
A ->.               // final rule (with dot). 'A' disappears
-> A                // emitting rule
```

## Turing Machine format

```
// context definition
0, 1, # in V

// rule format:
// <sym1> -> <state> <sym2>, <step>
// sym1 - look symbol (or empty string)
// sym2 - replacement
// state - next state
// step - one of L, S or R

// special case, when sym1 = sym2 = starting marker:
// >> <state>, <step>

// 'q0'/'qf' - always starting/ending state

q0: // 'replacer' state
    >> q0, R        // '>>' used when cursor meets starting marker
    0 -> q0 1, R    // replace '0' with '1'
    1 -> q0 0, R    // replace '1' with '0'
    -> q1, L        // empty left side = meets space symbol. Goto state q1

q1: // 'go back till starting marker' state
    0 -> q1 0, L    // leave all as it is
    1 -> q1 1, L    // keep going
    >> qf, S        // stop work
```

---

## Usage

- **matalg** - algorithms executor

```
usage: matalg [-h] [-f FILE] [-t] [-i TIMEOUT] [-T] [-M] [input]

Executes algorithm models.

positional arguments:
  input                 input string

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  algorithm source file
  -t, --trace           trace execution by steps
  -i TIMEOUT, --timeout TIMEOUT
                        set timeout [default=1 sec]
  -T                    parse as turing machine
  -M                    parse as markov algorifm 
```

Example normal algorifm that **doubles** input word:
```
// double.txt
for a, b in V
A, B not in V

Aa -> aBaA
Bab -> bBa
B ->
A ->.
-> A
```

```
matalg -f ./double.txt -M --trace "abcb"

start:  abcb
next:   Aabcb
...
next:   abcbabcbA
result: abcbabcb
```

More examples you can find in directory `./algorithms`.
