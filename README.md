# PO-Scheduling

O gerenciamento de atividades esportivas é uma área promissora e bastante explorada para aplicações de Pesquisa Operacional. As competições esportivas envolvem muitos aspectos econômicos e logísticos. Os problemas desta área em geral possuem formulações simples, porém são problemas difíceis de serem resolvidos computacionalmente, visto que, possuem diversas restrições e múltiplos objetivos.

A programação de tabelas é uma das principais aplicações de Pesquisa Operacional em esportes. As ligas esportivas precisam de tabelas que satisfaçam diferentes tipos de restrições e que otimizem objetivos tais como a distância viajada pelas equipes durante o campeonato ou, em uma competição de menor porte, objetivos que evite conflito de horários entre jogos.

O problema mais abordado de programação de tabelas consiste em decidir quando e onde os jogos de um determinado campeonato serão realizados. Este problema pode ser abordado como sequenciamento de tarefas, usualmente, estas são representadas pelos jogos e os recursos pelas equipes que participam do torneio.

O objetivo do trabalho será analisar a tabela do campeonato Arulíadas organizado pela Associação de Repúblicas da Unicamp de Limeira (ARULI). Esta é uma organização estudantil sem fins lucrativos, reconhecida pela UNICAMP.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Para a solução deste projeto foram feitas duas modelagens matemáticas. A primeira modelagem possui uma variável binária a mais que a segunda modelagem que armazena no programa se o slot de tempo está ocupado.

Há uma comparação entre solvers disponíveis no mercado: Gurobi e or-tools
