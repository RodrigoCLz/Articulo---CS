2025 IEEE International Conference on Quantum Artificial Intelligence (QAI)

# QHackBench: Benchmarking Large Language Models for Quantum Code Generation Using PennyLane Hackathon Challenges

Abdul Basit<sup>1</sup> , Minghao Shao<sup>1</sup> , Muhammad Haider Asif<sup>1,2</sup> , Nouhaila Innan<sup>1,2</sup> , Muhammad Kashif<sup>1,2</sup> , Alberto Marchisio<sup>1,2</sup> , Muhammad Shafique<sup>1,2</sup>

> _1eBRAIN Lab, Division of Engineering New York University (NYU) Abu Dhabi_ , Abu Dhabi, UAE

> _2Center for Quantum and Topological Systems (CQTS), NYUAD Research Institute, New York University Abu Dhabi_ , UAE

_{_ abdul.basit, shao.minghao, ma8183, nouhaila.innan, muhammadkashif, alberto.marchisio, muhammad.shafique _}_ @nyu.edu

**_Abstract_ —Recent advances in Large Language Models (LLMs) have demonstrated strong potential in code generation, yet their effectiveness in quantum computing remains underexplored. This paper benchmarks LLMs for PennyLane-based quantum code generation using real-world challenges from the Quantum Hackathon (QHack). We introduce** **_QHackBench_ , a novel benchmark dataset derived from QHack competitions, and evaluate model performance under vanilla prompting and Retrieval-Augmented Generation (RAG). Our structured evaluation framework assesses functional correctness, syntactic validity, and execution success across varying challenge difficulties. Results indicate that RAG-enhanced models, supplemented with an augmented PennyLane dataset, approximately generate similar results as the standard prompting, particularly in complex quantum algorithms. Additionally, we introduce a multi-agent evaluation pipeline that iteratively refines incorrect solutions, further enhancing execution success rates. To foster further research, we commit to publicly releasing** **_QHackBench_ , along with our evaluation framework and experimental results, enabling continued advancements in AI-assisted quantum programming.**

**_Index Terms_ —Quantum Computing, PennyLane, Large Language Models, Code Generation, Benchmarking, Retrieval-Augmented Generation.**

## I. Introduction and Motivation

Quantum computing has emerged as a transformative technology, offering approaches for potentially solving problems considered classically intractable [1]–[3]. With the increasing adoption of hybrid quantum-classical computing, tools such as PennyLane have gained prominence [4], facilitating Quantum Machine Learning (QML) and variational circuit optimization [5]–[9]. However, programming in quantum frameworks remains challenging due to the complexity of quantum circuits and domain-specific syntax.

Large Language Models (LLMs) [10] such as GPT-4 have demonstrated remarkable performance in classical code generation and completion [11]. However, their capabilities in quantum programming, particularly within the PennyLane framework, remain largely unexamined. Existing benchmarks, such as Qiskit HumanEval, primarily evaluate LLM performance for IBM’s Qiskit framework [12], leaving a significant gap in assessing LLM effectiveness for PennyLane-based quantum programming. This gap is critical, as PennyLane provides unique features such as automatic differentiation for QML and seamless hardware integration [4], necessitating a dedicated benchmark.

To address this issue, we introduce a novel benchmarking approach that leverages _Quantum Hackathon Challenges (QHack 2023–2024)_ as an evaluation dataset, integrated with our baseline evaluation framework. The framework incorporates both vanilla prompting and Retrieval-Augmented Generation (RAG), as well as a more complex agentic setup, to account for diverse usage scenarios aligned with modern LLM-based systems. It further employs a diverse set of model families to enhance flexibility and performance. Within this setting, we systematically analyze LLM-generated quantum code and compare a wide range of configurations to establish a comprehensive baseline on our proposed benchmark. Our study shows that while RAG improves accuracy in specific cases, such as reducing hallucinated API calls and refining circuit structures, current foundation models still face significant limitations in generating reliable quantum code.

_A. Motivational Case Study_

In our evaluation using the o3-mini model, the generated code was assessed on a challenge-by-challenge basis as either correct or incorrect.

|**Well–kno**|**wn QC Frameworks**|**Our Contributions**|QHack challenges<br>|
|---|---|---|---|
|Qiskit|Pennylane<br>Lack of pennylane<br>specific dataset|**Benchmark Dataset-QHackBench**<br>Compiled Pennylane Qhack<br>challenges from 2023-24|categorized in various<br>difficulty levels/topics<br>Self reasoning through<br>|
|Qiskit<br>Code<br>Assistant|Inaccurate code<br>generation|**Multi-Agent Evaluation Pipeline**<br>multi-agent system to iteratively<br>refine LLM-generated code|runtime logs and<br>debugging feedback|
|||**RAG-based Evaluation Framework**<br>|Enhanced prompts resulting|
||Absence of Standard<br>|Systematic Comparison of vanilla<br>|in better/correct code|
||Benchmark|vs. RAG enhanced prompts|generation|
||Fig. 1:|An overview of our contribu|tions.|

In this study, we report only binary outcomes—each challenge is either solved correctly or not. Our experiments show that when the model’s queries were supplemented with relevant PennyLane documentation via RAG, the number of challenges solved were approximately the same as the baseline approach. Furthermore, integrating a multi-agent refinement pipeline further improved the execution success rate significantly. These findings underscore the importance of iterative debugging and the inclusion of domain-specific documentation to enhance the reliability of LLM-assisted quantum programming.

## _B. Research Challenges_

This work addresses several key challenges in LLM-based quantum code generation:

- **Lack of PennyLane-Specific Training Data:** Current LLMs are trained on limited PennyLane-related code, often leading to incorrect function calls.

- **Inaccurate Code Generation:** Without additional context, LLMs struggle with function signatures, quantum execution flow, and circuit correctness.

- **Need for a Standardized Benchmark:** Unlike Qiskit, PennyLane lacks a dedicated benchmark for evaluating LLM-assisted code generation.

## _C. Novel Contributions_

- To overcome the above challenges, we make the following key

- contributions, which are also summarized in Fig. 1.

- **Benchmark Dataset:** We introduce _QHackBench_ , the first curated dataset of PennyLane coding challenges from QHack 2023-2024, specifically designed to evaluate LLM performance in quantum programming.

- **Baseline Evaluation Agent Framework:** We propose a structured evaluation framework that iteratively refines LLM-generated quantum code through automated execution, self-reasoning, and debugging feedback, while incorporating modern agent technologies such as RAG and multi-agent systems.

- **Comprehensive baseline Evaluation:** We systematically compare LLMs with various configurations, assessing the impact of different features on quantum code correctness and execution success.

**Paper Organization:** Section II discusses the basic concepts to understand the rest of the paper and presents the related work. Section III introduces our proposed QHackBench methodology. Section IV discusses the experiment settings. Section V reports the experimental results. Section VIII concludes the paper.

979-8-3315-6986-0/25/$31.00 ©2025 IEEE 316 DOI 10.1109/QAI63978.2025.00056 Authorized licensed use limited to: Universidad Internacional de La Rioja (UNIR). Downloaded on October 14,2026 at 22:09:01 UTC from IEEE Xplore.  Restrictions apply.

## II. Background and Related Work

_A. Large Language Models (LLMs) for Code Generation_

LLMs have demonstrated remarkable capabilities in code generation, as evidenced by models such as Codex [13], StarCoder [14], and IBM’s Granite models [11]. These models are trained on extensive programming datasets and benchmarked using standardized datasets like HumanEval [13] and MBPP [15]. However, their effectiveness in niche domains such as quantum computing is limited due to the scarcity of domain-specific training data [16].

Prior research has explored the application of LLMs to quantum programming, primarily focusing on IBM’s Qiskit framework. The Qiskit Code Assistant was fine-tuned to improve accuracy in quantum code generation tasks [17]. Additionally, Vishwakarma et al. introduced Qiskit HumanEval, a benchmark designed to assess LLM-generated Qiskit code [12]. However, despite PennyLane’s increasing adoption in QML, there has been limited research on evaluating LLMs for PennyLane-based quantum programming [18]. Our work fills this gap by systematically benchmarking LLM performance on PennyLane tasks using real-world coding challenges.

_B. Quantum Programming and PennyLane_

Quantum computing frameworks facilitate various approaches to quantum programming. IBM’s Qiskit focuses on hardware-oriented circuit execution, while Google’s Cirq optimizes for near-term quantum devices [19]. PennyLane, developed by Xanadu, is distinguished by its emphasis on quantum differentiability, making it particularly well-suited for hybrid quantum-classical computations [4]. By enabling automatic differentiation of quantum circuits, PennyLane supports the optimization of variational quantum algorithms and QML models.

Despite PennyLane’s advantages, there is currently no dedicated benchmark for evaluating LLM-generated code within this framework. The lack of large-scale PennyLane datasets presents a unique challenge, necessitating alternative evaluation methods such as RAG [20]. Our work introduces _QHackBench_ , the first structured benchmark dataset for PennyLane-based LLM evaluation, leveraging real-world challenges from QHack 2023-2024.

_C. Retrieval-Augmented Generation (RAG) for Quantum Code_

RAG has emerged as an effective technique for enhancing LLMs by incorporating relevant external knowledge sources dynamically [21]. In classical programming, RAG has been employed to improve code completion by retrieving real-time documentation references [20]. In the quantum computing domain, AWS Braket has integrated RAG-based solutions to improve LLM-generated quantum code by providing access to up-to-date quantum-specific knowledge.

Similarly, _PennyLang_ , a curated dataset of PennyLane-specific code examples and quantum computing resources, serves as a structured retrieval corpus that enhances LLM prompts with relevant contextual information. By leveraging PennyLang, LLMs can access previously solved quantum problems, reducing API hallucinations and improving functional correctness in PennyLane programming [22]. The dataset consists of four primary sources: unofficial GitHub repositories, official PennyLane documentation, open-source contributions from PennyLaneAI, and quantum computing books. The composition of the dataset is shown in Fig. 2.

_D. Multi-Agent Systems for Quantum Code Generation_ Multi-agent systems have been widely explored in AI research to enhance problem-solving by enabling specialized agents to collaborate on complex tasks [23]. In programming, multi-agent frameworks have been employed for code synthesis and debugging, where different agents handle distinct roles such as code generation, execution validation, and iterative refinement [24].

For quantum programming, a multi-agent approach is particularly valuable due to the inherent complexity of debugging quantum circuits, where execution errors often stem from subtle query misinterpretations or incorrect circuit logic [25].

![](images/p02-01.png)

Fig. 2: Composition analysis of the _PennyLang_ dataset (3,347 samples).

Our experimental results demonstrate that integrating a multi-agent framework significantly improves execution success rates compared to standalone prompting or RAG-based approaches. By systematically evaluating LLM performance in a multi-agent setting, we provide the first in-depth analysis of iterative refinement in quantum code generation.

## III. QHackBench Methodology

QHackBench systematically evaluates LLM performance in quantum code generation through an automated benchmarking framework for QHack challenges. Our methodology integrates RAG with the PennyLang dataset to enhance model responses, benchmarking them against non-RAG baselines. The evaluation assesses correctness, execution success, and iterative improvements within a structured pipeline.

_A. Automated Evaluation Pipeline_

To ensure consistency and reproducibility in benchmarking LLMs for quantum code generation, we design a structured evaluation pipeline that systematically assesses model performance across different configurations. The overall evaluation pipeline is illustrated in Algorithm 1. The process begins with dataset preparation, where QHack challenge descriptions, template notebooks, and corresponding test scripts from the years 2023 and 2024 are gathered to establish a standardized benchmark. Next, we integrate RAG by retrieving relevant code snippets from the PennyLang dataset [22], providing models with enhanced contextual knowledge for more accurate code completion. To analyze the effectiveness of RAG, we evaluate multiple LLMs, including GPT-4o mini (RAG and non-RAG) and GPT-o3 Mini (RAG and non-RAG), allowing a direct comparison between retrieval-enhanced responses and baseline prompting.

Once the solutions are generated, we employ an automated execution system that runs the code in an isolated environment, verifying functional validity and correctness against predefined test cases. This is followed by the performance evaluation, where we measure key metrics such as Pass@ _𝑘_ , execution success rate, and error classification to quantify model effectiveness. Additionally, we incorporate an iterative refinement process using a multi-agent system, wherein an automated validation mechanism analyzes execution errors and refines incorrect solutions iteratively. By following this structured sequence, spanning code generation, retrieval augmentation, correctness verification, iterative improvement, and automated execution, our pipeline provides a robust and scalable framework for benchmarking LLMs in quantum

317

![](images/p03-01.png)

QHack Challenges PennyLangDataset Chunks VectorsIndexing No SolutionFound Multi-Agent System<br>Query Incorrect Correct<br>No<br>Challenge Description Code Samples Iteration < 5 Reformulate Self-Reasoning Validator<br>Yes Query Agent<br>C Challenge Template O SS Embeddings — < > ) (Same LLM)<br>Retrieval<br>Runtime Logs<br>DeepSeek V3Claude 3.7 ’ eC 2 Retrieval Code Samples Enhanced ® 3 GPT o3-Mini Incorrect Results ;<br>1 LLaMa 4GPT 4.1 AuQuerygmented Augment Samples in Query | AuQuerygmented DeepSeek-V3... Test Bench Errors i<br>Qwen 3<br>Evaluation on Test BenchFunctionality Incorrect Automated ExecutionFunctionality<br>Correct Evaluation on Test Bench<br>Base Query<br>

Fig. 3: Overview of the _QHackBench_ . _⃝_ 1 _Base query._ The QHack challenge description and template are provided to LLMs (GPT-4.1, Claude 3.7, ...) for initial code generation. _⃝_ 2 _Retrieval-augmented query_ If enabled, relevant PennyLang code snippets are retrieved, embedded, and incorporated into the query to enhance accuracy. _⃝_ 2 _Multi-agent pipeline:_ a validator agent, implemented with the same LLM, inspects run-time logs and hidden-test feedback, performs self-reasoning, reformulates the query, and asks the builder to regenerate code. This ensures correctness evaluation, error diagnosis, and improved execution.

programming, enabling precise evaluation of their capabilities in solving QHack challenges.

**Algorithm 1** Automated Benchmarking Pipeline for QHack Challenges ~~—_—~~ **Require:** Quantum challenge dataset D, LLM models M, PennyLang retrieval corpus R 1: **for** each challenge ( _𝐶𝑖 , 𝑇𝑖_ ) ∈D **do**

- 2: Retrieve relevant context S _𝑖_ from R using embedding similarity. 3: **for** each model _𝑀 𝑗_ ∈M **do** 4: Generate quantum code Q _𝑖_<sup>_𝑗_usingRAG-assistedandnon-RAGprompting.</sup> 5: Execute Q _𝑖_<sup>_𝑗_inacontrolledenvironment.</sup>

- 6: Collect execution logs L _𝑖_<sup>_𝑗_andcorrectnessstatus.</sup>

- 7: **end for**

- 8: Perform error analysis and refine Q _𝑖_<sup>_𝑗_iteratively(ifmulti-agentmodeisenabled).</sup>

9: **end for**

- 10: Compute benchmark metrics: Pass@ _𝑘_ , execution success rate, error classification.

- _B. Retrieval-Augmented Generation with PennyLang Dataset_

To enhance LLM-based quantum code generation, we integrate retrieval from the PennyLang dataset, a curated collection of resources relevant to PennyLane-based quantum programming. For each challenge, a similarity-based retriever selects the most relevant context from R using a vector database. This retrieved knowledge is appended to the model prompt, improving accuracy and reducing hallucinations. The RAG process is outlined in Algorithm 2.

**Algorithm 2** Retrieval-Augmented Generation (RAG) for Quantum <u>Code</u>

**Require:** Query input _𝑄_ , retrieval corpus R, embedding model E

- 1: Compute query embedding _𝑒𝑄_ = E( _𝑄_ )

- 2: Retrieve top-_𝑘_ documents S = arg max _𝑆𝑖_ ∈R similarity( _𝑒𝑄 ,_ E( _𝑆𝑖_ ))

3: Construct prompt: P = system prompt + S + _𝑄_

- 4: Generate response: Q = LLM(P)

- 5: **return** Generated code Q

- _C. Multi-Agent System for Iterative Code Refinement_

- To improve the reliability of LLM-generated quantum code, we employ

- a multi-agent system that iteratively refines incorrect solutions. The system consists of two main agents:

- **Code Generation Agent** (GPT-o3-Mini, DeepSeek-V3): Generates initial quantum code solutions using either RAG or non-RAG methods.

- **Validation & Correction Agent** (GPT-o3-Mini): Executes the generated code, analyzes errors from execution logs, and iteratively refines the solution through self-reasoning and debugging.

The multi-agent system follows a structured pipeline designed to iteratively improve LLM-generated quantum code by leveraging both RAG and automated debugging. The process begins with the Code Generation Agent, which produces an initial quantum circuit implementation based on the QHack challenge description. This generated solution is then executed within a controlled Jupyter

![](images/p03-02.png)

~I<br>«I<br>~I<br>-I oy<br>o 1B Advanced<br>

Fig. 4: Difficulty distribution among all the challenges.

environment, where its correctness is evaluated against predefined test cases. If execution fails, the Validation & Correction Agent analyzes the runtime logs, extracting error messages, incorrect results, and test bench failures. Based on this analysis, the agent formulates a structured debugging report, identifying potential issues and suggesting modifications. The revised query, incorporating these debugging insights, is then sent back to the Code Generation Agent for solution refinement. If RAG is enabled, the retrieved context from the _PennyLang dataset_ is also included in the updated query to enhance code corrections. This process is repeated iteratively, with a maximum of five refinement attempts, ensuring that the solution is progressively improved until it successfully passes all test cases or reaches the retry limit.

## IV. Experimental Setup

## _A. Benchmark Dataset_

We curated a dataset comprising 49 unique QHack challenges from 2023-2024 [26], [27]. These challenges span multiple QC domains, including quantum algorithms, QML, and quantum chemistry. The dataset is structured based on the yearly challenge formats and categorized by difficulty levels and thematic divisions.

- _B. Structure of QHack Challenges_

QHack challenges adhere to a structured format, with problems assigned to predefined categories and difficulty levels. The dataset is categorized as follows:

- **2023:** Challenges were structured within five narrative-based thematic sets: A Tale of Timbits, Bending Bennett’s Laws, Fall of Sqynet, and Office Hijinks. Each narrative contained five challenges, with a standardized point distribution ranging from 100 to 500 points. A total of 28 challenges were included, with 8 tutorial challenges assigned 0 points. The introduction of a narrative-driven format added an engaging element to problem-solving.

318

- **2024:** The challenge structure evolved further with a thematic-based organization, introducing five core themes: Boson Beach, Dipole Desert, FemtoForest, Tensor Tundra, and Qutropolis. This iteration featured 21 challenges with difficulty levels spanning 100 to 600 points. Higher-difficulty problems were more prevalent in later themes, reflecting an increased focus on complex quantum problem-solving.

TABLE I: Full challenge list of QHackBench.

|**Year**|**Theme**|**Challenge**|**Points**|**Difficulty**|
|---|---|---|---|---|
|||Tutorial 1 (C1-E-23)|0|Easy|
|||Tutorial 2 (C2-E-23)|0|Easy|
|||Tutorial 3 (C3-E-23)<br>|0<br>|Easy<br>|
||Tutorials|Tutorial 4 (C4-E-23)|0|Easy|
|||Tutorial 5 (C5-E-23)|0|Easy|
|||Tutorial 6 (C6-E-23)|0|Easy|
|||Tutorial 7 (C7-E-23)|0|Easy|
|||Tutorial 8(C8-E-23)|0|Easy|
|||The Magic 5 Ball (C9-E-23)|100|Easy|
||A Tale of|Cascadar (C10-I-23)|200|Intermediate|
|es)|<br>Timbits|A Pauli Worded Problem (C11-I-23)|300|Intermediate|
|ng||Entangled Robot Swarms (C12-A-23)|400|Advanced|
|lle||One Bit Wonder(C13-A-23)|500|Advanced|
|Cha||Ctrl-Z (C14-E-23)|100|Easy|
|8|Bending|Sub Superdense Coding (C15-I-23)|200|Intermediate|
|(2|Bennett’s|Secrets in Spacetime (C16-I-23)|300|Intermediate|
|**023**|Laws|A Halfway Decent Photocopier (C17-A-23)|400|Advanced|
|**2**||The Itch to Switch(C18-A-23)|500|Advanced|
|||Sqy Trotter (C19-E-23)<br>|100<br>|Easy<br>|
||Fall of|Unitary Operators (C20-I-23)|200|Intermediate|
||<br>S|Don’t Hit the Ground (C21-I-23)|300|Intermediate|
||qynet|Desperate Measures (C22-A-23)|400|Advanced|
|||IsingUprising (C23-A-23)|500|Advanced|
|||Tick Tock Bloch (C24-E-23)|100|Easy|
||Office|The Super Parameter (C25-I-23)|200|Intermediate|
||fi<br>Hijinks|The Change of Qubit (C26-I-23)<br>|300<br>|Intermediate<br>|
|||The Lazy Colleague (C27-A-23)|400|Advanced|
|||The False Proof(C28-A-23)|500|Advanced|
|||Hacking for the UpGrayde (C1-E-24)<br>|100<br>|Easy<br>|
||Boson|Save QHack Beach (C2-I-24)<br>|200<br>|Intermediate<br>|
||Bh|Mathematicians at the Resort (C3-I-24)|300|Intermediate|
||eac|Mojito HHLime Twist (C4-A-24)|400|Advanced|
|||The Three ShippingCompanies(C5-A-24)|500|Advanced|
|||Dunes out of Context (C6-E-24)<br>|100<br>|Easy<br>|
|)|Dil|The Oasis Ruins (C7-I-24)|200|Intermediate|
|ges|poe<br>Dt|The Grand Hideaway Zone Inn (C8-I-24)|300|Intermediate|
|len|eser|A Market of Quantum Trinkets (C9-A-24)|400|Advanced|
|hal||The Wormhole Airdrome(C10-A-24)|500|Advanced|
|C||To View or Not to View (C11-E-24)|100|Easy|
|(21|Femto|Rainy Days at the Retreat (C12-I-24)|200|Intermediate|
|**24**|F|The Mach-Zehnder Cabin (C13-I-24)|300|Intermediate|
|**20**|orest|Stay Out of This Swamp! (C14-A-24)|400|Advanced|
|||LazyWorkers at the Terminal(C15-A-24)|500|Advanced|
|||The Chalet of the Random Gate (C16-E-24)|100|Easy|
||T|Hockey Night in the Cave (C17-I-24)|200|Intermediate|
||ensor<br>|Critical Coffee Conundrum (C18-I-24)|300|Intermediate|
||Tundra|The Triple H Hotel (C19-A-24)|400|Advanced|
|||Travellingon the Eigentracksly (C20-A-24)|500|Advanced|
||Qutropolis|Fireworks inQutropolis(C21-A-24)|600|Advanced|

Each challenge consists of a problem statement, a Jupyter Notebook or Python template for completing the code, and a structured testing methodology. The dataset includes problem descriptions, solution templates, and test functions.

To assess trends in quantum computing problem-solving, we conduct a statistical analysis of the challenge dataset (see Table I). Each challenge was assigned a difficulty score based on complexity: Easy (0–100 points), intermediate (200–300 points), and advanced (400–600 points). Key observations include:

- **Challenge Distribution:** Each year maintains a balanced distribution of challenges, with a gradual shift in complexity. In 2023, 28 challenges are introduced, spanning easy, intermediate, and advanced levels, while in 2024, 21 challenges are included, reflecting an increasing focus on more complex problem-solving.

- **Difficulty Levels:** Over time, the proportion of advanced-level challenges increased slightly, with 8 Advanced challenges in 2023 rising to 9 in 2024. Additionally, no tutorial-level challenges were included initially, but a 600-point problem was introduced in 2024, marking a shift toward higher-difficulty problem-solving.

Our evaluation considers functional correctness, i.e., the code execution must match expected outputs. Figure 4 shows a clear alignment between point values and difficulty levels: easy challenges cluster at 0–100 points, intermediate ones peak at 200–300, and advanced challenges dominate the 400–600 range. The sharp drop in count at 600 points highlights its rarity and difficulty. This reflects a deliberate and consistent mapping from score to challenge complexity.

_C. Evaluation Framework_

To benchmark the effectiveness of the multi-agent refinement process, we evaluate the system on QHack coding challenges from 2023 and 2024. Two evaluation settings are considered:

- **Single-agent generation.** A “builder” LLM receives the challenge and must solve it in at most five attempts, _with or without RAG_ .

- **Multi-agent refinement.** A validator LLM inspects failing runs and reformulates the query; the builder then regenerates code. Only this pipeline uses the lightweight validator models listed below. The following models are considered for Multi-agent evaluation but

- the pipeline is extendable.

- **GPT-o3-Mini (RAG and non-RAG)** : Lighter-weight model used for both code generation and debugging.

- **DeepSeek-V3** : Specialized model for advanced code completion.

- _1) Execution Pipeline_

Each challenge is processed through the following pipeline:

- 1) **Initial Code Generation:** The base query (problem description and template) is passed to the Code Generation Agent.

- 2) **Solution Execution:** The generated solution is injected into a Jupyter notebook and executed using **Papermill** .

- 3) **Validation and Debugging:** The Validator Agent extracts runtime logs, test errors, and execution failures.

- 4) **Solution Refinement:** Based on debugging feedback, the next iteration generates a revised solution.

- 5) **Iteration Limit:** The process repeats until a correct solution is found or a maximum of five attempts is reached.

- _2) Retrieval-Augmented Debugging_

Using RAG, the validator performs a _ChromaDB_ vectorsearch ( **MMR** , top-_𝑘_ =3) over the _PennyLang_ corpus and injects the most relevant code chunks into the follow-up query.

- _3) Evaluation Metrics_

- To compare the efficiency of RAG-based and non-RAG debugging,

- we measure:

- **Pass@** _𝑘_ **:** Probability of obtaining a correct solution within the first _𝑘_ attempts.

- **Execution Success Rate:** Percentage of solutions that execute without runtime errors.

- **Correction Efficiency:** Average number of iterations needed for successful code refinement.

- _4) Computational Resources_

- All experiments were conducted in a high-performance computing

- environment with:

- **Software:** Python 3.10, LangChain, OpenAI / Anthropic / DeepSeek APIs, JupyterLab, and Papermill for execution monitoring.

- **Retrieval Setup:** _ChromaDB_ for vector-based retrieval, optimized for PennyLang dataset queries.

By testing multiple LLMs across different retrieval and iteration strategies, we assess how retrieval-augmented debugging enhances quantum code generation accuracy.

## V. Results

**Benchmarking Results** : Out evaluation reveals substantial performance heterogeneity, as detailed in Table II. LLaMa 4 emerges as the most robust model overall, achieving a high average accuracy of 47.0% with RAG and 44.0% in its standard configuration, with corresponding scores of 2950 and 2600, respectively. While LLaMa

319

Challenge Iterations  RAG vs Non-RAG (2023 + 2024)

![](images/p05-01.png)

5<br>CLAUDE 3.7  RAG × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × × ×<br>CLAUDE 3.7  Non-RAG 1 × × 3 × 1 2 1 3 × × 4 × 5 × 4 × × 2 × × × × 1 × × × × 1 × × × × × × × × × 1 2 × 5 × 2 × × × × ×<br>DeepSeek V3  RAG 1 1 × × × 1 × × × × × × × 1 × × 1 × × × 1 × 1 1 × × × × 1 × × × × × × × × × 1 × × × × × × × × × × 4<br>DeepSeek V3  Non-RAG 1 × 1 1 × 1 1 1 1 1 × × × 1 × 2 1 × 1 × 4 × 1 1 × 1 × × 1 × × × × 1 × 1 × × 1 1 × 1 × 3 × 2 × 1 ×<br>GPT 4.1  RAG 1 3 × 3 × 1 3 × × × × 2 × 1 × 4 × × × × 1 × × 1 × × × × 1 × × × × × × × × × 2 × × × × 4 × × × 3 ×<br>3<br>GPT 4.1  Non-RAG 1 × × × × 1 3 × 4 × × × × 1 2 × × × 2 × 2 × × 1 × × × × 1 × × × × 2 × × × × 1 5 2 1 × 2 × 4 × × ×<br>LLama-4  RAG 1 × 2 2 × 1 × 1 3 2 × × × 2 × 1 1 × 3 × 3 × 1 1 5 2 × × 1 × × × × × × × × × 2 2 3 4 × 3 × × 2 × ×<br>LLama-4  Non-RAG 1 4 3 4 × 1 2 1 3 2 3 × × 1 × 1 1 × 3 4 × × 1 1 × × × × 1 × × × × 3 × × × × 3 2 × 3 × × × × 2 × × 2<br>Qwen-3  RAG × × × × × × × × × × × × × 1 × × × × × × × × × 1 × × × × 4 × × × × × × × × × 1 × × × × × × × × × ×<br>Qwen-3  Non-RAG 2 2 × × × × × × × 2 × × × × × × × × × × × × 1 1 × × × × 2 × × × × × × × × × × × × × × × × × × × ×<br>1<br>C1-E-23C2-E-23C3-E-23C4-E-23C5-E-23C6-E-23C7-E-23C8-E-23C9-E-23C10-I-23C11-I-23C12-A-23C13-A-23C14-E-23C15-I-23C16-I-23C17-A-23C18-A-23C19-E-23C20-I-23C21-I-23C22-A-23C23-A-23C24-E-23C25-I-23C26-I-23C27-A-23C28-A-23C1-E-24C2-I-24C3-I-24C4-A-24C5-A-24C6-E-24C7-I-24C8-I-24C9-A-24C10-A-24C11-E-24C12-I-24C13-I-24C14-A-24C15-A-24C16-E-24C17-I-24C18-I-24C19-A-24C20-A-24C21-A-24<br>Number of Iterations<br>

Fig. 5: Per–challenge performance heat-map for all models on the complete QHack 2023 & 2024 challenge suites. Each row corresponds to a model–prompting method pair (RAG or Non-RAG); each column is a single challenge, ordered first by 2023 codes (C1{E{23 . . . C28{A{23) followed by 2024 codes (C1{E{24 . . . C21{A{24). The integer written inside every solved cell is the number of iterations required before the model produced an accepted solution (lower is better). Color shading encodes the same metric monotonically from one to five iterations, while light-grey cells marked with “×” indicate that the challenge remained unsolved within the five-attempt budget. This compact view highlights (i) model-specific strengths, (ii) the impact of retrieval-augmented generation (compare each model’s RAG vs. Non-RAG row), and (iii) year-to-year differences in challenge difficulty across the full benchmark.

4 shows strong all-around capability, DeepSeek V3 establishes itself as the definitive leader in non-RAG performance, attaining the highest average accuracy of 49.4% and the top score of 3000. In contrast, GPT-4.1 maintains relatively stable, albeit more moderate, performance across both modes.

A significant finding is the pronounced year-over-year performance degradation observed in some models, suggesting the 2024 challenge set introduced greater difficulty. For instance, LLaMa 4’s RAG accuracy dropped from 60.7% in 2023 to 33.3% in 2024. Even more dramatically, DeepSeek V3’s RAG performance fell from 32.1% to a near-failure 4.8%. This trend indicates that model robustness over evolving task complexity remains a critical area for improvement across more diverse challenge sets. One possible explanation for the 2024 drop is that some models may have inadvertently memorized parts of the 2023 challenge set during pretraining, leading to data contamination in the earlier year.

||TABLE II:|Mode|l Accura|cy Perform|ance|||
|---|---|---|---|---|---|---|---|
|**Model**|**RAG**|**2023**||**2024**||**A**|**vg.**|
||**Acc. **|**(%) **|**Score **|**Acc. (%) **|**Score**|**Acc. **|**Score**|
|Claude 3.7|✓|0.0|0|0.0|0|0.0|0|
||✗|42.9|2400|19.0|1500|31.0|1950|
|DeepSeek V3|✓|32.1|1900|4.8|200|18.5|1050|
||✗|**60.7**|**3600**|38.1|2400|**49.4**|**3000**|
|GPT 4.1|✓|39.3|1900|14.3|700|26.8|1300|
||✗|35.7|2300|33.3|2300|34.5|2300|
|LLaMa 4|✓|**60.7**|**3600**|33.3|2300|**47.0**|**2950**|
||✗|**64.3**|**3500**|23.8|1700|44.0|2600|
|Qwen 3|✓|0.0|0|0.0|0|0.0|0|
||✗|21.4|1100|0.0|0|10.7|550|

**Legend:** Complete Failure (0%) — Best — Good (≥ 35%)

**Attempt Analysis** : Table II shows important insights into model problem-solving dynamics and computational resource allocation. Successful models typically converge within 1–3 iterations on elementary tasks, with iteration counts increasing systematically for more complex problems. DeepSeek V3 displays remarkable consistency across modes, often solving early-stage challenges in a single iteration and maintaining stable performance in medium-difficulty tasks. LLaMa 4, while efficient in RAG mode during the 2023 set, exhibits greater iteration variability in 2024, suggesting difficulty in adapting to new problem formulations. The universal failure of Claude 3.7 under RAG conditions, juxtaposed with its sporadic non-RAG successes, reinforces the earlier hypothesis of architectural misalignment with RAG paradigms.

For advanced-level challenges across both years, most models either

![](images/p05-02.png)

Challenge Success Comparison on o3 mini ({Method: Non RAG, RAG, Multi Agent})<br>Non RAG × × × × × ×<br>RAG × × × × × × ×  S<br>Multi Agent × × × ×<br>Challenge Iterations with Multi-Agent Approach Solved<br>(o3 mini vs. DeepSeek V3 Multi agent) Not Solved<br>o3 mini 1 1 2 2 2 5 1 5 3 2 3 2 4 1 5 3 2 5 Worst<br>DeepSeek V3 5 1 5 5 2 5 1 5 5 5 5 5 2 2 2 2 2 5<br>Best<br>C8-I-24C14-A-24C16-E-24C18-I-24C6-E-24C21-A-24C1-E-24C17-I-24C15-A-24C13-I-24C9-A-24C3-I-24C4-A-24C11-E-24C2-I-24C20-A-24C19-A-24C10-A-24<br>C8-I-24C14-A-24C16-E-24C18-I-24C6-E-24C21-A-24C1-E-24C17-I-24C15-A-24C13-I-24C9-A-24C3-I-24C4-A-24C11-E-24C2-I-24C20-A-24C19-A-24C10-A-24<br>Iterations<br>

Fig. 6: Top Panel: Matrix depicting the correctness of results given by each of the Non-RAG, RAG, and Multi-Agent system methods for each problem. All three methods use the o3-mini model as the model performing the code completion. The Multi-Agent system further uses the o3-mini model to debug prior incorrect responses. Bottom Panel: Heatmap comparing iteration counts (fewer is better) for each challenge under the o3-mini and DeepSeek V3 multi-agent methods. Green cells indicate lower iteration counts (better performance), while red cells represent higher iteration counts or unsolved tasks (worse performance).

exhaust the 5-iteration limit or fail to produce valid solutions, marking clear performance boundaries. This behavior affirms the discriminative strength of the QHackBench and highlights current limitations in scaling AI systems toward expert-level reasoning and problem-solving.

**RAG vs non-RAG** : The comparative analysis between RAG and non-RAG uncovers a crucial binary compatibility split among models. A particularly striking observation is the complete failure of certain architectures when integrated with RAG. Both Claude 3.7 and Qwen 3 achieve zero accuracy in all RAG test conditions. However, they retain partial functionality in non-RAG mode, with Claude 3.7 achieving 31.0% accuracy (1950 score) and Qwen 3 reaching 10.7% (550 score). This contrast underscores that for RAG to be effective, a model must possess baseline conceptual understanding compatible with the retrieval mechanism, which is further discussed in Section VI-B.

Among the RAG-enhanced models, performance tendencies diverge significantly. DeepSeek V3 exhibits a strong preference for non-RAG operation, with a 31-percentage-point accuracy advantage (49.4% vs. 18.5%), suggesting difficulties in utilizing retrieved context. In contrast, LLaMa 4 demonstrates relatively balanced performance, with a slight preference for RAG (47.0% vs. 44.0%), while GPT-4.1 also favors non-RAG mode (34.5% vs. 26.8%). These results indicate that beyond requiring a baseline understanding of task-relevant concepts and knowledge, models differ markedly in their ability to incorporate retrieved information, especially in tasks where training data is limited.

Fig. 5 provides a granular view of this behavior, revealing differences

320

TABLE III: Comparative Analysis of Error Rates on QHackBench by year and model ( **%** )

**Error Types:** Syn = Syntax Errors, NoOut = No Output, Inc = Incomplete Output, Run = Runtime Errors

|**Model**||**202**|**3**|||**20**|**24**|||**Aver**|**age**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**Syn**|**NoOut**|**Inc**|**Run**|**Syn**|**NoOut**|**Inc**|**Run**|**Syn**|**NoOut**|**Inc**|**Run**|
|**LLaMA 4**|**5.2**|**57.8**|**8.4**|**28.6**|**9.2**|**52.9**|**13.7**|**24.2**|**7.2**|**55.4**|**11.1**|**26.4**|
|**Qwen3**|**1.8**|**96.0**|**1.1**|**1.1**|**2.0**|**88.4**|**1.0**|**8.6**|**1.9**|**92.8**|**1.1**|**4.2**|
|**Deepseek-V3**|**0.0**|**96.3**|**0.0**|**3.7**|**1.3**|**91.6**|**0.0**|**7.1**|**0.6**|**94.0**|**0.0**|**5.3**|
|**GPT-4.1**|**5.3**|**74.9**|**9.6**|**9.6**|**11.2**|**66.5**|**6.8**|**15.5**|**8.0**|**71.0**|**8.3**|**12.4**|
|**Claude 3.7**|**0.4**|**96.3**|**0.4**|**2.9**|**1.0**|**94.2**|**0.0**|**4.9**|**0.7**|**95.3**|**0.2**|**3.8**|
||||**Color Sca**|**le:**<br>■0-|25%<br>■|25-50%<br>|■50-75%|■75-100|%||||

in performance consistency. DeepSeek V3 (non-RAG) and LLaMa 4 (in both modes) demonstrate broad success across a wide array of individual challenges. In contrast, the successes of GPT 4.1 and Qwen 3 (non-RAG) are more sporadic, indicating a narrower range of solvable problems. This suggests that top-performing models are distinguished not just by their average accuracy, but by their ability to generalize across a diverse set of tasks.

**Evaluation on multi-agent** Figure 6 compares three prompting methods, vanilla, RAG, and multi-agent, on QHack 2024 challenges using the o3-mini model. The multi-agent approach consistently outperforms both baselines, solving more tasks, including several that RAG or vanilla failed to address. When paired with DeepSeek V3, the multi-agent strategy further demonstrates lower or comparable iteration counts across many challenges, indicating faster convergence. These improvements highlight the effectiveness of an internal feedback loop, where agents iteratively refine and debug their outputs. Overall, the results affirm that multi-agent prompting enhances model capability in quantum programming tasks by leveraging structured self-correction.

## VI. Discussions

## _A. Failure Analysis_

Table III presents an analysis of the common failure modes observed during our baseline evaluation across the five tested models. The most prevalent failure type is the absence of generated output, with suppression rates ranging from 55.4% for LLaMA 4 to 95.3% for Claude 3.7. This widespread suppression behavior is primarily attributable to the models’ insufficient understanding of quantum programming tasks, which prevents them from generating valid solution code. These results highlight a critical limitation in current LLMs, as quantum programming appears to exceed their capability thresholds, leading many models to suppress output entirely rather than risk producing incorrect responses. The disparity in suppression rates is particularly notable: while Claude 3.7, DeepSeek-V3, and Qwen3 all exhibit suppression rates exceeding 90%, LLaMA 4 demonstrates considerably better responsiveness at 55.4%. This variation underscores substantial differences among model families, likely driven by factors such as model architecture, training data composition, and learning strategies, which in turn result in differing levels of adaptability to novel and conceptually demanding tasks.

For code that is successfully generated, runtime errors emerge as the most common form of active failure. This is particularly pronounced in LLaMA 4, which shows a 26.4% runtime error rate, significantly higher than 3.8%–12.4% range observed in other models. This pattern suggests that even if LLMs generally grasp the syntax of quantum programming on some challenges, they struggle with semantic correctness. The generated code is often syntactically valid but fails at execution due to logical flaws, such as improper gate sequencing or invalid qubit operations. In contrast, syntax errors, including, but not limited to, malformed function signatures or attempts to access non-existent properties or functions, remain consistently low (0.6%–8.0%). This indicates that structural language generation is largely a solved problem, specifically, Python on this task, with most

failures stemming from deeper conceptual misunderstandings rather than surface-level formatting.

**Insight** : These failure patterns highlight fundamental limitations in current LLMs’ understanding of quantum computing. First, the predominance of no output failure suggests models recognize quantum programming as distinct from classical programming but lack the training data or architectural adaptations to engage confidently with such tasks. Second, the high rate of runtime errors among models that do generate output indicates that syntactic fluency alone is insufficient, as quantum programming demands a deeper understanding of quantum principles, circuit constraints, and hardware-specific behaviors. Third, these challenges raise concerns about whether general-purpose LLMs can perform effectively in specialized scientific domains without architectural innovation or require purpose-built models trained on domain-specific data and evaluation protocols.

## _B. Case Studies_

To better understand RAG’s inconsistent performance in quantum code generation on QHackBench, we present two case studies on Tutorial 1 from QHack 2023 highlighting successful and failed use cases. We analyze instances where RAG improves generation quality (LLaMA4) and introduces critical errors (Qwen-3), conducting detailed error analysis to trace how retrieval noise causes failure. These cases illustrate how RAG’s effectiveness depends on both context quality and the model’s ability to integrate relevant information into executable code.

## Case 1: LLaMA-4 - RAG vs Non-RAG (Tutorial #1)

![](images/p06-01.png)

Challenge summary. Tutorial #1 asks competitors to<br>implement add_numbers so that the function passes a hidden<br>test-suite checking  𝑥 +  𝑦 within 10 −4 relative error. The task is<br>simple and most of the models solve it in first attempt.<br>1 # RAG solution<br>2 def add_numbers(numbers):<br>3 """<br>4 Return x + y , where numbers == [x, y].<br>5 Matches QHack it_adds_up checker tolerance<br>(1e-4).<br>6 """<br>7 x, y = numbers<br>8 return float(x) + float(y)<br>9<br>10 # non-RAG solution<br>11 def add_numbers(numbers):<br>12 x, y = map(float, numbers)<br>13 return x + y<br>Listing 1: LLaMA-4 Implementations (RAG equals Non-RAG)<br>

In Case 1, both RAG and non-RAG approaches yield correct solutions with LLaMA-4, with RAG offering model more slights on quantum code.

321

## Case 2: Qwen-3 - RAG vs Non-RAG (Tutorial #1)

![](images/p07-01.png)

Key observation.  Contrary to the LLaMA-4 case, Qwen-3’s RAG-augmented<br>variant exhausted the five-attempt budget without passing the checker.<br>Inspection of the retrieved context revealed irrelevant mathematical references<br>that distracted the model from the concise task specification.<br>Limitations Observed (RAG run):<br>

![](images/p07-02.png)

• Retrieved passages contained floating-point precision caveats that led the<br>model to over-engineer a tolerance loop and fail hidden tests.<br>• The function returned Decimal objects instead of float, breaking the<br>autograder’s type check.<br>• No explicit fallback when the retrieval step returned empty context.<br>1 def add_numbers(numbers):<br>2 x, y = map(float, numbers)<br>3 return x + y<br>Listing 2: Qwen-3 Implementation (Non-RAG: Correct ✓)<br>RAG trace (excerpt showing two rejected attempts):<br>1 # RAG attempt #1 (rejected)<br>2 <think> </think> ‘‘‘python #These tokens are<br>causing syntax error.<br>3 def add_numbers(numbers):<br>4 result = x + y<br>5 return str(result)<br>6<br>7 # RAG attempt #5 (rejected)<br>8 ### Problematic Code Example<br>9<br>10 Here’s an example of what might be causing the<br>error:<br>11 ‘‘‘python<br>12 def add_numbers(x, y):<br>13 return x + y<br>14 ‘‘‘<br>15 Even though the logic of ’return x + y’ is correct,<br>the character makes Python throw a<br>’SyntaxError’.<br>16 ---<br>17 ### Corrected Code<br>18 To fix it, simply remove the invalid characters and<br>ensure your function looks like this:<br>19 ‘‘‘python<br>20 def add_numbers(x, y):<br>21 return x + y<br>22 ‘‘‘<br>Listing 3: Qwen-3 Implementation (RAG: Incorrect ✗)<br>The model repeatedly introduces either incorrect tokens or other text, which<br>causes a syntax error in the running of the generated code. The extra tokens<br>are caused by LLM hallucination.<br>

This case highlights how RAG can degrade performance when irrelevant context misleads the model, demonstrating the importance of retrieval quality and fallback strategies. The retrieved mathematical references caused Qwen-3 to over-engineer the solution with unnecessary precision handling and type conversions, ultimately leading to systematic failures across all five attempts.

## VII. Limitations and Future Work

While QHackBench offers a structured benchmark for evaluating LLMs in quantum computing, our results highlight key limitations. (1) Even with RAG, models frequently produce hallucinated APIs and incorrect quantum circuits, revealing a lack of domain-specific understanding despite access to documentation. (2) Binary pass@k fails to capture semantic errors; many outputs are syntactically correct but fail at runtime due to flawed quantum logic. Future work should focus on quantum-specific training frameworks, richer datasets, and integrating quantum principles into training objectives. Agentic models tailored to quantum tasks are a promising direction, with QHackBench serving as both benchmark and testbed.

## VIII. Conclusion

We introduced _QHackBench_ , the first benchmark for evaluating LLMs on PennyLane-based quantum code generation using QHack

2023–2024 challenges, alongside a baseline framework for low-data settings. Comparing vanilla prompting, RAG, and a simple multi-agent refinement method, we find that RAG boosts correctness, while the multi-agent approach improves execution success via iterative reasoning. Our results show RAG’s effectiveness depends on the model’s quantum understanding, and agentic methods offer further gains. Evaluations on GPT-4o, GPT-o3-Mini, and DeepSeek-V3 highlight both capabilities and limitations in quantum programming, demonstrating the promise of agent-based techniques in this domain.

## Acknowledgment

This work was supported in part by the NYUAD Center for Quantum and Topological Systems (CQTS), funded by Tamkeen under the NYUAD Research Institute grant CG008, the NYUAD Center for CyberSecurity (CCS), funded by Tamkeen under the NYUAD Research Institute Award G1104, and the NYUAD High Performance Computing (HPC) center for providing necessary compute resources for the experiments.

## References

- [1] F. Arute _et al._ , “Quantum supremacy using a programmable superconducting processor,” _Nature_ , 2019.

- [2] M. Kashif, A. Marchisio, and M. Shafique, “Computational advantage in hybrid quantum neural networks: Myth or reality?” in _DAC_ , 2025.

- [3] M. Kashif and S. Al-Kuwari, “Demonstrating quantum advantage in hybrid quantum neural networks for model capacity,” in _ICRC_ , 2022, pp. 36–44.

- [4] V. Bergholm _et al._ , “PennyLane: Automatic differentiation of hybrid quantum-classical computations,” _arXiv:1811.04968_ , 2018.

- [5] J. Biamonte _et al._ , “Quantum machine learning,” _Nature_ , 2017.

- [6] K. Zaman, A. Marchisio, M. A. Hanif, and M. Shafique, “A survey on quantum machine learning: Current trends, challenges, opportunities, and the road ahead,” _arXiv preprint arXiv:2310.10315_ , 2023.

- [7] K. Dave _et al._ , “Optimizing low-energy carbon IIOT systems with quantum algorithms: Performance evaluation and noise robustness,” _IEEE IoT_ , 2025.

- [8] N. Innan, B. K. Behera, S. Al-Kuwari, and A. Farouk, “Qnn-vrcs: A quantum neural network for vehicle road cooperation systems,” _IEEE Transactions on Intelligent Transportation Systems_ , 2025.

- [9] N. Innan _et al._ , “Next-generation quantum neural networks: Enhancing efficiency, security, and privacy,” in _IOLTS_ , 2025.

- [10] M. Shao _et al._ , “Survey of different large language model architectures: Trends, benchmarks, and challenges,” _IEEE Access_ , 2024.

- [11] N. Dupuis _et al._ , “Qiskit Code Assistant: Training LLMs for generating Quantum Computing Code,” _arXiv preprint arXiv:2405.19495_ , 2024.

- [12] S. Vishwakarma _et al._ , “Qiskit HumanEval: An Evaluation Benchmark for Quantum Code Generative Models,” _arXiv:2406.14712_ , 2024.

- [13] M. Chen, J. Tworek, H. Jun _et al._ , “Evaluating large language models trained on code,” _arXiv preprint arXiv:2107.03374_ , 2021.

- [14] R. Li, A. Q. Jiang, C. Qian _et al._ , “Starcoder: May the source be with you!” _arXiv preprint arXiv:2305.06161_ , 2023.

- [15] J. Austin _et al._ , “Program synthesis with large language models,” _arXiv preprint arXiv:2108.07732_ , 2021.

- [16] L. Watson, “QHack 2022 - the one-of-a-kind celebration of quantum computing,” PennyLane Blog, uRL: https://pennylane.ai/blog/2022/03/ qhack-2022-the-one-of-a-kind-celebration-of-quantum-computing.

- [17] D. G. Almeida, J. Cruz-Benito, and R. Davis, “Introducing qiskit code assistant,” IBM Quantum Computing Blog (Oct 9, 2024), uRL: https://ww w.ibm.com/quantum/blog/qiskit-code-assistant.

- [18] A. Basit _et al._ , “Pennycoder: Efficient domain-specific llms for pennylanebased quantum code generation,” _arXiv preprint arXiv:2507.19562_ , 2025.

- [19] C. Gidney and M. Newman, “Cirq: A python framework for creating, editing, and invoking noisy intermediate scale quantum (nisq) circuits,” _QST_ , 2021.

- [20] Y. Kharkov _et al._ , “Accelerate quantum software development on amazon braket with claude-3,” AWS Quantum Technologies Blog (18 Sep 2024), uRL: https://aws.amazon.com/blogs/quantum-computing/accelerate-quant um-software-development-on-amazon-braket-with-claude-3/.

- [21] P. Lewis _et al._ , “Retrieval-augmented generation for knowledge-intensive nlp tasks,” _arXiv preprint arXiv:2005.11401_ , 2020.

- [22] A. Basit _et al._ , “Pennylang: Pioneering llm-based quantum code generation with a novel pennylane-centric dataset,” _arXiv:2503.02497_ , 2025.

- [23] M. Wooldridge, _An Introduction to MultiAgent Systems_ . John Wiley & Sons, 2009.

- [24] H. Jin, Z. Sun, and H. Chen, “Rgd: Multi-llm based agent debugger via refinement and generation guidance,” 2024.

- [25] W. Yang _et al._ , “Coast: Enhancing the code debugging ability of llms through communicative agent based data synthesis,” in _Findings of the Association for Computational Linguistics: NAACL 2025_ , 2025.

- [26] Xanadu AI, “Qhack 2023 coding challenges.” [Online]. Available: https://github.com/XanaduAI/qhack 2023 coding challenges

- [27] Xanadu AI, “Qhack 2024 coding challenges.” [Online]. Available: https://github.com/XanaduAI/QHack2024-coding-challenges

322
