import sys
from collections import defaultdict
from itertools import combinations

def read_text(filename):
    """Read link pairs (source_word, word) from a file."""
    pairs = []  # could skip making bigram pairs but makes handling a bit easier
    with open(filename, 'r') as file:
        for line in file:
            words = line.strip().split()
            for i in range(len(words) - 1):
                pairs.append(tuple(sorted([words[i], words[i + 1]])))
            # ^Generate pairs and extend the list of pairs (alphabetical)
    neighbors = defaultdict(set)  # adjacency list
    pair_count = defaultdict(int)
    outbound_count = defaultdict(int)
    words = set()
    for curr_pair in pairs:
        
        pair_count[curr_pair] += 1
        outbound_count[curr_pair[0]] += 1
        outbound_count[curr_pair[1]] += 1
        neighbors[curr_pair[0]].add(curr_pair[1])
        neighbors[curr_pair[1]].add(curr_pair[0])
        if curr_pair[0] not in words:
            words.add(curr_pair[0])
        if curr_pair[1] not in words:
            words.add(curr_pair[1])
    return (neighbors, words, pair_count, outbound_count)

def calculate_pagerank(words, neigh, pair_count, outbound_count, convergence_threshold, max_iterations, damping_factor=0.85):
    pagerank = {word: 0.1 for word in words}
    prev_pagerank = pagerank.copy()  # basically starts at default scores, too; need separate because are modifying pagerank with each word and want last round's info, not curr
    N = len(words)
    count = 0
    with open("textrank_work.output", "w") as file:
        file.write("0.1 for all 0th iterations\n\n")
        while count < max_iterations:
            file.write(f"Iteration {count + 1}:\n")
            for word in words:
                predecessor_sum_score = 0
                file.write(f"{word}: ")
                file.write("(")
                for i, nbor in enumerate(neigh[word]):
                    
                    # look at pair (alphabetical order)
                    neigh_conn_with_word = pair_count[tuple(sorted([word, nbor]))]
                    curr = neigh_conn_with_word * prev_pagerank[nbor]
                    if outbound_count[nbor] != 0:
                        curr /= outbound_count[nbor]

                    if i == 0:
                        file.write(f"{prev_pagerank[nbor]} * {neigh_conn_with_word}/{outbound_count[nbor]} ")
                    else:
                        file.write(f"+ {prev_pagerank[nbor]} * {neigh_conn_with_word}/{outbound_count[nbor]} ")
                    curr = round(curr, 4)
                    predecessor_sum_score += curr  
                pagerank[word] = round((1 - damping_factor) + damping_factor * predecessor_sum_score, 4)
                file.write(f")* {damping_factor} + (1 - {damping_factor}) = {round(pagerank[word], 3)}\n")
            # need to go through all words to see if curr score - prev score < threshold (using all func that takes in iterable)
            converged = all(abs(pagerank[word] - prev_pagerank[word]) < convergence_threshold for word in words)
            if converged:
                # normalize scores according to sum of scores
                total_sum = sum([score for score in pagerank.values()])
                for curr_word, score in pagerank.items():
                    pagerank[curr_word] /= total_sum
                break

            prev_pagerank = pagerank.copy()
            count += 1
    print(f"Rounds to converge: {count}")
    return pagerank

def write_pagerank(filename, pagerank):
    """Write sorted PageRank scores to a file."""
    with open(filename, 'w') as f:
        for word, score in sorted(pagerank.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{word} {round(score, 3)}\n")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python textrank.py <sentence_file> <d> <convergence_threshold> <max_iterations>")
        sys.exit(1)

    sen_file = sys.argv[1]
    damping_factor = float(sys.argv[2])
    convergence_threshold = float(sys.argv[3])
    max_iterations = int(sys.argv[4])

    # words - set of words
    # neigh - word : list of its neighbors (adjacency list)
    # pair_count - pair (alphabetical order) : frequency
    neigh, words, pair_count, outbound_count = read_text(sen_file)

    pagerank = calculate_pagerank(words, neigh, pair_count, outbound_count, convergence_threshold, max_iterations, damping_factor=damping_factor)

    write_pagerank("textrank.output", pagerank)
