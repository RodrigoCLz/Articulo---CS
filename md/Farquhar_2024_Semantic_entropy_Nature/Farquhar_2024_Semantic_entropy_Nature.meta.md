# Detecting hallucinations in large language models using semantic entropy

| Campo | Valor |
|---|---|
| Archivo | `Farquhar_2024_Semantic_entropy_Nature.pdf` |
| Autores | Sebastian Farquhar; Jannik Kossen; Lorenz Kuhn; Yarin Gal |
| Año | 2024 |
| Venue | Nature |
| DOI | 10.1038/s41586-024-07421-0 |
| arXiv | — |
| Páginas | 12 |
| Palabras | 11,308 |
| Caracteres | 78,008 |
| Tokens estimados | ~19.5 k |
| Figuras | 9 |
| Tablas | 2 |
| Referencias | 65 |
| Citas recibidas | 2596 |
| Densidad matemática | baja (1.4 por 1k palabras) |
| Estado | ok |
| Convertido | 2026-11-21 12:20 (7.3 s) |

## Abstract

Abstract Large language model (LLM) systems, such as ChatGPT 1 or Gemini 2 , can show impressive reasoning and question-answering capabilities but often ‘hallucinate’ false outputs and unsubstantiated answers 3,4 . Answering unreliably or without the necessary information prevents adoption in diverse fields, with problems including fabrication of legal precedents 5 or untrue facts in news articles 6 and even posing a risk to human life in medical domains such as radiology 7 . Encouraging truthfulness through supervision or reinforcement has been only partially successful 8 . Researchers need a general method for detecting hallucinations in LLMs that works even with new and unseen questions to which humans might not know the answer. Here we develop new methods grounded in statistics, proposing entropy-based uncertainty estimators for LLMs to detect a subset of hallucinations—confabulations—which are arbitrary and incorrect generations. Our method addresses the fact that one idea can be expressed in many ways by computing uncertainty at the level of meaning rather than specific sequences of words. Our method works across datasets and tasks without a priori knowledge of the task, requires no task-specific data and robustly generalizes to new tasks not seen before. By detecting when a prompt is likely to produce a confabulation, our method helps users understand when they must take extra care with LLMs and opens up new possibilities for using LLMs that are otherwise prevented by their unreliability.

## Palabras clave

- hallucination detection
- large language models
- semantic entropy
- uncertainty estimation
- confabulation
- LLM reliability
- generalization to unseen tasks
- honesty

## Avisos

- Sin avisos.
