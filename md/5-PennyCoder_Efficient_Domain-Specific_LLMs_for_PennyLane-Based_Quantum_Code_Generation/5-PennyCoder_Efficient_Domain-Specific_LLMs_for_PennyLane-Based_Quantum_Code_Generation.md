2025 IEEE International Conference on Quantum Computing and Engineering (QCE)

# PennyCoder: Efficient Domain-Specific LLMs for PennyLane-Based Quantum Code Generation

Abdul Basit<sup>1</sup> , Minghao Shao<sup>1</sup> , Muhammad Haider Asif<sup>1,2</sup> , Nouhaila Innan<sup>1,2</sup> , Muhammad Kashif<sup>1,2</sup> , Alberto Marchisio<sup>1,2</sup> ,

Muhammad Shafique<sup>1,2</sup>

> _1eBRAIN Lab, Division of Engineering New York University (NYU) Abu Dhabi_ , Abu Dhabi, UAE

> _2Center for Quantum and Topological Systems (CQTS), NYUAD Research Institute, New York University Abu Dhabi_ , UAE

_{_ abdul.basit, shao.minghao, ma8183, nouhaila.innan, muhammadkashif, alberto.marchisio, muhammad.shafique _}_ @nyu.edu

**_Abstract_ —The growing demand for robust quantum programming frameworks has unveiled a critical limitation: current large language model (LLM) based quantum code assistants heavily rely on remote APIs, introducing challenges related to privacy, latency, and excessive usage costs. Addressing this gap, we propose PennyCoder, a novel lightweight framework for quantum code generation, explicitly designed for local and embedded deployment to enable on-device quantum programming assistance without external API dependence. PennyCoder leverages a fine-tuned version of the LLaMA 3.1-8B model, adapted through parameter-efficient Low-Rank Adaptation (LoRA) techniques combined with domain-specific instruction tuning optimized for the specialized syntax and computational logic of quantum programming in PennyLane, including tasks in quantum machine learning and quantum reinforcement learning. Unlike prior work focused on cloud-based quantum code generation, our approach emphasizes device-native operability while maintaining high model efficacy. We rigorously evaluated PennyCoder over a comprehensive quantum programming dataset, achieving 44.3% accuracy with our fine-tuned model (compared to 33.7% for the base LLaMA 3.1-8B and 40.1% for the RAG-augmented baseline), demonstrating a significant improvement in functional correctness.**

**_Index Terms_ —Quantum Programming, Large Language Models, Edge AI, PennyLane Code Generation, Domain-Specific Fine-Tuning, Retrieval-Augmented Generation (RAG).**

## I. INTRODUCTION

Quantum computing is rapidly evolving from a theoretical pursuit to a practical technology, propelled by advances in both hardware and software. Milestones such as Google’s 105-qubit Willow processor [1], IBM’s 1,000-qubit Condor [2], and Microsoft’s Majorana 1 device [3] showcase growing capabilities in quantum hardware, driving demand for equally robust software tools. Frameworks like PennyLane [4] have facilitated quantum algorithm design and execution, particularly in emerging applications such as Quantum Machine Learning (QML) [5] and Quantum Reinforcement Learning (QRL) [6]. However, there remains a significant gap in intelligent programming support for such specialized quantum paradigms.

Simultaneously, Large Language Models (LLMs) have transformed code generation across domains, including software engineering [7], hardware design [8], robotics [9], and art [10]. These successes are often enabled by domain-specific tuning, allowing LLMs to manage specialized syntax and logic with improved accuracy.

Despite these advances, quantum code generation remains underexplored. Tools like IBM’s Qiskit Assistant [11] and RAG-based solutions [12]–[14] have demonstrated early promise, yet they largely depend on remote APIs (e.g., Codex, GPT-4), introducing latency, cost, privacy, and deployment constraints. Moreover, the intricate syntax and decision-making structures of quantum circuits designed for QRL, such as agent-based feedback, reward propagation, and dynamic Hamiltonian encoding, often exceed the capabilities of general-purpose models, even when augmented with retrieval.

Current approaches fall into two broad categories: (i) _General Foundation Models_ , which offer moderate performance but suffer from high hallucination rates; and (ii) _RAG-Augmented Models_ , which enhance contextual grounding at the cost of external dependencies. Neither approach sufficiently addresses the need for lightweight, locally deployable quantum programming assistants that can handle the evolving complexity of QRL environments.

Our empirical evaluation highlights this domain gap: baseline models like LLaMA 3.1-8B achieve only **33.7%** accuracy, while RAGaugmented variants reach **40.1%** on PennyLang [14] dataset tasks.

![](images/p01-01.png)

Quantum PennyCoder On-Device<br>Instruction<br>ProgrammingTasks LLaMa 3.1-8B + Tuning Quantum CodeAssistance<br>PennyLang Dataset<br>

Fig. 1. PennyCoder system, a lightweight on-device quantum code generation assistant. User queries are processed locally by a LoRA-tuned LLaMA 3.1-8B model, enhanced through domain-specific instruction tuning on the PennyLang dataset. The system outputs valid PennyLane-compatible quantum code and eliminates the need for external APIs by supporting embedded, privacyconscious deployment.

These limitations underscore the need for tailored solutions to meet the functional correctness requirements of quantum programming (see Section IV).

To address this challenge, we introduce _PennyCoder_ , a lightweight, domain-adapted LLM framework designed for quantum code generation. PennyCoder integrates two key components: (1) a domainspecific model fine-tuned on the PennyLang dataset using instruction tuning; and (2) an efficient deployment strategy using Low-Rank Adaptation (LoRA). We further investigate decoding strategies (e.g., temperature, nucleus sampling) to improve output fidelity. Our contributions are as follows:

1. We present _PennyCoder_ , a novel framework for quantum code generation that combines instruction fine-tuning with LoRAbased efficient adaptation.

2. We conduct a comprehensive evaluation demonstrating significant improvements over baseline and RAG-augmented models.

3. We analyze the impact of decoding hyperparameters on quantum code generation, offering insights for future system design.

4. We showcase the effectiveness of _PennyCoder_ on different use cases, including quantum algorithms, QML, and QRL tasks.

PennyCoder achieves an accuracy of **44.32%** on tasks from the PennyLang dataset using LLaMA 3.1-8B as the foundation model, substantially outperforming both baseline and RAG-augmented models.

## II. BACKGROUND AND RELATED WORK

## _A. Large Language Models (LLMs) for Code Generation_

Large Language Models (LLMs) have shown strong performance in general-purpose code generation, with models like Codex [7], StarCoder [15], and IBM’s Granite [16] trained on diverse programming corpora. Benchmarks such as HumanEval [7] and MBPP [17] have facilitated evaluation. However, their generalizability to niche quantum domains remains limited [18], particularly when addressing quantum learning tasks such as Quantum Reinforcement Learning.

Prior research has explored the application of LLMs to quantum programming, primarily focusing on IBM’s Qiskit framework. The Qiskit Code Assistant was fine-tuned to improve accuracy in quantum code generation tasks [19]. Additionally, Vishwakarma et al. introduced Qiskit HumanEval, a benchmark designed to assess LLMgenerated Qiskit code [20]. However, despite PennyLane’s increasing adoption in QML, there has been limited research on evaluating LLMs for PennyLane-based quantum programming [21]. Our work fills this gap by systematically benchmarking LLM performance on PennyLane tasks using real-world coding challenges.

979-8-3315-5736-2/25/$31.00 ©2025 IEEE 229 DOI 10.1109/QCE65121.2025.10324 Authorized licensed use limited to: Universidad Internacional de La Rioja (UNIR). Downloaded on October 14,2026 at 22:08:42 UTC from IEEE Xplore.  Restrictions apply.

## _B. Quantum Reinforcement Learning and PennyLane_

QRL is an emerging area where reinforcement learning paradigms intersect with quantum computing, enabling agents to interact with quantum environments to learn optimal policies [22]–[24]. It requires efficient modeling of quantum states, unitaries, and reward-based adaptation across quantum circuits. PennyLane [4], developed by Xanadu, is particularly suited for this due to its hybrid execution model and support for automatic differentiation in variational quantum algorithms. These features make it a key tool for implementing QML and QRL pipelines, yet robust tools for intelligent code assistance in such contexts are still lacking.

_C. Domain Adaptation and RAG in Quantum Programming_

LLM adaptation strategies for quantum domains include both parameter-efficient fine-tuning and retrieval-augmented generation (RAG). While RAG has been used to extend LLM capabilities for dynamic environments like AWS Braket [13], such methods introduce latency and external dependency issues, which limit practical deployment in privacy-sensitive QRL applications.

_PennyLang_ [14], a curated instruction-code dataset for PennyLane, provides the necessary grounding for adapting LLMs to quantum programming tasks, particularly for QML and QRL. It contains natural language prompts and corresponding PennyLane code samples, drawn from documentation, community repositories, and quantum textbooks. This structure enables both direct fine-tuning and retrievalbased augmentation, enhancing LLM accuracy in quantum-specific domains. Its composition is shown in Figure 2.

![](images/p02-01.png)

Data Categories<br>58.3%<br>Uno fficial GitHub repositories<br>w= GitHub (PennyLaneAl + others)<br>39.5% w= Official PennyLane Documentation<br>m= Quantum Computing Books<br>- 0.6%<br>1.6%<br>

Fig. 2. Composition of the _PennyLang_ dataset (3,347 samples).

_D. Comparison of Related Work_

Table I summarizes representative prior works and compares them with PennyCoder across key axes including backend framework, support for QRL/QML, deployment modality, and local inference capability.

TABLE I

COMPARISON OF RELATED WORK ON LLM-BASED QUANTUM CODE GEN

|**Method**|**Year**|**Backend**|**QML**|**QRL**|**Fine-Tuned**|
|---|---|---|---|---|---|
|Codex + Qiskit [7]|2021|Qiskit|✓|✗|✗|
|Qiskit Assistant [11]|2023|Qiskit|✓|✓|✓|
|Braket RAG [13]|2024|Braket|✓|✗|✗|
|PennyLang [14]|2024|PennyLane|✓|✓|✗|
|**PennyCoder (Ours)**|2025|PennyLane|✓|✓|✓|

III. PENNYCODER FRAMEWORK

The _PennyCoder_ framework is designed as a lightweight, domainadapted solution for quantum code generation within the PennyLane ecosystem, with a particular focus on enabling Quantum Reinforcement Learning (QRL) pipelines. Unlike prior cloud-dependent approaches, PennyCoder is optimized for _local and embedded deployment_ , facilitating on-device inference without relying on external APIs (e.g., OpenAI, DeepSeek).

The system is composed of three modules: (1) a domain-specific instruction-response dataset curated from PennyLane programming tasks, (2) a parameter-efficient fine-tuning pipeline based on LowRank Adaptation (LoRA) techniques, and (3) an additional RetrievalAugmented Generation (RAG) module to enhance model robustness for long-tail tasks. Figure 3 illustrates the PennyCoder framework.

## _A. Instruction Tuning with Domain-Specific Data_

We leverage an instruction-response formatted corpus derived from curated PennyLang dataset [14]. Each data point consists of a natural language instruction describing a quantum task, paired with its corresponding PennyLane code implementation. This structure enables effective supervised fine-tuning, improving the model’s ability to map textual quantum programming queries into executable code. The instruction-response format enables fine-tuning using simple supervised loss objectives such as cross-entropy minimization, allowing efficient and stable optimization even with limited computational resources.

- _1) Fine-tuning Configuration_

The fine-tuning was performed using the PennyLang dataset under a parameter-efficient training setup. A learning rate of 1 _×_ 10<sup>_−_6</sup> was used for 2 epochs on a single NVIDIA A100 80GB GPU. Due to limited batch size (1), gradient accumulation with 4 steps was employed. Mixed-precision training (fp16) was enabled to further optimize memory usage and computational efficiency. A maximum input token length of 15,000 was set to accommodate long instruction-code pairs common in QML routines.

- _2) Low-Rank Adaptation (LoRA)_

To support parameter-efficient fine-tuning, we apply LoRA to key transformer layers. Given an attention weight matrix _W ∈_ R<sup>_d×d_</sup> :

_W_<sup>_′_</sup> = _W_ + ∆ _W,_ ∆ _W_ = _AB,_

where _A ∈_ R<sup>_d×r_</sup> and _B ∈_ R<sup>_r×d_</sup> , with _r ≪ d_ .

- In PennyCoder:

- Rank _r_ = 8 was empirically selected.

- LoRA was applied to query and value matrices of self-attention layers.

- A dropout rate of 0.05 was used.

- The AdamW optimizer was used with the same learning rate.

This strategy enables adaptation to QML/QRL tasks without full model retraining, reducing memory cost and enhancing portability to QRL simulation environments and hardware-constrained quantum SDKs.

- _B. Retrieval-Augmented Generation (RAG) for Code Generalization_

While instruction fine-tuning provides a strong inductive bias, longtail QRL scenarios (e.g., dynamic circuit mutation, custom reward functions) benefit from contextual retrieval. We implement a RAG module based on [12], tuned for PennyLang.

The retrieval process proceeds as follows:

- 1) Embed the user query into a dense vector space using an Instructor-Large encoder.

- 2) Retrieve top-_k_ most similar instructions from the PennyLang corpus using cosine similarity in the vector space.

- 3) Concatenate the retrieved instruction-code pairs into the model input context window.

This mechanism improves output consistency in QML/QRL applications where direct instruction supervision is sparse. It complements the foundation model by injecting retrieval content.

PennyCoder combines the strengths of instruction fine-tuning and lightweight parameter-efficient adaptation techniques to deliver a robust, locally deployable LLM solution for PennyLane quantum programming. By addressing both data scarcity and compute constraints, PennyCoder provides a practical path forward for scalable, privacypreserving quantum code generation.

IV. EXPERIMENT SETTINGS

## _A. Dataset_

We use the PennyLang dataset [14] for both instruction fine-tuning and retrieval-augmented generation (RAG). The dataset contains 3,347 curated samples sourced from GitHub repositories, quantum computing textbooks, and the official PennyLane documentation. Each sample was manually verified for accuracy and relevance to quantum programming.

To adapt our model to the quantum domain, we apply instruction fine-tuning (see Section III) using LoRA for parameter-efficient

230

![](images/p03-01.png)

PennyLang Dataset RAG Pipeline Retrieval 2 Test DatasetPennyLang<br>Query<br>Retrieval Code Samples Foundational Model Functionality Incorrect<br>Instructions LLaMa 3.1-8B Instruct Evaluation Correct<br>Augment Samples in Query<br>Code Samples Embeddings<br>h 2 PennyLang<br>1 Domain Specific(Low Rank Fine-tuning Pretrained LLaMA 3.1Weights = 0 LLaMa 3.1-8B InstructFine-tuned Model Temperature ConfigurationsEvaluation Setting Test DatasetFunctionality Incorrect<br>Adaptation) ∈ℝ × = (0, 2) Evaluation Correct<br>Nucleus Sampling<br>x<br>Training Dataset<br>

Fig. 3. Overview of the PennyCoder framework. The PennyLang dataset, structured in an instruction-code format, is used both for direct domain-specific fine-tuning of a foundation model (using Low-Rank Adaptation) and for building a retrieval corpus in the RAG pipeline. During training, fine-tuning adapts a LLaMA 3.1-8B model to PennyLane quantum programming tasks. During evaluation, the system supports both direct generation and RAG to enhance few-shot generalization. Generated outputs are evaluated for functional correctness against the PennyLang test set, using controlled decoding settings such as temperature scaling and nucleus (top-_p_ ) sampling.

training. Each example is augmented with high-quality instructions generated by LLMs to contextualize the task and guide model behavior. This process enhances output relevance and accuracy in quantum-specific coding scenarios.

## _B. Benchmark and Metrics_

To evaluate PennyCoder, we created a custom benchmark comprising of 264 tasks for PennyLane code generation inspired by the Qiskit HumanEval benchmark [20], covering a range of difficulty levels and quantum topics such as circuit construction, algorithm implementation, variational quantum eigensolvers, and quantum machine learning. Tasks are drawn from prior competitions and categorized into foundational and advanced application domains.

![](images/p03-02.png)

Quantum Benchmark Task Distribution<br>Basic quantum circuits 109<br>Quantum machine learning 67<br>& Quantum Reinforcement learning<br>Quantum chemistry & simulation 40<br>Quantum protocols 37<br>Quantum algorithms 8<br>Compilation & noise simulation 3<br>0 15 30 45 60 75 90 105<br>Number of Tasks<br>

Fig. 4. Distribution of benchmark tasks across quantum programming categories. Basic circuits represent the largest share (41%). Each task is assigned to its most relevant category.

To measure performance, we use _Pass@k_ metrics, evaluating syntactic validity and functional correctness across _k_ = 1 _,_ 3 _,_ 5 model completions. This accounts for output variability and assesses the probability of generating a correct solution within _k_ attempts. All outputs are manually verified to ensure reliable evaluation.

_C. Implementation Details_

Our experiments use LLaMA 3.1 8B [25] as the base model. To explore decoding dynamics, we conduct a grid search over temperature and nucleus sampling (top-_p_ ) with values _{_ 0 _,_ 0 _._ 5 _,_ 1 _._ 0 _}_ . This analysis reveals the impact of generation hyperparameters on output determinism and creativity, informing optimal deployment configurations.

## V. RESULTS

## _A. PennyCoder Evaluation_

Table II presents a comparative evaluation of PennyCoder, which employs our proposed PennyCoder, against two baseline approaches: the base LLaMA model and LLaMA with RAG.

PennyCoder demonstrates substantial improvements over the base LLaMA model. With 117 successes versus LLaMA’s 89 (a 31.5% increase), PennyCoder significantly reduces failures from 175 to 147 (a 16% reduction). This performance boost translates to an accuracy improvement from 33.71% to 44.32%, representing an absolute gain

of 10.61 percentage points. When compared to the RAG-enhanced baseline, PennyCoder maintains its superiority. While LLaMA + RAG achieves 106 successes and 40.15% accuracy, PennyCoder surpasses it with 11 additional successes and a 4.17 percentage point accuracy increase.

These results establish PennyCoder as an effective approach among the three configurations. By achieving consistent performance gains across all metrics without requiring external retrieval mechanisms, our method demonstrates that low-rank adaptation fine-tuning successfully enhances model capabilities in the quantum computing domain.

TABLE II

PERFORMANCE OF PENNYCODER (WITH T=0.5 AND TOP <u>P=0.5)</u> COMPARED WITH OUR BASELINES.

||**PennyCoder (Ours)**|**LLaMA**|**LLaMA + RAG**|
|---|---|---|---|
|**Success**|117|89|106|
|**Failed**<br>|147<br>|175<br>|158<br>|
|**Accuracy** (%)|**44.32**|33.71|40.15|

_B. Category-wise Performance_

Figure 5 reveals variable performance across quantum computing categories. In Basic Quantum Circuits, the largest test set with 109 cases, the model achieved moderate proficiency with 52 successes against 57 failures. Similarly, in Quantum Machine Learning (67 cases), the model struggled with complex applications, producing only 26 successful outcomes versus 41 failures.

Performance declined further in specialized domains. Quantum Protocols showed limited success with 13 passes out of 37 tests, while Quantum Chemistry and Simulation yielded 17 successes from 40 tests. The Quantum Algorithms category, though smallest at 8 cases, resulted in an even split of 4 successes and 4 failures. Most concerning, PennyCoder failed all 3 Compilation and Noise Simulation tests, indicating no capability in hardware-level or noiseaware tasks.

Accuracy metrics show in Figure 5 reinforce these patterns. While the model achieved 50% accuracy in algorithms (limited sample size), it performed relatively well in basic circuits at 47.71%. Performance decreased progressively in chemistry and simulation (42.5%), machine learning (38.81%), and protocols (35.14%), with compilation and noise simulation at 0%.

These results suggest PennyCoder’s strengths lie in basic circuit construction and algorithmic reasoning, while significant challenges emerge in complex and specialized domains. The inaccuracies in the noise simulation suggest that dedicated adjustments are required to improve the performance for this category. Moving forward, both enhanced training protocols and architectural improvements will be essential to address these domain-specific quantum computing challenges.

231

![](images/p04-01.png)

Performance by Category<br>QML & QRL 50.0%<br>Circuits 47.7%<br>Chem+Sim 42.5%<br>Protocols 38.8%<br>Algorithms 35.1%<br>Comp+HW 0.0%<br>0 10 20 30 40 50<br>Accuracy (%)<br>Average (Active): 42.8% | Range: 35.1% 50.0%<br>Above Avg: 2/5 | Gap: 14.9%<br>

Fig. 5. Category-wised accuracy analysis. Explanation of task category abbreviation: Circuits=Basic quantum circuits; Comp+HW=Compilation, noise simulation & hardware mapping; Algorithms=Quantum algorithms, QML&QRL; Chem+Sim=Quantum chemistry & simulation; Protocols=Quantum protocols.

## _C. Impact of Temperature and Nucleus Sampling Values_

Table III summarizes the pass rate across different temperature ( _T_ ) and nucleus sampling (top-_p_ ) configurations. For _T_ = 0, the pass rate remained consistent at approximately 42.42% across top-_p_ values, with a slight improvement to 43.18% when top-_p_ = 1 _._ 0. When setting _T_ = 0 _._ 5, the model achieved its highest accuracy of 44.32% at top-_p_ = 0 _._ 5, suggesting that moderate randomness in generation improves model output. However, at _T_ = 0 _._ 5 and top-_p_ = 1 _._ 0, performance dropped to 37.88%, indicating that excessive sampling diversity can negatively impact generation quality. Notably, setting _T_ = 1 resulted in a consistent decline in accuracy—38.64%, 33.33%, and 5.68% for top-_p_ = 0 _._ 0, 0 _._ 5, and 1 _._ 0 respectively—reinforcing the notion that high temperature without proper sampling control leads to unstable and degraded model behavior. These results underscore the importance of fine-tuning decoding parameters, with _T_ = 0 _._ 5 and top-_p_ = 0 _._ 5 standing out as the most effective combination for maximizing performance.

TABLE III

PASS RATE OF DIFFERENT HYPERPARAMETER SETUP _{_ T=[0, 0.5, 1];

|||T|OP<br>P=[|0, 0.5,|1]_}_|||||
|---|---|---|---|---|---|---|---|---|---|
|||**T=0**|||**T=0.5**|||**T=1**||
|**top**<br>**p**|**0.0**|**0.5**|**1.0**|**0.0**|**0.5**|**1.0**|**0.0**|**0.5**|**1.0**|
|**Success**|112|112|114|112|**117**|100|102|88|15|
|**Failed**|152|152|150|152|**147**|164|162|176|249|
|**Accuracy (%)**|42.42|42.42|43.18|42.42|**44.32**|37.88|38.64|33.33|5.68|

VI. DISCUSSION

_A. Case Study I: PennyCoder vs. Foundation Model vs. RAG_

The task is to construct a QRL agent using a two-qubit parameterized circuit to choose between left or right in a 1D environment.

## PennyCoder Output

**Limitations Identified:**

- No state encoding in the quantum circuit.

- No environment interaction loop.

- Manual parameter updates without gradients.

- Limited learning mechanism.

1 <mark>import pennylane as qml</mark> 2 <mark>from pennylane import numpy as np</mark> 3 <mark>import torch</mark> 4 <mark>class QRLAgent:</mark> 5 <mark>def __init__(self):</mark> 6 <mark>self.device = qml.device(’default.qubit ’, wires =2)</mark> 7 <mark>self.circuit = qml.QNode(self._circuit , self.device)</mark> 8 <mark>self.params = qml.numpy.array ([0.1 , 0.1])</mark> 9 <mark>def _circuit(self , weights):</mark> 10 <mark>qml.RX(weights [0], wires =0)</mark> 11 <mark>qml.RX(weights [1], wires =1)</mark> 12 <mark>qml.CNOT(wires=[0, 1])</mark>

![](images/p04-02.png)

13 qml.RY(weights [0], wires =0)<br>14 qml.RY(weights [1], wires =1)<br>15 return qml.expval(qml.PauliZ (0))<br>16 def act(self , state):<br>17 prob = self.circuit(self.params)<br>18 if prob > 0.5:<br>19 return 1<br>20 else:<br>21 return 0<br>22 def update(self , reward , next_state):<br>23 # update the parameters using a simple<br>gradient descent<br>24 loss = (reward + 1) * (self.act(next_state)<br>- 0.5)<br>25 self.params -= 0.1 * loss<br>26 # example usage<br>27 agent = QRLAgent ()<br>28 state = 0<br>29 reward = 1<br>30 next_state = 1<br>31 agent.update(reward , next_state)<br>32 print(agent.act(state)) # prints 0 or 1 depending<br>on the updated parameters<br>

![](images/p04-03.png)

Listing 1. PennyCoder Implementation<br>

**Description:** The agent meets the basic requirements but lacks dynamic state encoding, proper reinforcement learning feedback, and gradient-based optimization, which limits its effectiveness in real QRL scenarios.

## LLaMA 3.1-8B Foundational Model (Wrong Output)

![](images/p04-04.png)

Limitations Identified:<br>

- No training mechanism or weight optimization.

- State is not encoded into the quantum circuit.

- Actions are selected randomly.

![](images/p04-05.png)

• Circuit output is not used to guide learning.<br>1 import gym<br>2 @qml.qnode(qml.device (" default.qubit", wires =2))<br>3 def circuit(params):<br>4 qml.RX(params [0], wires =0)<br>5 qml.RY(params [1], wires =0)<br>6 qml.RZ(params [2], wires =0)<br>7 qml.RX(params [3], wires =1)<br>8 qml.RY(params [4], wires =1)<br>9 qml.RZ(params [5], wires =1)<br>10 qml.CNOT(wires=[0, 1])<br>11 return qml.expval(qml.PauliZ(wires =1))<br>12 class QRLAgent:<br>13 def __init__(self , env , device):<br>14 self.env = env<br>15 self.device = device<br>16 self.params = [qml.numpy.array ([0.1]*6)]<br>17 self.qnode = qml.qnode(device ,<br>circuit=circuit)<br>18 def act(self):<br>19 self.qnode(self.params)<br>20 prob_left =<br>qml.math.probability(self.qnode , 0)<br>21 prob_right =<br>qml.math.probability(self.qnode , 1)<br>22 if prob_left > prob_right:<br>23 return 0<br>24 else:<br>25 return 1<br>26 def update(self , reward , new_state):<br>27 self.params = qml.math.adam(self.params ,<br>reward , lr =0.01)<br>28 env = gym.make(’CartPole -v1 ’)<br>29 device = qml.device (" default.qubit", wires =2)<br>30 agent = QRLAgent(env , device)<br>31 for episode in range (10):<br>32 state = env.reset ()<br>33 done = False<br>34 while not done:<br>35 action = agent.act()<br>36 new_state , reward , done , _ =<br>env.step(action)<br>37 agent.update(reward , new_state)<br>38 env.render () # Render the environment<br>39 print(f’Episode: {episode}, Reward: {reward}’)<br># Print the reward for each episode<br>

### Listing 2. LLaMA 3.1-8B Implementation (Baseline)

**Description:** Attempts to do the task, but the implementation lacks essential components such as learning dynamics, state encoding, and parameter updates, limiting its effectiveness in reinforcement learning tasks.

232

## LLaMA 3.1-8B + RAG (Wrong Output)

#### Limitations Identified:

   - No training or weight update mechanism.

   - The circuit output overwrites the parameter tensor.

   - State is not encoded into the quantum circuit.

   - Random action selection without policy guidance.

- 1 <mark>import pennylane as qml</mark>

- 2 <mark>from pennylane import numpy as np</mark>

- 3 <mark>import torch</mark>

- 4 <mark># Define the QRL agent</mark>

5 <mark>class QRLAgent:</mark> 6 <mark>def __init__(self , device , num_qubits , num_layers):</mark> 7 <mark>self.device = device</mark> 8 <mark>self.num_qubits = num_qubits</mark> 9 <mark>self.num_layers = num_layers</mark> 10 <mark>self.circuit = self._create_circuit ()</mark> 11 <mark>def _create_circuit(self):</mark> 12 <mark># Define the QRL circuit</mark> 13 <mark>@qml.qnode(self.device)</mark> 14 <mark>def circuit(weights , action):</mark> 15 <mark># Apply a parameterized circuit to choose between left or right</mark> 16 <mark>for i in range(self.num_layers):</mark> 17 <mark>qml.RX(weights [2 * i], wires =0)</mark> 18 <mark>qml.RX(weights [2 * i + 1], wires =1)</mark> 19 <mark>qml.CNOT(wires=[0, 1])</mark> 20 <mark>if action == 0: # Left</mark> 21 <mark>qml.RX(np.pi, wires =0)</mark> 22 <mark>else: # Right</mark> 23 <mark>qml.RX(-np.pi , wires =0)</mark> 24 <mark>return qml.expval(qml.PauliZ (0))</mark> 25 <mark>return circuit</mark> 26 <mark>def choose_action(self , weights , action):</mark> 27 <mark># Choose between left or right using the QRL circuit</mark> 28 <mark>return self.circuit(weights , action)</mark>

- 29 <mark># Create a QRL agent</mark>

30 <mark>device = qml.device (" default.qubit", wires =2)</mark> 31 <mark>num_qubits = 2</mark> 32 <mark>num_layers = 2</mark>

- 33 <mark>agent = QRLAgent(device , num_qubits , num_layers)</mark>

- 34 <mark># Define the environment</mark>

35 <mark>class Environment:</mark> 36 <mark>def __init__(self):</mark> 37 <mark>self.state = 0</mark> 38 <mark>def step(self , action):</mark> 39 <mark># Update the environment state based on the action</mark> 40 <mark>if action == 0: # Left</mark> 41 <mark>self.state -= 1</mark> 42 <mark>else: # Right</mark> 43 <mark>self.state += 1</mark> 44 <mark>return self.state</mark>

- 45 <mark># Create an environment</mark>

- 46 <mark>env = Environment ()</mark>

47 <mark># Train the QRL agent</mark> 48 <mark>weights = torch.randn (4)</mark>

49 <mark>for i in range (100):</mark> 50 <mark>action = 0 if np.random.rand() < 0.5 else 1</mark> 51 <mark>state = env.step(action)</mark> 52 <mark>reward = 1 if state == 0 else -1</mark>

53 <mark>weights = agent.choose_action(weights , action)</mark> 54 <mark>print(f"Iteration {i+1}, Action: {action}, Reward: {reward }")</mark>

5 <mark>Use a Bell state preparation and additional gates if necessary. Return the QNode ."""</mark> 6 7 <mark>@qml.qnode(qml.device(’default.qubit ’, wires =2))</mark> 8 <mark>def circuit ():</mark> 9 <mark>qml.Hadamard(wires =0)</mark> 10 <mark>qml.CNOT(wires=[0, 1])</mark> 11 <mark>return qml.state ()</mark> 12 13 <mark>return circuit</mark> 14 15 <mark># Example usage</mark> 16 <mark>circuit = superdense_coding_circuit ()</mark> 17 <mark>print(circuit ())</mark>

Listing 4. PennyCoder Implementation

**Description:** Creates a minimal two-qubit Bell-state circuit suitable for super-dense coding protocols. The function returns a ready-to-use QNode that outputs the full quantum state.

## LLaMA 3.1-8B Foundational Model (Compilation Errors)

#### Limitations Identified:

- Introduces unused classical arguments x, y

- Calls qml.PauliX(...).control(1) – unsupported syntax

- Multiple redundant single-qubit PauliX gates

- Returns qml.state() but gradient parameters are unused

1 <mark>import pennylane as qml</mark> 2

- 3 <mark>def superdense_coding_circuit ():</mark> 4 <mark>""" Design a circuit that prepares a state suitable for superdense coding. Use a Bell state preparation and additional gates if necessary. Return the QNode ."""</mark>

5 6 <mark># Define the QNode</mark>

- 7 <mark>@qml.qnode(qml.device (" default.qubit", wires =2))</mark> 8 <mark>def circuit(x, y):</mark>

- 9 <mark># Apply Hadamard gate to the first qubit</mark>

- 10 <mark>qml.Hadamard(wires =0)</mark>

11 <mark># Apply Pauli -X gate to the first qubit</mark> 12 <mark>qml.PauliX(wires =0)</mark> 13 <mark># Apply CNOT gate to the first and second qubits</mark> 14 <mark>qml.CNOT(wires=[0, 1])</mark> 15 <mark># Apply Pauli -X gate to the second qubit</mark> 16 <mark>qml.PauliX(wires =1)</mark> 17 <mark># Apply Pauli -X gate to the second qubit conditioned on the first qubit</mark> 18 <mark>qml.PauliX(wires =1).control (1)(wires =[0, 1])</mark> 19 <mark>return qml.state ()</mark> 20 21 <mark>return circuit</mark> 22 23 <mark># Example usage</mark>

24 <mark>circuit = superdense_coding_circuit ()</mark> 25 <mark>print(circuit(0, 0))</mark>

Listing 5. LLaMA 3.1-8B Implementation (Baseline)

**Description:** Attempts to extend the Bell-state circuit but introduces unsupported controlled operations and unused parameters, leading to runtime errors when executed.

Listing 3. LLaMA 3.1-8B + RAG Implementation (Partial)

**Description:** Attempts to do the task, but, the lack of state encoding, absence of a learning mechanism, and incorrect handling of circuit output limit the agent’s ability to learn or adapt over time.

## LLaMA 3.1-8B + RAG (Compilation Errors)

#### Limitations Identified:

- Tries to prepare basis state **outside** a QNode context

_B. Case Study II: PennyCoder vs. Foundation Model vs. RAG_

The task is to create a quantum circuit that prepares a state for superdense coding, and provide it as a QNode.

- Returns a bare qml.qnode object without a wrapped function

- Example call circuit() fails because no circuit body exists

1 <mark>import pennylane as qml</mark>

- 2 <mark>from pennylane import numpy as np</mark>

## PennyCoder Output (Working)

#### Limitations Identified:

   - Uses the default simulator; no hardware optimisation

- Returns the full state vector (may be large for bigger systems)

- 1 <mark>import pennylane as qml</mark> 2 3 <mark>def superdense_coding_circuit ():</mark> 4 <mark>""" Design a circuit that prepares a state suitable for superdense coding.</mark>

3

- 4 <mark>def superdense_coding_circuit ():</mark> 5 <mark>""" Design a circuit that prepares a state suitable for superdense coding. Use a Bell state preparation and additional gates if necessary. Return the QNode ."""</mark>

6 7 <mark># Prepare the Bell state</mark> 8 <mark>qml.BasisState ([0, 1], wires =[0, 1])</mark> 9 10 <mark># Apply a Hadamard gate to the first qubit</mark> 11 <mark>qml.Hadamard(wires =0)</mark>

233

![](images/p06-01.png)

12<br>13 # Apply a Pauli -X gate to the second qubit<br>14 qml.PauliX(wires =1)<br>15<br>16 # Return the QNode<br>17 return qml.qnode(qml.device (" default.qubit",<br>wires =2))<br>18<br>19 # Example usage<br>20 circuit = superdense_coding_circuit ()<br>21 print(circuit ())<br>Listing 6. LLaMA 3.1-8B + RAG Implementation (Partial)<br>Description: Moves towards using PennyLane primitives but places gate<br>operations outside any QNode scope and returns an uninitialised qnode,<br>causing errors when invoked.<br>

_C. Limitation and Future Work_

While PennyCoder demonstrates promising results in LLM-aided quantum code generation through domain-adaptive model fine-tuning, several key challenges remain within our current framework. First, our training dataset comprises only 3,000 samples, raising questions about potential improvements through data augmentation or enhanced instruction generation for specific scenarios. Could expanding the dataset or refining instruction templates lead to better performance?

Second, our experiments utilize LLaMA 3.1 8B as the foundation model. As state-of-the-art language models continue to evolve, it would be valuable to evaluate how newer architectures perform within the PennyCoder framework. Given that many modern inference models, including OpenAI o3 [26], Claude 3.7 [27], and DeepSeek R1 [28], incorporate Chain-of-Thought reasoning, future work should explore how to enhance both the output quality and reasoning capabilities of these models when integrated with PennyCoder.

Based on these limitations, future work on the PennyCoder framework should focus on two key directions. First, advanced data augmentation techniques to address the constraints of limited training data availability can be explored. Second, following work can enhance the model’s output quality and evaluation capabilities by incorporating agentic techniques, such as conversational feedback mechanisms and tool usage integration. These approaches will enable more sophisticated automated evaluation while improving the model’s practical utility in quantum code generation.

## VII. CONCLUSION

In this work, we presented _PennyCoder_ , a lightweight and efficient framework for PennyLane-based quantum code generation. By finetuning a foundation model using Low-Rank Adaptation (LoRA) techniques and leveraging domain-specific instruction datasets, PennyCoder achieves significant improvements in functional correctness compared to both standard foundation models and retrievalaugmented methods. Our model maintains competitive accuracy while being deployable locally, thus addressing critical challenges of latency, privacy, and deployment feasibility often associated with remote API-based solutions.

Our experiments highlight that fine-tuning alone, when carefully applied, can outperform RAG-augmented approaches without the need for complex retrieval pipelines. Additionally, we demonstrate that careful calibration of generation hyperparameters (temperature and nucleus sampling) can further boost the success rate of quantum code generation.

Future work will focus on expanding PennyCoder’s capabilities for advanced quantum hardware-aware tasks, incorporating noise models, and enabling broader support for hybrid classical-quantum workflows. We believe PennyCoder represents an important step toward building scalable, private, and robust LLM-based quantum programming assistants.

## ACKNOWLEDGMENT

This work was supported in part by the NYUAD Center for Quantum and Topological Systems (CQTS), funded by Tamkeen under the NYUAD Research Institute grant CG008, the NYUAD Center for CyberSecurity (CCS), funded by Tamkeen under the NYUAD Research Institute Award G1104, and the NYUAD High Performance

Computing (HPC) center for providing necessary compute resources for the experiments.

## REFERENCES

- [1] G. Q. A. Team, “Google ai quantum team unveils the willow processor,” https://blog.google/technology/ai/google-quantum-willow-processor-a nnouncement/, accessed: 2025-04-22.

- [2] I. Q. Team, “Ibm quantum roadmap: Building toward condor and beyond,” https://research.ibm.com/blog/ibm-quantum-condor-roadmap, accessed: 2025-04-22.

- [3] M. Q. Team, “Microsoft demonstrates majorana-based qubits with majorana 1,” https://cloudblogs.microsoft.com/quantum/2024/01/2 4/majorana-1-breakthrough/, accessed: 2025-04-22.

- [4] V. Bergholm, J. Izaac, M. Schuld, C. Gogolin, and N. Killoran, “Pennylane: Automatic differentiation of hybrid quantum-classical computations,” _arXiv preprint arXiv:1811.04968_ , 2018.

- [5] K. Zaman, A. Marchisio, M. A. Hanif, and M. Shafique, “A survey on quantum machine learning: Current trends, challenges, opportunities, and the road ahead,” _arXiv preprint arXiv:2310.10315_ , 2023.

- [6] A. Alomari and S. A. Kumar, “A survey of quantum reinforcement learning approaches: Current status and future research directions,” in _2025 IEEE Conference on Artificial Intelligence (CAI)_ . IEEE, 2025, pp. 1375–1382.

- [7] M. Chen, J. Tworek, H. Jun, Q. Yuan _et al._ , “Evaluating large language models trained on code,” _arXiv preprint_ , vol. arXiv:2107.03374, 2021. [Online]. Available: https://arxiv.org/abs/2107.03374

- [8] R. Chakraborty _et al._ , “Hardwaregpt: A domain-specific foundation model for hardware design,” _arXiv preprint arXiv:2309.04829_ , 2023.

- [9] N. Shinn _et al._ , “Reflexion: Language agents with verbal reinforcement learning,” _arXiv preprint arXiv:2303.11366_ , 2023.

- [10] A. Ramesh, P. Dhariwal, A. Nichol, C. Chu, and M. Chen, “Hierarchical text-conditional image generation with clip latents,” 2022.

- [11] N. Dupuis, L. Buratti, S. Vishwakarma _et al._ , “Qiskit code assistant: Training llms for generating quantum computing code,” 2024.

- [12] P. Lewis, E. Perez, A. Piktus _et al._ , “Retrieval-augmented generation for knowledge-intensive nlp tasks,” _arXiv preprint arXiv:2005.11401_ , 2020.

- [13] Y. Kharkov, Z. Mohammad, M. Beach, and E. Kessler, “Accelerate quantum software development on amazon braket with claude-3,” AWS Quantum Technologies Blog (18 Sep 2024), uRL: https://aws.amazon.c om/blogs/quantum-computing/accelerate-quantum-software-developme nt-on-amazon-braket-with-claude-3/.

- [14] A. Basit _et al._ , “Pennylang: Pioneering llm-based quantum code generation with a novel pennylane-centric dataset,” _arXiv:2503.02497_ , 2025.

- [15] R. Li, A. Q. Jiang, C. Qian _et al._ , “Starcoder: May the source be with you!” _arXiv preprint arXiv:2305.06161_ , 2023.

- [16] IBM-Granite, “granite-8b-code-base-4k,” 2023.

- [17] J. Austin _et al._ , “Program synthesis with large language models,” _arXiv preprint arXiv:2108.07732_ , 2021.

- [18] L. Watson, “QHack 2022 - the one-of-a-kind celebration of quantum computing,” PennyLane Blog (Mar 28, 2022), uRL: https://pennylane. ai/blog/2022/03/qhack-2022-the-one-of-a-kind-celebration-of-quantum -computing.

- [19] D. G. Almeida, J. Cruz-Benito, and R. Davis, “Introducing qiskit code assistant,” IBM Quantum Computing Blog (Oct 9, 2024), uRL: https: //www.ibm.com/quantum/blog/qiskit-code-assistant.

- [20] S. Vishwakarma, F. Harkins, S. Golecha, V. S. Bajpe, N. Dupuis, L. Buratti, D. Kremer, I. Faro, R. Puri, and J. Cruz-Benito, “Qiskit HumanEval: An Evaluation Benchmark for Quantum Code Generative Models,” _arXiv preprint arXiv:2406.14712_ , 2024.

- [21] A. Basit, M. Shao, H. Asif, N. Innan, M. Kashif, A. Marchisio, and M. Shafique, “Qhackbench: Benchmarking large language models for quantum code generation using pennylane hackathon challenges,” _arXiv preprint arXiv:2506.20008_ , 2025.

- [22] S. Y.-C. Chen, “An introduction to quantum reinforcement learning (qrl),” in _ICTC_ , 2024.

- [23] S. Jerbi, J. Gibbs, M. S. Rudolph, M. C. Caro, P. J. Coles, H.-Y. Huang, and Z. Holmes, “The power and limitations of learning quantum dynamics incoherently,” 2023.

- [24] S. Y.-C. Chen, S. Yoo, and Y.-L. L. Fang, “Quantum long short-term memory,” in _ICASSP_ , 2022.

- [25] Meta, “Introducing Llama 3.1: Our most capable models to date,” 2024, accessed: 2025-06-27. [Online]. Available: https://ai.meta.com/bl og/meta-llama-3-1/

- [26] OpenAI, “OpenAI O3 Mini,” 2024, accessed: 2025-06-21. [Online]. Available: https://openai.com/index/openai-o3-mini/

- [27] Anthropic, “Claude 3.7 Sonnet and Claude Code,” 2025, accessed: 2025-04-21. [Online]. Available: https://www.anthropic.com/news/claud e-3-7-sonnet

- [28] DeepSeek-AI, “Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning,” 2025.

234
