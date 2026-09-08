# The-coarsest-equitable-partition-vs-The-orbit-partition-induced-from-Aut-G-
This repository aims to find the coarsest equitable partition of the graph $G$ and the orbit partition induced from $Aut(G)$ for different real-world datasets and compare them.

Let $G=(V,E)$ be a graph. A partition $\pi=${C_1,...,C_t} of $V$ is equitable if the number of neighbours in $C_j$ of a vertex $u$ in $C_i$ is a constant $b_{ij}$, independent of $u$. Moreover, the $1$-Weisfeiler-Leman (WL) algorithm does not induce an arbitrary equitable partition; in fact, it produces the coarsest one, which is shown by $\pi_{cep(G)}$. We already know that the orbit partition induced from $Aut(G)$, denoted by $\pi_{Aut(G)}$ is equitable.

Therefore, the orbit partition $\pi_{Aut(G)}$ obtained from $Aut(G)$ is finer than the coarsest equitable partition $\pi_{cep(G)}$. On the other hand, it is meaningful to investigate how different they are for real-world datasets. For this aim, we take the datasets from [1], where Sánchez-García works with many different graphs, varying widely in size, to exploit their symmetries. Since the orbit cells are already present in the dataset, we compute the coarsest equitable partitions by following the iteration methodology of the $1$-WL test. The next step is to compare $\pi_{Aut(G)}$ and $\pi_{cep(G)}$ for the fixed graph $G$. We can do this by checking whether any cell of the coarsest equitable partition contains multiple orbit cells or not. However, it is enough to look at whether the number of cells in both partitions is equal to each other. 

In the code file of this repository, we see four different documents. "compute_cep.py" computes the coarsest equitable partitions for 11 of 13 datasets, except for HumanPPI and WordNet. Moreover, "compare_orbits.py" compares the orbit partition with the coarsest equitable partition for all of these 11 datasets, and obtain 100% equality between them. The reason we take HumanPPI and WordNet as seperated from the others is that the orbit cells for these two datasets start from $1$, although all the others are indexed from $0$. Hence, for these two datasets, we write the cells of the coarsest equitable partition using $1$-based labels. We then observe that if we apply the relabelling: $i \to i-1$ for $i > 1$ and $1 \to |V(G)|$ to the coarsest equitable partition, we obtain an equality with the orbit partition. The associated code is in "compare_humanppi_wordnet.py". The last document "combine_results.py" presents the whole results in a single file.

In fact, the following table shows our results:

=================================================================================================
Dataset                              n          CEP       Orbits       Diff   Equal?
=================================================================================================
Actors                         374,511      191,680      191,680          0     True
Amazon                         334,863      302,387      302,387          0     True
Astro-Ph                        17,903       14,660       14,660          0     True
CaliforniaRoads              1,957,027    1,917,379    1,917,379          0     True
HumanDisease                     1,419          686          686          0     True
HumanPPI                         9,270        8,294        8,294          0     True
InternetAS-koblenz              34,761       19,128       19,128          0     True
InternetAS-skitter           1,694,616    1,360,452    1,360,452          0     True
LiveJournal                  5,189,808    4,777,459    4,777,459          0     True
OpenFlights                      3,397        2,626        2,626          0     True
USPowerGrid                      4,941        4,466        4,466          0     True
WordNet                        145,145       87,244       87,244          0     True
Yeast                            1,647        1,256        1,256          0     True
=================================================================================================


We note that the orbit cells for the HumanPPI and WordNet datasets start from $1$, although all the others are indexed from $0$. Hence, for these two datasets, we write the cells of the coarsest equitable partition using $1$-based labels. We then observe that if we apply the relabelling: $i \to i-1$ for $i > 1$ and $1 \to |V(G)|$ to the coarsest equitable partition, we obtain an equality with the orbit partition.  

[1]:Sánchez-García, Rubén J. "Exploiting symmetry in network analysis." Communications Physics 3.1 (2020): 87.

The dataset is available at https://figshare.com/articles/dataset/Network_symmetry_datasets/11619792/1
