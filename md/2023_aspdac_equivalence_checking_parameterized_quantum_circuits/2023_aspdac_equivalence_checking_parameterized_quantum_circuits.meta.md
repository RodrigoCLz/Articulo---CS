# Equivalence Checking of Parameterized Quantum Circuits

| Campo | Valor |
|---|---|
| Archivo | `2023_aspdac_equivalence_checking_parameterized_quantum_circuits.pdf` |
| Autores | Tom Peham; Lukas Burgholzer; Robert Wille |
| Año | 2023 |
| Venue | Proceedings of the 28th Asia and South Pacific Design Automation Conference |
| DOI | 10.1145/3566097.3567932 |
| arXiv | — |
| Páginas | 7 |
| Palabras | 6,342 |
| Caracteres | 47,355 |
| Tokens estimados | ~11.8 k |
| Figuras | 9 |
| Tablas | 3 |
| Referencias | 42 |
| Citas recibidas | 45 |
| Densidad matemática | media (2.4 por 1k palabras) |
| Estado | ok |
| Convertido | 2026-11-21 12:15 (5.2 s) |

## Abstract

Variational quantum algorithms have been introduced as a promising class of quantum-classical hybrid algorithms that can already be used with the noisy quantum computing hardware available today by employing parameterized quantum circuits. Considering the non-trivial nature of quantum circuit compilation and the subtleties of quantum computing, it is essential to verify that these parameterized circuits have been compiled correctly. Established equivalence checking procedures that handle parameter-free circuits already exist. However, no methodology capable of handling circuits with parameters has been proposed yet. This work lls this gap by showing that verifying the equivalence of parameterized circuits can be achieved in a purely symbolic fashion using an equivalence checking approach based on the ZX-calculus. At the same time, proofs of inequality can be eciently obtained with conventional methods by taking advantage of the degrees of freedom inherent to parameterized circuits. We implemented the corresponding methods and proved that the resulting methodology is complete. Experimental evaluations (using the entire parametric ansatz circuit library provided by Qiskit as benchmarks) demonstrate the ecacy of the proposed approach. The implementation is open source and publicly available as part of the equivalence checking tool QCEC (https://github.com/cda-tum/qcec) which is part of the Munich Quantum Toolkit (MQT).

## Palabras clave

- equivalence checking
- variational quantum circuits
- variational quantum algorithms
- quantum circuit compilation
- ZX-calculus
- symbolic verification
- inequality proof
- hybrid quantum-classical algorithms

## Avisos

- Matemáticas moderadas: revisar ecuaciones
