1

# Software Testing with Large Language Models: Survey, Landscape, and Vision

Junjie Wang, Yuchao Huang, Chunyang Chen, Zhe Liu, Song Wang, Qing Wang

**Abstract** —Pre-trained large language models (LLMs) have recently emerged as a breakthrough technology in natural language processing and artificial intelligence, with the ability to handle large-scale datasets and exhibit remarkable performance across a wide range of tasks. Meanwhile, software testing is a crucial undertaking that serves as a cornerstone for ensuring the quality and reliability of software products. As the scope and complexity of software systems continue to grow, the need for more effective software testing techniques becomes increasingly urgent, making it an area ripe for innovative approaches such as the use of LLMs. This paper provides a comprehensive review of the utilization of LLMs in software testing. It analyzes 102 relevant studies that have used LLMs for software testing, from both the software testing and LLMs perspectives. The paper presents a detailed discussion of the software testing tasks for which LLMs are commonly used, among which test case preparation and program repair are the most representative. It also analyzes the commonly used LLMs, the types of prompt engineering that are employed, as well as the accompanied techniques with these LLMs. It also summarizes the key challenges and potential opportunities in this direction. This work can serve as a roadmap for future research in this area, highlighting potential avenues for exploration, and identifying gaps in our current understanding of the use of LLMs in software testing.

**Index Terms** —Pre-trained Large Language Model, Software Testing, LLM, GPT

✦

## 1 INTRODUCTION

Software testing is a crucial undertaking that serves as a cornerstone for ensuring the quality and reliability of software products. Without the rigorous process of software testing, software enterprises would be reluctant to release their products into the market, knowing the potential consequences of delivering flawed software to end-users. By conducting thorough and meticulous testing procedures, software enterprises can minimize the occurrence of critical software failures, usability issues, or security breaches that could potentially lead to financial losses or jeopardize user trust. Additionally, software testing helps to reduce maintenance costs by identifying and resolving issues early in the development lifecycle, preventing more significant complications down the line [1], [2].

The significance of software testing has garnered substantial attention within the research and industrial communities. In the field of software engineering, it stands as an immensely popular and vibrant research area. One can observe the undeniable prominence of software testing by simply examining the landscape of conferences and symposiums focused on software engineering. Amongst these events, topics related to software testing consistently dominate the submission numbers and are frequently selected for publication.

- _J. Wang,Y. Huang, Z. Liu, Q. Wang are with State Key Laboratory of Intelligent Game, Institute of Software Chinese Academy of Sciences, and University of Chinese Academy of Sciences, Beijing, China. J. Wang and Q. Wang are corresponding authors._

   - _E-mail: {junjie, yuchao2019, liuzhe2020, wq}@iscas.ac.cn_

- _C. Chen is with Monash University, Melbourne, Australia_

While the field of software testing has gained significant popularity, there remain dozens of challenges that have not been effectively addressed. For example, one such challenge is automated unit test case generation. Although various approaches, including search-based [3], [4], constraintbased [5] or random-based [6] techniques to generate a suite of unit tests, the coverage and the meaningfulness of the generated tests are still far from satisfactory [7], [8]. Similarly, when it comes to mobile GUI testing, existing studies with random-/rule-based methods [9], [10], model-based methods [11], [12], and learning-based methods [13] are unable to understand the semantic information of the GUI page and often fall short in achieving comprehensive coverage [14], [15]. Considering these limitations, numerous research efforts are currently underway to explore innovative techniques that can enhance the efficacy of software testing tasks, among which large language models are the most promising ones.

Large language models (LLMs) such as T5 and GPT-3 have revolutionized the field of natural language processing (NLP) and artificial intelligence (AI). These models, initially pre-trained on extensive corpora, have exhibited remarkable performance across a wide range of NLP tasks including question-answering, machine translation, and text generation [16]–[19]. In recent years, there has been a significant advancement in LLMs with the emergence of models capable of handling even larger-scale datasets. This expansion in model size has not only led to improved performance but also opened up new possibilities for applying LLMs as Artificial General Intelligence. Among these advanced LLMs, models like ChatGPT<sup>1</sup> and LLaMA<sup>2</sup> boast billions

   - _E-mail: chunyang.chen@monash.edu_

- _S. Wang is with York University, Toronto, Canada. E-mail: wangsong@yorku.ca_

1. https://openai.com/blog/chatgpt

> 2. https://ai.meta.com/blog/large-language-model-llama-meta-ai/

2

of parameters. Such models hold tremendous potential for tackling complex practical tasks in domains like code generation and artistic creation. With their expanded capacity and enhanced capabilities, LLMs have become game-changers in NLP and AI, and are driving advancements in other fields like coding and software testing.

LLMs have been used for various coding-related tasks including code generation and code recommendation [20]– [23]. On one hand, in software testing, there are many tasks related to code generation, such as unit test generation [7], where the utilization of LLMs is expected to yield good performance. On the other hand, software testing possesses unique characteristics that differentiate it from code generation. For example, code generation primarily focuses on producing a single, correct code snippet, whereas software testing often requires generating diverse test inputs to ensure better coverage of the software under test [1]. The existence of these differences introduces new challenges and opportunities when employing LLMs for software testing. Moreover, people have benefited from the excellent performance of LLMs in generation and inference tasks, leading to the emergence of dozens of new practices that use LLMs for software testing.

This article presents a comprehensive review of the utilization of LLMs in software testing. We collect 102 relevant papers and conduct a thorough analysis from both software testing and LLMs perspectives, as roughly summarized in Figure 1.

From the viewpoint of software testing, our analysis involves an examination of the specific software testing tasks for which LLMs are employed. Results show that LLMs are commonly used for test case preparation (including unit test case generation, test oracle generation, and system test input generation), program debugging, and bug repair, while we do not find the practices for applying LLMs in the tasks of early testing life-cycle (such as test requirement, test plan, etc). For each test task, we would provide detailed illustrations showcasing the utilization of LLMs in addressing the task, highlighting commonly-used practices, tracking technology evolution trends, and summarizing achieved performance, so as to facilitate readers in gaining a thorough overview of how LLMs are employed across various testing tasks.

From the viewpoint of LLMs, our analysis includes the commonly used LLMs in these studies, the types of prompt engineering, the input of the LLMs, as well as the accompanied techniques with these LLMs. Results show that about one-third of the studies utilize the LLMs through pre-training or fine-tuning schema, while the others employ prompt engineering to communicate with LLMs to steer their behavior for desired outcomes. For prompt engineering, the zero-shot learning and few-shot learning strategies are most commonly used, while other advances like chain-of-thought promoting and self-consistency are rarely utilized. Results also show that traditional testing techniques like differential testing and mutation testing are usually accompanied by LLMs to help generate more diversified tests.

Furthermore, we summarize the key challenges and potential opportunities in this direction. Although software testing with LLMs has undergone significant growth in the

![](images/p02-01.png)

+ Unit test case generation (20)<br>Testing || TestSystemoracle test Inputgeneration generation(4) (22)<br>“view oe Bug analysis (7)<br>(sec.4) Debug (13)<br>+ Repair (38) + ChatGPT (36)<br>+ Codex (23)<br>Waysorganizingof ,| SLIM models +++ GPT-4CodeTS (14)(18)<br>collected Fe cpT3(7)<br>studies —# Others<br>+ Zero-shot learning (51)<br>ww [atTypes of prompt 1++ Chain-of-thoughtFew-shot learning (7)(25)<br>o view o| |—& Selr-consistency (1)<br>pegs —+ AutamatcN/A ie. Pre-training prom (1<br>and/or fine-tuning) (38)<br>+ Code (78)<br>input of LLM + BU description 12)<br>—— Error information (7)<br>Ls others<br>Incorporating ++ +PureStatisticLLM (67)analysis (10)<br>other tech + Program analysis (9)<br>wih LLM | + Mutation testing (7)<br>+ + Syntactic repair (6)<br>+ + Differential testing (5)<br>+ + Others<br>

Fig. 1: Structure of the contents in this paper (the numbers in bracket indicates the number of involved papers, and a paper might involve zero or multiple items)

past two years, there are still challenges in achieving high coverage of the testing, test oracle problem, rigorous evaluations, and real-world application of LLMs in software testing. Since it is a new emerging field, there are many research opportunities, including exploring LLMs in an early stage of testing, exploring LLMs for more types of software and nonfunctional testing, exploring advanced prompt engineering, as well as incorporating LLMs with traditional techniques.

This paper makes the following contributions:

- We thoroughly analyze 102 relevant studies that used LLMs for software testing, regarding publication trends, distribution of publication venues, etc.

- We conduct a comprehensive analysis from the perspective of software testing to understand the distribution of software testing tasks with LLM and present a thorough discussion about how these tasks are solved with LLM.

- We conduct a comprehensive analysis from the perspective of LLMs, and uncover the commonly-used LLMs, the types of prompt engineering, input of the LLMs, as well as the accompanied techniques with these LLMs.

- We highlight the challenges in existing studies and present potential opportunities for further studies.

We believe that this work will be valuable to both researchers and practitioners in the field of software engineering, as it provides a comprehensive overview of the current state and future vision of using LLMs for software testing. For researchers, this work can serve as a roadmap for future research in this area, highlighting potential avenues for exploration and identifying gaps in our current understanding of the use of LLMs in software testing. For practitioners, this work can provide insights into the potential benefits and limitations of using LLMs for software testing, as well as practical guidance on how to effectively integrate them into

3

existing testing processes. By providing a detailed landscape of the current state and future vision of using LLMs for software testing, this work can help accelerate the adoption of this technology in the software engineering community and ultimately contribute to improving the quality and reliability of software systems.

## 2 BACKGROUND

### 2.1 Large Language Model (LLM)

Recently, pre-trained language models (PLMs) have been proposed by pretraining Transformer-based models over large-scale corpora, showing strong capabilities in solving various natural language processing (NLP) tasks [16]–[19]. Studies have shown that model scaling can lead to improved model capacity, prompting researchers to investigate the scaling effect through further parameter size increases. Interestingly, when the parameter scale exceeds a certain threshold, these larger language models demonstrate not only significant performance improvements but also special abilities such as in-context learning, which are absent in smaller models such as BERT.

To discriminate the language models in different parameter scales, the research community has coined the term large language models (LLM) for the PLMs of significant size. LLMs typically refer to language models that have hundreds of billions (or more) of parameters and are trained on massive text data such as GPT-3, PaLM, Codex, and LLaMA. LLMs are built using the Transformer architecture, which stacks multi-head attention layers in a very deep neural network. Existing LLMs adopt similar model architectures (Transformer) and pre-training objectives (language modeling) as small language models, but largely scale up the model size, pre-training data, and total compute power. This enables LLMs to better understand natural language and generate high-quality text based on given context or prompts.

Note that, in existing literature, there is no formal consensus on the minimum parameter scale for LLMs, since the model capacity is also related to data size and total compute. In a recent survey of LLMs [17], the authors focus on discussing the language models with a model size larger than 10B. Under their criteria, the first LLM is T5 released by Google in 2019, followed by GPT-3 released by OpenAI in 2020, and there are more than thirty LLMs released between 2021 and 2023 indicating its popularity. In another survey of unifying LLMs and knowledge graphs [24], the authors categorize the LLMs into three types: encoder-only (e.g., BERT), encoder-decoder (e.g., T5), and decoder-only network architecture (e.g., GPT-3). In our review, we take into account the categorization criteria of the two surveys and only consider the encoder-decoder and decoder-only network architecture of pre-training language models, since they can both support generative tasks. We do not consider the encoder-only network architecture because they cannot handle generative tasks, were proposed relatively early (e.g., BERT in 2018), and there are almost no models using this architecture after 2021. In other words, the LLMs discussed in this paper not only include models with parameters of over 10B (as mentioned in [17]) but also include other models that use the encoder-decoder and decoder-only network

architecture (as mentioned in [24]), such as BART with 140M parameters and GPT-2 with parameter sizes ranging from 117M to 1.5B. This is also to potentially include more studies to demonstrate the landscape of this topic.

### 2.2 Software Testing

Software testing is a crucial process in software development that involves evaluating the quality of a software product. The primary goal of software testing is to identify defects or errors in the software system that could potentially lead to incorrect or unexpected behavior. The whole life cycle of software testing typically includes the following tasks (demonstrated in Figure 4):

- Requirement Analysis: analyze the software requirements and identify the testing objectives, scope, and criteria.

- Test Plan: develop a test plan that outlines the testing strategy, test objectives, and schedule.

- Test Design and Review: develop and review the test cases and test suites that align with the test plan and the requirements of the software application.

- Test Case Preparation: the actual test cases are prepared based on the designs created in the previous stage.

- Test Execution: execute the tests that were designed in the previous stage. The software system is executed with the test cases and the results are recorded.

- Test Reporting: analyze the results of the tests and generate reports that summarize the testing process and identify any defects or issues that were discovered.

- Bug Fixing and Regression Testing: defects or issues identified during testing are reported to the development team for fixing. Once the defects are fixed, regression testing is performed to ensure that the changes have not introduced new defects or issues.

- Software Release: once the software system has passed all of the testing stages and the defects have been fixed, the software can be released to the customer or end user.

The testing process is iterative and may involve multiple cycles of the above stages, depending on the complexity of the software system and the testing requirements.

During the testing phase, various types of tests may be performed, including unit tests, integration tests, system tests, and acceptance tests.

- Unit Testing involves testing individual units or components of the software application to ensure that they function correctly.

- Integration Testing involves testing different modules or components of the software application together to ensure that they work correctly as a system.

- System Testing involves testing the entire software system as a whole, including all the integrated components and external dependencies.

- Acceptance Testing involves testing the software application to ensure that it meets the business requirements and is ready for deployment.

In addition, there can be functional testing, performance testing, unit testing, security testing, accessibility testing, etc, which explores various aspects of the software under test [25].

4

![](images/p04-01.png)

Major SE Venues<br>& AI Venues<br>START 3.1.1 Automatic Search Papers14,623  3.1.1 Automatic Filtering Papers1,239  3.1.2 Manual Search<br>1,278<br>Papers<br>Papers102  3.1.5 Snowballing Papers102 3.1.4 Quality Assessment Papers109  3.1.3 Inclusion and Exclusion Criteria<br>

Fig. 2: Overview of the paper collection process

## 3 PAPER SELECTION AND REVIEW SCHEMA

### 3.1 Paper Collection Methodology

Figure 2 shows our paper search and selection process. To collect as much relevant literature as possible, we use both automatic search (from paper repository database) and manual search (from major software engineering and artificial intelligence venues). We searched papers from Jan. 2019 to Jun. 2023 and further conducted the second round of search to include the papers from Jul. 2023 to Oct. 2023.

### _3.1.1 Automatic Search_

To ensure that we collect papers from diverse research areas, we conduct an extensive search using four popular scientific databases: ACM digital library, IEEE Xplore digital library, arXiv, and DBLP.

We search for papers whose title contains _keywords related to software testing tasks and testing techniques_ (as shown below) in the first three databases. In the case of DBLP, we use additional _keywords related to LLMs_ (as shown below) to filter out irrelevant studies, as relying solely on testingrelated keywords would result in a large number of candidate studies. While using two sets of keywords for DBLP may result in overlooking certain related studies, we believe it is still a feasible strategy. This is due to the fact that a substantial number of studies present in this database can already be found in the first three databases, and the fourth database only serves as a supplementary source for collecting additional papers.

- Keywords related with software testing tasks and techniques: test _OR_ bug _OR_ issue _OR_ defect _OR_ fault _OR_ error _OR_ failure _OR_ crash _OR_ debug _OR_ debugger _OR_ repair _OR_ fix _OR_ assert _OR_ verification _OR_ validation _OR_ fuzz _OR_ fuzzer _OR_ mutation.

- Keywords related with LLMs: LLM _OR_ language model _OR_ generative model _OR_ large model _OR_ GPT-3 _OR_ ChatGPT _OR_ GPT-4 _OR_ LLaMA _OR_ PaLM2 _OR_ CodeT5 _OR_ CodeX _OR_ CodeGen _OR_ Bard _OR_ InstructGPT. Note that, we only list the top ten most popular LLMs (based on Google search), since they are the search keywords for matching paper titles, rather than matching the paper content.

The above search strategy based on the paper title can recall a large number of papers, and we further conduct the automatic filtering based on the paper content. Specifically, we filter the paper whose content contains “LLM” or “language model” or “generative model” or “large model” or the name of the LLMs (using the LLMs in [17], [24] except those in our exclusion criteria). This can help eliminate the papers that do not involve the neural models.

### _3.1.2 Manual Search_

To compensate for the potential omissions that may result from automated searches, we also conduct manual searches. In order to make sure we collect highly relevant papers, we conduct a manual search within the conference proceedings and journal articles from top-tier software engineering venues (listed in Table 2).

In addition, given the interdisciplinary nature of this work, we also include the conference proceedings of the artificial intelligence field. We select the top ten venues based on the h5 index from Google Scholar, and exclude three computer vision venues, i.e., CVPR, ICCV, ECCV, as listed in Table 2.

### _3.1.3 Inclusion and Exclusion Criteria_

The search conducted on the databases and venue is, by design, very inclusive. This allows us to collect as many papers as possible in our pool. However, this generous inclusivity results in having papers that are not directly related to the scope of this survey. Accordingly, we define a set of specific inclusion and exclusion criteria and then we apply them to each paper in the pool and remove papers not meeting the criteria. This ensures that each collected paper aligns with our scope and research questions.

**Inclusion Criteria.** We define the following criteria for including papers:

- The paper proposes or improves an approach, study, or tool/framework that targets testing specific software or systems with LLMs.

- The paper applies LLMs to software testing practice, including all tasks within the software testing lifecycle as demonstrated in Section 2.2.

- The paper presents an empirical or experimental study about utilizing LLMs in software testing practice.

- The paper involves specific testing techniques (e.g., fuzz testing) employing LLMs.

If a paper satisfies any of the following criteria, we will include it.

**Exclusion Criteria.** The following studies would be excluded during study selection:

- The paper does not involve software testing tasks, e.g., code comment generation.

- The paper does not utilize LLMs, e.g., using recurrent neural networks.

- The paper mentions LLMs only in future work or discussions rather than using LLMs in the approach.

- The paper utilizes language models with encoder-only architecture, e.g., BERT, which can not directly be utilized for generation tasks (as demonstrated in Section 2.1).

- The paper focuses on testing the performance of LLMs, such as fairness, stability, security, etc. [125]–[127].

- The paper focuses on evaluating the performance of LLM-enabled tools, e.g., evaluating the code quality of the code generation tool Copilot [128]–[130].

For the papers collected through automatic search and manual search, we conduct a manual inspection to check whether they satisfy our inclusion criteria and filter those following our exclusion criteria. Specifically, the first two authors read each paper to carefully determine whether it

5

TABLE 1: Details of the collected papers

|**ID**<br>1|**Topic**<br><br>Unit test case eneration<br>|**Paper title**<br>**Year**<br>**Reference**<br>Unit Test Case Generation with Transformers and Focal Context<br>2020<br>[26]|
|---|---|---|
|2<br>3|g<br> <br>Unit test case generation<br> <br>Unit test case generation<br>|<br><br><br>Codet: Code Generation with Generated Tests<br>2022<br>[27]<br>Interactive Code Generation via Test-Driven User-Intent Formalization<br>2022<br>[28]|
|4|<br> <br>Unit test case generation<br>|<br><br><br>A3Test: Assertion-Augmented Automated Test Case Generation<br>2023<br>[29]|
|5<br>6|<br> <br>Unit test case generation<br> <br>Unit test case generation<br>|<br><br><br>An Empirical Evaluation of Using Large Language Models for Automated Unit Test Generation<br>2023<br>[30]<br>An Initial Investigation of ChatGPT Unit Test Generation Capability<br>2023<br>[31]|
|7|<br> <br>Unit test case generation<br>|<br><br>Automated Test Case Generation Using Code Models and Domain Adaptation<br>2023<br>[32]|
|8<br>9|<br> <br>Unit test case generation<br> <br>Unit test case generation<br>|<br><br>Automatic Generation of Test Cases based on Bug Reports: a Feasibility Study with Large Language Models<br>2023<br>[33]<br>Can Large Language Models Write Good Property-Based Tests?<br>2023<br>[34]|
|10<br>11|<br> <br>Unit test case generation<br> <br>Unit test case generation<br>|<br><br>CAT-LM Training Language Models on Aligned Code And Tests<br>2023<br>[35]<br>ChatGPT vs SBST: A Comparative Assessment of Unit Test Suite Generation<br>2023<br>[8]|
|12|Unit test case generation<br> <br>|ChatUniTest: a ChatGPT-based Automated Unit Test Generation Tool<br>2023<br>[36]<br> <br>|
|13<br>14<br>|Unit test case generation<br> <br>Unit test case generation<br> <br> <br>|CODAMOSA: Escaping Coverage Plateaus in Test Generation with Pre-trained Large Language Models<br>2023<br>[37]<br>Effective Test Generation Using Pre-trained Large Language Models and Mutation Testing<br>2023<br>[38]<br> <br>|
|15<br>|Unit test case generation<br> <br> <br>|Exploring the Effectiveness of Large Language Models in Generating Unit Tests<br>2023<br>[39]<br> <br><br>|
|16<br>17<br>|Unit test case generation<br> <br>Unit test case generation<br> <br> <br>|How Well does LLM Generate Security Tests?<br>2023<br>[40]<br>No More Manual Tests? Evaluating and Improving ChatGPT for Unit Test Generation<br>2023<br>[7]<br> <br><br>|
|18<br>19<br>|Unit test case generation<br> <br>Unit test case generation<br> <br> <br>|Prompting Code Interpreter to Write Better Unit Tests on Quixbugs Functions<br>2023<br>[41]<br>Reinforcement Learning from Automatic Feedback for High-Quality Unit Test Generation<br>2023<br>[42]<br> <br><br>|
|20<br>21<br>22|Unit test case generation<br> <br>Test oracle generation<br> <br>T l i<br>|Unit Test Generation using Generative AI: A Comparative Performance Analysis of Autogeneration Tools<br>2023<br>[43]<br>Generating Accurate Assert Statements for Unit Test Cases Using Pretrained Transformers<br>2022<br>[44]<br>i D Si f T Cli<br>2023<br>45|
|23<br>24|est orace generaton<br> <br>Test oracle generation; Program repair<br> <br>Test oracle eneration Proram reair<br>|earnng eep emantcs or est ompeton<br><br>[]<br>Using Transfer Learning for Code-Related Tasks<br>2023<br>[46]<br>Retrieval-Based Promt Selection for Code-Related Few-Shot Learnin<br>2023<br>[47]|
|25<br>26|g; g p<br> <br>System test input generation<br> <br>Sstem test input generation<br>|p     g<br><br><br>Automated Conformance Testing for JavaScript Engines via Deep Compiler Fuzzing<br>2021<br>[48]<br>Fill in the Blank: Context-aware Automated Text Input Generation for Mobile GUI Testing<br>2022<br>[49]|
|27|y<br> <br>System test input generation<br>|<br><br><br>Large Language Models are Pretty Good Zero-Shot Video Game Bug Detectors<br>2022<br>[50]|
|28|<br> <br>System test input generation<br>|<br><br><br>Slgpt: Using Transfer Learning to Directly Generate Simulink Model Files and Find Bugs in the Simulink Toolchain<br>2021<br>[51]|
|29|<br> <br>System test input generation<br>|<br><br><br>Augmenting Greybox Fuzzing with Generative AI<br>2023<br>[52]|
|30|<br> <br>System test input generation<br>|<br><br>Automated Test Case Generation Using T5 and GPT-3<br>2023<br>[53]|
|31|<br> <br>System test input generation<br>|<br><br>Automating GUI-based Software Testing with GPT-3<br>2023<br>[54]|
|32<br>33<br>34|<br> <br>System test input generation<br> <br>System test input generation<br> <br>System test input generation<br>i|<br>AXNav: Replaying Accessibility Tests from Natural Language<br>2023<br>[55]<br>Can ChatGPT Advance Software Testing Intelligence? An Experience Report on Metamorphic Testing<br>2023<br>[56]<br>Efficient Mutation Testing via Pre-Trained Language Models<br>2023<br>[57]|
|35|System test input generation<br>|Large Language Models are Edge-Case Generators:Crafting Unusual Programs for Fuzzing Deep Learning Libraries<br>2023<br>[58]|
|36<br>37<br>|System test input generation<br> <br>System test input generation<br> <br> <br>|Large Language Models are Zero Shot Fuzzers: Fuzzing Deep Learning Libraries via Large Language Models<br>2023<br>[59]<br>Large Language Models for Fuzzing Parsers (Registered Report)<br>2023<br>[60]<br> <br><br>|
|38<br>|System test input generation<br> <br> <br>|LLM for Test Script Generation and Migration: Challenges, Capabilities, and Opportunities<br>2023<br>[61]<br> <br><br>|
|39<br>40<br>|System test input generation<br> <br>System test input generation<br> <br> <br>|Make LLM a Testing Expert: Bringing Human-like Interaction to Mobile GUI Testing via Functionality-aware Decisions<br>2023<br>[14]<br>PentestGPT: An LLM-empowered Automatic Penetration Testing Tool<br>2023<br>[62]<br> <br><br>|
|41<br>42<br>|System test input generation<br> <br>System test input generation<br>i<br> <br>|SMT Solver Validation Empowered by Large Pre-Trained Language Models<br>2023<br>[63]<br>TARGET: Automated Scenario Generation from Traffic Rules for Testing Autonomous Vehicles<br>2023<br>[64]<br> <br><br>|
|43<br>44|System test input generation<br> <br>S  i i<br>|esting the Limits: Unusual Text Inputs Generation for Mobile App Crash Detection with Large Language Model<br>2023<br>[65]<br>ddi L L Mdl Bd F Di Gi<br>22<br>|
|45<br>46|ystem test nput generaton<br> <br>System test input generation<br> <br>Stm tt inut nratin<br>i|nerstanng arge anguage oe ase uzz rver eneraton<br>03<br>[66]<br>Universal Fuzzing via Large Language Models<br>2023<br>[67]<br>Variabl Dir with Lar Lanua Mdl fr Mtamrhi Ttin f Sintifi Sftwar<br>2023<br>[68]|
|47<br>48|yse es p geeo<br>i<br>System test input generation<br> <br>Bu analsis<br>|e scovey  ge gge oes o eopc esg o ceic oe<br><br><br>White-box Compiler Fuzzing Empowered by Large Language Models<br>2023<br>[69]<br>tier: an Automatic Issue Title Generation Tool<br>2022<br>[70]|
|49|g y<br> <br>Bug analysis<br>|g<br><br><br>CrashTranslator: Automatically Reproducing Mobile Application Crashes Directly from Stack Trace<br>2023<br>[71]|
|50|<br> <br>Bug analysis<br>|<br><br><br>Cupid: Leveraging ChatGPT for More Accurate Duplicate Bug Report Detection<br>2023<br>[72]|
|51<br>52|<br> <br>Bug analysis<br>i<br>Bug analysis<br>|<br><br><br>Employing Deep Learning and Structured Information Retrieval to Answer Clarification Questions on Bug Reports<br>2023<br>[73]<br>Explaining Software Bugs Leveraging Code Structures in Neural Machine Translation<br>2022<br>[74]|
|53|<br> <br>Bug analysis<br>|<br><br>Prompting Is All Your Need: Automated Android Bug Replay with Large Language Models<br>2023<br>[75]|
|54<br>55|<br> <br>Bug analysis<br> <br>Debug<br>i|<br><br>Still Confusing for Bug-Component Triaging? Deep Feature Learning and Ensemble Setting to Rescue<br>2023<br>[76]<br>Detect-Localize-Repair: A Unified Framework for Learning to Debug with CodeT5<br>2022<br>[77]|
|56<br>57|i<br>Debug<br> <br>Debug<br>|i<br>Large Language Models are Few-shot Testers: Exploring LLM-based General Bug Reproduction<br>2022<br>[78]<br>A Preliminary Evaluation of LLM-Based Fault Localization<br>2023<br>[79]|
|58|Debug<br>l<br><br>|Addressing Compiler Errors: Stack Overflow or Large Language Models?<br>2023<br>[80]<br> <br>|
|59<br>60<br>|Debug<br> <br>Debug<br> <br><br>i|Can LLMs Demystify Bug Reports?<br>2023<br>[81]<br>Dcc –help: Generating Context-Aware Compiler Error Explanations with Large Language Models<br>2023<br>[82]<br>i<br><br>|
|61<br>62<br>|Debug<br>i<br>Debug<br> <br><br>|Explainable Automated Debugging via Large Language Model-driven Scientific Debugging<br>2023<br>[83]<br>Large Language Models for Test-Free Fault Localization<br>2023<br>[84]<br> <br><br>|
|63<br>64<br>|Debug<br> <br>Debug<br> <br><br>|Large Language Models in Fault Localisation<br>2023<br>[85]<br>LLM4CBI: Taming LLMs to Generate Effective Test Programs for Compiler Bug Isolation<br>2023<br>[86]<br> <br><br>|
|65<br>|Debug<br> <br><br>|Nuances are the Key: Unlocking ChatGPT to Find Failure-Inducing Tests with Differential Prompting<br>2023<br>[87]<br> <br><br>|
|66<br>67<br>68|Debug<br> <br>Debug; Program repair<br> <br>P i<br>|eaching Large Language Models to Self-Debug<br>2023<br>[88]<br>A study on Prompt Design, Advantages and Limitations of ChatGPT for Deep Learning Program Repair<br>2023<br>[89]<br>ii ZSht Vlbilit Ri ith L L Mdl<br>2022<br>90|
|69<br>70|rogram repar<br> <br>Program repair<br> <br>P i<br>|xamnng ero-o uneray epar w arge anguage oes<br><br>[]<br>Automated Repair of Programs from Large Language Models<br>2022<br>[91]<br>i B ith Tf thh  Nl-Sbli Edit G<br>2022<br>[92]|
|71<br>72|rogram repar<br> <br>Program repair<br> <br>Proram reair<br>|x ugs w ransormer roug a euraymoc  rammar<br><br><br>Practical Program Repair in the Era of Large Pre-trained Language Models<br>2022<br>[93]<br>Reairin Bus in Pthon Assinments Usin Lare Lanuae Models<br>2022<br>[94]|
|73|g p<br> <br>Program repair<br>|pg g  y g g g gg<br><br><br>Towards JavaScript Program Repair with Generative Pre-trained Transformer (GPT-2)<br>2022<br>[95]|
|74<br>75|<br> <br>Program repair<br> <br>Program repair<br>|<br><br><br>An Analysis of the Automatic Bug Fixing Performance of ChatGPT<br>2023<br>[96]<br>An Empirical Study on Fine-Tuning Large Language Models of Code for Automated Program Repair<br>2023<br>[97]|
|76|<br> <br>Program repair<br>|<br><br>An Evaluation of the Effectiveness of OpenAI’s ChatGPT for Automated Python Program Bug Fixing using QuixBugs<br>2023<br>[98]|
|77|<br> <br>Program repair<br>|<br><br>An Extensive Study on Model Architecture and Program Representation in the Domain of Learning-based Automated Program Repair<br>2023<br>[99]|
|78|<br> <br>Program repair<br>|<br><br>Can OpenAI’s Codex Fix Bugs? An Evaluation on QuixBugs<br>2022<br>[100]|
|79|<br> <br>Program repair<br>|<br>CIRCLE: Continual Repair Across Programming Languages<br>2022<br>[101]|
|80<br>81<br>82|Program repair<br> <br>Program repair<br> <br>Program repair<br> <br>|Coffee: Boost Your Code LLMs by Fixing Bugs with Feedback<br>2023<br>[102]<br>Copiloting the Copilots: Fusing Large Language Models with Completion Engines for Automated Program Repair<br>2023<br>[103]<br>Domain Knowledge Matters: Improving Prompts with Fix Templates for Repairing Python Type Errors<br>2023<br>[104]<br> <br>|
|83<br>|Program repair<br> <br> <br>|Enhancing Genetic Improvement Mutations Using Large Language Models<br>2023<br>[105]<br> <br><br>|
|84<br>85<br>|Program repair<br> <br>Program repair<br> <br> <br>|FixEval: Execution-based Evaluation of Program Fixes for Programming Problems<br>2023<br>[106]<br>Fixing Hardware Security Bugs with Large Language Models<br>2023<br>[107]<br> <br><br>|
|86<br>87<br>|Program repair<br> <br>Program repair<br> <br> <br>|Fixing Rust Compilation Errors using LLMs<br>2023<br>[108]<br>Framing Program Repair as Code Completion<br>2022<br>[109]<br> <br><br>|
|88<br>89<br>|Program repair<br> <br>Program repair<br> <br>P i<br>|rustrated with Code Quality Issues? LLMs can Help!<br>2023<br>[110]<br>GPT-3-Powered Type Error Debugging: Investigating the Use of Large Language Models for Code Repair<br>2023<br>[111]<br>Effi A l k f Fii Si lbilii<br>22<br>112|
|90<br>91|rogram repar<br> <br>P i<br>|ow ectve re Neura Networs or xng ecurty Vunerates<br>03<br>[]<br>t f Cd L Mdl  Attd P Ri<br>2023<br>113|
|92|rogram repar<br> <br>Proram reair<br>i|mpac o oe anguage oes on uomae rogram epar<br><br>[]<br>nferfix: End-to-end Proram Reair with LLMs<br>2023<br>[114]|
|93<br>94<br>95|g p<br>i<br>Program repair<br> <br>Program repair<br> <br>Program repair<br>|i  g p<br><br><br>Keep the Conversation Going: Fixing 162 out of 337 bugs for $0.42 each using ChatGPT<br>2023<br>[115]<br>Neural Program Repair with Program Dependence Analysis and Effective Filter Mechanism<br>2023<br>[116]<br>Out of Context: How important is Local Context in Neural Program Repair?<br>2023<br>[117]|
|96|<br> <br>Program repair<br>|<br><br><br>Pre-trained Model-based Automated Software Vulnerability Repair: How Far are We?<br>2023<br>[118]|
|97<br>98|<br> <br>Program repair<br>i<br>Program repair<br>|<br><br>RAPGen: An Approach for Fixing Code Inefficiencies in Zero-Shot<br>2023<br>[119]<br>RAP-Gen: Retrieval-Augmented Patch Generation with CodeT5 for Automatic Program Repair<br>2023<br>[120]|
|99<br>100|<br> <br>Program repair<br> <br>Program repair<br>|<br><br>STEAM: Simulating the InTeractive BEhavior of ProgrAMmers for Automatic Bug Fixing<br>2023<br>[121]<br>Towards Generating Functionally Correct Code Edits from Natural Language Issue Descriptions<br>2023<br>[122]|
|101<br>102|<br> <br>Program repair<br> <br>Program repair<br>|<br><br>VulRepair: a T5-based Automated Software Vulnerability Repair<br>2022<br>[123]<br>What Makes Good In-Context Demonstrations for Code Intelligence Tasks with LLMs?<br>2023<br>[124]|

6

TABLE 2: Conference proceedings and journals considered for manual search

||**Acronym**|**Venue**|
|---|---|---|
||ICSE<br>ESEC/FSE|International Conference on Software Engineering<br>Joint European Software Engineering Conference and Symposium on the<br>Foundations of Software Engineering|
|**rence**|ASE<br>ISSTA|<br>International Conference on Automated Software Engineering<br>International Symposium on Software Testing and Analysis|
|**Confe**|ICST<br>ESEM|International Conference on Software Testing, Verification and Validation<br>International Symposium on Empirical Software Engineering and Mea-<br>surement|
|**SE**|MSR<br>QRS<br>ICSME<br>ISSRE|International Conference on Mining Software Repositories<br>International Conference on Software Quality, Reliability and Security<br>International Conference on Software Maintenance and Evolution<br>International Symposium on Software Reliability Engineering|
||TSE|Transactions on Software Engineering|
||TOSEM<br>EMSE|<br>Transactions on Software Engineering and Methodology<br>Empirical Software Engineering|
|**ournal**|ASE<br>JSS<br>JSEP|Automated Software Engineering<br>Journal of Systems and Software<br>Journal of Software: Evolution and Process|
|**SE J**|STVR<br>IEEE SOFTW.<br>IET SOFTW.|Software Testing, Verification and Reliability<br>IEEE Software<br>IET Software|
||IST<br>SQJ|Information and Software Technology<br>Software Quality Journal|
||ICLR|International Conference on Learning Representations|
|**nues**|NeurIPS<br>ICML|Conference on Neural Information Processing Systems<br>International Conference on Machine Learning|
|**Ve**|AAAI|<br>AAAI Conference on Artificial Intelligence|
|**AI **|EMNLP<br>ACL<br>IJCAI|i<br>Conference on Empirical Methods in Natural Language Processing<br>Annual Meeting of the Association for Computational Linguistics<br>International Joint Conference on Artificial Intelligence|

should be included based on the inclusion criteria and exclusion criteria, and any paper with different decisions will be handed over to the third author to make the final decision.

### _3.1.4 Quality Assessment_

In addition, we establish quality assessment criteria to exclude low-quality studies as shown below. For each question, the study’s quality is rated as “yes”, “partial” or “no” which are assigned values of 1, 0.5, and 0, respectively. Papers with a score of less than eight will be excluded from our study.

- Is there a clearly stated research goal related to software testing?

- Is there a defined and repeatable technique?

- Is there any explicit contribution to software testing?

- Is there an explicit description of which LLMs are utilized?

- Is there an explicit explanation about how the LLMs are utilized?

- Is there a clear methodology for validating the technique?

- Are the subject projects selected for validation suitable for the research goals?

- Are there control techniques or baselines to demonstrate the effectiveness of the proposed technique?

- Are the evaluation metrics relevant (e.g., evaluate the effectiveness of the proposed technique) to the research objectives?

- Do the results presented in the study align with the research objectives and are they presented in a clear and relevant manner?

### _3.1.5 Snowballing_

At the end of searching database repositories and conference proceedings and journals, and applying inclusion/exclusion criteria and quality assessment, we obtain the initial set of papers. Next, to mitigate the risk of omitting relevant literature from this survey, we also perform backward

![](images/p06-01.png)

200<br>150<br>100<br>82<br>50<br>19<br>1 2<br>0<br>2020 2021 2022 2023<br>Publication Year<br># Publications<br>

Fig. 3: Trend in the number of papers with year

snowballing [131] by inspecting the references cited by the collected papers so far. Note that, this procedure did not include new studies, which might because the surveyed topic is quite new and the reference studies tend to published previously, and we already include a relatively comprehensive automatic and manual search.

### 3.2 Collection Results

As shown in Figure 2, the collection process started with a total of 14,623 papers retrieved from four academic databases employing keyword searching. Then after automated filtering, manual search, applying inclusion/exclusion criteria, and quality assessment, we finally collected a total of 102 papers involving software testing with LLMs. Table 1 shows the details of the collected papers. Besides, we also use Table 5 (at the end of the paper) to provide a more comprehensive overview of these papers regarding the specific characteristics which will be illustrated in Section 4 and Section 5.

Note that, there are two studies which are respectively the extension of a previously published paper by the same authors ( [46] and [132], [68] and [133]), and we only keep the extended version to avoid duplicate.

### 3.3 General Overview of Collected Paper

Among the papers, 47% papers are published in software engineering venues, among which 19 papers are from ICSE, 5 papers are from FSE, 5 papers are from ASE, and 3 papers are from ISSTA. 2% papers are published in artificial intelligence venues such as EMNLP and ICLR, and 5% papers are published in program analysis or security venues like PLDI and S&P. Besides, 46% of the papers have not yet been published via peer-reviewed venues, i.e., they are disclosed on arXiv. This is understandable because this field is emerging and many works are just completed and in the process of submission. Although these papers did not undergo peer review, we have a quality assessment process that eliminates papers with low quality, which potentially ensures the quality of this survey.

Figure 3 demonstrates the trend of our collected papers per year. We can see that as the years go by, the number of papers in this field is growing almost exponentially. In 2020 and 2021, there were only 1 and 2 papers, respectively. In 2022, there were 19 papers, and in 2023, there have been 82

7

![](images/p07-01.png)

} mil 3 oe<br>aeneaton ow —<br>| BE T— os ow ow om mow ow<br>PaperCom 3 Paper Count<br>Requirement’ 0) * pigTest (0) andTestReview Design(0) PreparationTest Case(46) ExccutionTest (0)© BugReport(8)Test Report/ RegressionBug FixTest/  (50) ReleaseSoftware(0)<br>

Fig. 4: Distribution of testing tasks with LLMs (aligned with software testing life cycle [134]–[136], the number in bracket indicates the number of collected studies per task, and one paper might involve multiple tasks)

papers. It is conceivable that there will be even more papers in the future, which indicates the popularity and attention that this field is receiving.

## 4 ANALYSIS FROM SOFTWARE TESTING PERSPECTIVE

This section presents our analysis from the viewpoint of software testing and organizes the collected studies in terms of testing tasks. Figure 4 lists the distribution of each involved testing task, aligned with the software testing life cycle. We first provide a general overview of the distribution, followed by further analysis for each task. Note that, for each following subsection, the cumulative total of subcategories may not always match the total number of papers since a paper might belong to more than one subcategory.

We can see that LLMs have been effectively used in both the mid to late stages of the software testing lifecycle. In the test case preparation phase, LLMs have been utilized for tasks such as generating unit test cases, test oracle generation, and system test input generation. These tasks are crucial in the mid-phase of software testing to help catch issues and prevent further development until issues are resolved. Furthermore, in later phases such as the test report/bug reports and bug fix phase, LLMs have been employed for tasks such as bug analysis, debugging, and repair. These tasks are critical towards the end of the testing phase when software bugs need to be resolved to prepare for the product’s release.

### 4.1 Unit Test Case Generation

Unit test case generation involves writing unit test cases to check individual units/components of the software independently and ensure that they work correctly. For a method under test (i.e., often called the focal method), its corresponding unit test consists of a test prefix and a test oracle. In particular, the test prefix is typically a series of method invocation statements or assignment statements, which aims at driving the focal method to a testable state; and then the test oracle serves as the specification to check whether the current behavior of the focal method satisfies the expected one, e.g., the test assertion.

To alleviate manual efforts in writing unit tests, researchers have proposed various techniques to facilitate automated unit test generation. Traditional unit test generation techniques leverage search-based [3], [4], constraint-based [5] or random-based strategies [6] to generate a suite of unit tests with the main goal of maximizing the coverage in the software under test.

Nevertheless, the coverage and the meaningfulness of the generated tests are still far from satisfactory.

Since LLMs have demonstrated promising results in tasks such as code generation, and given that both code generation and unit test case generation involve generating source code, recent research has extended the domain of code generation to encompass unit test case generation. Despite initial success, there are nuances that set unit test case generation apart from general code generation, signaling the need for more tailored approaches.

**Pre-training or fine-tuning LLMs for unit test case generation.** Due to the limitations of LLMs in their earlier stages, a majority of the earlier published studies adopt this pre-training or fine-tuning schema. Moreover, in some recent studies, this schema continues to be employed to increase the LLMs’ familiarity with domain knowledge. Alagarsamy et al. [29] first pre-trained the LLM with the focal method and asserted statements to enable the LLM to have a stronger foundation knowledge of assertions, then fine-tuned the LLM for the test case generation task where the objective is to learn the relationship between the focal method and the corresponding test case. Tufano et al. [26] utilized a similar schema by pre-training the LLM on a large unsupervised Java corpus, and supervised fine-tuning a downstream translation task for generating unit tests. Hashtroudi et al. [32] leveraged the existing developerwritten tests for each project to generate a project-specific dataset for domain adaptation when fine-tuning the LLM, which can facilitate generating human-readable unit tests. Rao et al. [35] trained a GPT-style language model by utilizing a pre-training signal that explicitly considers the mapping between code and test files. Steenhoek et al. [42] utilizes reinforcement learning to optimize models by providing rewards based on static quality metrics that can be automatically computed for the generated unit test cases.

**Designing effective prompts for unit test case generation.** The advancement of LLMs has allowed them to excel at targeted tasks without pre-training or fine-tuning. Therefore most later studies typically focus on how to design the prompt, to make the LLM better at understanding the context and nuances of this task. Xie et al. [36] generated unit test cases by parsing the project, extracting essential information, and creating an adaptive focal context that includes a focal method and its dependencies within the predefined maximum prompt token limit of the LLM, and incorporating these context into a prompt to query the LLM.

8

TABLE 3: Performance of unit test case generation

|**Dataset**|**Correctness**|Coverage|LLM|Paper|
|---|---|---|---|---|
|5Javaprojects from Defects4J|16.21%|5%-13%(line coverage)|BART|[26]|
|10Javeprojects|40%|89%(line coverage),90%(branch coverage)|ChatGPT|[36]|
|CodeSearchNet|41%|N/A|ChatGPT|[7]|
|HumanEval|78%|87%(line coverage),92%(branch coverage)|Codex|[39]|
|SF110|2%|2%(line coverage),1%(branch coverage)|Codex|[39]|
|Note that, [39] experime|nts with Codex,|CodeGen, and ChatGPT, and the best performan|ce was achieved by|Codex.|

Dakhel et al. [38] introduced MuTAP for improving the effectiveness of test cases generated by LLMs in terms of revealing bugs by leveraging mutation testing. They augment prompts with surviving mutants, as those mutants highlight the limitations of test cases in detecting bugs. Zhang et al. [40] generated security tests with vulnerable dependencies with LLMs.

Yuan et al. [7] first performed an empirical study to evaluate ChatGPT’s capability of unit test generation with both a quantitative analysis and a user study in terms of correctness, sufficiency, readability, and usability. And results show that the generated tests still suffer from correctness issues, including diverse compilation errors and execution failures. They further propose an approach that leveraged the ChatGPT itself to improve the quality of its generated tests with an initial test generator and an iterative test refiner. Specifically, the iterative test refiner iteratively fixed the compilation errors in the tests generated by the initial test generator, which follows a validate-and-fix paradigm to prompt the LLM based on the compilation error messages and additional code context. Guilherme et al. [31] and Li et al. [41] respectively evaluated the quality of the generated unit tests by LLM using different metrics and different prompts.

**Test generation with additional documentation.** Vikram et al. [34] went a step further by investigating the potential of using LLMs to generate property-based tests when provided API documentation. They believe that the documentation of an API method can assist the LLM in producing logic to generate random inputs for that method and deriving meaningful properties of the result to check. Instead of generating unit tests from the source code, Plein et al. [33] generated the tests based on user-written bug reports.

**LLM and search-based method for unit test generation.** The aforementioned studies utilize LLMs for the whole unit test case generation task, while Lemieux et al. [37] focus on a different direction, i.e., first letting the traditional searchbased software testing techniques (e.g., Pynguin [137]) in generating unit test case until its coverage improvements stall, then asking the LLM to provide the example test cases for under-covered functions. These examples can help the original test generation redirect its search to more useful areas of the search space.

Tang et al. [8] conducts a systematic comparison of test suites generated by the LLM and the state-of-the-art searchbased software testing tool EvoSuite, by considering the correctness, readability, code coverage, and bug detection capability. Similarly, Bhatia [43] experimentally investigates the quality of unit tests generated by LLM compared to a commonly-used test generator Pynguin.

**Performance of unit test case generation.** Since the aforementioned studies of unit test case generation are based on different datasets, one can hardly derive a fair comparison and we present the details in Table 3 to let the readers obtain a general view. We can see that in the SF110 benchmark, all three evaluated LLMs have quite low performance, i.e., 2% coverage [39]. SF110 is an Evosuite (a search-based unit test case generation technique) benchmark consisting of 111 open-source Java projects retrieved from SourceForge, containing 23,886 classes, over 800,000 bytecode-level branches, and 6.6 million lines of code. The authors did not present detailed reasons for the low performance which can be further explored in the future. **4.2 Test Oracle Generation** A test oracle is a source of information about whether the output of a software system (or program or function or method) is correct or not [138]. Most of the collected studies in this category target the test assertion generation, which is inside a unit test case. Nevertheless, we opted to treat these studies as separate sections to facilitate a more thorough analysis.

Test assertion, which is to indicate the potential issues in the tested code, is an important aspect that can distinguish the unit test cases from the regular code. This is why some studies specifically focus on the generation of effective test assertions. Actually, before using LLMs, researchers have proposed RNN-based approaches that aim at learning from thousands of unit test methods to generate meaningful assert statements [139], yet only 17% of the generated asserts can exactly match with the ground truth asserts. Subsequently, to improve the performance, several researchers utilized the LLMs for this task.

Mastropaolo et al. [46], [132] pre-trained a T5 model on a dataset composed of natural language English text and source code. Then, it fine-tuned such a model by reusing datasets used in four previous works that used deep learning techniques (such as RNN as mentioned before) including test assertion generation and program repair, etc. Results showed that the extract match rate of the generated test assertion is 57%. Tufano et al. [44] proposed a similar approach which separately pre-trained the LLM with English corpus and code corpus, and then fine-tuned it on the asserts dataset (with test methods, focal methods, and asserts). This further improved the performance to 62% of the exact match rate. Besides the syntax-level data as previous studies, Nie et al. [45] fine-tuned the LLMs with six kinds of code semantics data, including the execution result (e.g., types of the local variables) and execution context (e.g., the last called method in the test method), which enabled LLMs to learn to understand the code execution information. The exact match rate

9

is 17% (note that this paper is based on a different dataset from all other studies mentioned under this topic).

The aforementioned studies utilized the pre-training and fine-tuning schema when using LLMs, and with the increasingly powerful capabilities of LLMs, they can perform well on specific tasks without these specialized pre-training or fine-tuning datasets. Subsequently, Nashid et al. [47] utilized prompt engineering for this task, and proposed a technique for prompt creation that automatically retrieves code demonstrations similar to the task, based on embedding or frequency analysis. They also present evaluations about the few-shot learning with various numbers (e.g., zero-shot, one-shot, or n-shot) and forms (e.g., random vs. systematic, or with vs. without natural language descriptions) of the prompts, to investigate its feasibility on test assertion generation. With only a few relevant code demonstrations, this approach can achieve an accuracy of 76% for exact matches in test assertion generation, which is the state-of-the-art performance for this task.

### 4.3 System Test Input Generation

This category encompasses the studies related to creating test input of system testing for enabling the automation of test execution. We employ three subsections to present the analysis from three different orthogonal viewpoints, and each of the collected studies may be analyzed in one or more of these subsections.

The first subsection is _input generation in terms of software types_ . The generation of system-level test inputs for software testing varies for specific types of software being tested. For example, for mobile applications, the test input generation requires providing a diverse range of text inputs or operation combinations (e.g., click a button, long press a list) [14], [49], which is the key to testing the application’s functionality and user interface; while for Deep Learning (DL) libraries, the test input is a program which covers diversified DL APIs [58], [59]. This subsection will demonstrate how the LLMs are utilized to generate inputs for different types of software.

The second subsection _input generation in terms of testing techniques_ . We have observed that certain approaches serve as specific types of testing techniques. For example, dozens of our collected studies specifically focus on using LLMs for fuzz testing. Therefore, this subsection would provide an analysis of the collected studies in terms of testing techniques, showcasing how the LLMs are employed to enhance traditional testing techniques.

The third subsection _input generation in terms of input and output_ . While most of the collected studies take the source code or the software itself as the input and directly output the software’s test input, there are studies that utilize alternative forms of input and output. This subsection would provide an analysis of such studies, highlighting different approaches and their input-output characteristics.

### _4.3.1 Input Generation in Terms of Software Types_

Figure 5 demonstrates the types of software under test in our collected studies. It is evident that the most prominent category is mobile apps, with five studies utilizing LLMs for testing, possibly due to their prevalence and importance

![](images/p09-01.png)

Mobile app 5<br>Deep learning library 2<br>Compiler 2<br>SMT solver 2<br>Autonomous driving system 1<br>Cyber physical system 1<br>GO toolchain 1<br>JavaScript engine 1<br>Quantum computing platform 1<br>Video game 1<br>0 1 2 3 4 5<br>Paper Count<br>Software Under Test<br>

Fig. 5: Distribution of software under test

in today’s business and daily life. Additionally, there are respectively two studies focusing on testing deep learning libraries, compilers, and SMT solvers. Moreover, LLM-based testing techniques have also been applied to domains such as cyber-physical systems, quantum computing platforms, and more. This widespread adoption of LLMs demonstrates their effectiveness in handling diverse test inputs and enhancing testing activities across various software domains. A detailed analysis is provided below.

**Test input generation for mobile apps.** For mobile app testing, one difficulty is to generate the appropriate text inputs to proceed to the next page, which remains a prominent obstacle for testing coverage. Considering the diversity and semantic requirement of valid inputs (e.g., flight departure, movie name), traditional techniques with heuristic-based or constraint-based techniques [10], [140] are far from generating meaningful text input. Liu et al. [49] employ the LLM to intelligently generate the semantic input text according to the GUI context. In detail, their proposed QTypist automatically extracts the component information related to the EditText for generating the prompts, and then inputs the prompts into the LLM to generate the input text.

Besides the text input, there are other forms of input for mobile apps, i.e., operations like ‘click a button’ and ‘select a list’. To fully test an app, it is required to cover more GUI pages and conduct more meaningful exploration traces through the GUI operations, yet existing studies with random-/rule-based methods [9], [10], model-based methods [11], [12], and learning-based methods [13] are unable to understand the semantic information of the GUI page thus could not conduct the trace planning effectively. Liu et al. [14] formulates the test input generation of mobile GUI testing problem as a Q&A task, which asks LLM to chat with the mobile apps by passing the GUI page information to LLM to elicit testing scripts (i.e., GUI operation), and executing them to keep passing the app feedback to LLM, iterating the whole process. The proposed GPTDroid extracts the static context of the GUI page and the dynamic context of the iterative testing process, and designs prompts for inputting this information to LLM which enables the LLM to better understand the GUI page as well as the whole testing process. It also introduces a functionality-aware memory prompting mechanism that equips the LLM with the ability to retain testing knowledge of the whole process and conduct long-term, functionality-based reasoning to guide exploration. Similarly, Zimmermann et al. utilize the LLM to

10

interpret natural language test cases and programmatically navigate through the application under test [54].

Yu et al. [61] investigate the LLM’s capabilities in the mobile app test script generation and migration task, including the scenario-based test generation, and the crossplatform/app test migration.

**Test input generation for DL libraries.** The input for testing DL libraries is DL programs, and the difficulty in generating the diversified input DL programs is that they need to satisfy both the input language (e.g., Python) syntax/semantics and the API input/shape constraints for tensor computations. Traditional techniques with API-level fuzzing [141], [142] or model-level fuzzing [143], [144] suffer from the following limitations: 1) lack of diverse API sequence thus cannot reveal bugs caused by chained API sequences; 2) cannot generate arbitrary code thus cannot explore the huge search space that exists when using the DL libraries. Since LLMs can include numerous code snippets invoking DL library APIs in their training corpora, they can implicitly learn both language syntax/semantics and intricate API constraints for valid DL program generation. Taken in this sense, Deng et al. [59] used both generative and infilling LLMs to generate and mutate valid/diverse input DL programs for fuzzing DL libraries. In detail, it first uses a generative LLM (CodeX) to generate a set of seed programs (i.e., code snippets that use the target DL APIs). Then it replaces part of the seed program with masked tokens using different mutation operators and leverages the ability of infilling LLM (InCoder) to perform code infilling to generate new code that replaces the masked tokens. Their follow-up study [58] goes a step further to prime LLMs to synthesize unusual programs for the fuzzing DL libraries. It is built on the well-known hypothesis that historical bug-triggering programs may include rare/valuable code ingredients important for bug finding and show improved bug detection performance.

**Test input generation for other types of software.** There are also dozens of studies that address testing tasks in various other domains, due to space limitations, we will present a selection of representative studies in these domains.

Finding bugs in a commercial cyber-physical system (CPS) development tool such as Simulink is even more challenging. Given the complexity of the Simulink language, generating valid Simulink model files for testing is an ambitious task for traditional machine learning or deep learning techniques. Shrestha et al. [51] employs a small set of Simulink-specific training data to fine-tune the LLM for generating Simulink models. Results show that it can create Simulink models quite similar to the open-source models, and can find a super-set of the bugs traditional fuzzing approaches found.

Sun et al. [63] utilize LLM to generate test formulas for fuzzing SMT solvers. It retrains the LLMs on a large corpus of SMT formulas to enable them to acquire SMT-specific domain knowledge. Then it further fine-tunes the LLMs on historical bug-triggering formulas, which are known to involve structures that are more likely to trigger bugs and solver-specific behaviors. The LLM-based compiler fuzzer proposed by Yang et al. [69] adopts a dual-model framework: (1) an analysis LLM examines the low-level optimization source code and produces requirements on the

high-level test programs that can trigger the optimization; (2) a generation LLM produces test programs based on the summarized requirements. Ye et al. [48] utilize the LLM for generating the JavaScript programs and then use the well-structured ECMAScript specifications to automatically generate test data along with the test programs, after that they apply differential testing to expose bugs.

_4.3.2 Input Generation in Terms of Testing Techniques_ By utilizing system test inputs generated by LLMs, the collected studies aim to enhance traditional testing techniques and make them more effective. Among these techniques, fuzz testing is the most commonly involved one. Fuzz testing, as a general concept, revolves around generating invalid, unexpected, or random data as inputs to evaluate the behavior of software. LLMs play a crucial role in improving traditional fuzz testing by facilitating the generation of diverse and realistic input data. This enables fuzz testing to uncover potential bugs in the software by subjecting it to a wide range of input scenarios. In addition to fuzz testing, LLMs also contribute to enhancing other testing techniques, which will be discussed in detail later.

**Universal fuzzing framework.** Xia et al. [67] present Fuzz4All that can target many different input languages and many different features of these languages. The key idea behind it is to leverage LLMs as an input generation and mutation engine, which enables the approach to produce diverse and realistic inputs for any practically relevant language. To realize this potential, they present a novel auto-prompting technique, which creates LLM prompts that are well-suited for fuzzing, and a novel LLM-powered fuzzing loop, which iteratively updates the prompt to create new fuzzing inputs. They experiment with six different languages (C, C++, Go, SMT2, Java and Python) as inputs and demonstrate higher coverage than existing language-specific fuzzers. Hu et al. [52] propose a greybox fuzzer augmented by the LLM, which picks a seed in the fuzzer’s seed pool and prompts the LLM to produce the mutated seeds that might trigger a new code region of the software. They experiment with three categories of input formats, i.e., formatted data files (e.g., json, xml), source code in different programming languages (e.g., JS, SQL, C), text with no explicit syntax rules (e.g., HTTP response, md5 checksum). In addition, effective fuzzing relies on the effective fuzz driver, and Zhang et al. [66] utilize LLMs on the fuzz driver generation, in which five query strategies are designed and analyzed from basic to enhanced.

**Fuzzing techniques for specific software.** There are studies that focus on the fuzzing techniques tailored to specific software, e.g., the deep learning library [58], [59], compiler [69], SMT solvers [63], input widget of mobile app [65], cyber-physical system [51], etc. One key focus of these fuzzing techniques is to generate diverse test inputs so as to achieve higher coverage. This is commonly achieved by combining the mutation technique with LLM-based generation, where the former produces various candidates while the latter is responsible for generating the executable test inputs [59], [63]. Another focus of these fuzzing techniques is to generate the risky test inputs that can trigger bugs earlier. To achieve this, a common practice is to

11

collect the historical bug-triggering programs to fine-tune the LLM [63] or treat them as the demonstrations when querying the LLM [58], [65].

**Other testing techniques.** There are studies that utilize LLMs for enhancing GUI testing for generating meaningful text input [49] and functionality-oriented exploration traces [14], which has been introduced in _Test input generation for mobile apps_ part of Section 4.3.1.

Besides, Deng et al. [62] leverage the LLMs to carry out penetration testing tasks automatically. It involves setting a penetration testing goal for the LLM, soliciting it for the appropriate operation to execute, implementing it in the testing environment, and feeding the test outputs back to the LLM for next-step reasoning.

### _4.3.3 Input Generation in Terms of Input and Output_

**Other output format of test generation.** Although most works use LLM to generate test cases directly, there are also some works generating indirect inputs like testing code, test scenarios, metamorphic relations, etc. Liu et al. [65] propose InputBlaster which leverages the LLM to automatically generate unusual text inputs for fuzzing the text input widgets in mobile apps. It formulates the unusual inputs generation problem as a task of producing a set of test generators, each of which can yield a batch of unusual text inputs under the same mutation rule. In detail, InputBlaster leverages LLM to produce the test generators together with the mutation rules serving as the reasoning chain and utilizes the in-context learning schema to demonstrate the LLM with examples for boosting the performance. Deng et al. [64] use LLM to extract key information related to the test scenario from a traffic rule, and represent the extracted information in a test scenario schema, then synthesize the corresponding scenario scripts to construct the test scenario. Luu et al. [56] examine the effectiveness of LLM in generating metamorphic relations (MRs) for metamorphic testing. Their results show that ChatGPT can be used to advance software testing intelligence by proposing MRs candidates that can be later adapted for implementing tests, but human intelligence should still inevitably be involved to justify and rectify their correctness.

**Other input format of test generation.** The aforementioned studies primarily take the source code or the software as the input of LLM, yet there are also studies that take natural language description as the input for test generation. Mathur et al. [53] propose to generate test cases from the natural language described requirements. Ackerman et al. [60] generate the instances from natural language described requirements recursively to serve as the seed examples for a mutation fuzzer.

### 4.4 Bug Analysis

This category involves analyzing and categorizing the identified software bugs to enhance understanding of the bug, and facilitate subsequent debug and bug repair. Mukherjee et al. [73] generate relevant answers to follow-up questions for deficient bug reports to facilitate bug triage. Su et al. [76] transform the bug-component triaging into a multiclassification task and a generation task with LLM, then ensemble the prediction results from them to improve the

performance of bug-component triaging further. Zhang et al. [72] first leverage the LLM under the zero-shot setting to get essential information on bug reports, then use the essential information as the input to detect duplicate bug reports. Mahbub et al. [74] proposes to explain software bugs with LLM, which generates natural language explanations for software bugs by learning from a large corpus of bug-fix commits. Zhang et al. [70] target to automatically generate the bug title from the descriptions of the bug, which aims to help developers write issue titles and facilitate the bug triaging and follow-up fixing process.

### 4.5 Debug

This category refers to the process of identifying and locating the cause of a software problem (i.e., bug). It involves analyzing the code, tracing the execution flow, collecting error information to understand the root cause of the issue, and fixing the issue. Some studies concentrate on the comprehensive debug process, while others delve into specific sub-activities within the process.

**Overall debug framework.** Bui et al. [77] proposes a unified Detect-Localize-Repair framework based on the LLM for debugging, which first determines whether a given code snippet is buggy or not, then identifies the buggy lines, and translates the buggy code to its fixed version. Kang et al. [83] proposes automated scientific debugging, a technique that given buggy code and a bug-revealing test, prompts LLMs to automatically generate hypotheses, uses debuggers to actively interact with buggy code, and thus automatically reaches conclusions prior to patch generation. Chen et al. [88] demonstrate that self-debugging can teach the LLM to perform rubber duck debugging; i.e., without any human feedback on the code correctness or error messages, the model is able to identify its mistakes by investigating the execution results and explaining the generated code in natural language. Cao et al. [89] conducts a study of LLM’s debugging ability for deep learning programs, including fault detection, fault localization and program repair.

**Bug localization.** Wu et al. [85] compare the two LLMs (ChatGPT and GPT-4) with the existing fault localization techniques, and investigate the consistency of LLMs in fault localization, as well as how prompt engineering and the length of code context affect the results. Kang et al. [79] propose AutoFL, an automated fault localization technique that only requires a single failing test, and during its fault localization process, it also generates an explanation about why the given test fails. Yang et al. [84] propose LLMAO to overcome the left-to-right nature of LLMs by fine-tuning a small set of bidirectional adapter layers on top of the representations learned by LLMs, which can locate buggy lines of code without any test coverage information. Tu et al. [86] propose LLM4CBI to tame LLMs to generate effective test programs for finding suspicious files.

**Bug reproduction.** There are also studies focusing on a sub-phase of the debugging process. For example, Kang et al. [78] and Plein et al. [81] respectively propose the framework to harness the LLM to reproduce bugs, and suggest bug reproducing test cases to the developer for facilitating debugging. Li et al. [87] focus on a similar aspect of finding the failure-inducing test cases whose test input can trigger

12

the software’s fault. It synergistically combines LLM and differential testing to do that.

There are also studies focusing on the bug reproduction of mobile apps to produce the replay script. Feng et al. [75] propose AdbGPT, a new lightweight approach to automatically reproduce the bugs from bug reports through prompt engineering, without any training and hard-coding effort. It leverages few-shot learning and chain-of-thought reasoning to elicit human knowledge and logical reasoning from LLMs to accomplish the bug replay in a manner similar to a developer. Huang et al. [71] propose CrashTranslator to automatically reproduce bugs directly from the stack trace. It accomplishes this by leveraging the LLM to predict the exploration steps for triggering the crash, and designing a reinforcement learning based technique to mitigate the inaccurate prediction and guide the search holistically. Taeb et al. [55] convert the manual accessibility test instructions into replayable, navigable videos by using LLM and UI element detection models, which can also help reveal accessibility issues.

**Error explanation.** Taylor et al. [82] integrates the LLM into the Debugging C Compiler to generate unique, novicefocused explanations tailored to each error. Widjojo et al. [80] study the effectiveness of Stack Overflow and LLMs at explaining compiler errors.

### 4.6 Program Repair

This category denotes the task of fixing the identified software bugs. The high frequency of repair-related studies can be attributed to the close relationship between this task and the source code. With their advanced natural language processing and understanding capabilities, LLM are well-equipped to process and analyze source code, making them an ideal tool for performing code-related tasks such as fixing bugs.

There have been template-based [145], heuristic-based [146], and constraint-based [147], [148] automatic program repair techniques. And with the development of deep learning techniques in the past few years, there have been several studies employing deep learning techniques for program repair. They typically adopt deep learning models to take a buggy software program as input and generate a patched program. Based on the training data, they would build a neural network model that learns the relations between the buggy code and the corresponding fixed code. Nevertheless, these techniques still fail to fix a large portion of bugs, and they typically have to generate hundreds to thousands of candidate patches and take hours to validate these patches to fix enough bugs. Furthermore, the deep learning based program repair models need to be trained with huge amounts of labeled training data (typically pairs of buggy and fixed code), which is time-and effortconsuming to collect the high-quality dataset. Subsequently, with the popularity and demonstrated capability of the LLMs, researchers begin to explore the LLMs for program repair.

**Patch single-line bugs.** In the early era of program repair, the focus was mainly on addressing defects related to single-line code errors, which are relatively simple and did not require the repair of complex program logic. Lajk´o et

al. [95] propose to fine-tune the LLM with JavaScript code snippets to serve as the purpose for the JavaScript program repair. Zhang et al. [116] employs program slicing to extract contextual information directly related to the given buggy statement as repair ingredients from the corresponding program dependence graph, which makes the fine-tuning more focused on the buggy code. Zhang et al. [121] propose a stage-wise framework STEAM for patching single-line bugs, which simulates the interactive behavior of multiple programmers involved in bug management, e.g., bug reporting, bug diagnosis, patch generation, and patch verification.

Since most real-world bugs would involve multiple lines of code, and later studies explore these more complex situations (although some of them can also patch the single-line bugs).

**Patch multiple-lines bugs.** The studies in this category would input a buggy function to the LLM, and the goal is to output the patched function, which might involve complex semantic understanding, code hunk modification, as well as program refactoring. Earlier studies typically employ the fine-tuning strategy to enable the LLM to better understand the code semantics. Fu et al. [123] fine-tune the LLM by employing BPE tokenization to handle Out-Of-Vocabulary (OOV) issues which makes the approach generate new tokens that never appear in a training function but are newly introduced in the repair. Wang et. al. [120] train the LLM based on both buggy input and retrieved bug-fix examples which are retrieved in terms of the lexical and semantical similarities. The aforementioned studies (including the ones in patching single-line bugs) would predict the fixed programs directly, and Hu et al. [92] utilize a different setup that predicts the scripts that can fix the bugs when executed with the delete and insert grammar. For example, it predicts whether an original line of code should be deleted, and what content should be inserted.

Nevertheless, fine-tuning may face limitations in terms of its reliance on abundant high-quality labeled data, significant computational resources, and the possibility of overfitting. To approach the program repair problem more effectively, later studies focus on how to design an effective prompt for program repair. Several studies empirically investigate the effectiveness of prompt variants of the latest LLMs for program repair under different repair settings and commonly-used benchmarks (which will be explored in depth later), while other studies focus on proposing new techniques. Ribeiro et al. [109] take advantage of LLM to conduct the code completion in a buggy line for patch generation, and elaborate on how to circumvent the open-ended nature of code generation to appropriately fit the new code in the original program. Xia et al. [115] propose the conversation-driven program repair approach that interleaves patch generation with instant feedback to perform the repair in a conversational style. They first feed the LLM with relevant test failure information to start with, and then learns from both failures and successes of earlier patching attempts of the same bug for more powerful repair. For earlier patches that failed to pass all tests, they combine the incorrect patches with their corresponding relevant test failure information to construct a new prompt for the LLM to generate the next patch, in order to avoid making the same mistakes. For earlier

13

TABLE 4: Performance of program repair

|**Dataset**|**% Correct patches**|**LLM**|**Paper**|
|---|---|---|---|
|Defects4J v1.2, Defects4J<br>v2.0,<br>QuixBugs,<br>HumanEval-Java|22/40 Jave bugs (QuixBugs dataset, with InCoder-6B, correct<br>code infilling setting)|PLBART, CodeT5, CodeGen, In-<br>Coder (each with variant pa-<br>rameters,10 LLMs in total)|[113]|
|QuixBugs|23/40 Python bugs, 14/40 Java bugs (complete function genera-<br>tion setting)|Codex-12B|[100]|
|Defects4J v1.2, Defects4J<br>v2.0,<br>QuixBugs,<br>Many-<br>Bugs|39/40 Python bugs, 34/40 Java bugs (QuixBugs dataset, with<br>Codex-12B, correct code infilling setting); 37/40 Python bugs,<br>32/40 Java bugs (QuixBugs dataset, with Codex-12B, complete<br>functiongeneration setting)|Codex, GPT-Neo, CodeT5, In-<br>Coder (each with variant pa-<br>rameters, 9 LLMs in total)|[93]|
|QuixBugs|31/40 Python bugs(completion functiongeneration setting)|ChatGPT-175B|[96]|
|DL programs from Stack-<br>Overflow|16/72 Python bugs (complete function generation setting)|ChatGPT-175B|[89]|
|Note that, for studies wit|h multiple datasets or LLMs, we only present the best performance|or in the most commonly utilized d|ataset.|

patches that passed all the tests (i.e., plausible patches), they further ask the LLM to generate alternative variations of the original plausible patches. This can further build on and learn from earlier successes to generate more plausible patches to increase the chance of having correct patches. Zhang et al. [94] propose a similar approach design by leveraging multimodal prompts (e.g., natural language description, error message, input-output-based test cases), iterative querying, test-case-based few-shot selection to produce repairs. Moon et al. [102] propose for bug fixing with feedback. It consists of a critic model to generate feedback, an editor to edit codes based on the feedback, and a feedback selector to choose the best possible feedback from the critic.

Wei et. al. [103] propose Repilot to copilot the AI “copilots” (i.e., LLMs) by synthesizing more valid patches during the repair process. Its key insight is that many LLMs produce outputs autoregressively (i.e., token by token), and by resembling human writing programs, the repair can be significantly boosted and guided through a completion engine. Brownlee et al. [105] propose to use the LLM as mutation operators for the search-based techniques of program repair.

**Repair with static code analyzer.** Most of the program repair studies would suppose the bug has been detected, while Jin et al. [114] propose a program repair framework paired with a static analyzer to first detect the bugs, and then fix them. In detail, the static analyzer first detects an error (e.g., null pointer dereference) and the context information provided by the static analyzer will be sent into the LLM for querying the patch for this specific error. Wadhwa et al. [110] focus on a similar task, and additionally employ an LLM as the ranker to assess the likelihood of acceptance of generated patches which can effectively catch plausible but incorrect fixes and reduce developer burden.

**Repair for specific bugs.** The aforementioned studies all consider the buggy code as the input for the automatic program repair, while other studies conduct program repairing in terms of other types of bug descriptions, specific types of bugs, etc. Fakhoury et al. [122] focus on program repair from natural language issue descriptions, i.e., generating the patch with the bug and fix-related information described in the issue reports. Garg et al. [119] aim at repairing performance issues, in which they first retrieve a prompt instruction from a pre-constructed knowledge-base of previous performance bug fixes and then generate a repair prompt using the retrieved instruction. There are studies focusing on the bug fixing of Rust programs [108] or

OCaml programs (an industrial-strength programming language) [111].

**Empirical study about program repair.** There are several studies related to the empirical or experimental evaluation of the various LLMs on program repair, and we summarize the performance in Table 4. Jiang et al. [113], Xia et al. [93], and Zhang et. al. [118] respectively conduct comprehensive experimental evaluations with various LLMs and on different automated program repair benchmarks, while other researchers [89], [96], [98], [100] focus on a specific LLM and on one dataset, e.g., QuixBugs. In addition, Gao et al. [124] empirically investigate the impact of in-context demonstrations for bug fixing, including the selection, order, and number of demonstration examples. Prenner et al. [117] empirically study how the local context (i.e., code that comes before or after the bug location) affects the repair performance. Horv´ath et al. [99] empirically study the impact of program representation and model architecture on the repair performance.

There are two commonly-used repair settings when using LLMs to generate patches: 1) complete function generation (i.e., generating the entire patch function), 2) correct code infilling (i.e., filling in a chunk of code given the prefix and suffix), and different studies might utilize different settings which are marked in Table 4. The commonlyused datasets are QuixBugs, Defects4J, etc. These datasets only involve the fundamental functionalities such as sorting algorithms, each program’s average number of lines ranging from 13 to 22, implementing one functionality, and involving few dependencies. To tackle this, Cao et al. [89] conducts an empirical study on a more complex dataset with DL programs collected from StackOverflow. Every program contains about 46 lines of code on average, implementing several functionalities including data preprocessing, DL model construction, model training, and evaluation. And the dataset involves more than 6 dependencies for each program, including TensorFlow, Keras, and Pytorch. Their results demonstrate a much lower rate of correct patches than in other datasets, which again reveals the potential difficulty of this task. Similarly, Haque et al. [106] introduce a dataset comprising of buggy code submissions and their corresponding fixes collected from online judge platforms, in which it offers an extensive collection of unit tests to enable the evaluations about the correctness of fixes and further information regarding time, memory constraints, and acceptance based on a verdict.

14

![](images/p14-01.png)

Others, 7<br>UniXCoder, 2<br>StarCoder, 3<br>5% 1% BART, 3<br>2%<br>ChatGPT, 36 2% GPT-2, 4<br>25% 3% CodeGPT, 4<br>3%<br>T5, 5<br>4%<br>4% PLBART, 5<br>4% InCoder, 5<br>4% CodeGen, 6<br>16% 5%<br>Codex, 23 GPT-3, 7<br>10%<br>13% GPT-4, 14<br>CodeT5, 18<br>

Fig. 6: LLMs used in the collected papers

## 5 ANALYSIS FROM LLM PERSPECTIVE

This section discusses the analysis based on the viewpoints of LLM, specifically, it’s unfolded from the viewpoints of utilized LLMs, types of prompt engineering, input of the LLMs, as well as the accompanied techniques when utilizing LLM.

### 5.1 LLM Models

As shown in Figure 6, the most commonly utilized LLM in software testing tasks is ChatGPT, which was released on Nov. 2022 by OpenAI. It is trained on a large corpus of natural language text data, and primarily designed for natural language processing and conversation. ChatGPT is the most widely recognized and popular LLM up until now, known for its exceptional performance across various tasks. Therefore, it comes as no surprise that it ranks in the top position in terms of our collected studies.

Codex, an LLM based on GPT-3, is the second most commonly used LLM in our collected studies. It is trained on a massive code corpus containing examples from many programming languages such as JavaScript, Python, C/C++, and Java. Codex was released on Sep. 2021 by OpenAI and powers GitHub Copilot– an AI pair programmer that generates whole code snippets, given a natural language description as a prompt. Since a large portion of our collected studies involve the source code (e.g., repair, unit test case generation), it is not surprising that researchers choose Codex as the LLM in assisting them in accomplishing the codingrelated tasks.

The third-ranked LLM is CodeT5, which is an opensourced LLM developed by salesforce<sup>3</sup> . Thanks to its open source, researchers can easily conduct the pre-training and fine-tuning with domain-specific data to achieve better performance. Similarly, CodeGen is also open-sourced and ranked relatively higher. Besides, for CodeT5 and CodeGen, there are more than half of the related studies involve the empirical evaluations (which employ multiple LLMs), e.g., program repair [112], [113], unit test case generation [39].

3. https://blog.salesforceairesearch.com/codet5/

There are already 14 studies that utilize GPT-4, ranking at the fourth place, which is launched on March 2023. Several studies directly utilize this state-of-the-art LLM of OpenAI, since it demonstrates excellent performance across a wide range of generation and reasoning tasks. For example, Xie et al. utilize GPT-4 to generate fuzzing inputs [67], while Vikram et al. employ it to generate property-based tests with the assistance of API documentation [34]. In addition, some studies conduct experiments using both GPT-4 and ChatGPT or other LLMs to provide a more comprehensive evaluation of these models’ performance. In their proposed LLMempowered automatic penetration testing technique, Deng et al. find that GPT-4 surpasses ChatGPT and LaMDA from Google [62]. Similarly, Zhang et al. find that GPT-4 shows its performance superiority over ChatGPT when generating the fuzz drivers with both the basic query strategies and enhanced query strategies [66]. Furthermore, GPT-4, as a multi-modal LLM, sets itself apart from the other mentioned LLMs by showcasing additional capabilities such as generating image narratives and answering questions based on images [149]. Yet we have not come across any studies that explore the utilization of GPT-4’s image-related features (e.g., UI screenshots, programming screencasts) in software testing tasks.

### 5.2 Types of Prompt Engineering

As shown in Figure 7, among our collected studies, 38 studies utilize the LLMs through pre-training or finetuning schema, while 64 studies employ the prompt engineering to communicate with LLMs to steer its behavior for desired outcomes without updating the model weights. When using the early LLMs, their performances might not be as impressive, so researchers often use pre-training or fine-tuning techniques to adjust the models for specific domains and tasks in order to improve their performance. Then with the upgrading of LLM technology, especially with the introduction of GPT-3 and later LLMs, the knowledge contained within the models and their understanding/inference capability has increased significantly. Therefore, researchers will typically rely on prompt engineering to consider how to design appropriate prompts to stimulate the model’s knowledge.

Among the 64 studies with prompt engineering, 51 studies involve zero-shot learning, and 25 studies involve fewshot learning (a study may involve multiple types). There are also studies involving the chain-of-though (7 studies), self-consistency (1 study), and automatic prompt (1 study).

**Zero-shot learning** is to simply feed the task text to the model and ask for results. Many of the collected studies employ the Codex, CodeT5, and CodeGen (as shown in Section 5.1), which is already trained on source code. Hence, for the tasks dealing with source code like unit test case generation and program repair as demonstrated in previous sections, directly querying the LLM with prompts is the common practice. There are generally two types of manners of zeroshot learning, i.e., with and without instructions. For example, Xie et al. [36] would provide the LLMs with the instructions as “please help me generate a JUnit test for a specific Java method ...” to facilitate the unit test case generation. In contrast, Siddiq et al. [39] only provide the code header

15

![](images/p15-01.png)

ATOmatc prompt. 1<br>Seifconsistency, 1<br>Chain-of though, 7<br>Pre training and/or<br>Fine-tuning, 38<br>Ra Few-shot learning. 25<br>__-Zero-shot learning, 51<br>Prompt engineering, 64<br>

Fig. 7: Distribution about how LLM is used (Note that, a study can involve multiple types of prompt engineering)

of the unit test case (e.g., “class $ _{_ className _}_ $ _{_ suffix _}_ Test _{_ ”), and the LLMs would carry out the unit test case generation automatically. Generally speaking, prompts with clear instructions will yield more accurate results, while prompts without instructions are typically suitable for very specific situations.

**Few-shot learning** presents a set of high-quality demonstrations, each consisting of both input and desired output, on the target task. As the model first sees the examples, it can better understand human intention and criteria for what kinds of answers are wanted, which is especially important for tasks that are not so straightforward or intuitive to the LLM. For example, when conducting the automatic test generation from general bug reports, Kang et al. [78] provide examples of bug reports (questions) and the corresponding bug reproducing tests (answers) to the LLM, and their results show that two examples can achieve the highest performance than no examples or other number of examples. Another example of test assertion generation, Nashid et al. [47] provide demonstrations of the focal method, the test method containing an <AssertPlaceholder>, and the expected assertion, which enables the LLMs to better understand the task.

**Chain-of-thought (CoT) prompting** generates a sequence of short sentences to describe reasoning logics step by step (also known as reasoning chains or rationales) to the LLMs for generating the final answer. For example, for program repair from the natural language issue descriptions [122], given the buggy code and issue report, the authors first ask the LLM to localize the bug, and then they ask it to explain why the localized lines are buggy, finally, they ask the LLM to fix the bug. Another example is for generating unusual programs for fuzzing deep learning libraries, Deng et al. [58] first generate a possible “bug” (bug description) before generating the actual “bug-triggering” code snippet that invokes the target API. The predicted bug description provides an additional hint to the LLM, indicating that the generated code should try to cover specific potential buggy behavior.

**Self-consistency** involves evaluating the coherence and consistency of the LLM’s responses on the same input in different contexts. There is one study with this prompt type, and it is about debugging. Kang et al. [83] employ a hypothesize-observe-conclude loop, which first generates a hypothesis about what the bug is and constructs an experiment to verify, using an LLM, then decide whether the hypothesis is correct based on the experiment result

(with a debugger or code execution) using an LLM, after that, depending on the conclusion, it either starts with a new hypothesis or opts to terminate the debugging process and generate a fix.

**Automatic prompt** aims to automatically generate and select the appropriate instruction for the LLMs, instead of requiring the user to manually engineer a prompt. Xia et al. [67] introduce an auto-prompting step that automatically distils all user-provided inputs into a concise and effective prompt for fuzzing. Specifically, they first generate a list of candidate prompts by incorporating the user inputs and auto prompting instruction while setting the LLM at high temperature, then a small-scale fuzzing experiment is conducted to evaluate each candidate prompt, and the best one is selected.

Note that there are fourteen studies that apply the iterative prompt design when using zero-shot or few-shot learning, in which the approach continuously refines the prompts with the running information of the testing task, e.g., the test failure information. For example, for program repair, Xia et al. [115] interleave patch generation with test validation feedback to prompt future generation iteratively. In detail, they incorporate various information from a failing test including its name, the relevant code line(s) triggering the test failure, and the error message produced in the next round of prompting which can help the model understand the failure reason and provide guidance towards generating the correct fix. Another example is for mobile GUI testing, Liu et al. [14] iteratively query the LLM about the operation (e.g., click a button, enter a text) to be conducted in the mobile app, and at each iteration, they would provide the LLM with current context information like which GUI pages and widgets have just explored.

**Mapping between testing tasks and how LLMs are used.** Figure 8 demonstrates the mapping between the testing tasks (mentioned in Section 4) and how LLMs are used (as introduced in this subsection). The unit test case generation and program repair share similar patterns of communicating with the LLMs, since both tasks are closely related to the source code. Typically, researchers utilize pretraining and/or fine-tuning and zero-shot learning methods for these two tasks. Zero-shot learning is suitable because these tasks are relatively straightforward and can be easily understood by LLMs. Moreover, since the training data for these two tasks can be automatically collected from source code repositories, pre-training and/or fine-tuning methods

16

![](images/p16-01.png)

[—<br>rogram epic isin:<br>unittest<br>Zershotlearing<br>| System test Few-shotleaing<br>sus nays<br>1 — L]EmreChantomatic Thovghtpromy<br>

Fig. 8: Mapping between testing tasks and how LLMs are used

![](images/p16-02.png)

Others, 12<br>View hierarchy file of UI, 6<br>10%<br>5% Error information, 7<br>6%<br>10%<br>Bug description, 12<br>68%<br>Code, 78<br>

Fig. 9: Input of LLM

are widely employed for these two tasks, which can enhance LLMs’ understanding of domain-specific knowledge.

In comparison, for system test input generation, zeroshot learning and few-shot learning methods are commonly used. This might be because this task often involves generating specific types of inputs, and demonstrations in fewshot learning can assist the LLMs in better understanding what should be generated. Besides, for this task, the utilization of pre-training and/or fine-tuning methods are not as widespread as in unit test case generation and program repair. This might be attributed to the fact that training data for system testing varies across different software and is relatively challenging to collect automatically.

### 5.3 Input of LLM

We also find that different testing tasks or software under test might involve diversified input when querying the LLM, as demonstrated in Figure 9.

The most commonly utilized input is the **source code** since a large portion of collected studies relate to program repair or unit test case generation whose input are source code. For unit test case generation, typical code-related information would be (i) the complete focal method, including the signature and body; (ii) the name of the focal class (i.e., the class that the focal method belongs to); (iii) the field in the focal class; and (iv) the signatures of all methods defined in the focal class [7], [26]. For program repair, there can be

different setups and involve different inputs, including (i) inputting a buggy function with the goal of outputting the patched function, (ii) inputting the buggy location with the goal of generating the correct replacement code (can be a single line change) given the prefix and suffix of the buggy function [93]. Besides, there can be variations for the buggy location input, i.e., (i) does not contain the buggy lines (but the bug location is still known), (ii) give the buggy lines as lines of comments.

There are also 12 studies taking the **bug description** as input for the LLM. For example, Kang et al. [78] take the bug description as input when querying LLM and let the LLM generate the bug-reproducing test cases. Fakhoury et al. [122] input the natural language descriptions of bugs to the LLM, and generate the correct code fixes.

There are 7 studies that would provide the **intermediate error information** , e.g., test failure information, to the LLM, and would conduct the iterative prompt (as described in Section 5.2) to enrich the context provided to the LLM. These studies are related to the unit test case generation and program repair, since in these scenarios, the running information can be acquired easily.

When testing mobile apps, since the utilized LLM could not understand the image of the GUI page, the **view hierarchy file** which represents the details of the GUI page usually acts as the input to LLMs. Nevertheless, with the emergence of GPT-4 which is a multimodal model and accepts both image and text inputs for model input, the GUI screenshots might be directly utilized for LLM’s input.

### 5.4 Incorporating Other Techniques with LLM

There are divided opinions on whether LLM has reached an all-powerful status that requires no other techniques. As shown in Figure 10, among our collected studies, 67 of them utilize LLMs to address the entire testing task, while 35 studies incorporate additional techniques. These techniques include mutation testing, differential testing, syntactic checking, program analysis, statistical analysis, etc. .

The reason why researchers still choose to combine LLMs with other techniques might be because, despite exhibiting enormous potential in various tasks, LLMs still possess limitations such as comprehending code semantics and handling complex program structures. Therefore, combining LLMs with other techniques optimizes their strengths and weaknesses to achieve better outcomes in specific scenarios. In addition, it is important to note that while LLMs are capable of generating correct code, they may not necessarily produce sufficient test cases to check for edge cases or rare scenarios. This is where mutation and other testing techniques come into play, as they allow for the generation of more diverse and complex code that can better simulate real-world scenarios. Taken in this sense, a testing approach can incorporate a combination of different techniques, including both LLMs and other testing strategies, to ensure comprehensive coverage and effectiveness.

**LLM + statistical analysis.** As LLMs can often generate a multitude of outputs, manually sifting through and identifying the correct output can be overwhelmingly laborious. As such, researchers have turned to statistical analysis techniques like ranking and clustering [28], [45], [78], [93], [116]

17

![](images/p17-01.png)

+ Others, 3<br>+ Statistic analysis, 10 + Reinforcement leaming, 3<br>LLM+X, 35<br>ER + Differential testing, 5<br>IS<br>pure LLM, 67 Lt Program analysis, 9 + Syntactic repair, 6<br>+ Mutation testing, 7<br>

Fig. 10: Distribution about other techniques incorporated with LLMs (Note that, a study can involve multiple types)

to efficiently filter through LLM’s outputs and ultimately obtain more accurate results.

**LLM + program analysis.** When utilizing LLMs to accomplish tasks such as generating unit test cases and repairing software code, it is important to consider that software code inherently possesses structural information, which may not be fully understood by LLMs. Hence, researchers often utilize program analysis techniques, including code abstract syntax trees (ASTs) [74], to represent the structure of code more effectively and increase the LLM’s ability to comprehend the code accurately. Researchers also perform the structure-based subsetting of code lines to narrow the focus for LLM [94], or extract additional code context from other code files [7], to enable the models to focus on the most task-relevant information in the codebase and lead to more accurate predictions.

**LLM + mutation testing.** It is mainly targeting at generating more diversified test inputs. For example, Deng et al. [59] first use LLM to generate the seed programs (e.g., code snippets using a target DL API) for fuzzing deep learning libraries. To enrich the pool of these test programs, they replace parts of the seed program with masked tokens using mutation operators (e.g., replaces the API call arguments with the span token) to produce masked inputs, and again utilize the LLMs to perform code infilling to generate new code that replaces the masked tokens.

**LLM + syntactic checking.** Although LLMs have shown remarkable performance in various natural language processing tasks, the generated code from these models can sometimes be syntactically incorrect, leading to potential errors and reduced usability. Therefore, researchers have proposed to leverage syntax checking to identify and correct errors in the generated code. For example, in their work for unit test case generation, Alagarsamy et al. [29] additionally introduce a verification method to check and repair the naming consistency (i.e., revising the test method name to be consistent with the focal method name) and the test signatures (i.e., adding missing keywords like public, void, or @test annotations). Xie et al. [36] also validates the generated unit test case and employs rule-based repair to fix syntactic and simple compile errors.

**LLM + differential testing.** Differential testing is wellsuited to find semantic or logic bugs that do not exhibit explicit erroneous behaviors like crashes or assertion failures. In this category of our collected studies, the LLM is mainly responsible for generating valid and diversified inputs, while the differential testing helps to determine

whether there is a triggered bug based on the software’s output. For example, Ye et al. [48] first uses LLM to produce random JavaScript programs, and leverages the language specification document to generate test data, then conduct the differential testing on JavaScript engines such as JavaScriptCore, ChakraCore, SpiderMonkey, QuickJS, etc. There are also studies utilizing the LLMs to generate test inputs and then conduct differential testing for fuzzing DL libraries [58], [59] and SAT solvers [63]. Li et al. [87] employs the LLM in finding the failure-inducing test cases. In detail, given a program under test, they first request the LLM to infer the intention of the program, then request the LLM to generate programs that have the same intention, which are alternative implementations of the program, and are likely free of the program’s bug. Then they perform the differential testing with the program under test and the generated programs to find the failure-inducing test cases.

## 6 CHALLENGES AND OPPORTUNITIES

Based on the above analysis from the viewpoints of software testing and LLM, we summarize the challenges and opportunities when conducting software testing with LLM.

### 6.1 Challenges

As indicated by this survey, software testing with LLMs has undergone significant growth in the past two years. However, it is still in its early stages of development, and numerous challenges and open questions need to be addressed.

### _6.1.1 Challenges for Achieving High Coverage_

Exploring the diverse behaviors of the software under test to achieve high coverage is always a significant concern in software testing. In this context, test generation differs from code generation, as code generation primarily focuses on producing a single, correct code snippet, whereas software testing requires generating diverse test inputs to ensure better coverage of the software. Although setting a high temperature can facilitate the LLMs in generating different outputs, it remains challenging for LLMs to directly achieve the required diversity. For example, for unit test case generation, in SF110 dataset, the line coverage is merely 2% and the branch coverage is merely 1% [39]. For system test input generation, in terms of fuzzing DL libraries, the API coverage for TensorFlow is reported to be 66% (2215/3316) [59].

18

From our collected studies, we observe that the researchers often utilize mutation testing together with the LLMs to generate more diversified outputs. For example, when fuzzing a DL library, instead of directly generating the code snippet with LLM, Deng et al. [59] replace parts of the selected seed (code generated by LLM) with masked tokens using different mutation operators to produce masked inputs. They then leverage the LLM to perform code infilling to generate new code that replaces the masked tokens, which can significantly increase the diversity of the generated tests. Liu et al. [65] leverage LLM to produce the test generators (each of which can yield a batch of unusual text inputs under the same mutation rule) together with the mutation rules for text-oriented fuzzing, which reduces the human effort required for designing mutation rules.

A potential research direction could involve utilizing testing-specific data to train or fine-tune a specialized LLM that is specifically designed to understand the nature of testing. By doing so, the LLM can inherently acknowledge the requirements of testing and autonomously generate diverse outputs.

### _6.1.2 Challenges in Test Oracle Problem_

The oracle problem has been a longstanding challenge in various testing applications, e.g., testing machine learning systems [150] and testing deep learning libraries [59]. To alleviate the oracle problem to the overall testing activities, a common practice in our collected studies is to transform it into a more easily derived form, often by utilizing differential testing [63] or focusing on only identifying crash bugs [14].

There are successful applications of differential testing with LLMs, as shown in Figure 10. For instance, when testing the SMT solvers, Sun et al. adopt differential testing which involves comparing the results of multiple SMT solvers (i.e., Z3, cvc5, and Bitwuzla) on the same generated test formulas by LLM [63]. However, this approach is limited to systems where counterpart software or running environment can easily be found, potentially restricting its applicability. Moreover, to mitigate the oracle problem, other studies only focus on the crash bugs which are easily observed automatically. This is particularly the case for mobile applications testing, in which the LLMs guide the testing in exploring more diversified pages, conducting more complex operational actions, and covering more meaningful operational sequences [14]. However, this significantly restricts the potential of utilizing the LLMs for uncovering various types of software bugs.

Exploring the use of LLMs to derive other types of test oracles represents an interesting and valuable research direction. Specifically, metamorphic testing is also widely used in software testing practices to help mitigate the oracle problem, yet in most cases, defining metamorphic relations relies on human ingenuity. Luu et al. [56] have examined the effectiveness of LLM in generating metamorphic relations, yet they only experiment with straightforward prompts by directly querying ChatGPT. Further exploration, potentially incorporating human-computer interaction or domain knowledge, is highly encouraged. Another promising avenue is exploring the capability of LLMs to automatically

generate test cases based on metamorphic relations, covering a wide range of inputs.

The advancement of multi-model LLMs like GPT-4 may open up possibilities for exploring their ability to detect bugs in software user interfaces and assist in deriving test oracles. By leveraging the image understanding and reasoning capabilities of these models, one can investigate their potential to automatically identify inconsistencies, errors, or usability issues in user interfaces.

### _6.1.3 Challenges for Rigorous Evaluations_

The lack of benchmark datasets and the potential data leakage issues associated with LLM-based techniques present challenges in conducting rigorous evaluations and comprehensive comparisons of proposed methods.

For program repair, there are only two well-known and commonly-used benchmarks, i.e., Defect4J and QuixBugs, as demonstrated in Table 4. Furthermore, these datasets are not specially designed for testing the LLMs. For example, as reported by Xia et al. [93], 39 out of 40 Python bugs in the QuixBugs dataset can be fixed by Codex, yet in real-world practice, the successful fix rate can be nowhere near as high. For unit test case generation, there are no widely recognized benchmarks, and different studies would utilize different datasets for performance evaluation, as demonstrated in Table 3. This indicates the need to build more specialized and diversified benchmarks.

Furthermore, the LLMs may have seen the widely-used benchmarks in their pre-training data, i.e., data leakage issues. Jiang et al. [113] check the CodeSearchNet and BigQuery, which are the data sources of common LLMs, and the results show that four repositories used by the Defect4J benchmark are also in CodeSearchNet, and the whole Defects4J repository is included by BigQuery. Therefore, it is very likely that existing program repair benchmarks are seen by the LLMs during pre-training. This data leakage issue has also been investigated in machine learning-related studies. For example, Tu et al. [151] focus on the data leakage in issue tracking data, and results show that information leaked from the “future” makes prediction models misleadingly optimistic. This reminds us that the performance of LLMs on software testing tasks may not be as good as reported in previous studies. It also suggests that we need more specialized datasets that are not seen by LLMs to serve as benchmarks. One way is to collect it from specialized sources, e.g., user-generated content from niche online communities.

### _6.1.4 Challenges in Real-world Application of LLMs in Software Testing_

As we mentioned in Section 5.2, in the early days of using LLMs, pre-training and fine-tuning are commonly used practice, considering the model parameters are relatively few resulting in weaker model capabilities (e.g., T5). As time progressed, the number of model parameters increased significantly, leading to the emergence of models with greater capabilities (e.g., ChatGPT). And in recent studies, prompt engineering has become a common approach. However, due to concerns regarding data privacy, when considering realworld practice, most software organizations tend to avoid

19

using commercial LLMs and would prefer to adopt opensource ones with training or fine-tuning using organizationspecific data. Furthermore, some companies also consider the current limitations in terms of computational power or pay close attention to energy consumption, they tend to fine-tune medium-sized models. It is quite challenging for these models to achieve similar performance to what our collected papers have reported. For instance, in the widelyused QuixBugs dataset, it has been reported that 39 out of 40 Python bugs and 34 out of 40 Java bugs can be automatically fixed [93]. However, when it comes to DL programs collected from Stack Overflow, which represent real-world coding practice, only 16 out of 72 Python bugs can be automatically fixed [89].

Recent research has highlighted the importance of highquality training data in improving the performance of models for code-related tasks [152], yet manually building highquality organization-specific datasets for training or finetuning is time-consuming and labor-intensive. To address this, one is encouraged to utilize the automated techniques of mining software repositories to build the datasets, for example, techniques like key information extraction techniques from Stack Overflow [153] offer potential solutions for automatically gathering relevant data.

In addition, exploring the methodology for better finetuning the LLMs with software-specific data is worth considering because software-specific data differs from natural language data as it contains more structural information, such as data flow and control flow. Previous research on code representations has shown the benefits of incorporating data flow, which captures the semantic-level structure of code and represents the relationship between variables in terms of “whether-value-comes-from” [154]. These insights can provide valuable guidance for effectively fine-tuning LLMs with software-specific data.

### 6.2 Opportunities

There are also many research opportunities in software testing with LLMs, which can greatly benefit developers, users, and the research community. While not necessarily challenges, these opportunities contribute to advancements in software testing, benefiting practitioners and the wider research community.

### _6.2.1 Exploring LLMs in the Early Stage of Testing_

As shown in Figure 4, LLMs have not been used in the early stage of testing, e.g., test requirements, and test planning. There might be two main reasons behind that. The first is the subjectivity in early-stage testing tasks. Many tasks in the early stages of testing, such as requirements gathering, test plan creation, and design reviews, may involve subjective assessments that require significant input from human experts. This could make it less suitable for LLMs that rely heavily on data-driven approaches. The second might be the lack of open-sourced data in the early stages. Unlike in later stages of testing, there may be limited data available online during early-stage activities. This could mean that LLMs may not have seen much of this type of data, and therefore may not perform well on these tasks.

Adopting a human-computer interaction schema for tackling early-stage testing tasks would harness the domainspecific knowledge of human developers and leverage the general knowledge embedded in LLMs. Additionally, it is highly encouraged for software development companies to record and provide access to early-stage testing data, allowing for improved training and performance of LLMs in these critical testing activities.

### _6.2.2 Exploring LLMs in Other Testing Phases_

We have analyzed the distribution of testing phases for the collected studies. As shown in Fig 11, we can observe that LLMs are most commonly used in unit testing, followed by system testing. However, there is still no research on the use of LLMs in integration testing and acceptance testing.

![](images/p19-01.png)

Unit test 24<br>Integration test 0<br>System test 22<br>Acceptance test 0<br>0 5 10 15 20 25<br>Paper Count<br>Testing Phases<br>

Fig. 11: Distribution of testing phases (note that we omit the studies which do not explicitly specify the testing phases, e.g., program repair)

For integration testing, it involves testing the interfaces between different software modules. In some software organizations, integration testing might be merged with unit testing, which can be a possible reason why LLM is rarely utilized in integration testing. Another reason might be that the size and complexity of the input data in this circumstance may exceed the capacity of the LLM to process and analyze (e.g., the source code of all involved software modules), which can lead to errors or unreliable results. To tackle this, a potential reference can be found in Section 4.1, where Xie et al. [36] design a method to organize the necessary information into the pre-defined maximum prompt token limit of the LLM. Furthermore, integration testing requires diversified data to be generated to sufficiently test the interface among multiple modules. As mentioned in Section 4.3, previous work has demonstrated the LLM’s capability in generating diversified test input for system testing, in conjunction with mutation testing techniques [48], [59]. And these can provide insights about generating the diversified interface data for integration testing.

Acceptance testing is usually conducted by business analysts or end-users to validate the system’s functionality and usability, which requires more non-technical language and domain-specific knowledge, thus making it challenging to apply LLM effectively. Since acceptance testing involves humans, it is well-suited for the use of human-in-the-loop schema with LLMs. This has been studied in traditional machine learning [155], but has not yet been explored with LLMs. Specifically, the LLMs can be responsible for automatically generating test cases, evaluating test coverage, etc, while human testers are responsible for checking the program’s behavior and verifying test oracle.

20

### _6.2.3 Exploring LLMs for More Types of Software_

We analyze what types of software have been explored in the collected studies, as shown in Figure 5. Note that, since a large portion of studies are focused on unit testing or program repair, they are conducted on publicly available datasets and do not involve specific software types.

From the analysis in Section 4.3, the LLM can generate not only the source code for testing DL libraries but also the textual input for testing mobile apps, even the models for testing CPS. Overall, the LLM provides a flexible and powerful framework for generating test inputs for a wide range of applications. Its versatility would make it useful for testing the software in other domains.

From one point of view, some proposed techniques can be applied to other types of software. For example, in the paper proposed for testing deep learning libraries [58], since it proposes techniques for generating diversified, complicated, and human-like DL programs, the authors state that the approach can be easily extended to test software systems from other application domains, e.g., interpreters, database systems, and other popular libraries. More than that, there are already studies that focus on universal fuzzing techniques [52], [67] which are designed to be adaptable and applicable to different types of test inputs and software.

From another point of view, other types of software can also benefit from the capabilities of LLMs to design the testing techniques that are better suited to their specific domain and characteristics. For instance, the metaverse, with its immersive virtual environments and complex interactions, presents unique challenges for software testing. LLMs can be leveraged to generate diverse and realistic inputs that mimic user behavior and interactions within the metaverse, which are never explored.

### _6.2.4 Exploring LLMs for Non-functional Testing_

In our collected studies, LLMs are primarily used for functional testing, and no practice in performance testing, usability testing or others. One possible reason for the prevalence of LLM-based solutions in functional testing is that they can convert functional testing problems into code generation or natural language generation problems [14], [59], which LLMs are particularly adept at solving.

On the other hand, performance testing and usability testing may require more specialized models that are designed to detect and analyze specific types of data, handle complex statistical analyses, or determine the buggy criteria. Moreover, there have been dozens of performance testing tools (e.g., LoadRunner [156]) that can generate a workload that simulates real-world usage scenarios and achieve relatively satisfactory performance.

The potential opportunities might let the LLM integrate the performance testing tools and acts like the LangChain [157], to better simulate different types of workloads based on real user behavior. Furthermore, the LLMs can identify the parameter combinations and values that have the highest potential to trigger performance problems. It is essentially a way to rank and prioritize different parameter settings based on their impact on performance and improve the efficiency of performance testing.

### _6.2.5 Exploring Advanced Prompt Engineering_

There are a total of 11 commonly used prompt engineering techniques as listed in a popular prompt engineering guide [158], as shown in Figure 12. Currently, in our collected studies, only the first five techniques are being utilized. The more advanced techniques have not been employed yet, and can be explored in the future for prompt design.

![](images/p20-01.png)

Zero-shot learning 51<br>Few-shot learning 25<br>Chain-of-thought 7<br>Self-consistency 1<br>Automatic prompt 1<br>Generate knowledge prompt 0<br>Tree-of-thoughts 0<br>Active-prompt 0<br>Directional stimulus prompt 0<br>ReAct prompt 0<br>Multimodal chain-of-thought 0<br>Graph prompt 0<br>Automatic reasoning 0<br>and tool-use<br>0 10 20 30 40 50<br>Paper Count<br>Prompt Engineering<br>

Fig. 12: List of advanced prompt engineering practices and those utilized in the collected papers

For instance, multimodal chain of thought prompting involves using diverse sensory and cognitive cues to stimulate thinking and creativity in LLMs [159]. By providing images (e.g., GUI screenshots) or audio recordings related to the software under test can help the LLM better understand the software’s context and potential issues. Besides, try to prompt the LLM to imagine itself in different roles, such as a developer, user, or quality assurance specialist. This perspective-shifting exercise enables the LLM to approach software testing from multiple viewpoints and uncover different aspects that might require attention or investigation.

Graph prompting [160] involves the representation of information using graphs or visual structures to facilitate understanding and problem-solving. Graph prompting can be a natural match with software engineering, consider it involves various dependencies, control flow, data flow, state transitions, or other relevant graph structure. Graph prompting can be beneficial in analyzing this structural information, and enabling the LLMs to comprehend the software under test effectively. For instance, testers can use graph prompts to visualize test coverage, identify untested areas or paths, and ensure adequate test execution.

### _6.2.6 Incorporating LLMs with Traditional Techniques_

There is currently no clear consensus on the extent to which LLMs can solve software testing problems. From the analysis in Section 5.4, we have seen some promising results from studies that have combined LLMs with traditional software testing techniques. This implies the LLMs are not the sole silver bullet for software testing. Considering the availability of many mature software testing techniques and tools, and the limited capabilities of LLMs, it is necessary to explore other better ways to combine LLMs with traditional testing or program analysis techniques and tools for better software testing.

21

Based on the collected studies, the LLMs have been successfully utilized together with various techniques such as differential testing (e.g., [63]), mutation testing (e.g., [59]), program analysis (e.g., [104], as shown in Figure 10. From one perspective, future studies can explore improved integration of these traditional techniques with LLMs. Take mutation testing as an example, current practices mainly rely on the human-designed mutation rules to mutate the candidate tests, and let the LLMs re-generate new tests [38], [59], [67], while Liu et al. directly utilize the LLMs for producing the mutation rules alongside the mutated tests [65]. Further explorations in this direction are of great interest.

From another point of view, more traditional techniques can be incorporated in LLMs for software testing. For instance, besides the aforementioned traditional techniques, the LLMs have been combined with formal verification for self-healing software detection in the field of software security [161]. More attempts are encouraged. Moreover, considering the existence of numerous mature software testing tools, one can explore the integration of LLMs with these tools, allowing them to act as a “LangChain” to better explore the potential of these tools.

## 7 RELATED WORK

The systematic literature review is a crucial manner for gaining insights into the current trends and future directions within a particular field. It enables us to understand and stay updated on the developments in that domain.

Wang et al. surveyed the machine learning and deep learning techniques for software engineering [162]. Yang et al. and Watson et al. respectively carried out surveys about the use of deep learning in software engineering domain [163], [164]. Bajammal et al. surveyed the utilization of computer vision techniques to improve software engineering tasks [165]. Zhang et al. provided a survey of techniques for testing machine learning systems [150]

With the advancements of artificial intelligence and LLMs, researchers also conduct systematic literature reviews about LLMs, and their applications in various fields (e.g., software engineering). Zhao et al. [17] reviewed recent advances in LLMs by providing an overview of their background, key findings, and mainstream techniques. They focused on four major aspects of LLMs, namely pre-training, adaptation tuning, utilization, and capacity evaluation. Additionally, they summarized the available resources for developing LLMs and discuss the remaining issues for future directions. Hou et al. conducted a systematic literature review on using LLMs for software engineering, with a particular focus on understanding how LLMs can be exploited to optimize processes and outcomes [166]. Fan et al. conducted a survey of LLMs for software engineering, and set out open research challenges for the application of LLMs to technical problems faced by software engineers [167]. Zan et al. conducted a survey of existing LLMs for NL2Code task (i.e., generating code from a natural language description), and reviewed benchmarks and metrics [168].

While these studies either targeted the broader software engineering domain (with a limited focus on software testing tasks) or focused on other software development tasks

(excluding software testing), this paper specifically focuses on the use of LLMs for software testing. It surveys related studies, summarizes key challenges and potential opportunities, and serves as a roadmap for future research in this area.

## 8 CONCLUSION

This paper provides a comprehensive review of the use of LLMs in software testing. We have analyzed relevant studies that have utilized LLMs in software testing from both the software testing and LLMs perspectives. This paper also highlights the challenges and potential opportunities in this direction. Results of this review demonstrate that LLMs have been successfully applied in a wide range of testing tasks, including unit test case generation, test oracle generation, system test input generation, program debugging, and program repair. However, challenges still exist in achieving high testing coverage, addressing the test oracle problem, conducting rigorous evaluations, and applying LLMs in real-world scenarios. Additionally, it is observed that LLMs are commonly used in only a subset of the entire testing lifecycle, for example, they are primarily utilized in the middle and later stages of testing, only serving the unit and system testing phases, and only for functional testing. This highlights the research opportunities for exploring the uncovered areas. Regarding how the LLMs are utilized, we find that various pre-training/fine-tuning and prompt engineering methods have been developed to enhance the capabilities of LLMs in addressing testing tasks. However, more advanced techniques in prompt design have yet to be explored and can be an avenue for future research.

It can serve as a roadmap for future research in this area, identifying gaps in our current understanding of the use of LLMs in software testing and highlighting potential avenues for exploration. We believe that the insights provided in this paper will be valuable to both researchers and practitioners in the field of software engineering, assisting them in leveraging LLMs to improve software testing practices and ultimately enhance the quality and reliability of software systems.

## REFERENCES

- [1] G. J. Myers, _The art of software testing (2. ed.)_ . Wiley, 2004. [Online]. Available: http://eu.wiley.com/WileyCDA/ WileyTitle/productCd-0471469122.html

- [2] M. Pezz`e and M. Young, _Software testing and analysis - process, principles and techniques_ . Wiley, 2007.

- [3] M. Harman and P. McMinn, “A theoretical and empirical study of search-based testing: Local, global, and hybrid search,” vol. 36, no. 2, 2010, pp. 226–247.

- [4] P. Delgado-P´erez, A. Ram´ırez, K. J. Valle-G´omez, I. MedinaBulo, and J. R. Romero, “Interevo-tr: Interactive evolutionary test generation with readability assessment,” _IEEE Trans. Software Eng._ , vol. 49, no. 4, pp. 2580–2596, 2023.

- [5] X. Xiao, S. Li, T. Xie, and N. Tillmann, “Characteristic studies of loop problems for structural test generation via symbolic execution,” in _2013 28th IEEE/ACM International Conference on Automated Software Engineering, ASE 2013, Silicon Valley, CA, USA, November 11-15, 2013_ , E. Denney, T. Bultan, and A. Zeller, Eds. IEEE, 2013, pp. 246–256.

- [6] C. Pacheco, S. K. Lahiri, M. D. Ernst, and T. Ball, “Feedbackdirected random test generation,” in _29th International Conference on Software Engineering (ICSE 2007), Minneapolis, MN, USA, May 20-26, 2007_ . IEEE Computer Society, 2007, pp. 75–84.

22

- [7] Z. Yuan, Y. Lou, M. Liu, S. Ding, K. Wang, Y. Chen, and X. Peng, “No more manual tests? evaluating and improving chatgpt for unit test generation,” _arXiv preprint arXiv:2305.04207_ , 2023.

- [8] Y. Tang, Z. Liu, Z. Zhou, and X. Luo, “Chatgpt vs SBST: A comparative assessment of unit test suite generation,” _CoRR_ , vol. abs/2307.00588, 2023. [Online]. Available: https: //doi.org/10.48550/arXiv.2307.00588

- [9] A. Developers, “Ui/application exerciser monkey,” 2012.

- [10] Y. Li, Z. Yang, Y. Guo, and X. Chen, “Droidbot: a lightweight uiguided test input generator for android,” in _ICSE_ . IEEE, 2017.

- [11] T. Su, G. Meng, Y. Chen, K. Wu, W. Yang, Y. Yao, G. Pu, Y. Liu, and Z. Su, “Guided, stochastic model-based gui testing of android apps,” in _Proceedings of the 2017 11th Joint Meeting on Foundations of Software Engineering_ , 2017, pp. 245–256.

- [12] Z. Dong, M. B¨ohme, L. Cojocaru, and A. Roychoudhury, “Timetravel testing of android apps,” in _ICSE_ . IEEE, 2020.

- [13] M. Pan, A. Huang, G. Wang, T. Zhang, and X. Li, “Reinforcement learning based curiosity-driven testing of android applications,” in _Proceedings of the 29th ACM SIGSOFT International Symposium on Software Testing and Analysis_ , 2020, pp. 153–164.

- [14] Z. Liu, C. Chen, J. Wang, M. Chen, B. Wu, X. Che, D. Wang, and Q. Wang, “Make LLM a testing expert: Bringing humanlike interaction to mobile GUI testing via functionality-aware decisions,” _CoRR_ , vol. abs/2310.15780, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2310.15780

- [15] T. Su, J. Wang, and Z. Su, “Benchmarking automated GUI testing for android against real-world bugs,” in _ESEC/FSE ’21: 29th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering, Athens, Greece, August 2328, 2021_ . ACM, 2021, pp. 119–130.

- [16] M. Shanahan, “Talking about large language models,” _CoRR_ , vol. abs/2212.03551, 2022. [Online]. Available: https: //doi.org/10.48550/arXiv.2212.03551

- [17] W. X. Zhao, K. Zhou, J. Li, T. Tang, X. Wang, Y. Hou, Y. Min, B. Zhang, J. Zhang, Z. Dong, Y. Du, C. Yang, Y. Chen, Z. Chen, J. Jiang, R. Ren, Y. Li, X. Tang, Z. Liu, P. Liu, J. Nie, and J. Wen, “A survey of large language models,” _CoRR_ , vol. abs/2303.18223, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2303.18223

- [18] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa, “Large language models are zeroshot reasoners,” in _NeurIPS_ , 2022. [Online]. Available: http://papers.nips.cc/paper <u>files/paper/2022/hash/</u> 8bb0d291acd4acf06ef112099c16f326-Abstract-Conference.html

- [19] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi, Q. V. Le, and D. Zhou, “Chain-of-thought prompting elicits reasoning in large language models,” in _NeurIPS_ , 2022. [Online]. Available: http://papers.nips.cc/paper <u>files/paper/2022/hash/</u> 9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html

- [20] J. Li, G. Li, Y. Li, and Z. Jin, “Structured chain-of-thought prompting for code generation,” 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:258615421

- [21] J. Li, Y. Li, G. Li, Z. Jin, Y. Hao, and X. Hu, “Skcoder: A sketch-based approach for automatic code generation,” in _2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE)_ , 2023, pp. 2124–2135.

- [22] J. Li, Y. Zhao, Y. Li, G. Li, and Z. Jin, “Acecoder: Utilizing existing code to enhance code generation,” 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:257901190

- [23] Y. Dong, X. Jiang, Z. Jin, and G. Li, “Self-collaboration code generation via chatgpt,” _CoRR_ , vol. abs/2304.07590, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2304.07590

- [24] S. Pan, L. Luo, Y. Wang, C. Chen, J. Wang, and X. Wu, “Unifying large language models and knowledge graphs: A roadmap,” _CoRR_ , vol. abs/2306.08302, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2306.08302

- [25] G. J. Myers, T. Badgett, T. M. Thomas, and C. Sandler, _The art of software testing_ . Wiley Online Library, 2004, vol. 2.

- [26] M. Tufano, D. Drain, A. Svyatkovskiy, S. K. Deng, and N. Sundaresan, “Unit test case generation with transformers and focal context,” _arXiv preprint arXiv:2009.05617_ , 2020.

- [27] B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin, J.-G. Lou, and W. Chen, “Codet: Code generation with generated tests,” _arXiv preprint arXiv:2207.10397_ , 2022.

- [28] S. K. Lahiri, A. Naik, G. Sakkas, P. Choudhury, C. von Veh, M. Musuvathi, J. P. Inala, C. Wang, and J. Gao, “Interactive

   - code generation via test-driven user-intent formalization,” _arXiv preprint arXiv:2208.05950_ , 2022.

- [29] S. Alagarsamy, C. Tantithamthavorn, and A. Aleti, “A3test: Assertion-augmented automated test case generation,” _arXiv preprint arXiv:2302.10352_ , 2023.

- [30] M. Sch¨afer, S. Nadi, A. Eghbali, and F. Tip, “An empirical evaluation of using large language models for automated unit test generation,” _IEEE Transactions on Software Engineering_ , pp. 1–21, 2023.

- [31] V. Guilherme and A. Vincenzi, “An initial investigation of chatgpt unit test generation capability,” in _8th Brazilian Symposium on Systematic and Automated Software Testing, SAST 2023, Campo Grande, MS, Brazil, September 25-29, 2023_ , A. L. Font˜ao, D. M. B. Paiva, H. Borges, M. I. Cagnin, P. G. Fernandes, V. Borges, S. M. Melo, V. H. S. Durelli, and E. D. Canedo, Eds. ACM, 2023, pp. 15–24. [Online]. Available: https://doi.org/10.1145/3624032.3624035

- [32] S. Hashtroudi, J. Shin, H. Hemmati, and S. Wang, “Automated test case generation using code models and domain adaptation,” _CoRR_ , vol. abs/2308.08033, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2308.08033

- [33] L. Plein, W. C. Ou´edraogo, J. Klein, and T. F. Bissyand´e, “Automatic generation of test cases based on bug reports: a feasibility study with large language models,” _CoRR_ , vol. abs/2310.06320, 2023. [Online]. Available: https://doi.org/10. 48550/arXiv.2310.06320

- [34] V. Vikram, C. Lemieux, and R. Padhye, “Can large language models write good property-based tests?” _CoRR_ , vol. abs/2307.04346, 2023. [Online]. Available: https://doi.org/ 10.48550/arXiv.2307.04346

- [35] N. Rao, K. Jain, U. Alon, C. L. Goues, and V. J. Hellendoorn, “CAT-LM training language models on aligned code and tests,” in _38th IEEE/ACM International Conference on Automated Software Engineering, ASE 2023, Luxembourg, September 1115, 2023_ . IEEE, 2023, pp. 409–420. [Online]. Available: https://doi.org/10.1109/ASE56229.2023.00193

- [36] Z. Xie, Y. Chen, C. Zhi, S. Deng, and J. Yin, “Chatunitest: a chatgpt-based automated unit test generation tool,” _arXiv preprint arXiv:2305.04764_ , 2023.

- [37] C. Lemieux, J. P. Inala, S. K. Lahiri, and S. Sen, “Codamosa: Escaping coverage plateaus in test generation with pre-trained large language models,” in _International conference on software engineering (ICSE)_ , 2023.

- [38] A. M. Dakhel, A. Nikanjam, V. Majdinasab, F. Khomh, and M. C. Desmarais, “Effective test generation using pre-trained large language models and mutation testing,” _CoRR_ , vol. abs/2308.16557, 2023. [Online]. Available: https: //doi.org/10.48550/arXiv.2308.16557

- [39] M. L. Siddiq, J. Santos, R. H. Tanvir, N. Ulfat, F. A. Rifat, and V. C. Lopes, “Exploring the effectiveness of large language models in generating unit tests,” _arXiv preprint arXiv:2305.00418_ , 2023.

- [40] Y. Zhang, W. Song, Z. Ji, D. Yao, and N. Meng, “How well does LLM generate security tests?” _CoRR_ , vol. abs/2310.00710, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2310.00710

- [41] V. Li and N. Doiron, “Prompting code interpreter to write better unit tests on quixbugs functions,” _CoRR_ , vol. abs/2310.00483, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2310. 00483

- [42] B. Steenhoek, M. Tufano, N. Sundaresan, and A. Svyatkovskiy, “Reinforcement learning from automatic feedback for highquality unit test generation,” 2023.

- [43] S. Bhatia, T. Gandhi, D. Kumar, and P. Jalote, “Unit test generation using generative ai : A comparative performance analysis of autogeneration tools,” 2023.

- [44] M. Tufano, D. Drain, A. Svyatkovskiy, and N. Sundaresan, “Generating accurate assert statements for unit test cases using pretrained transformers,” in _Proceedings of the 3rd ACM/IEEE International Conference on Automation of Software Test_ , 2022, pp. 54–64.

- [45] P. Nie, R. Banerjee, J. J. Li, R. J. Mooney, and M. Gligoric, “Learning deep semantics for test completion,” _arXiv preprint arXiv:2302.10166_ , 2023.

- [46] A. Mastropaolo, N. Cooper, D. Nader-Palacio, S. Scalabrino, D. Poshyvanyk, R. Oliveto, and G. Bavota, “Using transfer learning for code-related tasks,” _IEEE Trans. Software Eng._ , vol. 49, no. 4, pp. 1580–1598, 2023. [Online]. Available: https://doi.org/10.1109/TSE.2022.3183297

23

- [47] N. Nashid, M. Sintaha, and A. Mesbah, “Retrieval-based prompt selection for code-related few-shot learning,” in _Proceedings of the 45th International Conference on Software Engineering (ICSE’23)_ , 2023.

- [48] G. Ye, Z. Tang, S. H. Tan, S. Huang, D. Fang, X. Sun, L. Bian, H. Wang, and Z. Wang, “Automated conformance testing for javascript engines via deep compiler fuzzing,” in _Proceedings of the 42nd ACM SIGPLAN international conference on programming language design and implementation_ , 2021, pp. 435–450.

- [49] Z. Liu, C. Chen, J. Wang, X. Che, Y. Huang, J. Hu, and Q. Wang, “Fill in the blank: Context-aware automated text input generation for mobile gui testing,” _arXiv preprint arXiv:2212.04732_ , 2022.

- [50] M. R. Taesiri, F. Macklon, Y. Wang, H. Shen, and C.-P. Bezemer, “Large language models are pretty good zero-shot video game bug detectors,” _arXiv preprint arXiv:2210.02506_ , 2022.

- [51] S. L. Shrestha and C. Csallner, “Slgpt: using transfer learning to directly generate simulink model files and find bugs in the simulink toolchain,” in _Evaluation and Assessment in Software Engineering_ , 2021, pp. 260–265.

- [52] J. Hu, Q. Zhang, and H. Yin, “Augmenting greybox fuzzing with generative AI,” _CoRR_ , vol. abs/2306.06782, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2306.06782

- [53] A. Mathur, S. Pradhan, P. Soni, D. Patel, and R. Regunathan, “Automated test case generation using t5 and gpt-3,” in _2023 9th International Conference on Advanced Computing and Communication Systems (ICACCS)_ , vol. 1, 2023, pp. 1986–1992.

- [54] D. Zimmermann and A. Koziolek, “Automating gui-based software testing with gpt-3,” in _2023 IEEE International Conference on Software Testing, Verification and Validation Workshops (ICSTW)_ , 2023, pp. 62–65.

- [55] M. Taeb, A. Swearngin, E. Schoop, R. Cheng, Y. Jiang, and J. Nichols, “Axnav: Replaying accessibility tests from natural language,” _CoRR_ , vol. abs/2310.02424, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2310.02424

- [56] Q. Luu, H. Liu, and T. Y. Chen, “Can chatgpt advance software testing intelligence? an experience report on metamorphic testing,” _CoRR_ , vol. abs/2310.19204, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2310.19204

- [57] A. Khanfir, R. Degiovanni, M. Papadakis, and Y. L. Traon, “Efficient mutation testing via pre-trained language models,” _arXiv preprint arXiv:2301.03543_ , 2023.

- [58] Y. Deng, C. S. Xia, C. Yang, S. D. Zhang, S. Yang, and L. Zhang, “Large language models are edge-case fuzzers: Testing deep learning libraries via fuzzgpt,” _arXiv preprint arXiv:2304.02014_ , 2023.

- [59] ——, “Large language models are zero shot fuzzers: Fuzzing deep learning libraries via large language models,” _arXiv preprint arXiv:2209.11515_ , 2023.

- [60] J. Ackerman and G. Cybenko, “Large language models for fuzzing parsers (registered report),” in _Proceedings of the 2nd International Fuzzing Workshop, FUZZING 2023, Seattle, WA, USA, 17 July 2023_ , M. B¨ohme, Y. Noller, B. Ray, and L. Szekeres, Eds. ACM, 2023, pp. 31–38. [Online]. Available: https://doi.org/10.1145/3605157.3605173

- [61] S. Yu, C. Fang, Y. Ling, C. Wu, and Z. Chen, “LLM for test script generation and migration: Challenges, capabilities, and opportunities,” _CoRR_ , vol. abs/2309.13574, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2309.13574

- [62] G. Deng, Y. Liu, V. M. Vilches, P. Liu, Y. Li, Y. Xu, T. Zhang, Y. Liu, M. Pinzger, and S. Rass, “Pentestgpt: An llm-empowered automatic penetration testing tool,” _CoRR_ , vol. abs/2308.06782, 2023. [Online]. Available: https: //doi.org/10.48550/arXiv.2308.06782

- [63] M. Sun, Y. Yang, Y. Wang, M. Wen, H. Jia, and Y. Zhou, “SMT solver validation empowered by large pre-trained language models,” in _38th IEEE/ACM International Conference on Automated Software Engineering, ASE 2023, Luxembourg, September 11-15, 2023_ . IEEE, 2023, pp. 1288–1300. [Online]. Available: https://doi.org/10.1109/ASE56229.2023.00180

- [64] Y. Deng, J. Yao, Z. Tu, X. Zheng, M. Zhang, and T. Zhang, “Target: Automated scenario generation from traffic rules for testing autonomous vehicles,” 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:258588387

- [65] Z. Liu, C. Chen, J. Wang, M. Chen, B. Wu, X. Che, D. Wang, and Q. Wang, “Testing the limits: Unusual text inputs generation for mobile app crash detection with large language

model,” _CoRR_ , vol. abs/2310.15657, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2310.15657

- [66] C. Zhang, M. Bai, Y. Zheng, Y. Li, X. Xie, Y. Li, W. Ma, L. Sun, and Y. Liu, “Understanding large language model based fuzz driver generation,” _CoRR_ , vol. abs/2307.12469, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2307.12469

- [67] C. Xia, M. Paltenghi, J. Tian, M. Pradel, and L. Zhang, “Universal fuzzing via large language models,” _ArXiv_ , vol. abs/2308.04748, 2023. [Online]. Available: https://api. semanticscholar.org/CorpusID:260735598

- [68] C. Tsigkanos, P. Rani, S. M¨uller, and T. Kehrer, “Variable discovery with large language models for metamorphic testing of scientific software,” in _Computational Science - ICCS 2023 - 23rd International Conference, Prague, Czech Republic, July 3-5, 2023, Proceedings, Part I_ , ser. Lecture Notes in Computer Science, J. Mikyska, C. de Mulatier, M. Paszynski, V. V. Krzhizhanovskaya, J. J. Dongarra, and P. M. A. Sloot, Eds., vol. 14073. Springer, 2023, pp. 321–335. [Online]. Available: https://doi.org/10.1007/978-3-031-35995-8 <u>23</u>

- [69] C. Yang, Y. Deng, R. Lu, J. Yao, J. Liu, R. Jabbarvand, and L. Zhang, “White-box compiler fuzzing empowered by large language models,” _CoRR_ , vol. abs/2310.15991, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2310.15991

- [70] T. Zhang, I. C. Irsan, F. Thung, D. Han, D. Lo, and L. Jiang, “itiger: an automatic issue title generation tool,” in _Proceedings of the 30th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering_ , 2022, pp. 1637–1641.

- [71] Y. Huang, J. Wang, Z. Liu, Y. Wang, S. Wang, C. Chen, Y. Hu, and Q. Wang, “Crashtranslator: Automatically reproducing mobile application crashes directly from stack trace,” _CoRR_ , vol. abs/2310.07128, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2310.07128

- [72] T. Zhang, I. C. Irsan, F. Thung, and D. Lo, “Cupid: Leveraging chatgpt for more accurate duplicate bug report detection,” _CoRR_ , vol. abs/2308.10022, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2308.10022

- [73] U. Mukherjee and M. M. Rahman, “Employing deep learning and structured information retrieval to answer clarification questions on bug reports,” 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:259501524

- [74] P. Mahbub, O. Shuvo, and M. M. Rahman, “Explaining software bugs leveraging code structures in neural machine translation,” _arXiv preprint arXiv:2212.04584_ , 2022.

- [75] S. Feng and C. Chen, “Prompting is all your need: Automated android bug replay with large language models,” _CoRR_ , vol. abs/2306.01987, 2023. [Online]. Available: https: //doi.org/10.48550/arXiv.2306.01987

- [76] Y. Su, Z. Han, Z. Gao, Z. Xing, Q. Lu, and X. Xu, “Still confusing for bug-component triaging? deep feature learning and ensemble setting to rescue,” in _31st IEEE/ACM International Conference on Program Comprehension, ICPC 2023, Melbourne, Australia, May 15-16, 2023_ . IEEE, 2023, pp. 316–327. [Online]. Available: https://doi.org/10.1109/ICPC58990.2023.00046

- [77] N. D. Bui, Y. Wang, and S. Hoi, “Detect-localize-repair: A unified framework for learning to debug with codet5,” _arXiv preprint arXiv:2211.14875_ , 2022.

- [78] S. Kang, J. Yoon, and S. Yoo, “Large language models are few-shot testers: Exploring llm-based general bug reproduction,” _arXiv preprint arXiv:2209.11515_ , 2022.

- [79] S. Kang, G. An, and S. Yoo, “A preliminary evaluation of llm-based fault localization,” _CoRR_ , vol. abs/2308.05487, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2308.05487

- [80] P. Widjojo and C. Treude, “Addressing compiler errors: Stack overflow or large language models?” _CoRR_ , vol. abs/2307.10793, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2307. 10793

- [81] L. Plein and T. F. Bissyand´e, “Can llms demystify bug reports?” _CoRR_ , vol. abs/2310.06310, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2310.06310

- [82] A. Taylor, A. Vassar, J. Renzella, and H. A. Pearce, “Dcc –help: Generating context-aware compiler error explanations with large language models,” 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:261076439

- [83] S. Kang, B. Chen, S. Yoo, and J.-G. Lou, “Explainable automated debugging via large language model-driven scientific debugging,” _arXiv preprint arXiv:2304.02195_ , 2023.

24

- [84] A. Z. H. Yang, R. Martins, C. L. Goues, and V. J. Hellendoorn, “Large language models for test-free fault localization,” _CoRR_ , vol. abs/2310.01726, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2310.01726

- [85] Y. Wu, Z. Li, J. M. Zhang, M. Papadakis, M. Harman, and Y. Liu, “Large language models in fault localisation,” _CoRR_ , vol. abs/2308.15276, 2023. [Online]. Available: https: //doi.org/10.48550/arXiv.2308.15276

- [86] H. Tu, Z. Zhou, H. Jiang, I. N. B. Yusuf, Y. Li, and L. Jiang, “LLM4CBI: taming llms to generate effective test programs for compiler bug isolation,” _CoRR_ , vol. abs/2307.00593, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2307.00593

- [87] T.-O. Li, W. Zong, Y. Wang, H. Tian, Y. Wang, S.-C. Cheung, and J. Kramer, “Nuances are the key: Unlocking chatgpt to find failure-inducing tests with differential prompting,” in _2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE)_ , 2023, pp. 14–26.

- [88] X. Chen, M. Lin, N. Sch¨arli, and D. Zhou, “Teaching large language models to self-debug,” _CoRR_ , vol. abs/2304.05128, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2304.05128

- [89] J. Cao, M. Li, M. Wen, and S.-c. Cheung, “A study on prompt design, advantages and limitations of chatgpt for deep learning program repair,” _arXiv preprint arXiv:2304.08191_ , 2023.

- [90] H. Pearce, B. Tan, B. Ahmad, R. Karri, and B. Dolan-Gavitt, “Examining zero-shot vulnerability repair with large language models,” in _2023 IEEE Symposium on Security and Privacy (SP)_ . IEEE Computer Society, 2022, pp. 1–18.

- [91] Z. Fan, X. Gao, A. Roychoudhury, and S. H. Tan, “Automated repair of programs from large language models,” _arXiv preprint arXiv:2205.10583_ , 2022.

- [92] Y. Hu, X. Shi, Q. Zhou, and L. Pike, “Fix bugs with transformer through a neural-symbolic edit grammar,” _arXiv preprint arXiv:2204.06643_ , 2022.

- [93] C. S. Xia, Y. Wei, and L. Zhang, “Practical program repair in the era of large pre-trained language models,” _arXiv preprint arXiv:2210.14179_ , 2022.

- [94] J. Zhang, J. Cambronero, S. Gulwani, V. Le, R. Piskac, G. Soares, and G. Verbruggen, “Repairing bugs in python assignments using large language models,” _arXiv preprint arXiv:2209.14876_ , 2022.

- [95] M. Lajk´o, V. Csuvik, and L. Vid´acs, “Towards javascript program repair with generative pre-trained transformer (gpt-2),” in _Proceedings of the Third International Workshop on Automated Program Repair_ , 2022, pp. 61–68.

- [96] D. Sobania, M. Briesch, C. Hanna, and J. Petke, “An analysis of the automatic bug fixing performance of chatgpt,” _arXiv preprint arXiv:2301.08653_ , 2023.

- [97] K. Huang, X. Meng, J. Zhang, Y. Liu, W. Wang, S. Li, and Y. Zhang, “An empirical study on fine-tuning large language models of code for automated program repair,” in _38th IEEE/ACM International Conference on Automated Software Engineering, ASE 2023, Luxembourg, September 1115, 2023_ . IEEE, 2023, pp. 1162–1174. [Online]. Available: https://doi.org/10.1109/ASE56229.2023.00181

- [98] M. C. Wuisang, M. Kurniawan, K. A. Wira Santosa, A. Agung Santoso Gunawan, and K. E. Saputra, “An evaluation of the effectiveness of openai’s chatgpt for automated python program bug fixing using quixbugs,” in _2023 International Seminar on Application for Technology of Information and Communication (iSemantic)_ , 2023, pp. 295–300.

- [99] D. Horv´ath, V. Csuvik, T. Gyim´othy, and L. Vid´acs, “An extensive study on model architecture and program representation in the domain of learning-based automated program repair,” in _IEEE/ACM International Workshop on Automated Program Repair, APR@ICSE 2023, Melbourne, Australia, May 16, 2023_ . IEEE, 2023, pp. 31–38. [Online]. Available: https://doi.org/10.1109/APR59189.2023.00013

- [100] J. A. Prenner, H. Babii, and R. Robbes, “Can openai’s codex fix bugs? an evaluation on quixbugs,” in _Proceedings of the Third International Workshop on Automated Program Repair_ , 2022, pp. 69– 75.

- [101] W. Yuan, Q. Zhang, T. He, C. Fang, N. Q. V. Hung, X. Hao, and H. Yin, “Circle: continual repair across programming languages,” in _Proceedings of the 31st ACM SIGSOFT International Symposium on Software Testing and Analysis_ , 2022, pp. 678–690.

- [102] S. Moon, Y. Song, H. Chae, D. Kang, T. Kwon, K. T. iunn Ong, S. won Hwang, and J. Yeo, “Coffee: Boost your code llms by fixing bugs with feedback,” 2023.

- [103] Y. Wei, C. S. Xia, and L. Zhang, “Copiloting the copilots: Fusing large language models with completion engines for automated program repair,” in _Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering, ESEC/FSE 2023, San Francisco, CA, USA, December 3-9, 2023_ , S. Chandra, K. Blincoe, and P. Tonella, Eds. ACM, 2023, pp. 172–184. [Online]. Available: https://doi.org/10.1145/3611643.3616271

- [104] Y. Peng, S. Gao, C. Gao, Y. Huo, and M. R. Lyu, “Domain knowledge matters: Improving prompts with fix templates for repairing python type errors,” _CoRR_ , vol. abs/2306.01394, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2306.01394

- [105] A. E. I. Brownlee, J. Callan, K. Even-Mendoza, A. Geiger, C. Hanna, J. Petke, F. Sarro, and D. Sobania, “Enhancing genetic improvement mutations using large language models,” in _Search-Based Software Engineering - 15th International Symposium, SSBSE 2023, San Francisco, CA, USA, December 8, 2023, Proceedings_ , ser. Lecture Notes in Computer Science, P. Arcaini, T. Yue, and E. M. Fredericks, Eds., vol. 14415. Springer, 2023, pp. 153–159. [Online]. Available: https://doi.org/10.1007/978-3-031-48796-5 <u>13</u>

- [106] M. M. A. Haque, W. U. Ahmad, I. Lourentzou, and C. Brown, “Fixeval: Execution-based evaluation of program fixes for programming problems,” in _IEEE/ACM International Workshop on Automated Program Repair, APR@ICSE 2023, Melbourne, Australia, May 16, 2023_ . IEEE, 2023, pp. 11–18. [Online]. Available: https://doi.org/10.1109/APR59189.2023.00009

- [107] B. Ahmad, S. Thakur, B. Tan, R. Karri, and H. Pearce, “Fixing hardware security bugs with large language models,” _arXiv preprint arXiv:2302.01215_ , 2023.

- [108] P. Deligiannis, A. Lal, N. Mehrotra, and A. Rastogi, “Fixing rust compilation errors using llms,” _CoRR_ , vol. abs/2308.05177, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2308.05177

- [109] F. Ribeiro, R. Abreu, and J. Saraiva, “Framing program repair as code completion,” in _Proceedings of the Third International Workshop on Automated Program Repair_ , 2022, pp. 38–45.

- [110] N. Wadhwa, J. Pradhan, A. Sonwane, S. P. Sahu, N. Natarajan, A. Kanade, S. Parthasarathy, and S. K. Rajamani, “Frustrated with code quality issues? llms can help!” _CoRR_ , vol. abs/2309.12938, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2309. 12938

- [111] F. Ribeiro, J. N. C. de Macedo, K. Tsushima, R. Abreu, and J. Saraiva, “Gpt-3-powered type error debugging: Investigating the use of large language models for code repair,” in _Proceedings of the 16th ACM SIGPLAN International Conference on Software Language Engineering, SLE 2023, Cascais, Portugal, October 23-24, 2023_ , J. Saraiva, T. Degueule, and E. Scott, Eds. ACM, 2023, pp. 111–124. [Online]. Available: https://doi.org/10.1145/3623476.3623522

- [112] Y. Wu, N. Jiang, H. V. Pham, T. Lutellier, J. Davis, L. Tan, P. Babkin, and S. Shah, “How effective are neural networks for fixing security vulnerabilities,” _arXiv preprint arXiv:2305.18607_ , 2023.

- [113] N. Jiang, K. Liu, T. Lutellier, and L. Tan, “Impact of code language models on automated program repair,” _arXiv preprint arXiv:2302.05020_ , 2023.

- [114] M. Jin, S. Shahriar, M. Tufano, X. Shi, S. Lu, N. Sundaresan, and A. Svyatkovskiy, “Inferfix: End-to-end program repair with llms,” _arXiv preprint arXiv:2303.07263_ , 2023.

- [115] C. S. Xia and L. Zhang, “Keep the conversation going: Fixing 162 out of 337 bugs for $0.42 each using chatgpt,” _arXiv preprint arXiv:2304.00385_ , 2023.

- [116] Y. Zhang, G. Li, Z. Jin, and Y. Xing, “Neural program repair with program dependence analysis and effective filter mechanism,” _arXiv preprint arXiv:2305.09315_ , 2023.

- [117] J. A. Prenner and R. Robbes, “Out of context: How important is local context in neural program repair?” 2023.

- [118] Q. Zhang, C. Fang, B. Yu, W. Sun, T. Zhang, and Z. Chen, “Pre-trained model-based automated software vulnerability repair: How far are we?” _CoRR_ , vol. abs/2308.12533, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2308.12533

- [119] S. Garg, R. Z. Moghaddam, and N. Sundaresan, “Rapgen: An approach for fixing code inefficiencies in zero-shot,”

25

_CoRR_ , vol. abs/2306.17077, 2023. [Online]. Available: https: //doi.org/10.48550/arXiv.2306.17077

- [120] W. Wang, Y. Wang, S. Joty, and S. C. H. Hoi, “Rapgen: Retrieval-augmented patch generation with codet5 for automatic program repair,” in _Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering, ESEC/FSE 2023, San Francisco, CA, USA, December 3-9, 2023_ , S. Chandra, K. Blincoe, and P. Tonella, Eds. ACM, 2023, pp. 146–158. [Online]. Available: https://doi.org/10.1145/3611643.3616256

- [121] Y. Zhang, Z. Jin, Y. Xing, and G. Li, “STEAM: simulating the interactive behavior of programmers for automatic bug fixing,” _CoRR_ , vol. abs/2308.14460, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2308.14460

- [122] S. Fakhoury, S. Chakraborty, M. Musuvathi, and S. K. Lahiri, “Towards generating functionally correct code edits from natural language issue descriptions,” _arXiv preprint arXiv:2304.03816_ , 2023.

- [123] M. Fu, C. Tantithamthavorn, T. Le, V. Nguyen, and D. Phung, “Vulrepair: a t5-based automated software vulnerability repair,” in _Proceedings of the 30th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering_ , 2022, pp. 935–947.

- [124] S. Gao, X. Wen, C. Gao, W. Wang, H. Zhang, and M. R. Lyu, “What makes good in-context demonstrations for code intelligence tasks with llms?” in _38th IEEE/ACM International Conference on Automated Software Engineering, ASE 2023, Luxembourg, September 11-15, 2023_ . IEEE, 2023, pp. 761– 773. [Online]. Available: https://doi.org/10.1109/ASE56229. 2023.00109

- [125] C. Treude and H. Hata, “She elicits requirements and he tests: Software engineering gender bias in large language models,” _CoRR_ , vol. abs/2303.10131, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2303.10131

- [126] R. Kocielnik, S. Prabhumoye, V. Zhang, R. M. Alvarez, and A. Anandkumar, “Autobiastest: Controllable sentence generation for automated and open-ended social bias testing in language models,” _CoRR_ , vol. abs/2302.07371, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2302.07371

- [127] M. Ciniselli, L. Pascarella, and G. Bavota, “To what extent do deep learning-based code recommenders generate predictions by cloning code from the training set?” in _19th IEEE/ACM International Conference on Mining Software Repositories, MSR 2022, Pittsburgh, PA, USA, May 23-24, 2022_ . ACM, 2022, pp. 167–178. [Online]. Available: https://doi.org/10.1145/3524842.3528440

- [128] D. Erhabor, S. Udayashankar, M. Nagappan, and S. Al-Kiswany, “Measuring the runtime performance of code produced with github copilot,” _CoRR_ , vol. abs/2305.06439, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2305.06439

- [129] R. Wang, R. Cheng, D. Ford, and T. Zimmermann, “Investigating and designing for trust in ai-powered code generation tools,” _CoRR_ , vol. abs/2305.11248, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2305.11248

- [130] B. Yetistiren, I. Ozsoy,<sup>¨</sup> M. Ayerdem, and E. T¨uz¨un, “Evaluating the code quality of ai-assisted code generation tools: An empirical study on github copilot, amazon codewhisperer, and chatgpt,” _CoRR_ , vol. abs/2304.10778, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2304.10778

- [131] C. Wohlin, “Guidelines for snowballing in systematic literature studies and a replication in software engineering,” in _18th International Conference on Evaluation and Assessment in Software Engineering, EASE ’14, London, England, United Kingdom, May 13-14, 2014_ , M. J. Shepperd, T. Hall, and I. Myrtveit, Eds. ACM, 2014, pp. 38:1–38:10. [Online]. Available: https://doi.org/10.1145/2601248.2601268

- [132] A. Mastropaolo, S. Scalabrino, N. Cooper, D. Nader-Palacio, D. Poshyvanyk, R. Oliveto, and G. Bavota, “Studying the usage of text-to-text transfer transformer to support code-related tasks,” in _43rd IEEE/ACM International Conference on Software Engineering, ICSE 2021, Madrid, Spain, 22-30 May 2021_ . IEEE, 2021, pp. 336– 347.

- [133] C. Tsigkanos, P. Rani, S. M¨uller, and T. Kehrer, “Large language models: The next frontier for variable discovery within metamorphic testing?” in _IEEE International Conference on Software Analysis, Evolution and Reengineering, SANER 2023, Taipa, Macao, March 21-24, 2023_ , T. Zhang, X. Xia, and

   - N. Novielli, Eds. IEEE, 2023, pp. 678–682. [Online]. Available: https://doi.org/10.1109/SANER56733.2023.00070

- [134] G. J. Myers, _The art of software testing (2. ed.)_ . Wiley, 2004. [Online]. Available: http://eu.wiley.com/WileyCDA/ WileyTitle/productCd-0471469122.html

- [135] P. Farrell-Vinay, _Manage software testing_ . Auerbach Publ., 2008.

- [136] A. Mili and F. Tchier, _Software testing: Concepts and operations_ . John Wiley & Sons, 2015.

- [137] S. Lukasczyk and G. Fraser, “Pynguin: Automated unit test generation for python,” in _44th IEEE/ACM International Conference on Software Engineering: Companion Proceedings, ICSE Companion 2022, Pittsburgh, PA, USA, May 22-24, 2022_ . ACM/IEEE, 2022, pp. 168–172. [Online]. Available: https://doi.org/10.1145/3510454.3516829

- [138] E. T. Barr, M. Harman, P. McMinn, M. Shahbaz, and S. Yoo, “The oracle problem in software testing: A survey,” _IEEE transactions on software engineering_ , vol. 41, no. 5, pp. 507–525, 2014.

- [139] C. Watson, M. Tufano, K. Moran, G. Bavota, and D. Poshyvanyk, “On learning meaningful assert statements for unit test cases,” in _ICSE ’20: 42nd International Conference on Software Engineering, Seoul, South Korea, 27 June - 19 July, 2020_ , G. Rothermel and D. Bae, Eds. ACM, 2020, pp. 1398–1409.

- [140] Y. He, L. Zhang, Z. Yang, Y. Cao, K. Lian, S. Li, W. Yang, Z. Zhang, M. Yang, Y. Zhang, and H. Duan, “Textexerciser: Feedback-driven text input exercising for android applications,” in _2020 IEEE Symposium on Security and Privacy, SP 2020, San Francisco, CA, USA, May 18-21, 2020_ . IEEE, 2020, pp. 1071–1087.

- [141] A. Wei, Y. Deng, C. Yang, and L. Zhang, “Free lunch for testing: Fuzzing deep-learning libraries from open source,” in _44th IEEE/ACM 44th International Conference on Software Engineering, ICSE 2022, Pittsburgh, PA, USA, May 25-27, 2022_ . ACM, 2022, pp. 995–1007.

- [142] D. Xie, Y. Li, M. Kim, H. V. Pham, L. Tan, X. Zhang, and M. W. Godfrey, “Docter: documentation-guided fuzzing for testing deep learning API functions,” in _ISSTA ’22: 31st ACM SIGSOFT International Symposium on Software Testing and Analysis, Virtual Event, South Korea, July 18 - 22, 2022_ , S. Ryu and Y. Smaragdakis, Eds. ACM, 2022, pp. 176–188.

- [143] Q. Guo, X. Xie, Y. Li, X. Zhang, Y. Liu, X. Li, and C. Shen, “Audee: Automated testing for deep learning frameworks,” in _35th IEEE/ACM International Conference on Automated Software Engineering, ASE 2020, Melbourne, Australia, September 21-25, 2020_ . IEEE, 2020, pp. 486–498.

- [144] Z. Wang, M. Yan, J. Chen, S. Liu, and D. Zhang, “Deep learning library testing via effective model generation,” in _ESEC/FSE ’20: 28th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering, Virtual Event, USA, November 8-13, 2020_ , P. Devanbu, M. B. Cohen, and T. Zimmermann, Eds. ACM, 2020, pp. 788–799.

- [145] J. Jiang, Y. Xiong, H. Zhang, Q. Gao, and X. Chen, “Shaping program repair space with existing patches and similar code,” in _Proceedings of the 27th ACM SIGSOFT International Symposium on Software Testing and Analysis_ , ser. ISSTA 2018. New York, NY, USA: Association for Computing Machinery, 2018, p. 298–309. [Online]. Available: https://doi.org/10.1145/3213846.3213871

- [146] M. Wen, J. Chen, R. Wu, D. Hao, and S.-C. Cheung, “Contextaware patch generation for better automated program repair,” in _Proceedings of the 40th International Conference on Software Engineering_ , ser. ICSE ’18. New York, NY, USA: Association for Computing Machinery, 2018, p. 1–11. [Online]. Available: https://doi.org/10.1145/3180155.3180233

- [147] Y. Xiong, J. Wang, R. Yan, J. Zhang, S. Han, G. Huang, and L. Zhang, “Precise condition synthesis for program repair,” in _2017 IEEE/ACM 39th International Conference on Software Engineering (ICSE)_ , 2017, pp. 416–426.

- [148] J. Xuan, M. Martinez, F. DeMarco, M. Cl´ement, S. L. Marcote, T. Durieux, D. Le Berre, and M. Monperrus, “Nopol: Automatic repair of conditional statement bugs in java programs,” _IEEE Transactions on Software Engineering_ , vol. 43, no. 1, pp. 34–55, 2017.

- [149] S. Song, X. Li, and S. Li, “How to bridge the gap between modalities: A comprehensive survey on multimodal large language model,” _CoRR_ , vol. abs/2311.07594, 2023.

- [150] J. M. Zhang, M. Harman, L. Ma, and Y. Liu, “Machine learning testing: Survey, landscapes and horizons,” _IEEE Trans. Software Eng._ , vol. 48, no. 2, pp. 1–36, 2022.

- [151] F. Tu, J. Zhu, Q. Zheng, and M. Zhou, “Be careful of when: an empirical study on time-related misuse of issue tracking

26

   - data,” in _Proceedings of the 2018 ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering, ESEC/SIGSOFT FSE 2018, Lake Buena Vista, FL, USA, November 04-09, 2018_ , G. T. Leavens, A. Garcia, and C. S. Pasareanu, Eds. ACM, 2018, pp. 307–318. [Online]. Available: https://doi.org/10.1145/3236024.3236054

- [152] Z. Sun, L. Li, Y. Liu, X. Du, and L. Li, “On the importance of building high-quality training datasets for neural code search,” in _44th IEEE/ACM 44th International Conference on Software Engineering, ICSE 2022, Pittsburgh, PA, USA, May 25-27, 2022_ . ACM, 2022, pp. 1609–1620. [Online]. Available: https://doi.org/10.1145/3510003.3510160

   - [168] D. Zan, B. Chen, F. Zhang, D. Lu, B. Wu, B. Guan, Y. Wang, and J. Lou, “Large language models meet nl2code: A survey,” in _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2023, Toronto, Canada, July 9-14, 2023_ , A. Rogers, J. L. Boyd-Graber, and N. Okazaki, Eds. Association for Computational Linguistics, 2023, pp. 7443–7464. [Online]. Available: https://doi.org/10.18653/v1/2023.acl-long.411

- [153] L. Shi, Z. Jiang, Y. Yang, X. Chen, Y. Zhang, F. Mu, H. Jiang, and Q. Wang, “ISPY: automatic issue-solution pair extraction from community live chats,” in _36th IEEE/ACM International Conference on Automated Software Engineering, ASE 2021, Melbourne, Australia, November 15-19, 2021_ . IEEE, 2021, pp. 142–154. [Online]. Available: https://doi.org/10.1109/ASE51524.2021.9678894

- [154] D. Guo, S. Ren, S. Lu, Z. Feng, D. Tang, S. Liu, L. Zhou, N. Duan, A. Svyatkovskiy, S. Fu, M. Tufano, S. K. Deng, C. B. Clement, D. Drain, N. Sundaresan, J. Yin, D. Jiang, and M. Zhou, “Graphcodebert: Pre-training code representations with data flow,” in _9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021_ . OpenReview.net, 2021. [Online]. Available: https://openreview.net/forum?id=jLoC4ez43PZ

- [155] F. Yu, A. Seff, Y. Zhang, S. Song, T. Funkhouser, and J. Xiao, “Lsun: Construction of a large-scale image dataset using deep learning with humans in the loop,” _arXiv preprint arXiv:1506.03365_ , 2015.

- [156] LoadRunner, Inc., “Loadrunner,” 2023, microfocus.com.

- [157] LangChain, Inc., “Langchain,” 2023, https://docs.langchain. com/docs/.

- [158] Prompt engineering, “Prompt engineering guide,” 2023, https: //github.com/dair-ai/Prompt-Engineering-Guide.

- [159] Z. Zhang, A. Zhang, M. Li, H. Zhao, G. Karypis, and A. Smola, “Multimodal chain-of-thought reasoning in language models,” _CoRR_ , vol. abs/2302.00923, 2023.

- [160] Z. Liu, X. Yu, Y. Fang, and X. Zhang, “Graphprompt: Unifying pre-training and downstream tasks for graph neural networks,” in _Proceedings of the ACM Web Conference 2023, WWW 2023, Austin, TX, USA, 30 April 2023 - 4 May 2023_ , Y. Ding, J. Tang, J. F. Sequeda, L. Aroyo, C. Castillo, and G. Houben, Eds. ACM, 2023, pp. 417– 428.

- [161] Y. Charalambous, N. Tihanyi, R. Jain, Y. Sun, M. A. Ferrag, and L. C. Cordeiro, “A new era in software security: Towards selfhealing software via large language models and formal verification,” 2023.

- [162] S. Wang, L. Huang, A. Gao, J. Ge, T. Zhang, H. Feng, I. Satyarth, M. Li, H. Zhang, and V. Ng, “Machine/deep learning for software engineering: A systematic literature review,” _IEEE Trans. Software Eng._ , vol. 49, no. 3, pp. 1188–1231, 2023. [Online]. Available: https://doi.org/10.1109/TSE.2022.3173346

- [163] Y. Yang, X. Xia, D. Lo, and J. C. Grundy, “A survey on deep learning for software engineering,” _ACM Comput. Surv._ , vol. 54, no. 10s, pp. 206:1–206:73, 2022. [Online]. Available: https://doi.org/10.1145/3505243

- [164] C. Watson, N. Cooper, D. Nader-Palacio, K. Moran, and D. Poshyvanyk, “A systematic literature review on the use of deep learning in software engineering research,” _ACM Trans. Softw. Eng. Methodol._ , vol. 31, no. 2, pp. 32:1–32:58, 2022. [Online]. Available: https://doi.org/10.1145/3485275

- [165] M. Bajammal, A. Stocco, D. Mazinanian, and A. Mesbah, “A survey on the use of computer vision to improve software engineering tasks,” _IEEE Trans. Software Eng._ , vol. 48, no. 5, pp. 1722–1742, 2022. [Online]. Available: https://doi.org/10.1109/TSE.2020.3032986

- [166] X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo, J. C. Grundy, and H. Wang, “Large language models for software engineering: A systematic literature review,” _CoRR_ , vol. abs/2308.10620, 2023. [Online]. Available: https://doi.org/10.48550/arXiv.2308.10620

- [167] A. Fan, B. Gokkaya, M. Harman, M. Lyubarskiy, S. Sengupta, S. Yoo, and J. M. Zhang, “Large language models for software engineering: Survey and open problems,” _CoRR_ , vol. abs/2310.03533, 2023. [Online]. Available: https: //doi.org/10.48550/arXiv.2310.03533

|**Ref**|||**[26]**||[27]<br>|[28]|[29]|[30]|[31]||[32]<br>[33]|[34]|[35]<br>[8]|36|[]<br>[37]|[38]|[39]|[40]|[7]||[41]<br>[42]|[43]|[44]||[45]|[46]|27<br>[47]|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Venue**||**Arxiv**||ICLR 2023|Arxiv||Arxiv|Arxiv|SAST 2023|Arxiv|Arxiv|Arxiv|ASE 2023<br>Arxiv|Arxiv|ICSE 2023|Arxiv|Arxiv<br>|Arxiv|Arxiv|Arxiv|Arxiv|Arxiv|AST 2022|ICSE 2023||TSE 2022|ICSE 2023|
|**How**<br>**LLM**<br>**inte-**<br>|**grated**|**Pure LLM**||Pure LLM|Mutation<br>testing;<br>|Statistic analysis<br>|Syntactic repair|Syntactic repair|Pure LLM|Syntactic repair|Pure LLM|Pure LLM|Pure LLM<br>Pure LLM|Syntactic repair|Mutation<br>testing;<br>Program analysis|Mutation<br>testing;<br>Syntactic repair|Syntactic repair<br>|Pure LLM|Program analysis|Pure LLM|Program<br>analysis,<br>Reinforcement<br>learning|Pure LLM|Pure LLM|Statistic analysis||Pure LLM|Pure LLM|
|**Input to LLM**||**Code**||Code|Code||Code|Code; Others|Code|Code|Bug description|Code; Others|Code<br>Code|Code|Code|Code|Code<br>d|Coe|Code; Error in-<br>formation|Code|Code|Code|Code|Code||Code|Code|
|**How LLM is used**||Pre-training<br>and/or|Fine-tuning<br>|Zero-shot learning|Zero-shot learning||Pre-training<br>and/or<br>Fine-tunin|g<br>Zero-shot learning|Zero-shot learning|Pre-training<br>and/or<br>|Fine-tuning<br>Pre-training<br>and/or<br>Fine-tuning|Zero-shot learning|Pre-training<br>and/or<br>Fine-tuning<br>Zero-shot learning|Zero-shot learning|Zero-shot learning|Few-shot<br>learning;<br>Zero-shot learning|Zero-shot learning<br>h l|Few-sot earning|Zero-shot learning|Few-shot learning|Pre-training<br>and/or<br>Fine-tuning|Zero-shot learning|Pre-training<br>and/or<br>Fine-tuning|Pre-training<br>and/or|Fiti|ne-unng<br>Pre-training<br>and/or<br>Fine-tuning|Few-shot learning|
|**LM**||||||||||LaMA-2|ChatGPT||||||Codex;|||||||||||
|**Involved L**||BART||Codex|Codex||PLBART|ChatGPT|ChatGPT|CodeT5; L|CodeGPT;|GPT-4|GPT-neox<br>ChatGPT|ChatGPT|Codex|Codex|CodeGen;<br>ChatGPT<br>h|CatGPT|ChatGPT|GPT-4|Codex|ChatGPT|BART|CodeT5||T5|Codex|
|**Topic**||Unit test case gener-|ation<br>|Unit test case gener-<br>|ation<br>Unit test case gener-<br>|ation<br>|Unit test case gener-<br>ation|Unit test case gener-<br>ation|Unit test case gener-<br>ation|Unit test case gener-<br>|ation<br>Unit test case gener-<br>ation|Unit test case gener-<br>ti|aon<br>Unit test case gener-<br>ation<br>Unit test case gener-<br>ation|Unit test case gener-<br>i|aton<br>Unit test case gener-<br>ation|Unit test case gener-<br>ation|Unit test case gener-<br>ation<br>|Unit test case gener-<br>ation|Unit test case gener-<br>ation|Unit test case gener-<br>|ation<br>Unit test case gener-<br>ation|Unit test case gener-<br>ation|Test oracle genera-<br>tion|Test oracle genera-|ti|on<br>Test<br>oracle<br>gener-<br>ation; Program re-<br>|pair<br>Test<br>oracle<br>gener-<br>ation; Program re-<br>pair|
|**Year**||2021||2022|2022||2023|2023|2023|2023|2023|2023|2023<br>2023|2023|2023|2023|2023<br>|2023|2023|2023|2023|2023|2023|2023||2022|2023|
|**ID**<br>**Paper title**||1<br>Unit Test Case Generation with Transform-|ers and Focal Context<br><br>|2<br>Codet: Code Generation with Generated<br>|Tests<br>3<br>Interactive Code Generation via Test-Driven<br>|User-Intent Formalization<br><br>|4<br>A3Test: Assertion-Augmented Automated<br>Test Case Generation|<br>5<br>An Empirical Evaluation of Using Large<br>Language Models for Automated Unit Test<br>Gti|eneraon<br>6<br>An Initial Investigation of ChatGPT Unit<br>Test Generation Capability|<br>7<br>Automated Test Case Generation Using<br>|Code Models and Domain Adaptation<br>8<br>Automatic Generation of Test Cases based<br>on Bug Reports: a Feasibility Study with<br>Lare Lanuae Models|g gg<br>9<br>Can Large Language Models Write Good<br>PtBd Tt?|ropery-ase ess<br>10<br>CAT-LM Training Language Models on<br>Aligned Code And Tests<br>11<br>ChatGPT vs SBST: A Comparative Assess-<br>ment of Unit Test Suite Generation|<br>12<br>ChatUniTest: a ChatGPT-based Automated<br>Ui T Gi Tl|nt est eneraton oo<br>13<br>CODAMOSA: Escaping Coverage Plateaus<br>in Test Generation with Pre-trained Large<br>|Language Models<br>14<br>Effective Test Generation Using Pre-trained<br>Large Language Models and Mutation Test-<br>|ing<br>15<br>Exploring the Effectiveness of Large Lan-<br>guage Models in Generating Unit Tests<br><br>lld|16<br>How We oes LLM Generate Security<br>Tests?|17<br>No More Manual Tests? Evaluating and Im-<br>proving ChatGPT for Unit Test Generation|<br>18<br>Prompting Code Interpreter to Write Better<br>|Unit Tests on Quixbugs Functions<br>19<br>Reinforcement Learning from Automatic<br>Feedback for High-Quality Unit Test Gen-<br>eration|20<br>Unit Test Generation using Generative AI: A<br>Comparative Performance Analysis of Au-<br>togeneration Tools|<br>21<br>Generating Accurate Assert Statements for<br>Unit Test Cases Using Pretrained Trans-<br>formers|22<br>Learning Deep Semantics for Test Comple-|ti|on<br>23<br>Using Transfer Learning for Code-Related<br>Tasks|24<br>Retrieval-Based Prompt Selection for Code-<br>Related Few-Shot Learning|

|**Ref**|[48]|[49]|[50]<br>[51]||[52]<br>[53]|[54]<br>55|[]<br>[56]||[57]<br>[58]|[59]|[60]<br>[61]|[14]|[62]<br>[63]<br>[64]|[65]|[66]<br>67|28<br>[]<br>[68]|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Venue**|PLDI 2021|ICSE 2023|Arxiv<br>EASE 2021|Arxiv|ICACCS<br>2023|ICSTW<br>2023<br>Arxiv|Arxiv|Arxiv|ICSE 2024|ISSTA 2023|FUZZING<br>2023<br>Arxiv|ICSE 2024|Arxiv<br>ASE 2023<br>Arxiv|ICSE 2024|Arxiv<br>ICSE 2024|SANER<br>2023|
|**How**<br>**LLM**<br>**inte-**|**grated**<br>Differential testing;<br>Program analysis|Pure LLM|Pure LLM<br>Formal method|Pure LLM|Pure LLM|Pure LLM<br>Pure LLM|Pure LLM|Mutation testing|Differential testing|Mutation<br>testing;<br>Differential testing|Pure LLM<br>Pure LLM|Natural<br>language<br>processing|Pure LLM<br>Differential testing<br>Scenario testing|Pure LLM|Pure LLM<br>Mutation testing|Pure LLM|
|**InputtoLLM**|<br>Code|View hierarchy<br>file of UI|Others<br>Others|Code|NL<br>specifica-<br>tion|View hierarchy<br>file of UI<br>View hierarchy<br>fil f UI|ie o<br>Others|Code|Code|Code|NL<br>specifica-<br>tion<br>View hierarchy<br>file of UI|View hierarchy<br>file of UI|NL<br>specifica-<br>tion<br>Code<br>Others|View hierarchy<br>file of UI|Code; Others<br>Code|Others|
|**HowLLMisused**|<br>Pre-training<br>and/or<br>Fine-tuning|Pre-training<br>and/or<br>Fine-tuning|Chain-of-Thought;<br>Zero-shot learning<br>Pre-training<br>and/or<br>Fine-tuning|Few-shot learning|Pre-training<br>and/or<br>Fine-tuning;<br>Zero-shot<br>|learning<br>Pre-training<br>and/or<br>Fine-tuning<br>Chain-of-Thought|Zero-shot learning|Zero-shot learning|Chain-of-Thought; Pre-<br>training<br>and/or<br>Fine-<br>tuning; Zero-shot learn-<br>|ing; Few-shot learning<br>Zero-shot learning|Few-shot learning<br>Zero-shot learning|Zero-shot learning|Chain-of-Thought;<br>Few-shot learning<br>Pre-training<br>and/or<br>Fine-tuning<br>Zero-shot learning|Few-shot learning|Few-shot<br>learning;<br>Zero-shot learning<br>Few-shot learning; Au-<br>i|tomatc prompt<br>Zero-shot learning|
|**InvolvedLLM**|<br>GPT-2|GPT-3|InstructGPT<br>GPT-2|ChatGPT|GPT-3; T5|GPT-3<br>GPT-4|ChatGPT|CodeBert|Codex|Codex; InCoder|GPT-4<br>ChatGPT|GPT-3|ChatGPT;<br>GPT-4;<br>LaMDA<br>GPT-2<br>GPT-3|ChatGPT|ChatGPT; GPT-4<br>GPT-4; StarCoder|GPT-j|
||input|input|input<br><br>input|input|input|input<br><br>input|input|input|input|input|input<br><br>input|input|input<br><br>input<br><br>input|input|input<br><br>input|input|
|**Topic**|System<br>test<br>generation|System<br>test<br>generation|System<br>test<br>generation<br>System<br>test<br>generation|System<br>test<br>|generation<br>System<br>test<br>generation|System<br>test<br>generation<br>System<br>test<br>ti|generaon<br>System<br>test<br>generation|System<br>test<br>|generation<br>System<br>test<br>generation|System<br>test<br>generation|System<br>test<br>generation<br>System<br>test<br>generation|System<br>test<br>generation|System<br>test<br>generation<br>System<br>test<br>generation<br>System<br>test<br>generation|System<br>test<br>generation|System<br>test<br>generation<br>System<br>test<br>i|generaton<br>System<br>test<br>generation|
|**Year**|2021|2022|2022<br>2022|2023|2023|2023<br>2023|2023|2023|2023|2023|2023<br>2023|2023|2023<br>2023<br>2023|2023|2023<br>2023|2023|
|**ID**<br>**Papertitle**|<br>25<br>Automated<br>Conformance<br>Testing<br>for<br>JavaScript<br>Engines<br>via<br>Deep<br>Compiler<br>|Fuzzing<br>26<br>Fill in the Blank: Context-aware Automated<br>Text Input Generation for Mobile GUI Test-<br>|ing<br>27<br>Large Language Models are Pretty Good<br>Zero-Shot Video Game Bug Detectors<br>28<br>Slgpt: Using Transfer Learning to Directly<br>Generate Simulink Model Files and Find<br>Bus in the Simulink Toolchain|g<br>29<br>Augmenting Greybox Fuzzing with Gener-<br>|ative AI<br>30<br>Automated Test Case Generation Using T5<br>and GPT-3|31<br>Automating GUI-based Software Testing<br>with GPT-3<br>32<br>AXNav: Replaying Accessibility Tests from<br>Ntl L|aura anguage<br>33<br>Can ChatGPT Advance Software Testing In-<br>telligence? An Experience Report on Meta-<br>hi Tti|morpc esng<br>34<br>Efficient Mutation Testing via Pre-Trained<br>|Language Models<br>35<br>Large<br>Language<br>Models<br>are<br>Edge-Case<br>Generators:Crafting Unusual Programs for<br>Fuzzing Deep Learning Libraries|36<br>Large Language Models are Zero Shot<br>Fuzzers: Fuzzing Deep Learning Libraries<br>|via Large Language Models<br>37<br>Large Language Models for Fuzzing Parsers<br>(Registered Report)<br>38<br>LLM for Test Script Generation and Migra-<br>tion: Challenges, Capabilities, and Opportu-<br>|nities<br>39<br>Make<br>LLM<br>a<br>Testing<br>Expert:<br>Bringing<br>Human-like Interaction to Mobile GUI Test-<br>|ing via Functionality-aware Decisions<br>40<br>PentestGPT: An LLM-empowered Auto-<br>matic Penetration Testing Tool<br>41<br>SMT<br>Solver<br>Validation<br>Empowered<br>by<br>Large Pre-Trained Language Models<br>42<br>TARGET: Automated Scenario Generation<br>from Traffic Rules for Testing Autonomous<br>|Vehicles<br>43<br>Testing the Limits: Unusual Text Inputs<br>Generation for Mobile App Crash Detection<br>|with Large Language Model<br>44<br>Understanding<br>Large<br>Language<br>Model<br>Based Fuzz Driver Generation<br>45<br>Universal<br>Fuzzing<br>via<br>Large<br>Language<br>Mdl|oes<br>46<br>Variable Discovery with Large Language<br>Models for Metamorphic Testing of Scien-<br>tific Software|

|**Ref**|||[69]|[70]<br>[71]||[72]|[73]||[74]|[75]|[76]|[77]<br>[78]|[79]|[80]<br>[81]|[82]|[83]|[84]<br>[85]<br>[86]|[87]||||[88]<br>[89]|||[90]||[91]|2<br>92|9<br>[]<br>[93]|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Venue**||Arxiv|FSE 2022|ICSE 2024|Arxiv||Arxiv|ICSE 2023||ICSE 2024|ICPC 2023|EMNLP<br>2022<br>ICSE 2023|Arxiv|Arxiv<br>Arxiv|SIGCSE<br>2024|Arxiv|ICSE 2024<br>Arxiv<br>Arxiv|ASE 2023||Ai|rxv|Arxiv|SP 2023|||ICSE 2023||Arxiv|ICSE 2023|
|**How**<br>**LLM**<br>**inte-**<br>|**grated**|Pure LLM|<br>Pure LLM|Reinforcement<br>learning|Statistic analysis||Statistic analysis|Program analysis||Pure LLM|Statistic analysis|Pure LLM<br>Program<br>analysis;<br>Statistic analysis|Pure LLM|Pure LLM<br>Pure LLM|Pure LLM|Pure LLM|Pure LLM<br>Pure LLM<br>Mutation<br>testing;<br>Reinforcement|learning<br>Differential testing||P LLM|ure|Pure LLM|P LLM|ure||Pure LLM||Pure LLM|Statistic analysis|
|**Input to LLM**||Code|Bug description|Bug description|Bug description||Bug description|Code||Bug description|Bug description|Code<br>Bug description|Code|Error<br>informa-<br>tion<br>Bug description|Code; Error in-<br>formation|Code|Code<br>Code; Error in-<br>formation<br>Code|Code||Cd|oe|Code|CdBd|oe; ug e-|scription<br>|Code||Code|Code|
|**How LLM is used**||Few-shot learnin|g<br>Pre-training<br>and/or|Fine-tuning<br>Pre-training<br>and/or<br>Fine-tuning|Zero-shot learning||Zero-shot learning|Pre-training<br>and/or|Fine-tuning|Few-shot<br>learning;<br>Chain-of-Thought|Pre-training<br>and/or<br>Fine-tuning|Pre-training<br>and/or<br>Fine-tuning<br>Few-shot learning|Few-shot learning|Zero-shot learning<br>Zero-shot learning|Zero-shot learning|Self-consistency;<br>Zero-<br>shot learning|Pre-training<br>and/or<br>Fine-tuning<br>Zero-shot learning<br>Zero-shot learning|Zero-shot learning||Fh li|ew-sot earnng|Zero-shot learning|Zh li|ero-sot earnng||Zero-shot learning|<br><br>|Pre-training<br>and/or<br>Fii|ne-tunng<br>Few-shot<br>learning;<br>Zero-shot learning|
|**Involved LLM**||GPT-4 StarCoder|;<br>BART|ChatGPT|ChatGPT||CodeT5|CodeT5||ChatGPT|CodeT5|CodeT5<br>Codex|ChatGPT|ChatGPT; GPT-4<br>ChatGPT|ChatGPT|CodeGen;<br>Codex;<br>ChatGPT|CodeGen<br>ChatGPT; GPT-4<br>ChatGPT|ChatGPT||Cd<br>ChGPT|oex;<br>at;|GPT-4; StarCoder<br>ChatGPT|Cd|oex||Codex||CodeGPT|GPT-3;<br>Codex;<br>CodeT5; InCoder|
|**Topic**||Sstem<br>test<br>inut|y<br><br>p<br>generation<br>Bug analysis|Bug analysis|Bug analysis||Bug analysis|Bug analysis||Bug analysis|Bug analysis|Debug<br>Debug|Debug|Debug<br>Debug|Debug|Debug|Debug<br>Debug<br>Debug|Debug||Db|eug|Debug; Program re-<br>pair|P i|rogram repar||Program repair|<br>|Program repair|Program repair|
|**Year**||2023|2022|2023|2023||2023|2023||2023|2023|2022<br>2022|2023|2023<br>2023|2023|2023|2023<br>2023<br>2023|2023||2023||2023|2021|||2022||2022|2022|
|**ID**<br>**Paper title**||47<br>White-boxComilerFuzzinEmowered|p g p<br>by Large Language Models<br>48<br>Itiger: an Automatic Issue Title Generation|Tool<br>49<br>CrashTranslator: Automatically Reproduc-<br>ing Mobile Application Crashes Directly<br>from Stack Trace|<br>50<br>Cupid: Leveraging ChatGPT for More Ac-|curate Duplicate Bug Report Detection|<br>51<br>Employing Deep Learning and Structured<br>Information Retrieval to Answer Clarifica-<br>|tion Questions on Bug Reports<br>52<br>Explaining Software Bugs Leveraging Code|Structures in Neural Machine Translation|<br>53<br>Prompting Is All Your Need: Automated<br>Android Bug Replay with Large Language<br>|Models<br>54<br>Still Confusing for Bug-Component Triag-<br>ing? Deep Feature Learning and Ensemble<br>|Setting to Rescue<br>55<br>Detect-Localize-Repair: A Unified Frame-<br>work for Learning to Debug with CodeT5<br>56<br>Large<br>Language<br>Models<br>are<br>Few-shot<br>Testers: Exploring LLM-based General Bug<br>|Reproduction<br>57<br>A Preliminary Evaluation of LLM-Based<br>Fault Localization|58<br>Addressing Compiler Errors: Stack Over-<br>flow or Large Language Models?<br>59<br>Can LLMs Demystify Bug Reports?|60<br>Dcc –help: Generating Context-Aware Com-<br>piler Error Explanations with Large Lan-|guage Models<br>61<br>Explainable<br>Automated<br>Debugging<br>via<br>Large Language Model-driven Scientific De-<br>|bugging<br>62<br>Large Language Models for Test-Free Fault<br>Localization<br>63<br>Large Language Models in Fault Localisa-<br>tion<br>64<br>LLM4CBI: Taming LLMs to Generate Effec-<br>tive Test Programs for Compiler Bug Isola-|tion<br>65<br>Nuances are the Key: Unlocking ChatGPT<br>toFindFailure-InducinTestswithDiffer-|g   <br>ential Prompting|<br>66<br>ThiLLMdlSlf|eacng arge anguage oes to e-|Debug<br>67<br>A study on Prompt Design, Advantages and<br>Limitations of ChatGPT for Deep Learning<br>|Program Repair<br>68<br>EiiZShVlbiliRi|xamnng ero-ot uneraty epar|with Large Language Models<br><br>|69<br>Automated Repair of Programs from Large|Language Models<br><br><br><br><br><br>|70<br>Fix<br>Bugs<br>with<br>Transformer<br>through<br>a<br>NlSbli Edi G|eura-ymoc t rammar<br>71<br>Practical Program Repair in the Era of Large<br>Pre-trained Language Models|

|**Ref**<br>[94]|[95]<br>|[96]<br>[97]|[98]|[99]|[100]<br>[101]<br>[102]<br>[103]|[104]|[105]<br>[106]<br>[107]<br>|[108]<br>[109]<br>[110]<br>[111]|[112]|[113]|[114]|[115]|30<br>[116]|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Venue**<br>Arxiv<br>APR 2022|APR 2023|ASE 2023|iSemantic<br>2023|APR 2023|APR 2022<br>ISSTA 2022<br>Arxiv<br>FSE 2023|ICSE 2024|SSBSE 2023<br>APR 2023<br>Arxiv<br>Arxiv|ICSE 2022<br>Arxiv<br>SLE 2023|ISSTA 2023|ICSE 2023|FSE 2023|Arxiv|Arxiv|
|**How**<br>**LLM**<br>**inte-**<br>**grated**<br>Program analysis<br>Pure LLM|Pure LLM|Pure LLM|Pure LLM|Pure LLM|Pure LLM<br>Pure LLM<br>Pure LLM<br>Statistic analysis|Program analysis|Pure LLM<br>Pure LLM<br>Pure LLM<br>Pure LLM|Pure LLM<br>Pure LLM<br>Program analysis|Pure LLM|Pure LLM|Pure LLM|Pure LLM|Statistic analysis|
|**Input to LLM**<br>Code; Error in-<br>formation<br>Code|Code; Error in-<br>|formation<br>Code|Code|Code|Code<br>Code<br>Code<br>Code|Code|Code<br>Code<br>Code; Bug de-<br>scription<br>Code|Code<br>Code<br>Code|Code|Code|Code|Code; Error in-<br>formation|Code|
|**How LLM is used**<br>Few-shot<br>learning;<br>Zero-shot learning<br>Pre-training<br>and/or|Fine-tuning<br>Zero-shot learning|Pre-training<br>and/or<br>Fine-tuning|Zero-shot learning|Pre-training<br>and/or<br>Fine-tuning|Few-shot<br>learning;<br>Zero-shot learning<br>Pre-training<br>and/or<br>Fine-tuning<br>Pre-training<br>and/or<br>Fine-tuning<br>Zero-shot learning|Pre-training<br>and/or<br>Fine-tuning|Zero-shot learning<br>Pre-training<br>and/or<br>Fine-tuning<br>Few-shot<br>learning;<br>Zero-shot learning<br>Zero-shot learning|Zero-shot learning<br>Zero-shot learning<br>Zero-shot learning|Pre-training<br>and/or<br>Fine-tuning;<br>Zero-shot<br>|learning<br>Pre-training<br>and/or<br>Fine-tuning;<br>Zero-shot<br>|learning<br>Few-shot learning; Pre-<br>training<br>and/or<br>Fine-|tuning<br>Few-shot learning|Pre-training<br>and/or<br>Fine-tuning|
|**Involved LLM**<br>Codex<br>GPT-2|ChatGPT|PLBART;<br>CodeT5;<br>UniXCoder|ChatGPT|T5; CodeT5|Codex<br>T5<br>CodeLLAMA<br>CodeT5; InCoder|CodeT5|GPT-4<br>CodeT5; PLBART<br>Codex; CodeGen<br>ChatGPT; GPT-4|CodeGPT<br>ChatGPT; GPT-4<br>GPT-3|Codex;<br>CodeGen;<br>CodeT5;<br>PLBART;<br>|InCoder<br>PLBART;<br>CodeT5;<br>CodeGen; InCoder|Codex|ChatGPT|CodeT5|
|**Topic**<br>Program repair<br>Program repair|<br>Program repair|Program repair|Program repair|Program repair|Program repair<br>Program repair<br>Program repair<br>Program repair|Program repair|Program repair<br>Program repair<br>Program repair<br>Program repair|Program repair<br>Program repair<br>Program repair|Program repair|Program repair|Program repair|Program repair|Program repair|
|**Year**<br>2022<br>2022|2023|2023|2023|2023|2023<br>2023<br>2023<br>2023|2023|2023<br>2023<br>2023<br>2023|2023<br>2023<br>2023|2023|2023|2023|2023|2023|
|**ID**<br>**Paper title**<br>72<br>Repairing Bugs in Python Assignments Us-<br>ing Large Language Models<br>73<br>Towards JavaScript Program Repair with|Generative Pre-trained Transformer (GPT-2)<br>74<br>An Analysis of the Automatic Bug Fixing<br>|Performance of ChatGPT<br>75<br>An Empirical Study on Fine-Tuning Large<br>Language Models of Code for Automated<br>|Program Repair<br>76<br>An Evaluation of the Effectiveness of Ope-<br>nAI’s ChatGPT for Automated Python Pro-<br>|gram Bug Fixing using QuixBugs<br>77<br>An Extensive Study on Model Architecture<br>and Program Representation in the Domain<br>of Learning-based Automated Program Re-<br>i|par<br>78<br>Can OpenAI’s Codex Fix Bugs? An Evalua-<br>tion on QuixBugs<br>79<br>CIRCLE: Continual Repair Across Program-<br>ming Languages<br>80<br>Coffee: Boost Your Code LLMs by Fixing<br>Bugs with Feedback<br>81<br>Copiloting the Copilots: Fusing Large Lan-<br>guage Models with Completion Engines for|<br>Automated Program Repair<br>82<br>Domain<br>Knowledge<br>Matters:<br>Improving<br>Prompts with Fix Templates for Repairing<br>Pthon Te Errors|y yp<br>83<br>Enhancing Genetic Improvement Mutations<br>Using Large Language Models<br>84<br>FixEval: Execution-based Evaluation of Pro-<br>gram Fixes for Programming Problems<br>85<br>Fixing Hardware Security Bugs with Large<br>Language Models<br>86<br>Fixing Rust Compilation Errors using LLMs|87<br>Framing Program Repair as Code Comple-<br>tion<br>88<br>Frustrated with Code Quality Issues? LLMs<br>can Help!<br>89<br>GPT-3-Powered Type Error Debugging: In-<br>vestigating the Use of Large Language Mod-|els for Code Repair<br>90<br>How Effective Are Neural Networks for Fix-<br>ing Security Vulnerabilities|91<br>Impact of Code Language Models on Auto-<br>mated Program Repair|92<br>Inferfix: End-to-end Program Repair with<br>LLMs|93<br>Keep the Conversation Going: Fixing 162<br>out of 337 bugs for $0.42 each using Chat-|GPT<br>94<br>Neural Program Repair with Program De-<br>pendence<br>Analysis<br>and<br>Effective<br>Filter<br>Mechanism|

31

|**Ref**<br>[117]<br>[118]<br>[119]<br>[120]<br>[121]<br>[122]<br>[123]<br>[124]|
|---|
|**Venue**<br>ICSE 2024<br>IEEE TDSC<br>Arxiv<br>FSE 2023<br>Arxiv<br>Arxiv<br>FSE 2022<br>ASE 2023|
|**How**<br>**LLM**<br>**inte-**<br>**grated**<br>Pure LLM<br>Pure LLM<br>Pure LLM<br>Statistic analysis<br>Pure LLM<br>Pure LLM<br>Pure LLM<br>Pure LLM|
|**Input to LLM**<br>Code<br>Code<br>Code<br>Code<br>Code<br>Code; Bug de-<br>scription<br>Code<br>Code|
|**used**<br>and/or<br>and/or<br>learning;<br>ought<br>and/or<br>rning<br>learning;<br>learning;<br>ought<br>and/or<br>rning|
|**How LLM is**<br>Pre-training<br>Fine-tuning<br>Pre-training<br>Fine-tuning<br>Few-shot<br>Chain-of-Th<br>Pre-training<br>Fine-tuning<br>Zero-shot lea<br>Few-shot<br>Zero-shot<br>Chain-of-Th<br>Pre-training<br>Fine-tuning<br>Few-shot lea|
|**LLM**<br>UniX-<br>deGPT<br>atGPT<br>atGPT|
|**Involved **<br>CodeT5<br>CodeT5;<br>Coder; Co<br>Codex<br>CodeT5<br>ChatGPT<br>Codex; Ch<br>T5<br>Codex; Ch|
|**Topic**<br>Program repair<br>Program repair<br>Program repair<br>Program repair<br>Program repair<br>Program repair<br>Program repair<br>Program repair|
|**Year**<br>2023<br>2023<br>2023<br>2023<br>2023<br>2023<br>2023<br>2023|
|important is Local<br>gram Repair?<br>sed Automated Soft-<br>pair: How Far are We?<br>h for Fixing Code In-<br>i  ot<br>ugmented Patch Gen-<br> for Automatic Pro-<br>he InTeractive BEhav-<br>or Automatic Bug Fix-<br> Functionally Correct<br>ural Language Issue<br> Automated Software<br>-Context Demonstra-<br>lligence<br>Tasks<br>with|
|ow<br>ro<br>ba<br>e<br>ac<br>i  Sh<br>A<br>T5 <br> t<br>f<br>g <br>at<br>ed<br> <br> In<br>te|
|text: H<br>eural P<br> Model-<br>ability R<br>n Appro<br>i n Zero-<br>etrieval-<br>h Code<br> <br>ulating <br>AMmers<br>eneratin<br> from N<br><br> T5-bas<br>y Repair<br>s Good <br>Code<br>In|
|**tle**<br> Con<br>in N<br>ned <br>lner<br>: A<br>iies i<br>n: R<br> wit<br>pair<br>: Sim<br>ogr<br>s G<br>dits <br>ions<br>ir: a<br>bilit<br>ake<br>or<br>|
|**ti**<br>f <br>xt<br>ai<br>Vu<br>en<br>inc<br>Ge<br>n <br>Re<br>M<br>Pr<br>d<br> E<br>pt<br>pa<br>ra<br> M<br>f<br>?|
|**Paper **<br><br>Out o<br>Conte<br><br>Pre-tr<br>ware<br><br>RAPG<br>efficie<br><br>RAP-<br>eratio<br>gram<br><br>STEA<br>ior of<br>ing<br>0<br>Towar<br>Code <br>Descri<br>1<br>VulRe<br>Vulne<br>2<br>What <br>tions<br>LLMs|
|**ID**<br>95<br>96<br>97<br>98<br>99<br>10<br>10<br>10|
