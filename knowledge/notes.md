# Knowledge Notes: Quantum Reservoir Computing

## Scope and framing
This synthesis targets quantum reservoir computing (QRC) with PCA/angle encoding, entanglement ablations, and matched classical baselines.

## Cross-paper synthesis
- Entanglement is beneficial in several QRC/QELM settings but gains depend on measurement design and noise budget.
- Kernel interpretations clarify when performance comes from feature-map expressivity versus readout optimization.
- Measurement-operator choice is repeatedly cited as a dominant bottleneck and optimization lever.
- MNIST can saturate under PCA; stronger datasets and harder protocols are needed for credible advantage claims.
- Baseline parity requires matched preprocessing, readout capacity, and train/test protocol controls.

## Equation/claim anchors by source
- arxiv:2603.21371: eq=[] | claim=[] | assumptions=0 | limits=0
- arxiv:2603.20167: eq=ing M labels or values {ym }M  m=0 (e.g., an entanglement | claim=[] | assumptions=0 | limits=0
- arxiv:2603.17182: eq=non-Markovian quantum dynamics. Section III QELM                                 P̂m (χ) = cos(χ)I + i sin(χ)Ŝm           (3) | claim=[] | assumptions=0 | limits=0
- arxiv:2602.21544: eq=superconducting processor ibm kawasaki as well as its             state matrix Xt,k = xt,k with X ∈ RT,K and xt = | claim=[] | assumptions=0 | limits=0
- arxiv:2602.19700: eq=noise (p = 0.005), the MSE degrades to 10−3 –10−1 . Asymmetric resource allocation—10 shots for | claim=[] | assumptions=0 | limits=0
- arxiv:2602.19644: eq=D(ϕ) = diag eiϕ0 , eiϕ1 , . . . , eiϕm−1 ,            (1) | claim=[] | assumptions=0 | limits=0
- arxiv:2602.18377: eq=d2 ) on the d-dimensional Hilbert space H, where d = 2n in terms of the number of qubits n. Given | claim=[] | assumptions=0 | limits=0
- arxiv:2602.17440: eq=through an M -mode linear optical network described by a unitary V ∈ U (M ). Let |S⟩ = |s1 s2 . . . sM ⟩ be | claim=[] | assumptions=0 | limits=0
- arxiv:2602.14677: eq=D         Hilbert space dimension (D = 2N ) | claim=[] | assumptions=0 | limits=0
- arxiv:2602.13531: eq=via efficient measurement of the quantum reservoir featur-                   X = (𝑋𝑡 : 𝑡 ∈ Z− ): 𝑌0 = 𝐻 ★ (X), where the process IO is distributed | claim=[] | assumptions=0 | limits=0
- arxiv:2602.13094: eq=∆n (u) = ∆0 + ru, | claim=[] | assumptions=0 | limits=0
- arxiv:2602.00610: eq=multiple local observables. Our results demonstrate a                           atom array system is (ℏ = 1) [23, 27, 28] | claim=[] | assumptions=0 | limits=0
- arxiv:2601.23084: eq=line, with the equation w · x + b = 0. Here, w is termed          calculated using hypotheses returned as f →  − w · x + b. | claim=[] | assumptions=0 | limits=0
- arxiv:2601.22194: eq=i=1 , where yi ∈ {+1, −1}, the Support Vector Machine (SVM) solves the following | claim=[] | assumptions=0 | limits=0
- arxiv:2601.04812: eq=f (x1 ), . . . , f (xn ) follow a multivariate normal distribu-          Then, given the parameters {αi , ωi }ni=1 | claim=[] | assumptions=0 | limits=0
- arxiv:2512.18612: eq=Let the dataset be denoted by D = {(Xi , Yi )}N | claim=[] | assumptions=0 | limits=0
- arxiv:2512.11367: eq=Overall, while quantum approaches have begun to ap-         To formalise this, consider a training dataset D = | claim=[] | assumptions=0 | limits=0
- arxiv:2511.01387: eq=iness of the training process, reservoir computers and ex-                                 xk = f (uk ) .                (1) | claim=[] | assumptions=0 | limits=0
- arxiv:2510.01797: eq=rt = R(ut , rt−1 ; W ) ∈ RN .                             (1) | claim=[] | assumptions=0 | limits=0
- arxiv:2509.06873: eq=|ψ⟩ = cos( ) |0⟩ + eiϕ sin( ) |1⟩             (1) | claim=[] | assumptions=0 | limits=0
- arxiv:2503.22380: eq=U (sk , mk−1 )        =         R(ain sk )    R(af b m0k−1 )     R(af b m1k−1 )   UHaar | claim=[] | assumptions=0 | limits=0
- arxiv:2503.17939: eq=nonlinear function yk = f ({sl }kl=1 ). The protocol con- | claim=[] | assumptions=0 | limits=0
- arxiv:2502.06281: eq=applies PauliFeatureMap (paulis = [’ZI’,’IZ’,’ZZ’]) with a default data mapping φS . In addition, we used five encod- | claim=[] | assumptions=0 | limits=0
- arxiv:2412.06758: eq=H(t) =           (|gj ⟩ ⟨rj | + |rj ⟩ ⟨gj |) | claim=[] | assumptions=0 | limits=0
- arxiv:2409.00998: eq=|ψ⟩ = cos( ) |0⟩ + eiϕ sin( ) |1⟩              (1) | claim=[] | assumptions=0 | limits=0
- arxiv:2407.02553: eq=H(t) =           (|gj ⟩ ⟨rj | + |rj ⟩ ⟨gj |) | claim=[] | assumptions=0 | limits=0
- arxiv:2403.08998: eq=The quantum reservoir we employ is a network of N = | claim=[] | assumptions=0 | limits=0
- arxiv:2310.06706: eq=superconducting quantum computers, it can be adapted                       ρt t =          Tra Mmt Û (ut )(ρt−1t−1 ⊗σa )Û † (ut )Mm | claim=[] | assumptions=0 | limits=0
- arxiv:2309.03307: eq=max L(α) =                    αi −             αi αj yi yj xi · xj | claim=[] | assumptions=0 | limits=0
- arxiv:2212.08693: eq=Table 1: Quantum Kernel Angle Encoding Results with Image Data (N=60, Train=42, Test=18) | claim=[] | assumptions=0 | limits=0
- arxiv:2209.05142: eq=comparison to the classical support vector machine. Surpris-                    Accuracy =                                       (1) | claim=[] | assumptions=0 | limits=0
- arxiv:2205.06809: eq=ther on repeating (part of) the reservoir dynamics or on          tum system state in discrete time steps, with k = t/∆t | claim=[] | assumptions=0 | limits=0
- arxiv:2201.07969: eq=R p , p = 1, . . . M with similar structures, each consisting of n p qubits. A quantum state of a particular QR at the timestep i is | claim=[] | assumptions=0 | limits=0
- arxiv:2102.11831: eq=xk = f (sk , xk−1 ),                (1) | claim=[] | assumptions=0 | limits=0

## Reusable limitations
- Many findings are simulator-heavy and may not transfer unchanged to noisy hardware.
- Shot complexity and decoherence can offset representational gains from entangling maps.
- Dataset separability and PCA rank choices can dominate differences between reservoir types.

## Protocol implications for downstream phases
- Keep PCA fit within train folds to avoid leakage.
- Use matched linear readout (same regularization family and hyperparameter budget).
- Run entangling vs non-entangling reservoirs with identical Hamiltonian and observable budgets.
- Report both accuracy and error-rate families, plus sensitivity to observables and shot count.

- **Recovery note (arXiv:2603.21371):** Added IPC decomposition and benchmark equations (Lorenz-63, Mackey-Glass) plus protocol-control parameters (r, ϑ, h, γ) to ground memory/nonlinearity design claims for downstream parity analysis.
