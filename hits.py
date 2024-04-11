
from collections import defaultdict


def hits(filename, num_iterations):
    ins = defaultdict(list)
    outs = defaultdict(list)
    all_nodes = set()

    with open(filename, 'r', encoding="utf8") as file:
        for line in file:
            nodes = line.strip().split()

            origin_node = nodes[0]
            destination_nodes = nodes[1:]

            all_nodes.add(origin_node)

            for n in destination_nodes:
                ins[n].append(origin_node)
                outs[origin_node].append(n)

                all_nodes.add(n)

    all_nodes_sorted = sorted(list(all_nodes))

    iteration = 0

    # Scores in tuple are in the form (hub, authority)
    old_scores = {n: (1, 1) for n in all_nodes}
    new_scores = {}

    while iteration < num_iterations:
        iteration += 1

        for n in all_nodes:
            hub_score = 0
            authority_score = 0

            for v in outs[n]:
                hub_score += old_scores[v][1]

            for v in ins[n]:
                authority_score += old_scores[v][0]

            new_scores[n] = (hub_score, authority_score)

        print(f"Iteration {iteration}")

        for n in all_nodes_sorted:
            print(f"{n}: \t h = {new_scores[n][0]} \t a = {new_scores[n][1]}")

        print()

        old_scores = new_scores
        new_scores = {}


def main():
    hits("hits_test.txt", 2)



if __name__ == "__main__":
    main()
