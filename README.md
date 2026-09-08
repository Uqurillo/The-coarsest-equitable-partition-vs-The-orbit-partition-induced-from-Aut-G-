# The-coarsest-equitable-partition-vs-The-orbit-partition-induced-from-Aut-G-
This repository aims to find the coarsest equitable partition of the graph $G$ and the orbit partition induced from $Aut(G)$ for different real-world datasets and compare them.

Let $G=(V,E)$ be a graph. A partition $\pi=\{C_1\ldots,C_t\}$ of $V$ is equitable if the number of neighbours in $C_j$ of a vertex $u$ in $C_i$ is a constant $b_{ij}$, independent of $u$. Moreover, the $1$-Weisfeiler-Leman (WL) algorithm does not induce an arbitrary equitable partition; in fact, it produces the coarsest one, which is shown by $\pi_{cep(G)}$. We already know that the orbit partition induced from $Aut(G)$, denoted by $\pi_{Aut(G)}$ is equitable:

Let $u,v \in D \in \pi_{Aut(G)}$, implying that there exists $P \in Aut(G)$ such that $P(u)=v$. For an arbitrary cell $C \in \pi_{Aut(G)}$, we consider
$
con(v,C)=|\mathcal{N}(v) \cap C|=|\mathcal{N}(P(u)) \cap C|=|P(\mathcal{N}(u)) \cap P(C)|=|P(\mathcal{N}(u) \cap C)|=|\mathcal{N}(u) \cap C|=con(u,C),
$
where $\mathcal{N}(P(u))=\mathcal{N}(v)=P(\mathcal{N}(u))$ for $P \in Aut(G)$. Moreover, $P(C)=C$ is satisfied by the definition of orbits. This yields that $\pi_{Aut(G)}$ is equitable.
