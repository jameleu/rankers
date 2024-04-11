python pagerank.py test_pagerank.txt 0.85 0.01 100
run pagerank with input of <file>, d=0.85, convergence = 0.01, max iterations = 100

python topic_pagerank.py topic_edges.txt topics.txt topic_nodes.txt  0.85 0.1 2
run topic sensitive pagerank with input of edges in graph, node names, nodes' associations, damping factor as 0.85, 0.1 convergence, 2 max iterations

python textrank.py textrank_test.txt 0.85 0.1 1
run textrank with input of testrank_test.txt, d=0.85, convergence = 0.01, max iterations = 100

