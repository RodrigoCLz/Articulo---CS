# Agent-Q: Fine-Tuning Large Language Models for Quantum Circuit Generation and Optimization

| Campo | Valor |
|---|---|
| Archivo | `Agent-Q_2025_QCE_LLM_quantum_circuit_generation.pdf` |
| Autores | Linus Jern; Valter Uotila; Cong Yu; Bo Zhao |
| Año | — |
| Venue | — |
| DOI | — |
| arXiv | 2504.11109 |
| Páginas | 12 |
| Palabras | 11,084 |
| Caracteres | 73,081 |
| Tokens estimados | ~18.3 k |
| Figuras | 15 |
| Tablas | 4 |
| Referencias | — |
| Citas recibidas | — |
| Densidad matemática | baja (0.6 por 1k palabras) |
| Estado | ok |
| Convertido | 2026-11-21 12:20 (20.4 s) |

## Abstract

Large language models (LLMs) have achieved re-markable outcomes in complex problems, including math, coding, and analyzing large amounts of scientific reports. Yet, few works have explored the potential of LLMs in quantum computing. The most challenging problem is to leverage LLMs to automatically generate quantum circuits at a large scale. Fundamentally, the ex-isting pre-trained LLMs lack the knowledge of quantum circuits. In this paper, we address this challenge by fine-tuning LLMs and injecting the domain-specific knowledge of quantum computing. We describe AGENT-Q, an LLM fine-tuning system to gen-erate and optimize quantum circuits. In particular, AGENT-Q implements the mechanisms to generate training data sets and constructs an end-to-end pipeline to fine-tune pre-trained LLMs to generate parameterized quantum circuits for various optimization problems. AGENT-Q provides 14,000 quantum cir-cuits covering a large spectrum of the quantum optimization landscape: 12 optimization problem instances and their opti-mized QAOA, VQE, and adaptive VQE circuits. Based thereon, AGENT-Q fine-tunes LLMs and constructs syntactically correct parametrized quantum circuits in OpenQASM 3.0. We have eval-uated the quality of the LLM-generated circuits and parameters by comparing them to the optimized expectation values and distributions. Experimental results show superior performance of AGENT-Q, compared to several state-of-the-art LLMs and better parameters than random. AGENT-Q can be integrated into an agentic workflow, and the generated parametrized circuits with initial parameters can be used as a starting point for further optimization, e.g., as templates in quantum machine learning and as benchmarks for compilers and hardware.

## Palabras clave

- large language models
- fine-tuning
- quantum circuit generation
- optimization
- parameter initialization

## Avisos

- DOI no detectado
