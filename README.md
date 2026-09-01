# Password Strength Checker

A Python tool that estimates how long it would take to crack your password using both a **classical computer** and a **quantum computer** — a fun way to understand password security and the coming impact of quantum computing.

## Features

- Estimates crack time using classical brute-force attack
- Estimates crack time under a quantum attack (Grover's algorithm)
- Colour-coded strength feedback (Weak / Moderate / Strong / Uncrackable)
- Explains *why* a password is weak and how to improve it
- No password is stored or transmitted — runs entirely locally

## How It Works

**Classical attack** — assumes brute-force at ~10 billion guesses/second (modern GPU).

**Quantum attack** — applies Grover's algorithm, which gives a quadratic speedup: a quantum computer can search an N-item space in √N steps, effectively halving the bit-strength of any password.

```
Classical time = charset^length / guesses_per_second
Quantum time   = sqrt(charset^length) / quantum_guesses_per_second
```

## Getting Started

```bash
git clone https://github.com/abdwashere/passwordchecker
cd passwordchecker
python checker.py
```

```
Enter your password: ••••••••••••
Classical crack time : 3.2 years
Quantum crack time   : 4.7 hours
Strength             : Moderate — add symbols and increase length
```

## Tech Stack

| Component | Tool |
|---|---|
| Language | Python |
| Math | `math`, `string` standard libraries |

## What I Learned

- How brute-force attack complexity is calculated
- Grover's algorithm and quantum speedup fundamentals
- Why password length matters more than complexity
- The real-world implications of quantum computing on cybersecurity
