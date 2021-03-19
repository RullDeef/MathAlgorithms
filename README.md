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
a, b, c in V     // iterators for input alphabet
A, B, C not in V // meta symbols

Aa -> aA         // 'a' iterates over input alphabet
A ->.            // final rule (with dot)
-> A             // spawning rule
```

---

## Usage

- **nalg** - algorifms executor

```
nalg [-h] [-f FILE] [input]

Executes normal algorifms.

positional arguments:
    input                 input string

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  algorifm source file
```

Example algorifm that **doubles** input word `double.txt`:
```
a, b in V
A, B not in V

Aa -> aBaA
Bab -> bBa
B ->
A ->.
-> A
```

```
nalg -f ./double.txt "abcb"

start conf: abcb
...
final conf: abcbabcb
```
