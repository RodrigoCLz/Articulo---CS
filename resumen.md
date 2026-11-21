# Resumen de artículos

11 artículos convertidos desde `pdf's/`.

| ID | Título de la investigación | Autores | Año | Revista / Conferencia | Cuartil (SJR / JCR) | Citas | URL / DOI | Aporte Principal |
|---|---|---|---|---|---|---|---|---|
| 1 | Benchmarking the Benchmarks for Quantum Code Generation with LLMs | Feng, Y.; Yang, X.; Sha, K.; et al. (4) | 2026 | DCAS 2026 | — (congreso) | 0 | [10.1109/DCAS69364.2026.11545019](https://doi.org/10.1109/DCAS69364.2026.11545019) | Revisa los benchmarks de generación de código cuántico y los unifica en cuatro dimensiones (validez sintáctica/API, corrección semántica y física, viabilidad de recursos y feedback de ejecución), proponiendo una lista de verificación mínima para reportar resultados. |
| 2 | Quantum-Rag: Retrieval-Augmented Generation Framework for Quantum Circuit Code Generation | Stapleton, N.; Afrose, S.; Seefried, E.; et al. (6) | 2026 | DCAS 2026 | — (congreso) | 0 | [10.1109/DCAS69364.2026.11544968](https://doi.org/10.1109/DCAS69364.2026.11544968) | Propone Quantum-RAG, un pipeline de tres etapas que indexa documentación, notebooks y literatura para aumentar un LLM especializado; mejora la generación de circuitos Qiskit sobre Qiskit HumanEval. |
| 3 | Code generation for classical-quantum software systems modeled in UML | Jiménez-Navajas, L.; Pérez-Castillo, R.; Piattini, M. | 2025 | Software and Systems Modeling | Q2 (SJR) | 4 | [10.1007/s10270-024-01259-w](https://doi.org/10.1007/s10270-024-01259-w) | Define una transformación modelo-a-texto (Epsilon/EGL) que genera código Python y Qiskit desde modelos UML extendidos, cubriendo la fase de ingeniería directa en la modernización de sistemas híbridos clásico-cuánticos; validada con 7 casos. |
| 4 | QuanBench: Benchmarking Quantum Code Generation with Large Language Models | Guo, X.; Wang, M.; Zhao, J. | 2025 | ASE 2025 | — (congreso) | 4 | [10.1109/ASE63991.2025.00218](https://doi.org/10.1109/ASE63991.2025.00218) | Presenta QuanBench, un benchmark de 44 tareas evaluadas por corrección funcional (Pass@K) y equivalencia semántica cuántica (Process Fidelity); los LLM evaluados no superan el 40% de acierto. |
| 5 | PennyCoder: Efficient Domain-Specific LLMs for PennyLane-Based Quantum Code Generation | Basit, A.; Shao, M.; Asif, M.; et al. (7) | 2025 | QCE 2025 | — (congreso) | 2 | [10.1109/QCE65121.2025.10324](https://doi.org/10.1109/QCE65121.2025.10324) | Desarrolla PennyCoder, un LLM ligero (LLaMA 3.1-8B con LoRA e instrucciones de dominio) desplegable localmente para generar código PennyLane sin depender de APIs remotas, con mejoras en sintaxis y tareas de QML/QRL. |
| 6 | QHackBench: Benchmarking Large Language Models for Quantum Code Generation Using PennyLane Hackathon Challenges | Basit, A.; Shao, M.; Asif, M.; et al. (7) | 2025 | QAI 2025 | — (congreso) | 3 | [10.1109/QAI63978.2025.00056](https://doi.org/10.1109/QAI63978.2025.00056) | Introduce QHackBench, un benchmark construido con retos reales del hackathon QHack, y compara prompting estándar frente a RAG; el RAG no mejora de forma clara en los algoritmos complejos. |
| 7 | Model-Driven Quantum Code Generation Using Large Language Models and Retrieval-Augmented Generation | Siavash, N.; Moin, A. | 2025 | MODELS 2025 | — (congreso) | 4 | [10.1109/MODELS67397.2025.00031](https://doi.org/10.1109/MODELS67397.2025.00031) | Explora la generación de código cuántico desde modelos UML combinando LLM y RAG con ejemplos de Qiskit de GitHub; prompts bien diseñados multiplican hasta por cuatro el CodeBLEU. |
| 8 | Enhancing LLM-based Quantum Code Generation with Multi-Agent Optimization and Quantum Error Correction | Campbell, C.; Chen, H.; Luk, W.; et al. (4) | 2025 | DAC 2025 | — (congreso) | 8 | [10.1109/DAC63849.2025.11133316](https://doi.org/10.1109/DAC63849.2025.11133316) | Propone el primer framework multi-agente para generar código cuántico tolerante a fallos: agentes especializados en corrección de errores cuánticos que refinan el código mediante análisis semántico iterativo. |
| 9 | Quantum-Aware Large Language Models: Taxonomy, Architectures, and Future Applications | Dede, R. | 2025 | ICECCE 2025 | — (congreso) | 0 | [10.1109/ICECCE67514.2025.11257941](https://doi.org/10.1109/ICECCE67514.2025.11257941) | Survey que organiza la intersección entre computación cuántica y LLM: generación automática de código cuántico, arquitecturas transformer híbridas y procesamiento de lenguaje natural cuántico (QNLP), con modelos, benchmarks y aplicaciones. |
| 10 | Qiskit HumanEval: An Evaluation Benchmark for Quantum Code Generative Models | Vishwakarma, S.; Harkins, F.; Golecha, S.; et al. (10) | 2024 | QCE 2024 | — (congreso) | 19 | [10.1109/QCE60285.2024.00137](https://doi.org/10.1109/QCE60285.2024.00137) | Publica Qiskit HumanEval, un conjunto curado de más de 100 tareas con prompt, solución canónica, tests y escala de dificultad, y evalúa la capacidad de los LLM de producir código Qiskit ejecutable. |
| 11 | Ket Quantum Programming | Da Rosa, E.; De Santiago, R. | 2021 | ACM Journal on Emerging Technologies in Computing Systems | Q2 (SJR) | 14 | [10.1145/3474224](https://doi.org/10.1145/3474224) | Presenta una arquitectura de ejecución clásico-cuántica con generación de código en runtime y el concepto de futures, implementada en el framework Ket (lenguaje embebido en Python, librería C++ Libket y simulador bitwise). |

## Notas

- **Citas**: contador de OpenAlex (consultado en octubre de 2026).
- **Cuartil**: SJR de Scimago (2026) para las revistas; los congresos no tienen cuartil SJR/JCR.
  Factor de impacto JCR orientativo: *Software and Systems Modeling* 3.0; *ACM JETC* 2.3.
  El cuartil JCR exacto requiere suscripción a Clarivate.
- **Aportes**: resumen propio a partir del abstract; edítalos en `aportes.json`.
- Fichas completas: `md/<id>/<id>.meta.md`.

### Congresos citados

- **ASE 2025**: 2025 40th IEEE/ACM International Conference on Automated Software Engineering (ASE)
- **DAC 2025**: 2025 62nd ACM/IEEE Design Automation Conference (DAC)
- **DCAS 2026**: 2026 IEEE 19th Dallas Circuits and Systems Conference (DCAS)
- **ICECCE 2025**: 2025 International Conference on Electrical, Communication and Computer Engineering (ICECCE)
- **MODELS 2025**: 2025 ACM/IEEE 28th International Conference on Model Driven Engineering Languages and Systems (MODELS)
- **QAI 2025**: 2025 IEEE International Conference on Quantum Artificial Intelligence (QAI)
- **QCE 2024**: 2024 IEEE International Conference on Quantum Computing and Engineering (QCE)
- **QCE 2025**: 2025 IEEE International Conference on Quantum Computing and Engineering (QCE)
