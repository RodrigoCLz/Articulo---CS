# Toward Automatic Verification of Quantum Programs

Mingsheng Ying

Centre for Quantum Software and Information, University of Technology Sydney, Australia State Key Laboratory of Computer Science, Institute of Software, Chinese Academy of Sciences, China Department of Computer Science and Technology, Tsinghua University, China Email: Mingsheng.Ying@uts.edu.au; Yuan.Feng@uts.edu.au

Abstract—This paper summarises the results obtained by the author and his collaborators in a program logic approach to the verification of quantum programs, including quantum Hoare logic, invariant generation and termination analysis for quantum programs. It also introduces the notion of proof outline and several auxiliary rules for more conveniently reasoning about quantum programs. Some problems for future research are proposed at the end of the paper.

## I. INTRODUCTION

Programming is error-prone. Programming a quantum computer and designing quantum communication protocols are even worse due to the weird nature of quantum systems [Yin16]. Therefore, verification techniques and automatic tools for quantum programs and quantum protocols will be indispensable whence commercial quantum computers and quantum communication systems are available. In the last 10 years, various verification techniques for classical programs have been extended to deal with quantum programs; in particular, several quantum program logics have been proposed:

- Brunet and Jorrand [BJ04] proposed to apply Birkhoffvon Neumann quantum logic in reasoning about quantum programs. In the Birkhoff-von Neumann logic, closed subspaces of the state Hilbert space of a quantum system are used to represent the properties of the system, and logical connectives ¬ (negation), ∧ (and), ∨ (or) are interpreted as the operations: ortho-complement, meet and join, respectively, in the orthomodular lattice of all closed subspaces of the Hilbert space. The idea of [BJ04] is to add quantum operations (e.g. unitary transformations and quantum measurements) into the language of quantum logic so that it can be employed to describe and reason about the dynamics (evolution) of a quantum system (e.g. a quantum program).

- Chadha, Mateus and Sernadas [CMS06] presented one of the first attempts to develop a Hoare-like logic for quantum programs. The quantum programs considered in [CMS06] can have both classical and quantum variables (memories). But only bounded iterations are allowed in these quantum programs. The logic given in [CMS06] is an extension of exogenous quantum logic [MS06], which has terms representing amplitudes

   - of quantum states, obtained by introducing the axioms for unitary transformations and quantum measurements. Roughly speaking, the assertions (preconditions and postconditions) in this logic are properties of the real and imaginary components of the amplitudes.

- Baltag and Smets [BS06] chose to develop a quantum generalisation of Propositional Dynamic Logic (PDL), which is an extension of Hoare logic for verification of classical programs. The approach of [BS06] is different from [BJ04], [CMS06], and it can be essentially seen as a reinterpretation of the language of PDL where a quantum action is interpreted as a (classical) relation between quantum states and models the input-output relation of a quantum program. In particular, by introducing some axioms to handle separation and locality, their proof system can be used to reason about the behaviours (e.g. entanglement) of compound quantum systems.

- Kakutani [Ka09] proposed a quantum extension of Den Hartog and De Vink’s probabilistic Hoare logic [KV02]. The quantum programming language used in [Ka09] is Selinger’s QPL [Sel04] without recursive calls but with while loops. The assertions in this logic are probabilistic predicates (or assertions) used in [KV02] but, of course, re-interpreted in the setting of quantum computation (e.g. the probability that qubit variable q returns to 0 upon the measurement in the computational basis is 4<sup>1).</sup>

- Some useful proof rules for reasoning about quantum programs were introduced by Feng et al. [FDJY07]. The programming language employed in [FDJY07] is a natural quantum extension of the while-language. For simplicity of presentation, only purely quantum programs without classical variables were considered there. The assertions in these proof rules are physical observables (mathematically modelled by Hermitian operators), or quantum predicates as called in [DP06]. Furthermore, a Hoare-like logic for both partial and total correctness of quantum programs with (relative) completeness was established in [Yin11].

The mathematic foundations, the programming languages and the expressivity of the assertions of the quantum pro-

gram logics presented in [CMS06], [Ka09], [Yin11] are carefully compared in a recent survey [Rand17].

Except program logics, model-checking techniques have also been developed for verification of quantum communication protocols and quantum programs. For example, Gay, Papanikolaou and Nagarajan [GPN08] developed a modelchecker for verifying properties of the quantum systems that can be modelled in the stabiliser formalism. Feng et al. [FYY13] presented an algorithm for model-checking quantum systems described as super-operator valued Markov chains, and the algorithm was implemented by Feng et al. in [FHTZ15]. The problem of checking linear-time properties of quantum systems was studied in [YLYF14], where lineartime properties are defined to be infinite sequences of sets of atomic propositions modelled as closed subspaces of the state Hilbert spaces, as in the Birkhoff-von Neumann quantum logic.

The main purpose of this paper is to summarise the results obtained by the author and his collaborators in a program logic approach to the verification of quantum programs. The paper is an extension of an invited talk at SETTA’2016 [Yin16a], but the results presented in Sections IV and V as well as the examples given in Section III are new and have not been published elsewhere.

The paper is organised as follows: The syntax and semantics of a quantum extension of the while-language is defined and a logic of Hoare-style for reasoning about quantum programs is presented in Section II. As is well-known, correctness specification of classical programs can be very tricky. Indeed, correctness specification of quantum programs can be even much trickier. In Section III, we present several simple examples through which the reader can better understand the difference between classical and quantum correctness specifications. The notion of proof outline is introduced and a strong soundness theorem is proved for quantum programs in Section IV. Several auxiliary axioms and inference rules are given in Section V, which can help to simplify verifications of quantum programs. Some basic ideas for mechanising quantum program verification based on the quantum Hoare logic are described in Section VI. The algorithms for generating invariants and termination analysis of quantum programs are summarised in Sections VII and VIII, respectively. Some topics for future studies are pointed out in the concluding section. For convenience of the reader, several basic properties of operators in Hilbert spaces needed in this paper are listed in Appendix A. Several simple quantum relations (i.e. quantum predicates in a tensor product of state Hilbert spaces) were employed in Section III, a brief discussion on composition of quantum relations that can be used to generate more sophisticated quantum relations from these simple ones is given in Appendix A. For readability, the proofs of the results in Sections IV and V are deferred to Appendix A.

## II. HOARE LOGIC FOR QUANTUM PROGRAMS

Hoare logic is a cornerstone in verification of classical programs. As mentioned in Section I, several attempts [BJ04], [CMS06], [BS06], [FDJY07], [Ka09], [Yin11] have been made to build a Hoare-like logic for quantum programs. In this section, we focus on the one presented in [Yin11] because it is the only quantum Hoare logic with (relative) completeness in the existing literature.

## A. Syntax and Semantics

Let us first briefly recall the syntax of a quantum extension of the while-language. It is assumed that the reader is familiar with the basic notions of quantum computing. (A reader not familiar with them can have a quick look at Section 2 of [Yin11] or Section 1.1 of [YYW17]; for more details, we refer to [NC00] or [Yin16].) We assume a countably infinite set Var of quantum variables. For each q ∈ Var, we write Hq for its state Hilbert space.

Definition 2.1 (Syntax [Yin11], [Yin16]): The quantum while-programs are defined by the grammar:

![](images/p02-01.png)

P ::= skip | P1; P2 | q := |0⟩| q := U [q] (1)<br>

![](images/p02-02.png)

| if (□m · M [q] = m → Pm) fi (2)<br>

![](images/p02-03.png)

| while M [q] = 1 do P od (3)<br>

The command “q := |0⟩” is an initialisation that sets quantum variable q to a basis state |0⟩. The statement “q := U [q]” means that unitary transformation U is performed on quantum register q, leaving the states of the variables not in q unchanged. The construct “if · · · fi” is a quantum generalisation of case or switch statement. In executing it, measurement M = {Mm} is performed on q, and then a subprogram Pm is selected to be executed next according to the outcomes m of measurement. The statement “while · · · od” is a quantum generalisation of while-loop. The measurement in it has only two possible outcomes 0, 1. If the outcome 0 is observed, then the program terminates, and if the outcome 1 occurs, the program executes the loop body P and continues the loop.

To further illustrate these program constructs, let us see two simple examples, both of which are quantum generalisations of certain probabilistic programs. The first is taken from [YYW17], and it is the quantum version of the example of three dials in [KMMM10].

Example 2.1 (Three Quantum Dials): Consider a slot machine that has three dials d1, d2, d3 and two suits ♥ and ♦. It spins the dials independently so that they come to rest on each of the suits with equal probability. This machine can be modelled as a probabilistic program:

![](images/p02-04.png)

flip ≡ (d1 := ♥⊕ 21 d1 := ♦); (d2 := ♥⊕ 1 2 d2 := ♦);<br>(d3 := ♥⊕ 21 d3 := ♦)<br>

where P1 ⊕p P2 stands for a probabilistic choice which chooses to execute P with probability p and to execute Q with probability 1 − p.

We can define a quantum variant of flip as follows:

![](images/p03-01.png)

qflip ≡ H[d1]; H[d2]; H[d3]<br>

where H is the Hadamard gate in the 2-dimensional Hilbert space H2 with {|♥⟩, |♦⟩} as an orthonormal basis. The program qflip also spins the dials, but does it in a quantum way modelled by the Hadamard “coin-tossing” operator H.

It is worth pointing out an interesting difference between the probabilistic and quantum setting: spinning the dials with equal probability can be implemented in many different ways in the quantum world; e.g. a quantum gate different from the Hadamard gate.

The second example is a quantum generalisation of random walk that every one working on probabilistic algorithms or programming must be familiar with. Here is a simplified version (taken from [YYFD13]) of the one-dimensional quantum walks defined in [ABNVW01].

Example 2.2 (Quantum Walk): Let Hc be the 2-dimensional Hilbert space with orthonormal basis states |L⟩ and |R⟩, indicating directions Left and Right, respectively. It is the state space of a quantum coin. Let Hp be the n-dimensional Hilbert space with orthonormal basis states |0⟩, |1⟩, ..., |n − 1⟩, where vector |i⟩ denotes position i for each 0 ≤ i < n. The state space of the walk is H = Hc ⊗Hp. The initial state is |L⟩|0⟩. Each step of the walk consists of:

- 1) Measure the position of the system to see whether it is 1. If the outcome is “yes”, then the walk terminates, otherwise, it continues. The measurement is mathematically modelled by M = {Myes, Mno}, where

![](images/p03-02.png)

Myes = |1⟩⟨1|, Mno = Ip − Myes = � |i⟩⟨i|<br>i=1̸<br>

and Ip is the identity operator in the position space Hp;

- 2) The Hadamard “coin-tossing” operator H is applied in the coin space Hc;

- 3) The shift operator S defined by

![](images/p03-03.png)

S|L, i⟩ = |L, i ⊖ 1⟩, S|R, i⟩ = |R, i ⊕ 1⟩<br>

for i = 0, 1, ..., n − 1 is performed on the space H. Intuitively, the system walks one step left or right according to the direction state. Here, ⊕ and ⊖ stand for addition and subtraction modulo n, respectively. The operator S can be equivalently written as

![](images/p03-04.png)

n−1 n−1<br>S = � |L⟩⟨L| ⊗|i ⊖ 1⟩⟨i| + � |R⟩⟨R| ⊗|i ⊕ 1⟩⟨i|.<br>i=0 i=0<br>

![](images/p03-05.png)

(Sk) ⟨skip, ρ⟩→⟨↓, ρ⟩<br>

![](images/p03-06.png)

(In) ⟨q := |0⟩, ρ⟩→⟨↓, ρ q 0 ⟩<br>

![](images/p03-07.png)

(UT) ⟨q := U [q], ρ⟩→⟨↓, UρU † ⟩<br>⟨P1, ρ⟩→⟨P1 ′, ρ′⟩<br>(SC)<br>⟨P1; P2, ρ⟩→⟨P1 ′; P2, ρ′⟩<br>

![](images/p03-08.png)

(IF) ⟨if (□m · M [q] = m → Pm) fi, ρ⟩→⟨Pm, MmρMm † ⟩<br>(L0) ⟨while M [q] = 1 do P od, ρ⟩→⟨↓, M0ρM0 †⟩<br>(L1) ⟨while M [q] = 1 do P od, ρ⟩→<br>⟨P ; while M [q] = 1 do P od, M1ρM1 †⟩<br>

Figure 1. Transition Rules for Quantum while-Programs. In (IN), ρ<sup>q</sup> 0 = |0⟩q⟨0|ρ|0⟩q⟨0| + |0⟩q⟨1|ρ|1⟩q⟨0| if type(q) = Bool and ρ<sup>q</sup> 0<sup>=�</sup> n<sup>∞</sup> =−∞<sup>|0⟩q⟨n|ρ|n⟩q⟨0|iftype(q)=Int.In(SC),wemake</sup> the convention ↓; P2 = P2. In (IF), m ranges over every possible outcome of measurement M = {Mm}.

This walk can be written as the quantum while-loop:

![](images/p03-09.png)

QW ≡ c := |L⟩; p := |0⟩;while M [p] = no do c := H[c];<br>c, p := S[c, p] od<br>

It is worth noticing an essential difference between the quantum walk and a classical random walk: the coin (or direction) variable c can be in a superposition of |L⟩ and |R⟩ like |+⟩ = √12<sup>(|L⟩+ |R⟩),andthusthewalkerismoving</sup> left and right “simultaneously”; for example,

![](images/p03-10.png)

1 1<br>√2 (|L⟩ + |R⟩)|i⟩→ √2 (|L⟩|i ⊖ 1⟩ + |R⟩|i ⊕ 1⟩).<br>

This means that if the walker is currently at position i, then after one step she/he will be at both position i ⊖ 1 and i ⊕ 1.

Similar to the case of classical while-programs, the operational semantics of quantum programs can be defined as a transition relation between configurations. For each quantum program P , we write var (P ) for the set of quantum variables occurring in P . Let

![](images/p03-11.png)

HP = � Hq<br>q∈var (P )<br>

be the state Hilbert space of P . A partial density operator is defined as a positive operator ρ with trace tr (ρ) ≤ 1. We write D(HP ) for the set of partial density operators in HP . A configuration is a pair ⟨P, ρ⟩, where P is a program or the termination symbol ↓, and ρ ∈D(HP ) denotes the state of quantum variables.

Definition 2.2 (Operational Semantics [Yin11], [Yin16]): The operational semantics of quantum programs is defined by the transition rules in Figure 1.

It is worth pointing out that the transition rules (In), (UT), (IF), (L0) and (L1) are decreed by the basic postulates of quantum mechanics. A major difference between the operational semantics of classical and quantum programs should be noticed. During the execution of a classical case

statement or a while-loop, checking its guard does not change the state of program variables. In contrast, checking the guard of a quantum case statement or a quantum loop requires to perform a measurement on (the system denoted by) the program variables, which, again decreed by a basic postulate of quantum mechanics, changes the state of these variables. From the operational semantics, we see that the control flow of a quantum program is determined by the outcomes of the quantum measurements occurring in the case statements or loops. Note that the outcomes of quantum measurements are classical information, so the control flows of quantum programs considered in this paper are classical. Quantum programs with quantum control flows were studied in [vT04], [AG05], [Zu05], [BP15], [SVV18] and Chapters 6 and 7 of [Yin16].

Definition 2.3 (Denotational Semantics [Yin11], [Yin16]): For any program P , its semantic function is the mapping:

![](images/p04-01.png)

�P � : D(HP ) →D(HP )<br>�P �(ρ) = � {|ρ ′ : ⟨P, ρ⟩→ ∗ ⟨↓, ρ ′ ⟩|}<br>

for every ρ ∈D(HP ), where →<sup>∗</sup> is the reflexive and transitive closure of →, and {| · |} denotes a multi-set.

The defining equation of �P �(ρ) deserves an explanation. It is clear from rules (IF), (L0) and (L1) that transition relation → is usually not deterministic; that is, {|ρ<sup>′</sup> : ⟨P, ρ⟩→<sup>∗</sup> ⟨↓, ρ<sup>′</sup> ⟩|} may have more than one element. This is different from the case of classical while-programs. The summation in the right-hand side of the equation comes from the essential linearity of quantum mechanics. It is proved that �P �(·) is a quantum operation (or a super-operator) (for the definition of quantum operation, see [NC00], Chapter 8 or [Yin16], Chapter 2).

To illustrate the above two definitions, let reconsider the three quantum dials in Example 2.1.

Example 2.3 (Semantics of Three Quantum Dials): — A Continuation of Example 2.1. A state of probabilistic program flip is a configuration of the slot machine, i.e. a mapping from dials to suits. The semantics of flip is a function that maps each initial state to a uniform distribution of states in which every configurations has probability<sup>1</sup> 8<sup>.</sup>

In contrast, the state Hilbert space of quantum program qflip is then H2<sup>⊗3.Forinstance,ifwewrite:</sup>

![](images/p04-02.png)

1 1<br>|+⟩ = √2 (|♥⟩ + |♦⟩), |−⟩ = √2 (|♥⟩−|♦⟩)<br>

for the equal superpositions of |♥⟩ and |♦⟩, then:

![](images/p04-03.png)

�qflip�(|+, −, +⟩) = |♥, ♦, ♥⟩;<br>

if we write:

![](images/p04-04.png)

1<br>|W ⟩ = √3 (|♥, ♥, ♦⟩ + |♥, ♦, ♥⟩ + |♦, ♥, ♥⟩)<br>

for the Werner state, a typical entangled state of three qubits, then

![](images/p04-05.png)

1<br>�qflip�(|W ⟩) =<br>2√6 (3|♥, ♥, ♥⟩ + |♥, ♥, ♦⟩ + |♥, ♦, ♥⟩<br>−|♥, ♦, ♦⟩ + |♦, ♥, ♥⟩−|♦, ♥, ♦⟩<br>−|♦, ♦, ♥⟩− 3|♦, ♦, ♦⟩).<br>

(Note that Definitions 2.2 and 2.3 are given in a more general way; i.e. in terms of density operators. Here, for simplicity, a pure state |ψ⟩ is identified with the corresponding density operator ρ = |ψ⟩⟨ψ|.)

The Löwner order between operators in the state Hilbert space HP of a quantum program is defined as follows:

![](images/p04-06.png)

A ⊑ B if B − A is a positive operator.<br>

This order can be naturally lifted to an order between quantum operations (or super-operators). It can be shown that the set D(HP ) of partial density operators in HP with the Löwner order ⊑ is a complete partial order (CPO), and all quantum operations in HP form a CPO too. Then a fixed point characterisation for the denotational semantics of quantum while-loops can be derived (see Proposition 5.1(6) and Corollary 5.1 in [Yin11], or Proposition 3.3.2 and Corollary 3.3.1 in [Yin16]).

## B. Partial Correctness and Total Correctness

Now we review the notions of partial and total correctness for quantum programs. Recall from [MM05] that probabilistic predicates (or assertions, e.g. preconditions and postconditions) are defined to be bounded real-valued functions interpreted as the expectations of random variables. As introduced in [DP06], a quantum predicate in a Hilbert space H is an observable (a Hermitian operator) A in H with 0 ⊑ A ⊑ I, where 0 and I are the zero operator and the identity operator in H, respectively, and ⊑ stands for the Löwner order. In the quantum foundations literature, a quantum predicate is called an effect (see, for example, [Kr83]).

Definition 2.4 (Correctness Formula [Yin11], [Yin16]): A correctness formula (or a Hoare triple) is a statement of the form

![](images/p04-07.png)

{A}P {B}<br>

where P is a quantum program, and both A, B are quantum predicates in HP , called the precondition and postcondition, respectively.

The appearance of a quantum Hoare triple is exactly the same as that of its classical counterpart. But in a classical Hoare triple, precondition A and postcondition B stands for (first-order) logical formulas, and in a quantum Hoare triple, A and B are two operators that are interpreted as observables in physics.

Definition 2.5 (Correctness [Yin11], [Yin16]): — Partial and Total.

- 1) The correctness formula {A}P {B} is true in the sense of total correctness, written |=tot {A}P {B}, if for all input states ρ ∈D(HP ) we have:

tr(Aρ) ≤ tr(B�P �(ρ)). (4)

- 2) The correctness formula {A}P {B} is true in the sense of partial correctness, written |=par {A}P {B}, if for all input states ρ ∈D(HP ) we have:

![](images/p05-01.png)

tr(Aρ) ≤ tr(B�P �(ρ)) + [tr(ρ) − tr(�P �(ρ))]. (5)<br>

A key to understanding the above definition is the observation that tr (Aρ) is the expected (average) value of observable A when the system is in state ρ. The following lemma shows that the defining inequalities (4) and (5) for total and partial correctness can be restated in a form of Löwner order, which is often easier to manipulate because the universal quantifier over density operator ρ is eliminated.

Let us consider the three quantum dials in Examples 2.1 and 2.3 once again to illustrate the notion of correctness introduced in the above definition.

Example 2.4 (Correctness of Three Quantum Dials): We write:

![](images/p05-02.png)

1<br>|GHZ ⟩ = √2 (|♥, ♥, ♥⟩ + |♦, ♦, ♦⟩)<br>

for the GHZ (Greenberger-Horne-Zeilinger) state, another typical entangled state of three qubits,

![](images/p05-03.png)

|Φ⟩ = 1<br>2 (|♥, ♥, ♥⟩ + |♥, ♦, ♦⟩ + |♦, ♥, ♦⟩ + |♦, ♦, ♥⟩),<br>

and |Ψ⟩ = |♥, ♥, ♥⟩. Then A = |Φ⟩⟨Φ|, B = |Ψ⟩⟨Ψ| and C = |GHZ ⟩⟨GHZ | are all quantum predicates. It is easy to check that

![](images/p05-04.png)

|=tot {A}qflip{C}, |=tot { 1<br>4 B}qflip{C}.<br>

This means that if the input is state |Φ⟩, then program qflip will certainly output the GHZ state; and if the input is state |Ψ⟩, it will output a state |Γ⟩ that is similar to the GHZ state in the sense:

Pr(|Γ⟩ and the GHZ state cannot be discriminated) ≥<sup>1</sup> 4<sup>.</sup>

Note that partial and total correctness are the same for qflip because it does not contain any loop.

The quantum predicates A, B, C in the above example are very simple and defined by a particular input/output state. More examples of correctness specifications will be given in Section III.

Lemma 2.1: 1) |=tot {A}P {B} if and only if A ⊑ �P �<sup>∗</sup> (B). 2) |=par {A}P {B} if and only if:

![](images/p05-05.png)

A ⊑ �P � ∗ (B) + (I − �P � ∗ (I))<br>

(Ax.Sk) {A}Skip{A}

![](images/p05-06.png)

(Ax.In.B) {|0⟩q⟨0|A|0⟩q⟨0| + |1⟩q⟨0|A|0⟩q⟨1|}q := |0⟩{A}<br>∞<br>(Ax.In.I) � |n⟩q⟨0|A|0⟩q⟨n| q := |0⟩{A}<br>�n=−∞ �<br>

![](images/p05-07.png)

(Ax.UT) {U † AU }q := U [q] {A}<br>{A}P1{B} {B}P2{C}<br>(R.SC)<br>{A}P1; P2{C}<br>

![](images/p05-08.png)

{Am}Pm{B} for all m<br>(R.IF)<br>��m M † m A m M m� if (□m · M [q] = m → Pm) fi{B}<br>{B}P �M0 †AM0 + M † 1 BM1 �<br>(R.LP)<br>{M0 †AM0 + M † 1 BM1}while M [ q] = 1 do P od{A}<br>A ⊑ A ′ {A ′ }P {B ′ } B ′ ⊑ B<br>(R.Or)<br>{A}P {B}<br>

Figure 2. Proof System qPD for Quantum while-Programs. In (Ax.In.B), type(q) = Boolean. In (Ax.In.I), type(q) = Int.

![](images/p05-09.png)

• {Q}S{M0 †PM0 + M † 1 QM1}<br>

![](images/p05-10.png)

• for any ǫ > 0, tǫ is a (M1 †QM1, ǫ)−ranking<br>function of loop while M [q] = 1 do S od<br>(R.LT)<br>{M0 †PM0 + M † 1 QM1}while M [ q] = 1 do S od{P }<br>

Figure 3. Proof System qTD for Quantum while-Programs.

where I is the identity operator in HP , and �P �<sup>∗</sup> stands for the dual of super-operator �P � (see Definition A.1 in Appendix A).

Proof: Immediate from Lemma 4.1.2 in [Yin16] and Lemma A.2 in Appendix A.

The above lemma will be extensively used in the proofs of the results in Section V.

## C. Quantum Hoare Logic

A Hoare-like logic for quantum programs is established in [Yin11]. It consists of:

- A proof system qPD for partial correctness: The axioms and inference rules of qPD are presented in Figure 2.

- A proof system qTD for total correctness: qTD is obtained from qPD by replacing rule (R.LP) with the rule (R.LT) given in Figure 3. The notion of ranking function used in rule (R.LT) is defined in the following: Definition 2.6 ([Yin11], [Yin16]): Let A be a quantum predicate in Hvar (P )∪q<sup>andrealnumberǫ>0.A</sup> function

t : D(Hvar (P )∪q<sup>) →N(nonnegativeintegers)</sup>

is called a (A, ǫ)-ranking function of quantum loop “while M [q] = 1 do P od” if it satisfies the following two conditions: for all ρ ∈D(Hvar (P )∪q<sup>),</sup>

![](images/p06-01.png)

1) t �S� M1ρM1 † ≤ t(ρ); and<br>� � ��<br>

2) tr(Pρ) ≥ ǫ implies t �S� M1ρM1<sup>†</sup> < t(ρ). � � ��

It is interesting to carefully compare the Hoare rule for partial correctness of classical loops:

![](images/p06-02.png)

{ϕ ∧ b}P {ϕ}<br>

![](images/p06-03.png)

{ϕ}while b do P od{ϕ ∧¬b}<br>

and its variant for total correctness with the corresponding rules (R.LP) and (R.LT) for quantum loops, respectively. At the first glance, the rules for classical loops and those for quantum loops are very different. But actually there is a certain similarity between them: in the rules for classical loops, ϕ∧b (resp. ϕ∧¬b) can be thought of as the restriction of ϕ under b (resp. ¬b). If we set:

![](images/p06-04.png)

D = M0 †AM0 + M † 1 BM1,<br>

then B can be seen as the restriction of D under M1 and A the restriction of D under M0, and M0 can be considered as the negation of M1. Furthermore, as we will see at the end of Section VII, rules (R.LP) and (R.LT) can also be understood in the context of inductive assertion.

The soundness and (relative) completeness of both proof system qPD and qTD were proved in [Yin11], [Yin16]. Theorem 2.1 (Completeness [Yin11], [Yin16]): For any quantum while-program P , and for any quantum predicates A, B,

![](images/p06-05.png)

|=par {A}P {B} ⇔⊢qPD {A}P {B},<br>|=tot {A}P {B} ⇔⊢qTD {A}P {B}.<br>

![](images/p06-06.png)

III. EXAMPLES OF QUANTUM CORRECTNESS<br>SPECIFICATION<br>

In this section, let us see several simple examples, which shows some interesting and tricky differences between specifying correctness of classical programs and that of quantum programs.

## A. Unary Quantum Predicates

A quantum predicate about a single quantum system q; i.e. an observable (between the zero and identity operators) in state Hilbert space Hq can be understood as a unary quantum predicate.

Example 3.1: An equality like x = c with x being a variable and c a constant often appears in precondition or postcondition of a classical program correctness formula, e.g.

![](images/p06-07.png)

|=tot {x = 1}x := x + 1{x = 2}<br>

Let q be a quantum variable and |ψ⟩ a given (constant) state in Hq. Then equality “q = |ψ⟩” can be expressed as quantum predicate A = |ψ⟩⟨ψ| in Hq, and we have:

![](images/p06-08.png)

|=tot {U † |ψ⟩⟨ψ|U } q := U [q] {A}, (6)<br>

![](images/p06-09.png)

|=tot {A} q := U [q] {U |ψ⟩⟨ψ|U † } (7)<br>

for any unitary operator U in Hq. The precondition in (6) and the postcondition in (7) express equalities “q = U<sup>†</sup> |ψ⟩”, “q = U |ψ⟩”, respectively. More generally, for any closed subspace X of Hq, Membership “q ∈ X” can be expressed as quantum predicate PX (the projection onto X) and we have:

![](images/p06-10.png)

|=tot {PU †(X)} q := U [q] {PX }, (8)<br>

![](images/p06-11.png)

|=tot {PX } q := U [q] {PU(X)} (9)<br>

The precondition in (8) and the postcondition in (9) express memberships “q ∈ U<sup>†</sup> (X)”, “q ∈ U (X)”, respectively.

## B. Quantum Relations

A quantum predicate about multiple quantum systems q1, ..., qn; i.e. an observable (between the zero and identity operators) in the tensor product:

![](images/p06-12.png)

n<br>� Hqi ,<br>i=1<br>

can be understood as a quantum relation among q1, ..., qn. In particular, a quantum predicate A in H1 ⊗H2 can be seen as a quantum (binary) relation between H1 and H2. The following are two examples showing some quantum relations used in preconditions and postconditions. A further discussion about quantum relation is given in Appendix A.

Example 3.2: An equality like x = y between two variables x, y also often appears in precondition or postcondition of a classical program correctness formula, e.g.

![](images/p06-13.png)

|=tot {x = y} x := x + 1; y := y + 1 {x = y}<br>

- 1) Let p, q be two quantum variables with the same state Hilbert space H. Then equality “p = q” can be expressed as the symmetrisation operator:

![](images/p06-14.png)

S+ = 1<br>2 (I + SWAP)<br>

where I is the identity operator in H⊗H, and operator SWAP in H ⊗H is defined by

![](images/p06-15.png)

SWAP|ϕ, ψ⟩ = |ψ, ϕ⟩<br>

for all |ϕ⟩, |ψ⟩∈H, together with linearity. It is easy to see that SWAP · S+ = S+ · SWAP = SWAP · S+ · SWAP = S+. Furthermore, for any unitary operator U in H, it holds that:

![](images/p06-16.png)

|=tot {S+} p := U [p]; q := U [q] {S+}<br>

It is interesting to note that a similar conclusion holds for the anti-symmetrisation operator:

![](images/p06-17.png)

S− = 1<br>2 (I − SWAP)<br>

that is, we have SWAP · S− = S− · SWAP = −S−, SWAP · S− · SWAP = S− and

![](images/p06-18.png)

|=tot {S−} p := U [p]; q := U [q] {S−}<br>

- 2) Equality “x = y” can also be expressed in a different way; that is, as the operator

![](images/p07-01.png)

=B = |Ψ⟩⟨Ψ|<br>

in H ⊗H, where d = dim H and |Ψ⟩ = √1d �i<sup>|ii⟩is</sup> the maximally entangled state defined by an orthonormal basis B = {|i⟩} of H. This equality =B has an intuitive explanation. The Hilbert-Schmidt inner product of two operators A, B in H:

![](images/p07-02.png)

⟨A|B⟩ = tr �A † B�<br>

is often used to measure the similarity between A and B. For two (mixed) states ρ, σ in H, it follows immediately from equation (9.73) in [NC00] that

![](images/p07-03.png)

⟨ρ|σ⟩ = d · ⟨Ψ|ρ ⊗ σ|Ψ⟩ = d · tr (=B (ρ ⊗ σ)) .<br>

The quantity tr (=B (ρ ⊗ σ)) can be interpreted as the degree that ρ, σ satisfies relation =B. Obviously, we have:

![](images/p07-04.png)

|=tot {=U †(B)} p := U [p]; q := U [q] {=B}<br>

![](images/p07-05.png)

|=tot {=B} p := U [p]; q := U [q] {=U(B)}<br>

where =U(B), =U †(B) are the equalities defined by orthonormal bases U (B) = {U |i⟩} and U<sup>†</sup> (B) = �U<sup>†</sup> |i⟩�, respectively. Example 3.3: Consider the following correctness formula for classical programs:

![](images/p07-06.png)

|=tot {X = x ∧ Y = y} R := X; X := Y ; Y := R<br>{X = y ∧ Y = x}<br>

It means that after executing the program, the values of variables X and Y are exchanged. To properly specify the precondition and postcondition, auxiliary (ghost) variables x, y are introduced. In quantum computing, statements R := X, X := Y and Y := R cannot be directly realised as prohibited by the no-cloning theorem [WZ82]. But we can consider the following modification: let X, Y, R be three quantum variables with the same state Hilbert space H. Then we have:

![](images/p07-07.png)

|=tot {A}R, X := SWAP[R, X]; Y, Y := SWAP[X, Y ];<br>Y, R := SWAP[Y, R] {(SWAP ⊗ I)A(SWAP ⊗ I)}<br>(10)<br>

for any quantum predicate A in H⊗H⊗H, where the first, second and third H are the state Hilbert spaces of X, Y, R respectively, and I is the identity operator in H. Note that we do not use any auxiliary (ghost) variable in correctness formula (10). In particular, if

![](images/p07-08.png)

A = |ϕ⟩⟨ϕ| ⊗|ψ⟩⟨ψ| ⊗ I,<br>

where |ϕ⟩, |ψ⟩∈H, and I is the identity operator in H, then it holds that

![](images/p07-09.png)

|=tot {|ϕ⟩⟨ϕ| ⊗|ψ⟩⟨ψ| ⊗ I}R, X := SWAP[R, X];<br>Y, Y := SWAP[X, Y ]; Y, R := SWAP[Y, R] (11)<br>{|ψ⟩⟨ψ| ⊗|ϕ⟩⟨ϕ| ⊗ I}<br>

Intuitively, the precondition and postcondition of (11) means “X = |ϕ⟩ and Y = |ψ⟩”, “X = |ψ⟩ and Y = |ϕ⟩”, respectively. Here, auxiliary variables |ϕ⟩, |ψ⟩ are employed.

All of the examples given in the previous subsection and this subsection can be proved using axiom (Ax.UT) and rule (R.SC) in Figure 2. A more interesting example using rule (R.IF) will be presented in Section IV.

## C. Logical Connectives

Logical connectives are widely used in specifying (the preconditions and postconditions of) classical programs. Here, we show that several quantum counterparts of them can be used in specifying correctness of quantum programs. However, it is not the case that every logical connective has an appropriate quantum counterpart.

Example 3.4: The predicate “True” and “False” are described by the identity and zero operators I and 0, respectively, in the state Hilbert space HP of the program P under consideration.

![](images/p07-10.png)

• |=par {I}P {B} means that for any density operator ρ,<br>

![](images/p07-11.png)

tr (B�P �(ρ)) = tr (�P �(ρ));<br>

that is, the probability that postcondition B is satisfied by the output is equal to the probability that the program terminates.

- |=par {A}P {I} always holds, because A ⊑ I implies that for any partial density operator ρ,

tr (Aρ) ≤ tr (ρ) = tr(�P �(ρ)) + [tr(ρ) − tr (�P �(ρ))].

- |=tot {I}P {B} means that for any density operator ρ, tr (B�P �(ρ)) = 1.

Since B ⊑ I, we have tr (B�P �(ρ)) ≤ tr(�P �(ρ)) and thus tr (�P �(ρ)) = 1; that is, program P always terminates, and output �P �(ρ) satisfies postcondition B.

- |=tot {A}P {I} means that for any density operator, tr(Aρ) ≤ tr(�P �(ρ)); intuitively, if precondition A is satisfied by input ρ to P , then P terminates.

- Example 3.5: 1) Negation in classical logic has a quantum counterpart: for each quantum predicate in Hilbert space H, I − A can be used as the negation of A. In fact, for any density operator ρ in H,

tr[(I − A)ρ] = 1 − tr (Aρ).

- 2) Conjunction in classical logic does not always have an appropriate quantum counterpart; some difficulties

caused by this fact in reasoning about quantum programs were discussed in [YCFD07]. But if A1 and A2 are quantum predicates in H1, H2, respectively, then A1 ⊗ A2 can be used as the conjunction (in H1 ⊗H2) of A1 and A2 because for any density operator ρ1 in H1 and ρ2 in H2, it holds that

tr ((A1 ⊗ A2)(ρ1 ⊗ ρ2)) = tr (A1ρ1) · tr (A2ρ2);

for example, see equation (11).

- 3) For a family {Ai}of quantum predicates in the same Hilbert space H, and a probability distribution {pi}, we often use the convex combination<sup>�</sup> i<sup>piAiasa</sup> connective; for example, see rules (R.CC) and (R.Inv) in Figure 7.

- 4) In a sense, quantum predicate<sup>�</sup> m<sup>M †</sup> m<sup>AmMmin rule</sup> (R.IF) in Figure 2 can be understood as the disjunction of (the conjunction of) “the outcome of measurement M is m” and quantum predicate Am.

IV. PROOF OUTLINES

The notion of proof outline can be introduced to structure a correctness proof of a classical while-program, according to the structure of the program itself, so that the proof is easier to follow (see [ABO09], Section 3.4). It is also a basis for defining non-interference in reasoning about parallel programs with shared variables. In this section, we generalise this notion to the quantum case.

Definition 4.1: Let S be a quantum while-programs.

- 1) A proof outline for partial correctness of S is a formula {A}P<sup>∗</sup> {B} formed by the formation axioms and rules in Figure 4, where P<sup>∗</sup> results from P by interspersing quantum predicates.

- 2) A proof outline for total correctness of S is defined by introducing ranking function into rule (R.LP’) (see Definition 2.6 and rule (R.LT)).

Let us consider a simple example to illustrate the above definition.

Example 4.1 (Teleportation [BBCJPW92]): Quantum teleportation is a protocol that can send quantum states only using a classical communication channel. Suppose that Alice possesses two qubits p, q and Bob possesses qubit r, and there is entanglement, i.e. the EPR (Einstein-PodolskyRosen) pair:

![](images/p08-01.png)

1<br>|β00⟩ = √2 (|00⟩ + |11⟩),<br>

between q and r. Then Alice can send a quantum state |ψ⟩ = α|0⟩ + β|1⟩ to Bob, i.e. from p to r, by twobit classical communication (for detailed description, see [NC00], Section 1.3.7). This protocol can be written as quantum program QTEL in Figure 5. The correctness of QTEL can be described as the Hoare triple:

{|ψ⟩p⟨ψ| ⊗|β00⟩q,r⟨β00|} QTEL {Ip ⊗ Iq ⊗|ψ⟩r⟨ψ|} .

A proof outline for the correctness of QTEL is also presented in Figure 5.

We can define the notion of subprogram of a quantum program in a familiar way; namely by induction on the length of the program. Then a special form of proof outline is defined in the following:

Definition 4.2: A proof outline {A}P<sup>∗</sup> {B} of P is called standard if every subprogram Q of P is proceeded by exactly one quantum predicate, denoted pre(Q), in P<sup>∗</sup> .

The next proposition shows that standard proof outlines are indeed sufficient for reasoning about correctness of quantum programs.

- Proposition 4.1: 1) If {A}P<sup>∗</sup> {B} is a proof outline for partial correctness (respectively, total correctness), then ⊢qPD {A}P {B} (respectively, ⊢qTD {A}P {B}).

- 2) If ⊢qPD {A}P {B} (respectively, ⊢qTD {A}P {B}), then there is a standard proof outline {A}P<sup>∗</sup> {B} for partial correctness (respectively, total correctness).

- Proof: Induction on the lengths of proof and

formation.

![](images/p08-02.png)

As in classical programming, another usage of proof outline is that it enables us to establish a strong soundness of quantum Hoare logic. To this end, we need the following:

Definition 4.3: Let P be a quantum while-program and T a subprogram of P . Then at (T, P ) is inductively defined as follows:

- 1) If T ≡ P , then at (T, P ) ≡ P ;

- 2) If P ≡ P1; P2, then at (T, P ) ≡ at (T, P1); P2 when T is a subprogram of P1, and at (T, P ) ≡ at (T, P2) when T is a subprogram of P2;

- 3) If P ≡ if (□m · M [q] = m → Pm) fi, then for each m, whenever T is a subprogram of Pm, at (T, P ) ≡ at (T, Pm);

- 4) If P ≡ while M [q] = 1 do P<sup>′</sup> od and T is a subprogram of P<sup>′</sup> , then at (T, P ) ≡ at (T, P<sup>′</sup> ); P .

Intuitively, at (T, P ) denotes the remainder of P to be executed when the control is at subprogram T .

Definitions 4.1 to 4.3 are straightforward generalisations of the corresponding concepts for classical programs (see for example [ABO09], Section 3.4). However, the strong soundness (Theorem 3.3 in [ABO09]) cannot be straightforwardly generalised to the quantum case. To present the strong soundness for quantum programs, we also need to extend the transition relation between configurations given in Definition 2.2 to a transition relation between configuration ensembles. We define a configuration ensemble as a multiset {|⟨Pi, ρi⟩|} of configurations with

![](images/p08-03.png)

� tr (ρi) ≤ 1.<br>i<br>

For simplicity, we identify a singleton {|⟨P, ρ⟩|} with the configuration ⟨P, ρ⟩.

![](images/p09-01.png)

(Ax.Sk ′ ) {A}Skip{A}<br>(Ax.In.B ′ ) {|0⟩q⟨0|A|0⟩q⟨0| + |1⟩q⟨0|A|0⟩q⟨1|}q := |0⟩{A}<br>∞<br>(Ax.In.I ′ ) � |n⟩q⟨0|A|0⟩q⟨n| q := |0⟩{A}<br>�n=−∞ �<br>(Ax.UT ′ ) {U † AU }q := U [q] {A}<br>{A}P1 ∗{B} {B}P2 ∗{C}<br>(R.SC ′ )<br>{A}P1 ∗; {B}P 2  ∗{C}<br>{Ami}Pm ∗ i {B} (i = 1, ..., k)<br>(R.IF ′ )<br>i=1 M † mi Am i Mm i if M [q] = m1 →{Am1 } Pm ∗ 1<br>��k �<br>..................<br>□ M [q] = mk →{Amk } Pm ∗ k<br>fi {B}<br>{B}P ∗ � M0 †AM0 + M † 1 BM1 �<br>(R.LP ′ )<br>{M0 †AM0 + M † 1 BM1} while M [ q] = 1 do {B} P ∗ � M0 †AM0 + M † 1 BM1 � od {A}<br>A ⊑ A ′ {A ′ }P ∗ {B ′ } B ′ ⊑ B<br>(R.Or ′ )<br>{A}{A ′ }P {B ′ }{B}<br>{A}P ∗ {B}<br>(R.Del)<br>{A}P ∗∗ {B}<br>

Figure 4. Formation Axioms and Rules for Partial Correctness of Quantum while-Programs. In (R.IF’), {m1, ..., mk} is the set of all possible outcomes of measurement M . In (R.Del), S<sup>∗∗</sup> is obtained by deleting some quantum predicates from S<sup>∗</sup> .

![](images/p09-02.png)

{|ψ⟩p⟨ψ| ⊗|β00⟩q,r⟨β00|}<br>⊑{|β00⟩p,q⟨β00| ⊗|ψ⟩r⟨ψ| + |β10⟩p,q⟨β10| ⊗|ψ1⟩r⟨ψ1|<br>

![](images/p09-03.png)

+ |β01⟩p,q⟨β01| ⊗|ψ2⟩r⟨ψ2| + |β11⟩p,q⟨β11| ⊗|ψ3⟩r⟨ψ3|}<br>

![](images/p09-04.png)

QTEL ≡ p, q := CNOT[p, q];<br>{|+⟩p⟨+| ⊗|0⟩q⟨0| ⊗|ψ⟩r⟨ψ| + |−⟩p⟨−| ⊗|0⟩q⟨0| ⊗|ψ1⟩r⟨ψ1|<br>+ |+⟩p⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨ |+⟩p⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨+⟩p⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟩p⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨p⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨ + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨ |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨1⟩q⟨1| ⊗|ψ3⟩r⟨⟩q⟨1| ⊗|ψ3⟩r⟨q⟨1| ⊗|ψ3⟩r⟨⟨1| ⊗|ψ3⟩r⟨1| ⊗|ψ3⟩r⟨| ⊗|ψ3⟩r⟨ψ3⟩r⟨3⟩r⟨⟩r⟨r⟨⟨ψ3|}<br>p := H[p];<br>{|0⟩p⟨0| ⊗|0⟩q⟨0| ⊗|ψ⟩r⟨ψ| + |1⟩p⟨1| ⊗|0⟩q⟨0| ⊗|ψ1⟩r⟨ψ1|<br>+ |0⟩p⟨0| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |1⟩p⟨1| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨ψ3|}<br>if M [q] = 0 →{|0⟩p⟨0| ⊗ Iq ⊗|ψ⟩r⟨ψ| + |1⟩p⟨1| ⊗ Iq ⊗|ψ1⟩r⟨ψ1|} skip<br>□ 1 →{|0⟩p⟨0| ⊗ Iq ⊗|ψ2⟩r⟨ψ2| + |1⟩p⟨1| ⊗ Iq ⊗|ψ3⟩r⟨ψ3|} r := X[r]<br>fi;<br>{|0⟩p⟨0| ⊗ Iq ⊗|ψ⟩r⟨ψ| + |1⟩p⟨1| ⊗ Iq ⊗|ψ1⟩r⟨ψ1|}<br>if M [p] = 0 →{Ip ⊗ Iq ⊗|ψ⟩r⟨ψ|} skip<br>□ 1 →{Ip ⊗ Iq ⊗|ψ1⟩r⟨ψ1|} r := Z[r]<br>fi {Ip ⊗ Iq ⊗|ψ⟩r⟨ψ|}<br>

![](images/p09-05.png)

+ |+⟩p⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨ |+⟩p⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨+⟩p⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟩p⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨p⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨+| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨| ⊗|1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨1⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟩q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨q⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨1| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨| ⊗|ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨ψ2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨2⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨ψ2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨2| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨| + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨ + |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨ |−⟩p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨p⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨⟨−| ⊗|1⟩q⟨1| ⊗|ψ3⟩r⟨1⟩q⟨1| ⊗|ψ3⟩r⟨⟩q⟨1| ⊗|ψ3⟩r⟨q⟨1| ⊗|ψ3⟩r⟨⟨1| ⊗|ψ3⟩r⟨1| ⊗|ψ3⟩r⟨| ⊗|ψ3⟩r⟨ψ3⟩r⟨3⟩r⟨⟩r⟨r⟨⟨ψ3|}<br>

Figure 5. Quantum Teleportation Program and Correctness Proof Outline. (1) Quantum states: |ψ1⟩ = α|0⟩− β|1⟩, |ψ2⟩ = β|0⟩ + α|1⟩, |ψ3⟩ = −β|0⟩ + α|1⟩. (2) Entangled states: |β01 = √12<sup>(|01⟩+|10⟩,|β10=</sup> √12<sup>(|00⟩−|11⟩,|β01=</sup> √12<sup>(|01⟩−|10⟩.(3)Measurementinthe</sup> computational basis: M = {M0, M1}, where M0 = |0⟩⟨0|, M1 = |1⟩⟨1|.

Definition 4.4: The transition relation between configuration ensembles is of the form:

![](images/p10-01.png)

{|⟨Pi, ρi⟩|} →{|⟨Qj, σj⟩|} (12)<br>

and defined by rules (Sk), (In), (UT), (SC) in Figure 1 together with the rules presented in Figure 6.

Now we are ready to present the strong soundness of the quantum Hoare logic.

Theorem 4.1 (Strong Soundness): Let {A}P<sup>∗</sup> {B} be a standard proof outline for partial correctness. If

![](images/p10-02.png)

⟨P, ρ⟩→ ∗ {|⟨Pi, ρi⟩|},<br>

then:

![](images/p10-03.png)

1) for each i, Pi ≡ at (Ti, P ) for some subprogram Ti of<br>P or Pi ≡↓; and<br>2) tr (Aρ) ≤ � i tr (Biρi), where<br>B if Pi ≡↓,<br>Bi =<br>�pre (Ti) if Pi ≡ at (Ti, P ) .<br>

Proof: See Appendix A.

![](images/p10-04.png)

A difference between the above theorem and the strong soundness for classical while-programs (see [ABO09], Theorem 3.3) should be noticed. The summation in the righthand side of the inequality in clause 2 of the above theorem indicates that we have to consider all the reached programs Pi collectively in the quantum case. The reason behind it is that certain nondeterminism is introduced in the operational semantics of case statements and while-loops in quantum computation.

![](images/p10-05.png)

V. AUXILIARY AXIOMS AND RULES<br>

Several auxiliary axioms and rules introduced in [Gor75], [Har79] (see also [ABO09], Section 3.8) are very useful for simplifying the presentation of correctness proofs of classical programs. In this section, we generalise some of them into the quantum case. For this purpose, we first introduce several notations. Let X ⊆ Y ⊆ Var, and let A be an operator in

![](images/p10-06.png)

HX = � Hq.<br>q∈X<br>

Then operator:

![](images/p10-07.png)

cl Y (A) = A ⊗ IHY \X<br>

is called the cylindric extension of A in HY . If X, Y ⊆ Var and X ∩ Y = ∅. Then partial trace tr Y is a mapping from operators in HX∪Y to operators in HX defined by

![](images/p10-08.png)

tr Y (|ϕ⟩⟨ψ| ⊗|ϕ ′ ⟩⟨ψ ′ |) = ⟨ψ ′ |ϕ ′ ⟩· |ϕ⟩⟨ψ|<br>

for every |ϕ⟩, |ψ⟩ in HX and |ϕ<sup>′</sup> ⟩, |ψ<sup>′</sup> ⟩ in HY .

Now we can present the auxiliary axioms and rules for quantum programs in Figure 7.

It is interesting to compare our auxiliary axioms and rules for quantum programs with those for classical programs:

- The appearance of axiom (Ax.Inv) is the same as axiom (INVARIANCE) in Section 3.8 of [ABO09].

- Obviously, rule (R.SO) is quantum generalisations of rule (SUBSTITUTION) in [ABO09], with the substitution z := t being replaced by an arbitrary superoperator E.

- It is easy to see that rules (R.CC) and (R.Inv) are generalisations of rules (CONJUNCTION) and (INVARIANCE), respectively, in [ABO09], with logical conjunction being replaced by a probabilistic (convex) combination.

- It is more interesting to note that rule (R.TI) is a quantum generalisation of two rules (DISJUNCTION) and (∃-INTRODUCTION) in [ABO09], where partial trace is considered as a quantum counterpart of logical disjunction and existence quantifier.

The following theorem establishes soundness of the auxiliary axioms and rules in Figure 7.

- Theorem 5.1: 1) The axiom (Ax.Inv) is sound for partial correctness.

- 2) The rules (R.TI), (R.CC), (R.Inv), (R.SO) and (R.Lim) are sound both for partial and total correctness.

- Proof: See Appendix B

Before concluding this section, let us see a simple example to show how the auxiliary axioms and rules can be used to derive some new properties of a quantum program.

Example 5.1: Let q be a qubit variable. Then by (Ax.UT) in Figure 3 we obtain:

![](images/p10-09.png)

{|−⟩⟨−|} q := H[q] {|1⟩⟨1|} (13)<br>

where H is the Hadamard gate and |−⟩ = √12<sup>(|0⟩−|1⟩).</sup> The rule (R.SO) in Figure 7 is especially useful for reasoning about quantum computation with noise. The amplitude damping channel is an important type of quantum noise where energy is lost from a quantum system with a certain probability γ. It can be modelled by quantum operation:

![](images/p10-10.png)

E(ρ) = E0ρE0 + E1ρE1<br>

for any density operator ρ, where

![](images/p10-11.png)

E0 = � 01 √10 − γ � , E1 = � 10 √0γ � .<br>Then applying (R.SO) to (13) yields:<br>√1 − γ<br>|0⟩⟨0| − (|0⟩⟨1| + |1⟩⟨0|) + 1 − γ |1⟩⟨1|<br>� 1 +2 γ 2 2 �<br>q := H[q] {γ|0⟩⟨0| + (1 − γ)|1⟩⟨1|} .<br>

Then applying (R.SO) to (13) yields:

VI. MECHANISING QUANTUM PROGRAM VERIFICATION

Proving correctness of classical programs using Hoare logic is very fiddly and tedious. As we saw from the example given in Figure 5, it is even worse to prove correctness of

![](images/p11-01.png)

(IF ′ ) ⟨if (□m · M [q] = m → Pm) fi, ρ⟩→{|⟨Pm, MmρMm † ⟩|}<br>(L ′ ) ⟨while M [q] = 1 do P od, ρ⟩→{|⟨↓, M0ρM0 †⟩, ⟨P ; while M [ q] = 1 do P od, M1ρM1 †⟩|}<br>⟨P, ρ⟩∈A ⟨P, ρ⟩→B<br>(MS)<br>A → (A \ {|⟨P, ρ⟩|}) ∪B<br>

Figure 6. Extended Transition Rules for Quantum while-Programs. In (MU), A, B are configuration ensembles.

![](images/p11-02.png)

(Ax.Inv) {A} P {A}<br>{A}P {B}<br>(R.TI)<br>{tr W A} P {B}<br>{Ai} P {Bi} (i = 1, ..., m)<br>(R.CC)<br>{ �m i=1 piAi} P {�m i=1 piBi}<br>{A}P {B}<br>(R.Inv)<br>{pA + qC}P {pB + qC}<br>{A}P {B}<br>(R.SO)<br>{E ∗ (A)} P {E ∗ (B)}<br>limn→∞ An = A {An} P {Bn} limn→∞ Bn = B<br>(R.Lim)<br>{A}P {B}<br>

Figure 7. Auxiliary Axioms and Rules. In (Ax.Inv), var (P ) ∩ V = ∅ and A = cl V ∪var (P )(B) for some V ⊆ Var and for some quantum predicate B in HV . In (R.TI), V, W ⊆ Var , V ∩ W = ∅, A, B are quantum predicates in HV ∪W and HV , respectively, and var (P ) ⊆ V. In (R.CC), pi ≥ 0 (i = 1, ..., m) and<sup>�m</sup> i=1<sup>pj≤1.In(R.Inv),p, q≥0,p + q≤1,andCisaquantumpredicateinHVforsomeV⊆VarwithV∩var(P ) = ∅.In</sup> (R.SO), E is a quantum operation (or super-operator) in HV for some V ⊆ Var with V ∩ var (P ) = ∅. In (R.Lim), {An} and {Bn} are increasing and decreasing, respectively sequences with respect to the Löwner order.

quantum programs because a huge amount of vector and matrix calculations is involved. Thus, automatic tools will be very helpful.

Similar to the case of classical programs, a verifier can prove the correctness:

## ⊢par {A}P {B} (or ⊢tot {A}P {B})

of a quantum program P in the following three steps:

- Annotating the program: insert quantum predicates at the intermediate points (in a way similar to a proof outline described in Section IV). Intuitively, an inserted statement is intended to hold when the control reaches the corresponding point.

- Generating verification conditions (VCs): a set of mathematical statements, usually of the form Ai ⊑ Bi (see Lemma 2.1), is generated from the annotated program, where Ai, Bi are matrices, and ⊑ stands for the Löwner order. It is required that if all the generated VCs are true, then ⊢par {A}P {B} (or ⊢tot {A}P {B}).

- Proving VCs: prove that matrix Bi − Ai is positive semi-definite for each VC Ai ⊑ Bi.

Recently, a theorem prover was built by Liu, Li, Wang et al. in [LLW16] for the quantum Hoare logic based on the proof assistant Isabelle/HOL. It has been used to verify several quantum programs, including Grover search and phase

estimation, which is a key in Shor’s factoring algorithm. We can expect that more automatic tools for verification of quantum programs and quantum cryptographic protocols will be built after quantum computers be commercialised.

## VII. INVARIANTS OF QUANTUM PROGRAMS

It has been well-understood since the very beginning that invariant generation is crucial for automatic verification of programs, and the problem of invariant generation has been intensively studied for classical programs. At this moment, invariants are provided by humans to the theorem prover for quantum programs developed in [LLW16] rather than generated by the system itself. But the issue of generating quantum invariants was recently considered in [YYW17]. In this section, we briefly review the main results in [YYW17].

We first observed that the control flow of a quantum program can be represented by a super-operator-valued transition system (SVTS):

Definition 7.1 (Super-Operator-Valued Transition Systems [YYW17]): An SVTS is a 5-tuple:

![](images/p11-03.png)

S = ⟨H, L, l0, T , Θ⟩,<br>

where:

- 1) H is a Hilbert space;

- 2) L is a finite set of locations;

- 3) l0 ∈ L is the initial location;

- 4) Θ is a quantum predicate in H denoting the initial condition; and

- 5) T is a set of transitions. Each transition τ ∈T is written as τ = l →E l′ with l, l′ ∈ L and E being a super-operator in H. For each l ∈ L, it is required that

![](images/p12-01.png)

El = �{|E : l →E l′ ∈T |}<br>

is trace-preserving, i.e. tr (El(ρ)) = tr(ρ) for all ρ.

Now we assume that the control flow SVTS of quantum program P is SP with state Hilbert space HP (see [YYW17] for detailed construction of SP ). A set Π of paths in HP is said to be prime if for each

![](images/p12-02.png)

E1 En−1<br>π = l1 → ... → ln ∈ Π,<br>

its proper initial segments

![](images/p12-03.png)

E1 Ek−1<br>l1 → ... → lk ∈/ Π<br>

for all k < n. We write Eπ for the composition of E1, ..., En−1 and EΠ =<sup>�</sup> {|Eπ : π ∈ Π|}. Then we can define invariants for quantum programs:

Definition 7.2 (Invariants of Quantum Programs [YYW17]): Let SP = ⟨HP , L, l0, T , Θ⟩ be the control flow SVTS of quantum program P and l ∈ L. An invariant at location l ∈ L is a quantum predicate O in HP satisfying the condition: for any density operator ρ and prime set Π of paths from l0 to l, we have:

## tr(Θρ) ≤ 1 − tr (EΠ(ρ)) + tr (OEΠ(ρ)) .

It was shown in [YYW17] that invariants can be used to establish partial correctness of quantum programs. We can also introduce the notion of inductive assertion for quantum programs. It is not easy to identify the invariant in the proof rules (R.LP) and (R.LT) for quantum loops, at least not as explicit as in the Hoare rule for classical loops. Example 4.1 in [YYW17] indicates that the quantum predicate M0<sup>†AM0+M †</sup> 1<sup>BM1inrules(R.LP)and(R.LT)canbe</sup> viewed as an inductive assertion (invariant). Furthermore, by generalising the constraint-based technique of Colón et al. [CSS03], [SSM04], it was demonstrated in [YYW17] that invariant generation for quantum programs can be reduced to an SDP (Semidefinite Programming) problem. In particular, the method proposed in [YYW17] was actually applied to generate the invariants of the quantum walk in Example 2.2 and quantum Metropolis sampling [TOVPV11].

## VIII. TERMINATIONS ANALYSIS OF QUANTUM PROGRAMS

As is well-known, termination analysis is a key step in proving total correctness of programs. Termination of quantum programs has been researched along the following two lines:

- Algorithmic analysis of termination for quantum programs was first considered in [YF10] where the Jordan decomposition of complex matrices was employed as the main tool. In [YYFD13], the author and his collaborators introduced quantum Markov chains as a semantic model of quantum programs. Then in a series of their papers [YFYY13], [YY12], [LYY14], termination of quantum programs was reduced to the reachability problem of quantum Markov chains, which is in turn tackled by developing a theory of quantum graphs (see [Yin16], Section 5.2). Indeed, this line of research also paves a way to model-checking quantum systems.

- The notion of ranking function was defined in [Yin11] in order to present the proof rule (R.LT) for total correctness of quantum loops. It was recalled as Definition 2.6 in this paper. In the last few years, (super)martingales have been employed as a powerful mathematical tools for termination analysis of probabilistic programs [CS13], [FH15], [CFNH16]. Recently, a notion of quantum (super)martingales was introduced in [LY18] as a generalisation of Definition 2.6 and used to characterise the termination of quantum programs. The synthesis problem of (super)martingales for quantum programs was also investigated there. The basic idea is that the fundamental Gleason theorem [Gle57] in quantum foundations can be used to determine the template of ranking functions, and then the synthesis problem of quantum (super)martingales with certain templates can also be reduced to an SDP problem. It seems that a further development of this line of research requires us to systematically establish a mathematical theory of quantum (super)martingales first.

The termination of the quantum walk in Example 2.2 was analysed by both of the above approaches [YYFD13], [LY18], and the second approach was also used in [LY18] to analyse the termination of quantum Bernoulli factory, a quantum algorithm for random number generation [DJR15].

## IX. CONCLUSION

We conclude this paper by pointing out several problems for future research:

- Combining Classical Computation and Quantum Computation: We have been focusing on pure quantum programs without classical computation. This allows us to have a clean theory of quantum programming. But almost all existing quantum algorithms involves both quantum and classical computation, and the stateof-art quantum programming languages like Quipper [GLR13], LIQUi|> [WS14], Q# [SGT18], Scaffold [JPK15] and QWire [PRZ17] include both classical and quantum variables. So, it is desirable to generalise the verification techniques discussed in this paper to quantum programs involving classical computation.

Indeed, a kind of correctness formulas (Hoare triples) involving both classical and quantum variables were already introduced in [YF11], but a Hoare-like logic for programs with both classical and quantum variables is still to be developed.

- Parallel and Distributed Quantum Programs: Distributed quantum computing has been studied for 20 years since [Gro97] and [CB97], including finding quantum algorithms for solving paradigmatic problems from classical distributed computing [TKM05], experiments toward physical implementation of distributed quantum computing [SMB06] and architecture of distributed quantum hardware systems [MMN08]. In particular, since practical quantum computers with large qubit capacity are still out of the current technology’s reach, it is an attractive idea to use the physical resources of two or more small-capacity quantum computers to realise a large-capacity quantum computing system. So, another interesting problem is how the program logic and related techniques considered in this paper can be extended for reasoning about parallel and distributed quantum programs. The notion of proof outline for quantum programs introduced in Section IV should be helpful in dealing with the (non)interference of the variables shared by component quantum programs.

- Verification of Quantum Cryptographic Protocols: Over the last 10 years, quantum communication has blossomed into a viable commercial technology. But verifying correctness and security of quantum communication protocols is a notoriously difficult problem. Process algebra approach has been introduced for verification of quantum cryptographic protocols [AGN14], [FY15], [KKK16]. On the other hand, a (probabilistic) relational Hoare logic (pRHL) and a machine-checked framework for reasoning about security and privacy in classical computing and communicating systems were established by Barthe, Fournet, Köpf et al. [BFG14], [BKO13]. The success of this line of research suggests us to develop verification techniques for quantum cryptographic protocols by extending our quantum Hoare logic. Indeed, the first attempt to develop a quantum relational Hoare logic (qRHL) was already made by Unruh in [Unruh18], where a tool for the verification based on qRHL was implemented and successfully used to the security proof of several quantum cryptographic protocols.

Acknowledgment: The author likes to thank Professors Martin Fränzle, Deepak Kapur and Naijun Zhan for inviting me to give a talk at SETTA’2016. This work was partly supported by the Australian Research Council (Grant No: DP160101652) and the Key Research Program of Frontier Sciences, Chinese Academy of Sciences.

## REFERENCES

- [AG05] T. Altenkirch and J. Grattage, A functional quantum programming language, In: Proceedings of the 20th IEEE Symposium on Logic in Computer Science (LICS), 2005, 249-258.

- [ABNVW01] A. Ambainis, E. Bach, A. Nayak, A. Vishwanath and J. Watrous, One-dimensional quantum walks, In: Proceedings of the 33rd ACM Symposium on Theory of Computing (STOC), 2001, pp. 37-49.

- [ABO09] K. R. Apt, F. S. de Boer and E. -R. Olderog, Verification of Sequential and Concurrent Programs, Springer, London 2009.

- [AGN14] E. Ardeshir-Larijani, S. J. Gay and R. Nagarajan, Verification of concurrent quantum protocols by equivalence checking, Proc. of the 20th International Conference on Tools and Algorithms for the Construction and Analysis of Systems (TACAS), 2014, pp. 500-514.

- [BP15] C. Bˇadescu and P. Panangaden, Quantum alternation: prospects and problems, in: Proc. of the 12th International Workshop on Quantum Physics and Logic (QPL), 2015, pp. 33-42.

- [BS06] A. Baltag and S. Smets, LQP: the dynamic logic of quantum information, Mathematical Structures in Computer Science, 16(2006)491-525.

- [BFG14] G. Barthe, C. Fournet, B. Grégoire, P. -Y. Strub, N. Swamy and S. Zanella Béguelin, Probabilistic relational verification for cryptographic implementations, In: Proc. of the 41st Annual ACM Symposium on Principles of Programming Languages (POPL), 2014, pp. 193-206.

- [BKO13] G. Barthe, B. Köpf, F. Olmedo and Z. Zanella Béguelin, Probabilistic relational reasoning for differential privacy, ACM Transactions on Programming Languages and Systems 35(2013) Art. No. 9.

- [BBCJPW92] C. H. Bennett, G. Brassard, C. Crepeau, R. Jozsa, A. Peres and W. K. Wootters, Teleporting an unknown quantum state via dual classical and Einstein-PodolskyRosen channels, Physical Review Letters, 70(1993) 18951899.

- [BJ04] O. Brunet and P. Jorrand, Dynamic quantum logic for quantum programs, International Journal of Quantum Information, 2(2004)45-54.

- [CMS06] R. Chadha, P. Mateus and A. Sernadas, Reasoning about imperative quantum programs, Electronic Notes in Theoretical Computer Science, 158(2006)19-39.

- [CS13] A. Chakarov and S. Sankaranarayanan, Probabilistic program analysis with martingales, In: Proc. of the 25th International Conference on Computer Aided Verification (CAV), 2013, Springer LNCS 8044, 511-526.

- [CFNH16] K. Chatterjee, H. F. Fu, P. Novotný and R. Hasheminezhad, Algorithmic analysis of qualitative and quantitative termination problems for affine probabilistic programs, In: Proc. of the 43rd Annual ACM Symposium on Principles of Programming Languages (POPL), 2016, 327-342.

- [CB97] R. Cleve and H. Buhrman, Substituting quantum entanglement for communication, Physical Review A 56(1997) 1201-1204.

- [CSS03] M. A. Colón, S. Sankaranarayanan and H. B. Sipma, Linear invariant generation using non-linear constraint solving, In: Proc. of the 15th International Conference on Computer Aided Verification (CAV), 2003, Springer LNCS, pp. 420-433.

- [DJR15] H. Dale, D. Jennings and T. Rudolph, Provable quantum advantage in randomness processing, Nature Communications 6(2015), art. no. 8203.

- [DP06] E. D’Hondt and P. Panangaden, Quantum weakest preconditions, Mathematical Structures in Computer Science, 16(2006)429-451.

- [FDJY07] Y. Feng, R. Y. Duan, Z. F. Ji and M. S. Ying, Proof rules for the correctness of quantum programs, Theoretical Computer Science 386 (2007)151-166.

- [FHTZ15] Y. Feng, E. M. Hahn, A. Turrini and L. J. Zhang, QPMC: a model checker for quantum programs and protocols, Proceedings of the 20th International Symposium on Formal Methods (FM), 2015, Springer LNCS 9109, pp. 265-272.

- [FY15] Y. Feng and M. S. Ying, Toward automatic verification of quantum cryptographic protocols, Proc. of the 26th International Conference on Concurrency Theory (CONCUR), 2015, pp. 441-455.

- [FYY13] Y. Feng, N. K. Yu and M. S. Ying, Model checking quantum Markov chains, Journal of Computer and System Sciences, 79(2013)1181-1198.

- [FH15] L. M. F. Fioriti and H. Hermanns, Probabilistic termination: soundness, completeness, and compositionality. In: Proc. of the 42nd Annual ACM Symposium on Principles of Programming Languages (POPL), 2015, 489-501.

- [GPN08] S. J. Gay, N. Papanikolaou and R. Nagarajan, QMC: a model checker for quantum systems. Proceedings of the 20th International Conference on Computer Aided Verification (CAV), 2008, Springer LNCS 5123, pp. 543547.

- [Gle57] A. M. Gleason, Measures on the closed subspaces of a Hilbert space, Journal of Mathematics and Mechanics 6(1957)885-893.

- [Gor75] G. A. Gorelick, A complete axiomatic system for proving assertions about recursive and non-recursive programs, Technical Report, Department of Computer Science, University of Toronto, 1975.

- [GLR13] A. Green, P. L. Lumsdaine, N. J. Ross, P. Selinger and B. Valiron, Quipper: A scalable quantum programming language, In: Proceedings of the 34th ACM Conference on Programming Language Design and Implementation (PLDI), 2013, pp. 333?342.

- [Gro97] L.K. Grover, Quantum telecomputation, arXiv:quantph/9704012, 1997.

- [Har79] D. Harel, First-Order Dynamic Logic, LNCS 68, Springer, 1979.

- [KV02] J. Den Hartog and E. P. de Vink, Verifying probabilistic programs using a Hoare like logic, International Journal of Foundations of Computer Science 13(2002)315-340.

- [Kle99] T. Leymann, Hoare logic and auxiliary variables, Formal Aspect of Computing 11(1999)541-566.

- [KMMM10] J. -P. Katoen, A. McIver, L. Meinicke and C. C. Morgan, Linear-invariant generation for probabilistic programs - Automated support for proof-based methods, in: Proc. 17th International Symposium on Static Analysis (SAS), 2010, Springer LNCS 6337, pp. 390-406.

- [KKK16] T. Kubota, Y. Kakutani, G. Kato, Y. Kawano and H. Sakurada, Semi-automated verification of security proofs of quantum cryptographic protocols, Journal of Symbolic Computation 73(2016) 192-220.

- [JPK15] A. JavadiAbhari, S. Patil, D. Kudrow, J. Heckey, A. Lvov, F. T. Chong and M. Martonosi, ScaffCC: Scalable compilation and analysis of quantum programs, Parallel Computing 45(2015) 2-17.

- [Ka09] Y. Kakutani, A logic for formal verification of quantum programs, in: Proceedings of the 13th Asian Computing Science Conference (ASIAN 2009), Springer LNCS 5913, pp. 79-93.

- [Kr83] K. Kraus, States, Effects, and Operations: Fundamental Notions of Quantum Theory, Springer, 1983.

- [LY18] Y. J. Li and M. S. Ying, Algorithmic analysis of termination problems for quantum programs, In: Proc. of the 45th Annual ACM Symposium on Principles of Programming Languages (POPL), 2018, pp. 35.1-29.

- [LYY14] Y. J. Li, N. K. Yu and M. S. Ying, Termination of nondeterministic quantum programs, Acta Informatica 51(2014) 1-24.

- [LLW16] T. Liu, Y. J. Li, S. L. Wang et al., A theorem prover for quantum Hoare logic and its applications, arXiv:1601.03835.

- [MS06] P. Mateus and A. Sernadas, Weakly complete axiomatization of exogenous quantum propositional logic, Information and ComputationVolume 204(2006)771-794.

- [MMN08] R. van Meter, W.J. Munro, K. Nemoto and K.M. Itoh, Arithmetic on a distributed-memory quantum multicomputer, ACM Journal on Emerging Technologies in Computing Systems 3(2008) Art. No. 17.

- [MM05] A. McIver and C. Morgan, Abstraction, Refinement and Proof for Probabilistic Systems, Springer, 2005.

- [NC00] M. A. Nielsen and I. L. Chuang, Quantum Computation and Quantum Information, Cambridge University Press, 2000.

- [PRZ17] J. Paykin, R. Rand and S. Zdancewic, QWIRE: a core language for quantum circuits, In: Proc. of the 44th Annual ACM Symposium on Principles of Programming Languages (POPL), 2017, pp. 846-858.

- [Rand17] R. Rand, Verification Logics for Quantum Programs, http://www.cis.upenn.edu/∼rrand/wpe.pdf

- [SVV18] A. Sabry, B. Valiron, J. K. Vizzotto, From symmetric pattern-matching to quantum control, in: Proc. of the 21st International Conference on Foundations of Software Science and Computation Structures (FoSSaCS), 2018, pp. 348-364.

- [SSM04] S. Sankaranarayanan, H. B. Sipma and Z. Manna, Nonlinear loop invariant generation using Gröbner bases, In: Proc. of the 31st ACM Symposium on Principles of Programming Languages (POPL), 2004, pp. 318-329.

- [Sel04] P. Selinger, Towards a quantum programming language, Mathematical Structures in Computer Science 14, (2004) 527-586.

- [SMB06] A. Serafini, S. Mancinians and S. Bose, Distributed quantum computation via optical fibers, Physical Review Letters 96(2006) Art. No. 010503.

- [SGT18] K. Svore, A. Geller, M. Troyer, J. Azariah, C. Granade, B. Heim, V. Kliuchnikov, M. Mykhailova, A. Paz and M. Roetteler, Q#: Enabling scalable quantum computing and development with a high-level DSL, In: Proceedings of the Real World Domain Specific Languages Workshop 2018, art. no. 8.

- [TKM05] S. Tani, H. Kobayashi and K. Matsumoto, Exact quantum algorithms for the leader election problem, ACM Transactions on Computation Theory 4(2012) Art. No. 1.

- [TOVPV11] K. Temme, T. J. Osborne, K. G. Vollbrecht, D. Poulin, and F. Verstraete. Quantum Metropolis sampling. Nature, 471(2011) 87-90.

- [Unruh18] D. Unruh, Quantum relational Hoare logic, https://arxiv.org/pdf/1802.03188.pdf.

- [vT04] A. van Tonder, A lambda calculus for quantum computation, SIAM Journal on Computing, 33(2004)1109-1135.

- [WS14] D. Wecker and K. M. Svore, LIQUi|>: A software design architecture and domain-specific language for quantum computing, arXiv:1402.4467, 2014.

- [WZ82] W. K. Wootters and W. H. Zurek, A single quantum cannot be cloned, Nature, 299(1982) 802-803.

- [Yin11] M. S. Ying, Floyd-Hoare logic for quantum programs, ACM Transactions on Programming Languages and Systems 39 (2011), art. no. 19.

- [Yin16] M. S. Ying, Foundations of Quantum Programs, MorganKaufmann, 2016.

- [Yin16a] M. S. Ying, Toward automatic verification of quantum programs (extended abstract), In: Proc. of the 2nd International Symposium on Dependable Software Engineering: Theories, Tools, and Applications (SETTA), 2016.

- [YCFD07] M. S. Ying, J. X. Chen, Y. Feng and R. Y. Duan, Commutativity of quantum weakest preconditions, Information Processing Letters 104 (2007) 152-158.

- [YF10] M. S. Ying and Y. Feng, Quantum loop programs, Acta Informatica 47 (2010), 221-250.

- [YF11] M. S. Ying and Y. Feng, A flow-chart language for quantum programming, IEEE Transactions on Software Engineering 37 (2011) 466-485.

- [YLYF14] M. S. Ying, Y. J. Li, N. K. Yu and Y. Feng, Modelchecking linear-time properties of quantum systems, ACM Transactions on Computational Logic, 15(2014), art. no. 22.

- [YYW17] M. S. Ying, S. G. Ying and X. D. Wu, Invariants of quantum programs: characterisations and generation, In: Proc. of the 44th Annual ACM Symposium on Principles of Programming Languages (POPL), 2017, pp. 818-832.

- [YYFD13] M. S. Ying, N. K. Yu, Y. Feng and R. Y. Duan, Verification of quantum programs, Science of Computer Programming, 78(2013)1679-1700.

- [YFYY13] S. G. Ying, Y. Feng, N. K. Yu and M. S. Ying, Reachability analysis of quantum Markov chains, In: Proc. of the 24th International Conference on Concurrency Theory (CONCUR), 2013, pp. 334-348.

- [YY12] N. K. Yu and M. S. Ying, Reachability and termination analysis of concurrent quantum programs, In: Proc. of the 23th International Conference on Concurrency Theory (CONCUR), 2012, pp. 69-83.

- [Zu05] P. Zuliani, Compiling quantum programs, Acta Informatica, 41(2005)435-474.

## APPENDIX

For convenience of the reader, we first review some basic properties of operators and super-operators needed in the proofs presented in Appendix A. The following lemma gives a characterisation of the Löwner order in terms of trace.

Lemma A.1: Let A, B be observables (i.e. Hermitian operators) in Hilbert space H. Then A ⊑ B if and only if tr (Aρ) ≤ tr (Bρ) for all density operators in H.

The notion of dual super-operator is introduced in the next definition. It will be extensively used in Appendix A.

Definition A.1: Let E be a quantum operation (i.e. superoperator) in Hilbert space H with the Kraus representation E =<sup>�</sup> i<sup>Ei ◦E</sup> i<sup>†.Thenits(Schrödinger-Heisenberg) dualis</sup> the super-operator E<sup>∗</sup> defined by

![](images/p15-01.png)

E ∗ (A) = � Ei †AEi<br>i<br>

for any observable A in H.

The next lemma presents a characterisation of duality between super-operators in terms of trace.

Lemma A.2: For any quantum operation E, observable A and density operator ρ in H, we have:

## tr (AE(ρ)) = tr (E<sup>∗</sup> (A)ρ).

In particular, tr(E(ρ)) = tr (E<sup>∗</sup> (I)ρ), where I is the identity operator in H.

Positivity of operators and the Löwner order between operators in a tensor product of Hilbert spaces are considered in the following:

- Lemma A.3: 1) If A1, A2 are positive operators in H1 and H2, respectively, then A1 ⊗ A2 is a positive operator in H1 ⊗H2.

- 2) For any operators A1, B1 in H1 and A2, B2 in H2, A1 ⊑ B1 and A2 ⊑ B2 implies A1 ⊗ A2 ⊑ B1 ⊗ B2.

- The proofs of all of the above lemmas can be found in

- any standard textbook on the theory of operators in Hilbert spaces.

In Section III, we already saw some simple quantum relations (i.e. quantum predicates in the tensor product of more than one state Hilbert spaces) in specifying correctness of quantum programs. The notion of composition of classical relations is well-defined and widely used to construct complicated relations from simple ones. However, it is highly nontrivial to find an appropriate definition of the notion of composition of quantum relations. Here, we give several tentative definitions:

Definition A.2: Let A be a quantum relation between H1 and H2 (i.e. an observable in H1 ⊗H2 between the zero and identity operators) and B a quantum relation between H2 and H3. We define three kinds of their compositions:

- 1) Circle composition:

![](images/p16-01.png)

A ◦B B = 1 �⟨ii|A ⊗ B|ii⟩<br>d2<br>i<br>

where and in the sequel d2 = dim H2 and B = {|i⟩} is an orthonormal basis of H2.

- 2) Bullet composition:

![](images/p16-02.png)

A •B B = ⟨Ψ|A ⊗ B|Ψ⟩<br>

where |Ψ⟩B = √1d2 �i<sup>|ii⟩is the (unnormalised) max-</sup> imal entanglement defined by an orthonormal basis B = {|i⟩} of H2.

- 3) Diamond composition:

![](images/p16-03.png)

A ⋄v B = tr H⊗2 2 [Sv(A ⊗ B)Sv]<br>

where v ∈{+, −}, S± are the symmetrisation and anti-symmetrisation operators (see Example 3.2), and tr H⊗2 2 stands for tracing out the middle two H2’s in H1 ⊗H2 ⊗H2 ⊗H3.

The algebraic structure of quantum relations equipped with the above composition operations and corresponding transitive closures is a very interesting topic for future research.

In this section, we provide the proofs of theorems omitted in the main part of this paper.

- A. Proof of Theorem 4.1

To prove the strong soundness, suppose that

We proceed by induction on the length n of computation.

Induction Basis: For n = 0, {|⟨Pi, ρi⟩|} is a singleton {|⟨P1, ρ1⟩|} with P1 ≡ P and ρ1 ≡ ρ. Then we can choose T1 ≡ P and it holds that P1 ≡ at (T1, P ). Note that in the proof outline {A}P<sup>∗</sup> {B}, we have A ⊑ pre(P ) = B1. Thus,

![](images/p16-04.png)

tr(Aρ) ≤ tr(B1ρ1) = � tr(Biρi).<br>i<br>

Induction Step: Now we assume that

⟨P, ρ⟩→<sup>n−1</sup> {|⟨Pi, ρi⟩|} →{|⟨Pi, ρi⟩|i̸ = i0|}∪{|⟨Qj, σj⟩|} where

![](images/p16-05.png)

⟨Pi0 , ρi0 ⟩→{|⟨Qj, σj⟩|}<br>

is derived by one of the rules used in defining transition relation (12). Then we need to consider the following cases:

◮ Case 1. The last step uses rule (IF<sup>′</sup> ). Then Pi0 can be written in the following form:

![](images/p16-06.png)

Pi0 ≡ if (□m · M [q] = m → Rm) fi,<br>

= and for each j, Qj ≡ Rm ≡ at (Rm, P ) and σj Mmρi0 Mm<sup>†for some m. On the other hand, a segment of the</sup> proof outline {A}P<sup>∗</sup> {B} must be derived by the following inference:

![](images/p16-07.png)

{Am}Rm ∗ {C} for every m<br>��m M † m A m M m� if (□m · M [q] = m →{Am} Rm ∗ ) fi{C}<br>

and

![](images/p16-08.png)

Bi0 = pre (Pi0 ) ⊑ � Mm † AmMm, Am = pre (Rm) .<br>m<br>

Therefore,

![](images/p16-09.png)

tr (Bi0 ρi0 ) ≤ tr Mm † AmMmρi 0<br>��m �<br>= � tr �Mm † AmMmρi 0 �<br>m<br>= � tr �AmMmρi0 Mm † �<br>m<br>=<br>� tr (pre (Qj) σj) .<br>j<br>

By the induction hypothesis, we obtain:

![](images/p16-10.png)

tr (Aρ) ≤ � tr (Biρi) + tr (Bi0 ρi0 )<br>i≠ i0<br>≤ � tr (Biρi) + � tr (pre (Qj) σj) .<br>i≠ i0 j<br>

So, the conclusion is true in this case.

◮ Case 2. The last step uses rule (L<sup>′</sup> ). Then Pi0 must be in the following form:

![](images/p16-11.png)

⟨P, ρ⟩→ n {|⟨Pi, ρi⟩|}. Pi0 ≡ while M [q] = 1 do R od<br>

## and

{|⟨Qj, σj⟩|} = {|⟨Q0, σ0⟩, ⟨Q1, σ1⟩|}

with Q0 ≡ skip, σ0 = M0ρi0 M0<sup>†, Q1≡R; Pi</sup> 0<sup>andσ1=</sup> M1ρi0 M1<sup>†.Asegmentof{A}P ∗{B}mustbederivedby</sup> the inference in Figure 8 and Bi0 ⊑ M0CM0<sup>†+ M1DM †</sup> 1<sup>.</sup> Then Q0 ≡ at (skip, P ), pre(Q0) = C, Q1 ≡ at(R, P ) and pre(Q1) = D. It follows that

![](images/p17-01.png)

tr (Bi0 ρi0 ) ≤ tr ��M0CM0 † + M1DM † 1 � ρi0 �<br>= tr M0CM0 †ρi 0 + tr M1DM1 †ρi 0<br>� � � �<br>= tr CM0 †ρi 0 M0 + tr DM1 †ρi 0 M1<br>� � � �<br>= tr (pre(Q0)σ0) + tr (pre(Q1)σ1) .<br>Furthermore, by the induction hypothesis, we have:<br>tr (Aρ) ≤ � tr (Biρi) + tr (Bi0 ρi0 )<br>i≠ i0<br>≤ � tr (Biρi) + � tr (pre (Qj) σj) .<br>i≠ i0 j<br>

Furthermore, by the induction hypothesis, we have:

Thus, the conclusion is true in this case.

◮ Case 3. The last step uses rule (Sk), (In) or (UT). Similar but easier.

B. Proof of Theorem 5.1

We only prove the theorem for partial correctness; the case of total correctness is simpler.

1. We first prove that rule (Ax.Inv) is sound for partial correctness. Since var (P ) ∩ V = ∅, �P � can be seen as a super-operator E in HV c . Then when considering �P � as a super-operator in H, we have:

![](images/p17-02.png)

�P � ∗ (A) + [I − �P � ∗ (I)]<br>= B ⊗E ∗ (IV c) + [I − IV ⊗E ∗ (IV c )]<br>= B ⊗E ∗ (IV c ) + IV ⊗ [IV c −E ∗ (IV c )]<br>⊒ B ⊗E ∗ (IV c) + B ⊗ [IV c −E ∗ (IV c)]<br>= B ⊗ IV c = A<br>

because B ⊑ IV c and E<sup>∗</sup> (IV c) ⊑ IV c, where I stands for the identity operator in H.

2. Now we prove the soundness of rule (R.TI) for partial correctness. Assume that |=par {A}P {B}. Then it holds that

![](images/p17-03.png)

A ⊑ �P � ∗ (B ⊗ IW ) + (I − �P � ∗ (I))<br>

where I is the identity operator in HV ∪W . Note that var (P ) ⊆ V . Then we have:

![](images/p17-04.png)

tr W (�P � ∗ (B ⊗ IW )) = �P � ∗ (B)<br>

where the occurrences of �P � in the left-hand side and righthand side are seen as a super-operator in HV ∪W and one

in HV , respectively. Similarly, we have tr W (�P �<sup>∗</sup> (I)) = �P �<sup>∗</sup> (IV ). Therefore, it follows that

![](images/p17-05.png)

tr W A ⊑ tr W �P � ∗ (B ⊗ IW ) + tr W (I − �P � ∗ (I))<br>= �P � ∗ (B) + (IV − �P � ∗ (IV ))<br>

and |=par {tr W A} P {B}.

3. We prove the soundness of (R.CC) for partial correctness. If for every i = 1, ..., m, |=par {Ai}P {Bi}, then by Lemma 2.1 we have:

![](images/p17-06.png)

Ai ⊑ �P � ∗ (Bi) + [I − �P � ∗ (I)] .<br>

Consequently, it holds that

![](images/p17-07.png)

m m<br>� piAi ⊑ � pj (�P � ∗ (Aj) + [I − �P � ∗ (I)])<br>i=1 i=1<br>= �P � ∗ � piBi + [I − �P � ∗ (I)]<br>� i=1m �<br>

because �P �<sup>∗</sup> (·) is linear, and I − �P �<sup>∗</sup> (I) is positive. Thus, we have:

![](images/p17-08.png)

|=par � piAi P � piBi .<br>� i=1m � � i=1m �<br>

4. We prove the soundness of (R.Inv) for partial correctness. From |=par {A}P {B}, i.e. A ⊑ �P �<sup>∗</sup> (B) + (I − �P �<sup>∗</sup> (I)), we derive that

![](images/p17-09.png)

pA + qC ⊑ p�P � ∗ (B) + p (I − �P � ∗ (I))<br>= (p�P � ∗ (B) + qC) + p (I − �P � ∗ (I))<br>⊑ (p�P � ∗ (B) + qC) + (I − �P � ∗ (I))<br>= �P � ∗ (pB + qC) + (I − �P � ∗ (I))<br>

because p ≤ 1 and V ∩ var (P ) = ∅ implies �P �<sup>∗</sup> (C) = C. Therefore, we have |=par {pA + qC}P {pB + qC}.

5. We prove that rule (R.SO) is sound for partial correctness. Suppose that |=par {A}P {B}, i.e. A ⊑ �P �<sup>∗</sup> (B) + (I − �P �<sup>∗</sup> (I)). Note that E is a super-operator in HV and V ∩ var (P ) = ∅. Then E<sup>∗</sup> and �P �<sup>∗</sup> commutes, i.e. E<sup>∗</sup> ◦ �P �<sup>∗</sup> = �P �<sup>∗</sup> ◦E<sup>∗</sup> . Moreover, it holds that E<sup>∗</sup> (I) ⊑ I and thus

![](images/p17-10.png)

(I − �P � ∗ ) (E ∗ (I)) ⊑ (I − �P � ∗ ) (I)<br>

where I is the identity super-operator. Therefore, we obtain:

![](images/p17-11.png)

E ∗ (A) ⊑E ∗ [�P � ∗ (B) + (I − �P � ∗ (I))]<br>= E ∗ (�P � ∗ (B)) + [E ∗ (I) −E ∗ (�P � ∗ (I))]<br>= �P � ∗ (E ∗ (B)) + (I − �P � ∗ ) (E ∗ (I))<br>⊑ �P � ∗ (E ∗ (B)) + (I − �P � ∗ ) (I)<br>= �P � ∗ (E ∗ (B)) + (I − �P � ∗ (I))<br>

and |=par {E<sup>∗</sup> (A)}P {E<sup>∗</sup> (B)}.

![](images/p18-01.png)

{D}R ∗ {M0CM0 † + M1DM † 1 }<br>{M0CM0 † + M1DM † 1 } while M [ q] = 0 do {C} skip {C}<br>= 1 do R ∗ {M0CM0 † + M1DM † 1 } od {C}<br>

Figure 8. Proof of Theorem 4.1

6. Finally, we prove the soundness of (R.Lim) for partial correctness. The existence of limn→∞ An and limn→∞ Bn is guaranteed by Lemma 4.1.3 in [Yin16]. Assume that |=par {An}P {Bn}. Then

![](images/p18-02.png)

An ⊑ �P � ∗ (Bn) + [I − �P � ∗ (I)]<br>

and the continuity of super-operator �P �<sup>∗</sup> yields:

![](images/p18-03.png)

A = nlim→∞ An ⊑ n lim →∞ (�P �∗(Bn) + [I − �P �∗(I)])<br>= �P � ∗ (nlim→∞ Bn) + [I − �P �∗(I)]<br>= �P � ∗ (B) + [I − �P � ∗ (I)] .<br>

Thus, |=par {A}P {B}.
