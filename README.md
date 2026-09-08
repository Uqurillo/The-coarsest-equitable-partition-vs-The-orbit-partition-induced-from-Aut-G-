# The-coarsest-equitable-partition-vs-The-orbit-partition-induced-from-Aut-G-
This repository aims to find the coarsest equitable partition of the graph $G$ and the orbit partition induced from $Aut(G)$ for different real-world datasets and compare them.

Let $G=(V,E)$ be a graph. A partition $\pi=\{C_1\ldots,C_t\}$ of $V$ is equitable if the number of neighbours in $C_j$ of a vertex $u$ in $C_i$ is a constant $b_{ij}$, independent of $u$. Moreover, the $1$-Weisfeiler-Leman (WL) algorithm does not induce an arbitrary equitable partition; in fact, it produces the coarsest one, which is shown by $\pi_{cep(G)}$. We already know that the orbit partition induced from $Aut(G)$, denoted by $\pi_{Aut(G)}$ is equitable:

Let $u,v \in D \in \pi_{Aut(G)}$, implying that there exists $P \in Aut(G)$ such that $P(u)=v$. For an arbitrary cell $C \in \pi_{Aut(G)}$, we consider $con(v,C)=|\mathcal{N}(v) \cap C|=|\mathcal{N}(P(u)) \cap C|=|P(\mathcal{N}(u)) \cap P(C)|=|P(\mathcal{N}(u) \cap C)|=|\mathcal{N}(u) \cap C|=con(u,C),$ where $\mathcal{N}(P(u))=\mathcal{N}(v)=P(\mathcal{N}(u))$ for $P \in Aut(G)$. Moreover, $P(C)=C$ is satisfied by the definition of orbits. This yields that $\pi_{Aut(G)}$ is equitable.

Therefore, the orbit partition $\pi_{Aut(G)}$ obtained from $Aut(G)$ is finer than the coarsest equitable partition $\pi_{cep(G)}$. On the other hand, it is meaningful to investigate how different they are for real-world datasets. For this aim, we take the datasets from [1], where Sánchez-García works with many different graphs, varying widely in size, to exploit their symmetries. Since the orbit cells are already present in the dataset, we compute the coarsest equitable partitions by following the iteration methodology of the $1$-WL test. The next step is to compare $\pi_{Aut(G)}$ and $\pi_{cep(G)}$ for the fixed graph $G$. We can do this by checking whether any cell of the coarsest equitable partition contains multiple orbit cells or not. However, it is enough to look at whether the number of cells in both partitions is equal to each other. In fact, Table shows that we have $100\%$ equality between the cells of them. The code and the documents storing the partitions are available \textcolor{red}{here}.

\begin{table}[H]
\centering
\small
\begin{tabular}{lrrrr}
\hline
Dataset & $|V|$ & Orbit Cells & Coarsest Equitable Cells & Agreement \\
\hline
HumanDisease       & 1419 & 686 & 686 & 100\% \\
Yeast              & 1647 & 1256 & 1256 & 100\% \\
OpenFlights        & 3397 & 2626 & 2626 & 100\% \\
USPowerGrid        & 4941 & 4466 & 4466 & 100\% \\
HumanPPI           & 9270 & 8294 & 8294 & 100\% \\
Astro-Ph           & 17,903 & 14,660 & 14,660 & 100\% \\
InternetAS         & 34,761 & 19,128 & 19,128 & 100\% \\
WordNet            & 145,145 & 87,244 & 87,244 & 100\% \\
Amazon             & 334,863 & 302,387 & 302,387 & 100\% \\
Actors             & 374,511 & 191,680 & 191,680 & 100\% \\
InternetAS-skitter & 1,694,616 & 1,360,452 & 1,360,452 & 100\% \\
CaliforniaRoads    & 1,957,027 & 1,917,379 & 1,917,379 & 100\% \\
LiveJournal        & 5,189,808 & 4,777,459 & 4,777,459 & 100\% \\
\hline
\end{tabular}
\caption{Comparison between $\pi_{Aut(G)}$ and $\pi_{cep(G)}$, where $G$ is the graph notation of the corresponding dataset. The third and fourth columns show the number of cells in the orbit partition and the coarsest equitable partition, respectively. Moreover, the last column indicates the percentage of cells that belong to both partitions.}
\label{tab:orbit-equitable-comparison}
\end{table}

We note that the orbit cells for the HumanPPI and WordNet datasets start from $1$, although all the others are indexed from $0$. Hence, for these two datasets, we write the cells of the coarsest equitable partition using $1$-based labels. We then observe that if we apply the relabelling: $i \to i-1$ for $i > 1$ and $1 \to |V(G)|$ to the coarsest equitable partition, we obtain an equality with the orbit partition.  

[1]:Sánchez-García, Rubén J. "Exploiting symmetry in network analysis." Communications Physics 3.1 (2020): 87.

The dataset is available at https://figshare.com/articles/dataset/Network_symmetry_datasets/11619792/1
