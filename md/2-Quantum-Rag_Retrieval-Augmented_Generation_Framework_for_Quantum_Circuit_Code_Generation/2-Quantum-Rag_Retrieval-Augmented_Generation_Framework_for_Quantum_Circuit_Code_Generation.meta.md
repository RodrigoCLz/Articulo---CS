# Quantum-Rag: Retrieval-Augmented Generation Framework for Quantum Circuit Code Generation

| Campo | Valor |
|---|---|
| Archivo | `2-Quantum-Rag_Retrieval-Augmented_Generation_Framework_for_Quantum_Circuit_Code_Generation.pdf` |
| Autores | Nicholas Stapleton; Sharmin Afrose; Ethan Seefried; Vicente Leyton Ortega; Travis S. Humble; Tirthankar Ghosal |
| Año | 2026 |
| Venue | 2026 IEEE 19th Dallas Circuits and Systems Conference (DCAS) |
| DOI | 10.1109/DCAS69364.2026.11544968 |
| arXiv | — |
| Páginas | 5 |
| Palabras | 3,117 |
| Caracteres | 23,258 |
| Tokens estimados | ~5.8 k |
| Figuras | 1 |
| Tablas | 4 |
| Referencias | 20 |
| Citas recibidas | 0 |
| Densidad matemática | baja (1.0 por 1k palabras) |
| Estado | ok |
| Convertido | 2026-10-21 18:26 (5.1 s) |

## Abstract

Generating correct and executable quantum circuit code remains a significant barrier for both newcomers and experienced practitioners in quantum computing. While Large Language Models (LLMs) have shown promise in classical code generation, their application to quantum programming is ham-pered by limited domain-specific training data and the rapidly evolving nature of quantum software frameworks. In this work, we present Quantum-RAG, an extended Retrieval-Augmented Generation framework that couples a domain-specialized lan-guage model with a curated, multi-source knowledge corpus to produce Qiskit-based quantum circuit code. Our three-stage pipeline ingests documentation, educational notebooks, and re-search literature into a dense retrieval index and augments the generation model with the most relevant context at inference time. Evaluated on the Qiskit HumanEval benchmark, Quantum-RAG achieves a Pass@1 of 0.4132, a Pass@3 of 0.6291, and a Pass@5 of 0.7020, surpassing the domain-adapted Granite-Qiskit baseline by 101%, 72%, and 47% at each respective threshold. These results demonstrate that retrieval-augmented approaches can substantially improve quantum code generation without expensive model retraining.

## Palabras clave

- Quantum computing
- quantum circuits
- code generation
- retrieval-augmented generation
- large language mod-els
- Qiskit

## Avisos

- Sin avisos.
