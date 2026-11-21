# Benchmarking the Benchmarks for Quantum Code Generation with LLMs

Yunhe Feng<sup>_∗_</sup> , Xiaokun Yang<sup>_†_</sup> , Kewei Sha<sup>_∗_</sup> , Junhua Ding<sup>_∗_</sup>

> _∗_ University of North Texas, Denton, TX, USA _†_ University of Houston–Clear Lake, Houston, TX, USA

> _∗_ yunhe.feng@unt.edu, _†_ yangxia@uhcl.edu, _∗_ kewei.sha@unt.edu, _∗_ Junhua.Ding@unt.edu

**_Abstract_ —Large Language Models (LLMs) are increasingly deployed as quantum coding copilots, assisting researchers by generating complex programs for frameworks such as Qiskit, PennyLane, and OpenQASM. However, accurately evaluating the practical utility of these models remains a significant challenge. Existing benchmarks are highly fragmented, ranging from syntax-centric unit tests to simulator-and hardware-aware metrics, making results difficult to compare across different languages and hardware targets. To address this fragmentation, this paper systematically reviews recent evaluation suites and post-training methodologies for quantum code generation. We distill current evaluation criteria into four practical dimensions: syntax and API validity, semantic and physical correctness, resource and hardware feasibility, and execution-based feedback. Building upon these dimensions, we present a unified taxonomy that maps current benchmarks to emerging model adaptation techniques, specifically retrieval-augmented generation (RAG), fine-tuning, multi-agent workflows, and reinforcement learning (RL). Our analysis highlights a clear shift: moving away from prompt-only baselines and toward agentic workflows driven by quantum-verifiable rewards. This shift directly targets the semantic gap between superficially compilable code and physically executable quantum programs. In addition, we identify key research opportunities—such as standardized semantic metrics and integration with quantum error correction—aimed at fostering a more reproducible, verifiable, and hardware-grounded ecosystem for automated quantum software development.**

**_Index Terms_ —Quantum Code Generation, LLM, Benchmarking, Retrieval-Augmented Generation, RAG, Multi-Agent Systems, Reinforcement Learning, Qiskit, PennyLane, OpenQASM.**

## I. INTRODUCTION

Quantum software development has emerged as a significant bottleneck within the quantum computing field [1], as algorithm designers must translate complex, high-level computational intent into executable quantum circuits [2]. This translation requires navigating strict hardware constraints, including specific gate sets, connectivity limitations, and circuit depth considerations [3], [4], all while meticulously preserving quantum semantics. Within this challenging environment, Large Language Models (LLMs) have gained attention as an appealing interface layer to assist with quantum programming, potentially automating the generation of code for frameworks such as Qiskit [5], PennyLane [6], and OpenQASM [7].

However, quantum code generation presents unique challenges that distinguish it from classical programming, and existing evaluation metrics struggle to keep pace with these complexities. First, the lack of sufficient training data and rapidly evolving APIs creates a significant data scarcity and limit during pretraining [8]. Second, a profound semantic gap exists between code that compiles and code that is

semantically correct in its quantum execution, making syntaxbased assessments inherently unreliable [9]. Third, correct program verification is often execution-dependent, demanding feedback from simulators or hardware to account for circuit depth, noise models, and backend topology [10]. Given the current scarcity and high cost of Quantum Processing Unit (QPU) time, misleading “paper correctness” on conventional benchmarks can translate into wasted experiments and erroneous scientific conclusions; therefore, robust and physicallygrounded evaluation is not peripheral but essential to progress in LLM-driven quantum software.

To address these critical challenges, a coherent and physicsaware evaluation framework is essential for: (i) facilitating comparative analysis of different models across varied target languages, (ii) ensuring robust measurement of progress to avoid overstated claims of LLM capability, and (iii) informing post-training methodologies to optimize for physics-grounded objectives rather than simplistic syntactic matches. Motivated by this need, this paper introduces a comprehensive review and comparative analysis of recent evaluation suites and posttraining methodologies for quantum code generation.

By _benchmarking the benchmarks_ , we aim to accelerate the transition toward reliable quantum software automation by clarifying what current benchmarks measure, what they miss, and where new evaluation infrastructure can unlock practical impact, lower entry barriers, and ensure dependable hardware execution. Our main contributions are as follows.

- We distill evaluation into key practical dimensions, from syntax validity to execution-based feedback

- We provide a unified taxonomy linking emerging benchmarks to specific model adaptation techniques, including retrieval-augmented generation (RAG), fine-tuning, multi-agent workflows, and reinforcement learning (RL).

- We identify clear research trends and opportunities toward verifiable, reproducible, and hardware-grounded quantum software assessment.

## II. WHAT SHOULD A BENCHMARK MEASURE?

A rigorous evaluation of quantum code generation should rely on multiple complementary signals rather than a single aggregate metric. In practice, these signals can be organized along a spectrum ranging from inexpensive static checks to high-fidelity execution-based validation. This layered view is especially important in the quantum setting, where code may appear correct at the syntactic level while failing to preserve the intended quantum behavior or satisfy backend constraints.

979-8-3315-5193-3/26/$31.00 © 2026 IEEE

TABLE I

COMPARATIVE ANALYSIS OF QUANTUM CODE GENERATION BENCHMARKS AND METHODOLOGIES

|**Framework**|**Target**|**B**<br>**FT**|**RAG**|**MA**|**RL**|**Y/M**|**Key Insight**|
|---|---|---|---|---|---|---|---|
|QHE [11]|Qiskit|✓||||2024/06|Establishes baseline feasibility for LLM quantum generation.|
|QuanBench [9]|Qiskit|✓||||2025/10|Adds semantic metrics; high syntax score_̸_ = semantic success.|
|QCoder [10]|Qiskit|✓||||2025/10|Simulator feedback scores physical feasibility vs. humans.|
|PennyLang [12]|PennyLane|✓|✓|||2025/03|Docs/repo benchmark; RAG aids open models more than closed.|
|QHackBench [13]|PennyLane|✓|✓|✓||2025/06|Hackathon tasks show value of retrieval & iterative refinement.|
|Instr-LLM [14]|Qiskit|✓||||2025/11|Instruction tuning narrows gap to quantum-specific syntax.|
|PennyCoder [15]|PennyLane|✓|✓|||2025/07|LoRA improves syntax; FT often outperforms RAG for APIs.|
|MD-RAG [16]|Py/Qiskit||✓|||2025/08|UML-to-code retrieval; prompt structure dominates naive RAG.|
|QAgent [17]|OpenQASM||✓|✓||2025/08|Multi-agent decomposition improves accuracy on complex tasks.|
|QEC-Agent [18]|Qiskit||✓|✓||2025/04|Agentic generation paired with QEC for fault-tolerance.|
|QUASAR [19]|OpenQASM|✓|||✓|2025/10|Agentic RL with hierarchical rewards optimizes task objectives.|
|QSpark [20]|Qiskit|✓|||✓|2025/07|Preference optimization (ORPO) improves reliability.|
|QVR-RL [21]|Qiskit|✓|||✓|2025/08|Execution-based verifiable rewards beat prompt baselines.|

**Legend:** ✓=Uses/Proposes; B=Benchmark; FT=Fine-Tuning; RAG=Retrieval-Augmented Generation; MA=Multi-Agent; RL=Reinforcement Learning.

## _A. Syntax and API Validity_

The most immediate requirement is compilability: whether the generated code parses correctly and uses the target framework API appropriately, such as Qiskit, PennyLane, or OpenQASM. Qiskit HumanEval (QHE), for example, emphasizes unit-test-style functional checks and Pass@k metrics [11]. These measures provide an important first-pass filter, since code that does not compile or call the correct APIs is unusable in practice. However, syntax-oriented evaluation alone can substantially overestimate model capability, as LLMs may generate plausible scaffolding that satisfies surface-level checks without implementing the intended quantum procedure.

## _B. Semantic and Physical Correctness_

Beyond compilability, a benchmark should assess whether the generated program is semantically correct from a quantum perspective. A circuit can be syntactically valid yet still be incorrect due to issues such as improper gate ordering, qubit misindexing, incorrect ancilla usage, or flawed decompositions. QuanBench addresses this limitation by incorporating semantic-aware metrics, including _process fidelity_ and notions of quantum semantic equivalence, demonstrating that high syntactic accuracy does not necessarily translate into correct quantum behavior [9]. This dimension is particularly important because the true objective in quantum programming is not merely executable code, but code that faithfully represents the intended transformation or measurement outcome.

## _C. Resource and Hardware Feasibility_

Even when a program is semantically correct in an abstract sense, it may still be impractical for deployment on real devices. Quantum hardware imposes strict constraints related to supported gate sets, circuit depth, qubit connectivity, calibration quality, and transpilation overhead. As a result, a useful benchmark should also measure whether generated circuits are feasible under realistic hardware assumptions. QCoder moves in this direction by incorporating simulator-based evaluators that penalize hardware-relevant violations and thereby provide a more deployment-oriented notion of correctness [10]. This

dimension helps distinguish theoretically valid programs from circuits that can actually be executed efficiently and reliably on target platforms.

## _D. Execution-Based Feedback_

The most faithful evaluation signals arise from execution, where the generated program is run on a simulator or quantum backend and assessed through its observable outcomes. Such feedback captures aspects of correctness that are difficult to verify statically, including output distributions, robustness under noise, and interactions with backend-specific compilation constraints. Recent work has begun to use simulator feedback both during benchmark evaluation [10] and as part of posttraining objectives through execution-based reward signals, often described as “quantum verifiable rewards” [19], [21]. This direction is especially promising because it aligns optimization with physically meaningful behavior rather than superficial code similarity, thereby narrowing the gap between compilable programs and experimentally valid quantum solutions.

## _E. A Minimal Reporting Checklist_

To improve transparency and reproducibility, benchmark reports should include several pieces of essential context. At a minimum, we recommend documenting: (i) the target language, framework, and software versions; (ii) whether the evaluation is static, simulator-based, or hardware-based; (iii) the semantic metrics used, if any; and (iv) how hardware constraints such as gate set, depth, and topology are handled. Where applicable, authors should also clarify backend configuration, transpilation settings, and noise assumptions. In many cases, this contextual information is more informative than reporting aggregate Pass@k scores alone, because it reveals what notion of “correctness” the benchmark is actually measuring.

## III. COMPARATIVE ANALYSIS OF BENCHMARKS AND METHODOLOGIES

Table I summarizes representative studies through a comparative analysis of benchmark design and model adaptation

techniques. First, benchmark development is progressively moving beyond syntax-only scoring toward evaluation criteria that better capture semantic validity, physical correctness, and execution behavior [9], [10]. Second, methodological progress is shifting from prompt-only baselines toward approaches that explicitly adapt, guide, or optimize models through retrieval, post-training, tool use, and reward-driven learning [17], [19], [21]. These trends indicate that advances in quantum code generation depend not only on stronger foundation models, but also on evaluation protocols that reflect the realities of quantum software development and hardware deployment.

## _A. Prompting and Retrieval-Augmented Generation_

Retrieval-augmented generation (RAG) aims to mitigate API drift, incomplete pretraining coverage, and long-tail framework details by grounding model outputs in external documentation, code repositories, and curated examples. This strategy is particularly attractive in the quantum setting, where libraries evolve quickly and many framework-specific patterns are underrepresented in general-purpose pretraining corpora.

Evidence from PennyLane-centered studies suggests that retrieval can improve library-specific usage and API compliance by supplying relevant contextual material at generation time [12]. At the same time, work on UML-to-code generation indicates that retrieval quality alone does not determine success; prompt organization and task decomposition can be equally important in shaping downstream outputs [16]. Overall, RAG appears most effective for improving _syntax and API correctness_ , especially when tasks depend on up-todate documentation or framework-specific conventions. However, without stronger semantic supervision or execution-based feedback, its gains are often limited when the task requires deeper reasoning about circuit behavior, algorithmic intent, or hardware-aware correctness [15].

## _B. Fine-Tuning and Domain Adaptation_

Fine-tuning and related domain adaptation methods address one of the core bottlenecks in quantum code generation: the mismatch between general-purpose language model pretraining and the specialized structure of quantum programming tasks. By adapting models to framework-specific syntax, idiomatic coding styles, and domain-relevant instruction formats, these approaches can improve both fluency and consistency in generated outputs.

Qiskit-focused instruction tuning has been shown to improve quantum coding competence by better aligning the model with quantum-specific programming patterns and task formulations [14]. Similarly, PennyCoder demonstrates that lightweight adaptation methods such as Low-Rank Adaptation (LoRA) [22] can yield substantial gains within a single framework while remaining more efficient than full-scale model retraining [15]. A complementary direction is illustrated by QAOA-GPT, which targets structured circuit families and suggests that specialized generators can reduce reliance on costly iterative optimization procedures [23]. Overall, finetuning is particularly promising when the goal is to improve

performance within a defined ecosystem or task family, although its benefits may depend on the quality, provenance, and version stability of the adaptation data.

## _C. Agentic Workflows and Tool Use_

Agentic workflows move beyond one-shot generation by introducing iterative reasoning and interaction loops, such as planning, drafting, execution, debugging, verification, and refinement. This paradigm is well suited to quantum programming, where correctness often depends on intermediate checks, tool feedback, and structured decomposition of complex tasks.

QAgent exemplifies this direction by decomposing OpenQASM programming tasks into smaller subproblems and combining tool use with dynamically selected exemplars [17]. In more advanced settings, QEC-Agent argues that useful code generation for fault-tolerant quantum computing must be coupled with quantum error correction (QEC) components and additional optimization steps rather than treated as a standalone code synthesis problem [18]. Agent-Q further broadens the role of LLMs by showing that these systems can support not only code generation itself, but also related tasks such as proposing parameter initializations for variational quantum algorithms [24]. More broadly, agentic systems are appealing because they provide a natural mechanism for self-correction, tool grounding, and modular reasoning, all of which are valuable for reducing brittle failures in complex quantum code generation workflows.

## _D. Reinforcement Learning and Quantum-Verifiable Rewards_

Ultimately, closing the semantic gap in quantum code generation requires optimizing models against objectives that are themselves meaningful and verifiable. Reinforcement learning and related post-training strategies offer a natural framework for this goal by enabling models to improve based on feedback tied to execution outcomes rather than surface-level similarity.

Preference-based optimization has already shown promise for improving reliability in quantum code generation settings [20]. More directly, QUASAR and QVR-RL use simulator and QPU outcomes as reward signals, aligning generation with executable behavior and task performance instead of purely textual resemblance to reference solutions [19], [21]. This direction is especially important for quantum software, where two pieces of code may look similar yet produce materially different quantum behavior. At the same time, RL-based progress raises new benchmarking requirements, including stable reward definitions, robust treatment of noise and backend variability, and careful attention to reproducibility across simulators and hardware platforms. As a result, advances in reward-driven training are tightly linked to advances in evaluation design itself.

## IV. EMERGING TRENDS AND RESEARCH OPPORTUNITIES

Recent work reveals several clear trends in quantum code generation research. First, evaluation is becoming increasingly execution-first, with simulator feedback and semantic

metrics being used more frequently to move beyond syntaxonly assessment [9], [10]. Second, the field is shifting from prompt-only strategies toward post-training approaches, where instruction tuning and preference optimization help reduce brittle prompting and improve model reliability [14], [20]. Third, agentic systems are emerging as an important interface for quantum programming tasks, enabling decomposition, tool use, and iterative self-correction in complex workflows [17], [18]. Finally, reinforcement learning with execution-grounded, verifiable rewards is gaining momentum as a way to optimize models for semantic correctness rather than surface-level textual similarity [19], [21].

At the same time, these developments expose several research opportunities. A key priority is the development of standardized semantic metrics across frameworks, since current evaluation suites remain highly framework-specific and limit direct comparability. Benchmarks should also adopt multiobjective scoring schemes that better reflect deployability by jointly considering correctness, circuit depth, gate-set compliance, topology constraints, and computational cost. In addition, hardware-aware evaluation would benefit from more systematic robustness reporting, particularly with respect to noise models, transpiler settings, and backend drift. Reproducible dataset provenance and versioning are likewise essential for supporting fair longitudinal evaluation [8]. More broadly, future benchmarks should more tightly integrate quantum error correction and verification, as fault-tolerant workflows require coordinated reasoning over circuits, decoders, and hardware constraints, making agentic designs a promising foundation for next-generation systems [18].

## V. CONCLUSION

This paper reviewed recent benchmarks and post-training methods for LLM-based quantum code generation, showing that reliable evaluation must extend beyond syntax to include semantic correctness, hardware feasibility, and executionbased feedback. Our analysis indicates a clear shift from prompt-only baselines toward fine-tuning, agentic workflows, and reinforcement learning with quantum-verifiable rewards. Moving forward, progress in this area will depend on more standardized, reproducible, and hardware-aware benchmarks that better reflect real quantum software deployment.

## ACKNOWLEDGMENT

This work is supported in part by the U.S. National Science Foundation (NSF) under grants CCF-2447834, DUE-2225229, and CNS-2231519.

## REFERENCES

- [1] M. Piattini, G. Peterssen, R. P´erez-Castillo, J. L. Hevia, M. A. Serrano, G. Hern´andez, I. G. R. De Guzm´an, C. A. Paradela, M. Polo, E. Murina _et al._ , “The talavera manifesto for quantum software engineering and programming.” in _QANSWER_ , 2020, pp. 1–5.

- [2] B. Bichsel, M. Baader, T. Gehr, and M. Vechev, “Silq: A high-level quantum language with safe uncomputation and intuitive semantics,” in _Proceedings of the 41st ACM SIGPLAN Conference on Programming Language Design and Implementation_ , 2020, pp. 286–300.

- [3] M. Y. Siraichi, V. F. d. Santos, C. Collange, and F. M. Q. Pereira, “Qubit allocation,” in _Proceedings of the 2018 international symposium on code generation and optimization_ , 2018, pp. 113–125.

- [4] F. T. Chong, D. Franklin, and M. Martonosi, “Programming languages and compiler design for realistic quantum hardware,” _Nature_ , vol. 549, no. 7671, pp. 180–187, 2017.

- [5] A. Javadi-Abhari, M. Treinish, K. Krsulich, C. J. Wood, J. Lishman, J. Gacon, S. Martiel, P. D. Nation, L. S. Bishop, A. W. Cross _et al._ , “Quantum computing with qiskit,” _arXiv:2405.08810_ , 2024.

- [6] V. Bergholm, J. Izaac, M. Schuld, C. Gogolin, S. Ahmed, V. Ajith, M. S. Alam, G. Alonso-Linaje, B. AkashNarayanan, A. Asadi _et al._ , “Pennylane: Automatic differentiation of hybrid quantum-classical computations,” _arXiv preprint arXiv:1811.04968_ , 2018.

- [7] A. Cross, A. Javadi-Abhari, T. Alexander, N. De Beaudrap, L. S. Bishop, S. Heidel, C. A. Ryan, P. Sivarajah, J. Smolin, J. M. Gambetta _et al._ , “Openqasm 3: A broader and deeper quantum assembly language,” _ACM Transactions on Quantum Computing_ , vol. 3, no. 3, pp. 1–50, 2022.

- [8] N. Dupuis, L. Buratti, S. Vishwakarma, A. V. Forrat, D. Kremer, I. Faro, R. Puri, and J. Cruz-Benito, “Qiskit code assistant: Training llms for generating quantum computing code,” in _2024 IEEE LLM Aided Design Workshop (LAD)_ . IEEE, 2024, pp. 1–4.

- [9] X. Guo, M. Wang, and J. Zhao, “Quanbench: Benchmarking quantum code generation with large language models,” _arXiv preprint arXiv:2510.16779_ , 2025.

- [10] T. Mikuriya, T. Ishigaki, M. Kawarada, S. Minami, T. Kadowaki, Y. Suzuki, S. Naito, S. Takada, T. Kato, T. Basseda _et al._ , “Qcoder benchmark: Bridging language generation and quantum hardware through simulator-based feedback,” in _Proceedings of the 18th International Natural Language Generation Conference_ , 2025, pp. 743–752.

- [11] S. Vishwakarma, F. Harkins, S. Golecha, V. S. Bajpe, N. Dupuis, L. Buratti, D. Kremer, I. Faro, R. Puri, and J. Cruz-Benito, “Qiskit humaneval: An evaluation benchmark for quantum code generative models,” in _2024 IEEE International Conference on Quantum Computing and Engineering (QCE)_ , vol. 1. IEEE, 2024, pp. 1169–1176.

- [12] A. Basit, N. Innan, M. H. Asif, M. Shao, M. Kashif, A. Marchisio, and M. Shafique, “Pennylang: Pioneering llm-based quantum code generation with a novel pennylane-centric dataset,” _arXiv preprint arXiv:2503.02497_ , 2025.

- [13] A. Basit, M. Shao, M. H. Asif, N. Innan, M. Kashif, A. Marchisio, and M. Shafique, “Qhackbench: Benchmarking large language models for quantum code generation using pennylane hackathon challenges,” _arXiv preprint arXiv:2506.20008_ , 2025.

- [14] S. Chen, Y. Zhang, and Q. Guan, “Bridging the quantum coding gap: Instruction-tuned llms for qiskit,” _The International Conference for High Performance Computing, Networking, Storage, and Analysis, Research Posters_ , 2025.

- [15] A. Basit, M. Shao, M. H. Asif, N. Innan, M. Kashif, A. Marchisio, and M. Shafique, “Pennycoder: Efficient domain-specific llms for pennylanebased quantum code generation,” _arXiv:2507.19562_ , 2025.

- [16] N. Siavash and A. Moin, “Model-driven quantum code generation using large language models and retrieval-augmented generation,” _arXiv preprint arXiv:2508.21097_ , 2025.

- [17] Z. Fu, F. Chen, and L. Jiang, “Qagent: An llm-based multi-agent system for autonomous openqasm programming,” _arXiv preprint arXiv:2508.20134_ , 2025.

- [18] C. Campbell, H. M. Chen, W. Luk, and H. Fan, “Enhancing llm-based quantum code generation with multi-agent optimization and quantum error correction,” _arXiv preprint arXiv:2504.14557_ , 2025.

- [19] C. Yu, V. Uotila, S. Deng, Q. Wu, T. Shi, S. Jiang, L. You, and B. Zhao, “Quasar: Quantum assembly code generation using tool-augmented llms via agentic rl,” _arXiv preprint arXiv:2510.00967_ , 2025.

- [20] K. Kheiri, A. Aamir, A. Miranskyy, and C. Ding, “Qspark: Towards reliable qiskit code generation,” _arXiv preprint arXiv:2507.12642_ , 2025.

- [21] N. Dupuis, A. Tiwari, Y. Mroueh, D. Kremer, I. Faro, and J. Cruz-Benito, “Quantum verifiable rewards for post-training qiskit code assistant,” _arXiv preprint arXiv:2508.20907_ , 2025.

- [22] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen _et al._ , “Lora: Low-rank adaptation of large language models.” _ICLR_ , 2022.

- [23] I. Tyagin, M. H. Farag, K. Sherbert, K. Shirali, Y. Alexeev, and I. Safro, “Qaoa-gpt: Efficient generation of adaptive and regular quantum approximate optimization algorithm circuits,” _arXiv:2504.16350_ , 2025.

- [24] L. Jern, V. Uotila, C. Yu, and B. Zhao, “Agent-q: fine-tuning large language models for quantum circuit generation and optimization,” in _2025 IEEE International Conference on Quantum Computing and Engineering (QCE)_ , vol. 1. IEEE, 2025, pp. 1621–1632.
