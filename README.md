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

## Algorifm format (future)

```
// comment starts with '//'
for a, b, c in V     // iterators for input alphabet
A, B, C not in V     // meta symbols

// you can combine algorifms using following constructions:
// A * B        >> A(B(x))
// A ( B | C )  >> if (A(x) == lambda) then B(x) else C(x)
// A { B }      >> while A(x) == lambda do x := B(x)
// A < B >      >> while A(x) <> lambda do x := B(x)

// 'alg' and 'is' required for complex algorifms
alg Comb is
    Traverse * Traverse

// each simple algorifm starts with 'alg <name>'
alg Traverse:
    Aa -> aA         // 'a' iterates over input alphabet
    A ->.            // final rule (with dot)
    -> A             // emitting rule
```

## Turing Machine format (far future)

```
0, 1, # in V
for a in {0, 1} // iterate over specific symbols in alphabet

// Turing machine for determining constructive positive number
tur IsCNN
    q_0 * -> q_0 *, R
    q_0 -> q_f , L
    q_0 0 -> q_1 0, R
    q_0 1 -> q_f 1, L

/* possible syntax simplification:
    q_0:
        * -> q_0 *, R
        -> q_f , L
        0 -> q_1 0, R
        1 -> q_f 1, L

    q_1:
        ...
*/
```

---

## Usage

- **matalg** - algorithms executor

```
usage: nalg [-h] [-f FILE] [-t | --trace | --no-trace] [input]

Executes algorithms.

positional arguments:
  input                 input string

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  algorithm source file
  -t, --trace, --no-trace
                        trace execution by steps
```

Example algorithm that **doubles** input word:
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
matalg -f ./double.txt --trace "abcb"

start:  abcb
...
result: abcbabcb
```
