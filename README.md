# Markov algorifms executor

---

Advanced Markov Algorifms executor for executing Markov Algorifms.

---

## Installation

Using setuptools:

```
python setup install
```

---

## Algorifm format

```
// comment starts with '//'
for a, b, c in V     // iterators for input alphabet
A, B, C not in V     // meta symbols

// you can combine algorifms using following constructions:
// A * B        >> A(B(x))
// A ( B | C )  >> if (A(x) == lambda) then B(x) else C(x) *not available for now*
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

---

## Usage

- **nalg** - algorifms executor

```
usage: nalg [-h] [-f FILE] [-t | --trace | --no-trace] [input]

Executes normal algorifms.

positional arguments:
  input                 input string

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  algorifm source file
  -t, --trace, --no-trace
                        trace execution by steps
```

Example algorifm that **doubles** input word (`double.txt`):
```
for a, b in V
A, B not in V

alg Double
    Aa -> aBaA
    Bab -> bBa
    B ->
    A ->.
    -> A
```

```
nalg -f ./double.txt --trace "abcb"

start:  abcb
...
result: abcbabcb
```
