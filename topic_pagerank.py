import sys
from collections import defaultdict

def read_topics(filename):  # topic, query relevance
    topic_dict = {}  # topic : query relevance
    with open(filename, 'r') as f:
        for line in f:
            curr_line = line.strip().split()
            topic_dict[curr_line[0]] = float(curr_line[1])
    return topic_dict
def count_topic_totals(filename):  # topic, count
    biases = defaultdict(int)
    urls = set()
    url_topics = defaultdict(set)
    with open(filename, 'r') as f:
        for line in f:
            curr_line = line.strip().split()
            biases[curr_line[1]] += 1
            urls.add(curr_line[0])
            url_topics[curr_line[0]].add(curr_line[1])
    return biases, urls, url_topics
def read_links(filename):
    """Read link pairs (source_URL, URL) from a file."""
    with open(filename, 'r') as f:
        links = []
        for line in f:
            curr_line = line.strip().split()
            links.append(tuple(curr_line))
    return links

def calculate_pagerank(urls, links, biases, query_rel, url_topics, convergence_threshold, max_iterations, damping_factor=0.85):
    # Default 0.25 starting scores
    N = len(urls)
    # get outbound links count
    outbound_links_count = defaultdict(int)
    for source, target in links:
        outbound_links_count[source] += 1
    topics_to_word_scores = defaultdict(dict)
    with open("topic_pagerank_work.output", "w") as file:
        for curr_bias in query_rel.keys(): 
            topics_to_word_scores[curr_bias] = {url: 0.25 for url in urls}
            pagerank = topics_to_word_scores[curr_bias]
            prev_pagerank = pagerank.copy()
            count = 0
            file.write(f"Current topic: {curr_bias}\n")
            while count < max_iterations:
                file.write(f"Iteration {count + 1}\n")
                for url in urls:
                    file.write(f"{url}: ")
                    bias_factor = 0
                    if curr_bias in url_topics[url]:
                        bias_factor = float(1)/biases[curr_bias]
                    predecessor_sum_score = 0
                    file.write("[")
                    i = 0    
                    for source, target in links:
                        if target == url and outbound_links_count[source] != 0:
                            predecessor_sum_score += prev_pagerank[source] / outbound_links_count[source]
                            if i == 0:
                                file.write(f"({prev_pagerank[source]} / {outbound_links_count[source]}) ")
                            else:
                                file.write(f"+ ({prev_pagerank[source]} / {outbound_links_count[source]}) ")
                            i += 1
                    predecessor_sum_score = round(predecessor_sum_score, 4)
                    pagerank[url] = round(((1 - damping_factor) * bias_factor + damping_factor * predecessor_sum_score), 3)
                    file.write(f"] * {damping_factor} + (1 - {damping_factor}) * {bias_factor} = {round(pagerank[url], 3)}\n")
                # need to go through all urls to see if curr score - prev score < threshold (using all func that takes in iterable)
                file.write("\n")
                converged = all(abs(pagerank[url] - prev_pagerank[url]) < convergence_threshold for url in urls)
                if converged:
                    # normalize scores according to sum of scores
                    total_sum = sum([score for score in pagerank.values()])
                    for curr_url, score in pagerank.items():
                        pagerank[curr_url] /= total_sum
                    break
                prev_pagerank = pagerank.copy()
                count += 1
            file.write("\n")
        print(f"Rounds to converge: {count}")
    return topics_to_word_scores

def calculate_final_ranks(query_rel, pagerank_set, biases, urls):
    final = defaultdict(float)
    with open("topic_pagerank_work.output", "a") as file:
        file.write("Final Query Relevance Rank Calculations:\n")
        for url in urls:
            curr_score = 0
            i = 0
            file.write(f"{url}: ")
            for topic, rel in query_rel.items():
                curr_score += pagerank_set[topic][url] * rel
                if i == 0:
                    file.write(f"{pagerank_set[topic][url]} * {rel}")
                else:
                    file.write(f" + {pagerank_set[topic][url]} * {rel}")
                i += 1    
            final[url] = round(curr_score, 4)
            file.write(f" = {final[url]}\n")
    return final
        
def write_pagerank(filename, pagerank):
    """Write sorted PageRank scores to a file."""
    with open(filename, 'w') as f:
        for url, score in sorted(pagerank.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{url} {score}\n")

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python topic_pagerank.py <links_file> <topics_file> <url_association_file> <d> <convergence_threshold> <max_iterations>")
        sys.exit(1)

    # urls_file = sys.argv[1]
    links_file = sys.argv[1]
    topics_file = sys.argv[2]
    url_association_file = sys.argv[3]  # what topic each node associates with
    damping_factor = float(sys.argv[4])
    convergence_threshold = float(sys.argv[5])
    max_iterations = int(sys.argv[6])
    

    # list of tuples (source, target)
    links = read_links(links_file)
    # query_rel is: topic : relevance_factor
    query_rel = read_topics(topics_file)
    # biases is topic : topic_count
    # urls is nodes (unique)
    # urls_topics is url : set of its associated topics
    biases, urls, urls_topics = count_topic_totals(url_association_file)
    
    pagerank = calculate_pagerank(urls, links, biases, query_rel, urls_topics, convergence_threshold, max_iterations, damping_factor=damping_factor)
    ranks = calculate_final_ranks(query_rel, pagerank, biases, urls)
    write_pagerank("topic_pagerank.output", ranks)
