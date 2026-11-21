# NOTAS — Fase 0: revisión de fuentes

Actualizado: 2026-11-21.

Criterio: solo se afirma lo que se puede comprobar en un texto completo (`md/`) o en
Crossref/arXiv. Lo que no tiene texto completo se marca `[VERIFICAR]`.

Advertencia sobre versiones: varias fuentes se usan desde su **preprint en arXiv** porque
la versión publicada no es de acceso abierto. Antes de citar cualquier número o frase,
hay que comparar con la versión publicada. Esas fuentes van marcadas como *(preprint)*.

## 1. Cómo se verificó

- **Metadatos y DOI:** Crossref (`api.crossref.org`), arXiv (`export.arxiv.org`) y Unpaywall
  (para saber si hay copia de acceso abierto).
- **Texto completo:** `md/<carpeta>/*.md`, generado con `./convertir`.
- **Chen et al. 2021:** texto completo revisado; el estimador insesgado de pass@k está en la **ecuación (1)**.

## 2. Fuentes con texto completo

### 2.1 Pruebas y verificación de programas cuánticos

| Fuente | DOI / arXiv | Texto | Aporte para este trabajo |
|---|---|---|---|
| Quito (Wang et al., ASE 2021) | 10.1109/ASE51524.2021.9678798 | `md/Quito_*` | Oráculos **WOO** (salida inválida) y **OPO** (distribución de salida con Wilcoxon de una muestra y nivel de significancia configurable). Validado con un solo programa. Base para nuestras pruebas estadísticas de distribución. |
| QuSBT (ICSE 2022; autores no comprobados) | 10.1145/3510454.3516839 | `md/QuSBT_*` | Búsqueda genética de suites que maximizan pruebas fallidas. Falla de distribución (**wodf**) con **chi-cuadrado de Pearson**. Referencia para nuestra prueba de chi-cuadrado. |
| QuraTest (Ye et al., ASE 2023) | 10.1109/ASE56229.2023.00196 | `md/QuraTest_*` | Generadores de entradas que cubren magnitud, fase y entrelazamiento. Evalúa con **mutation score** usando **QmutPy** sobre 26 programas. Motiva un held-out con entradas que cubran fase y entrelazamiento. |
| Equivalencia de circuitos parametrizados (Peham, Burgholzer, Wille; ASP-DAC 2023) | 10.1145/3566097.3567932 | `md/2023_aspdac_*` | Equivalencia de circuitos con parámetros mediante ZX-calculus, completa en el caso simbólico. Referencia para verificar compilación de algoritmos variacionales. El PDF tiene una errata en el título ("Qantum"). |
| Qbricks (Chareton et al., LNCS 2021) | 10.1007/978-3-030-72019-3_6 | `md/An_Automated_Deductive_*` | Verificación deductiva automática de programas de construcción de circuitos, con especificaciones paramétricas (Shor, QPE, Grover). Referencia de verificación formal de alto costo. |
| AutoQ (LNCS 2023; autores no comprobados) | 10.1007/978-3-031-37709-9_7 | `md/AutoQ_*` | Verificador automático basado en autómatas, con propiedades relacionales antes y después del circuito. Referencia de verificación completa en circuitos pequeños. |
| Ying, "Toward automatic verification of quantum programs" (FAC 2019) — versión publicada, autor: Mingsheng Ying | 10.1007/s00165-018-0465-3 | `md/Toward_automatic_verification_*` (PDF publicado) y `md/Ying_2019_*` (preprint arXiv 1807.11610) | Resumen de la lógica de programas para cuánticos: lógica de Hoare cuántica, generación de invariantes y análisis de terminación. **No trata de pruebas dinámicas**; se cita como verificación formal deductiva, no como alternativa práctica. Para citar, usar la versión publicada. |
| Wei, Tsai, Jhang, Jiang: "Accurate BDD-based unitary operator manipulation for scalable and robust quantum circuit verification" (DAC 2022) | 10.1145/3489517.3530481 | `md/Accurate_BDD-based_*` (PDF publicado) | Extiende una representación algebraica basada en BDD para vectores de estado, a operadores unitarios. Equivalencia de circuitos con **mayor escalabilidad y exactitud** que los métodos basados en diagramas de decisión con pesos en las aristas, que son inexactos. **Útil para justificar nuestro alcance de equivalencia**: los métodos exactos escalan hasta cierto número de qubits. Los autores ya están confirmados. |
| Bugs en programas cuánticos (SANER 2022) | 10.1109/SANER53432.2022.00147 | `md/A_Comprehensive_Study_*` | Estudio de 96 bugs reales en Qiskit, Cirq, Q# y ProjectQ. Más del 80% son bugs específicos de lo cuántico. Motiva el catálogo de fallos de las tareas. |

### 2.2 LLM y código cuántico

| Fuente | DOI / arXiv | Texto | Aporte para este trabajo |
|---|---|---|---|
| Qiskit HumanEval (QCE 2024) | 10.1109/QCE60285.2024.00137 | `md/10-Qiskit_*` | Benchmark público de más de 100 tareas. **No se usa como held-out** (decisión: solo tareas propias). Trabajo previo citado. |
| QHackBench (QAI 2025) | 10.1109/QAI63978.2025.00056 | `md/6-QHackBench_*` | Benchmark de PennyLane con RAG frente a prompting; el RAG no mejora de forma clara en algoritmos complejos. Comparación previa de tipo similar. |
| Generación multiagente con QEC (DAC 2025) | 10.1109/DAC63849.2025.11133316 | `md/8-Enhancing_*` | Framework multiagente con análisis semántico iterativo y corrección de errores cuánticos. **Es el trabajo más cercano a la condición C.** Hay que diferenciarse explícitamente. |
| **Agent-Q (QCE 2025) — preprint arXiv 2504.11109** | 10.1109/QCE65121.2025.00179 | `md/Agent-Q_2025_*` | Ajuste fino de LLM para generar y optimizar circuitos parametrizados, con un conjunto de unos 14.000 circuitos. La calidad de los datos se mide con la probabilidad del estado correcto, calculada analíticamente, no con pruebas. **Útil como contraste:** nuestra evaluación no entrena el modelo y usa verificación en el bucle. |
| Chen et al. 2021 (Codex) — arXiv 2107.03374 | arXiv 2107.03374 | Texto completo | Define el estimador insesgado de **pass@k** (ecuación 1). Métrica de corrección del diseño. |

### 2.3 Marco general de LLM

| Fuente | DOI / arXiv | Texto | Aporte para este trabajo |
|---|---|---|---|
| **FunSearch (Nature 2023)** | 10.1038/s41586-023-06924-6 | `md/Romera-Paredes_*` | LLM emparejado con un **evaluador sistemático** (función `evaluate` que puntúa candidatos) en un bucle evolutivo. Es la analogía más directa de nuestra condición C: el evaluador define qué candidato sobrevive. Diferencia: FunSearch optimiza un objetivo numérico, no la corrección de un programa. |
| Semantic entropy (Nature 2024) | 10.1038/s41586-024-07421-0 | `md/Farquhar_*` | Detecta alucinaciones con entropía sobre clusters semánticos de respuestas muestreadas. **Alternativa a la verificación explícita**; útil para la discusión (¿se puede detectar error sin oráculo?). |
| Encuesta de alucinaciones (TOIS 2025) — preprint arXiv 2311.05232 | 10.1145/3703155 | `md/Huang_2025_*` | Taxonomía de alucinaciones en LLM. Para la introducción: motiva por qué el código generado necesita comprobación externa. |
| Encuesta de evaluación de LLM (TIST 2024) — preprint arXiv 2307.03109 | 10.1145/3641289 | `md/Chang_2024_*` | Describe que los protocolos actuales usan **benchmarks estáticos y públicos**, lo que dificulta medir la capacidad real. Sustenta nuestra discusión sobre contaminación. |
| Pruebas de software con LLM (TSE 2024) — preprint arXiv 2307.07221 | 10.1109/TSE.2024.3368208 | `md/Wang_2024_Software_*` | Revisa 102 estudios sobre LLM en pruebas. Señala como desafíos abiertos el **problema del oráculo de prueba** y las evaluaciones rigurosas. Marco general para la sección de trabajo relacionado. |

## 3. Fuentes sin texto completo

| Fuente | DOI | Estado | Qué falta |
|---|---|---|---|
| Ali & Yue, "Quantum Software Testing: A Brief Introduction" (ICSE-C 2023, pp. 332–333) | 10.1109/ICSE-Companion58688.2023.00093 | DOI y autores verificados (Shaukat Ali, Tao Yue). Texto no disponible: es un artículo de dos páginas sin copia abierta. **Equivalente parcial:** el artículo de ERCIM News 128 (pp. 13–15), de Yue, Arcaini y Ali (ver sección 4). | Subir el PDF si se quiere citar ese artículo. Mientras tanto, citar ERCIM para lo que leímos allí. |
| SBDAC | 10.1109/VLSITSA64674.2025.11046530 | **El DOI no existe en Crossref (404).** Búsqueda bibliográfica sin resultados. | Confirmar el nombre completo de la venue o el DOI correcto. **No citar.** |

**Resumen:** de las 19 fuentes de la lista, 17 tienen texto completo (16 más Wei et al.).
Ali & Yue tiene un equivalente parcial en ERCIM. SBDAC sigue sin identificar.

## 4. Fuentes adicionales de la biblioteca

- **ERCIM News 128, "Quantum Software Testing: Challenges, Early Achievements, and Opportunities"** (Tao Yue, Paolo Arcaini, Shaukat Ali), en `md/ERCIM_*`, páginas 13 a 15 de la revista. Es **un equivalente parcial** de Ali & Yue (ICSE-C 2023): mismos autores y mismo tema, pero es un artículo de divulgación y no la misma publicación. Su contenido no es idéntico y no podemos asumir que coincidan. Para citarlo: `Yue, T., Arcaini, P., Ali, S., "Quantum Software Testing: Challenges, Early Achievements, and Opportunities", ERCIM News 128, pp. 13–15`. Puntos útiles:
  - Logros: coverage criteria, búsqueda, mutation testing (**Muskit**, Mendiluze et al., ASE 2021, herramienta), combinatorial testing y **aserciones estadísticas y de proyección**.
  - Desafíos: problema del oráculo de prueba y medición de estados internos.
  - Dirección: **metamorphic testing** como alternativa al oráculo explícito.
  - Limitación: **las técnicas se desarrollan para simuladores sin ruido**. Justifica nuestro requisito de ruido y limita las conclusiones.
- **Benchmarking the Benchmarks (paper 1):** cuatro dimensiones de evaluación (validez de sintaxis y API, corrección semántica y física, viabilidad de recursos, feedback de ejecución). Marco para describir nuestras métricas.
- **QuanBench (paper 4):** Pass@K y Process Fidelity frente a una solución canónica. **Competidor más directo**: la diferenciación debe estar frente a él.
- **Quantum-RAG (paper 2), PennyCoder (paper 5), Quantum-aware LLM survey (paper 9):** contexto de trabajo previo; uso secundario.
- **Ket (paper 11), UML (papers 3 y 7):** fuera de alcance; solo contexto.

## 5. Hallazgos que afectan al diseño (para DECISIONES.md)

1. **Prueba estadística de distribución.** Quito usa Wilcoxon de una muestra; QuSBT usa chi-cuadrado. Nuestra elección (chi-cuadrado con 8192 shots, α = 0,01 y Bonferroni) debe justificarse frente a Wilcoxon y registrarse.
2. **Evaluador como bucle (FunSearch).** Nuestra condición C es análoga a FunSearch, pero con un evaluador de corrección y no de puntuación. Hay que citarlo como antecedente y explicar la diferencia.
3. **Mutantes.** QuraTest usa QmutPy; ERCIM menciona Muskit. Nuestros operadores deben describirse como propios, con ambas herramientas como antecedentes. Comprobar la licencia de QmutPy antes de usarla.
4. **Equivalencia con ruido.** ERCIM confirma que las técnicas existentes se evalúan sin ruido. Nuestro umbral de fidelidad calibrado es una aportación, pero el resultado depende de la calibración.
5. **Circularidad.** Quito y QuraTest usan el mismo oráculo o los mismos operadores para generar y evaluar. El held-out debe usar familias de mutantes y propiedades distintas (decisión 11).
6. **Contaminación.** La encuesta de evaluación (Chang et al., preprint) documenta el problema de los benchmarks públicos. Sustenta la decisión de usar solo tareas propias.
7. **Aserciones dinámicas.** Ninguna fuente de la lista las define. Añadir la fuente primaria `[VERIFICAR]` (candidata: Huang & Martonosi, ISCA 2019).
8. **Semantic entropy.** Propone detectar error sin oráculo. Ofrece una alternativa que podemos comparar en la discusión, pero no es parte de nuestro diseño.
9. **Alcance de la equivalencia (Wei et al., DAC 2022).** Los métodos exactos basados en BDD escalan mejor que los que usan diagramas con pesos en las aristas. Aun así, su escalabilidad tiene límites. Esto respalda el límite de 8 qubits de la decisión 5, pero hay que comprobar en el texto a partir de cuántos qubits se degrada el método antes de citar una cifra concreta.

## 6. Mapa de secciones del artículo

| Sección | Fuentes principales |
|---|---|
| Introducción | Huang (alucinaciones), ERCIM (desafíos), SANER (bugs), Chang (evaluación) |
| Trabajo relacionado: testing | Quito, QuSBT, QuraTest, ERCIM, Ali & Yue `[VERIFICAR]` |
| Trabajo relacionado: verificación formal | Peham, Qbricks, AutoQ, Ying (publicada), Wei et al. |
| Trabajo relacionado: LLM y código cuántico | Paper 8 (multiagente), paper 6, paper 2, paper 10, paper 4, Agent-Q (preprint) |
| Trabajo relacionado: LLM con evaluador | FunSearch, semantic entropy, TSE (preprint) |
| Métricas | Chen 2021 (pass@k), paper 1 (dimensiones), paper 4 (Process Fidelity) |
| Amenazas a la validez | ERCIM (ruido), Chang (contaminación), Wang TSE (oráculo) |

## 7. Búsqueda de novedad (pendiente, fuera de este entorno)

Scopus y WoS requieren acceso institucional. Registrar aquí cadenas, fechas y resultados:

- [ ] Scopus: `[pendiente]`
- [ ] WoS: `[pendiente]`
- Cobertura de preprints: limitada (arXiv no revisado de forma sistemática).

## 8. Pendientes de Fase 0

- Subir Ali & Yue (ICSE-C 2023) si se quiere citar ese artículo concreto (opcional, hay equivalente en ERCIM).
- Confirmar el DOI o la venue de SBDAC (pendiente, no citar).
- Confirmar los autores de QuSBT y AutoQ (Wei et al. ya confirmados).
- Confirmar la licencia de QmutPy (Fortunato et al.), citada en QuraTest pero no verificada.
- Comparar cada preprint con su versión publicada antes de citar cifras.
