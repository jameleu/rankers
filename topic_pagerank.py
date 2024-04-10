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
    for curr_bias in query_rel.keys(): 
        print("**********************", curr_bias)
        topics_to_word_scores[curr_bias] = {url: 0.25 for url in urls}
        pagerank = topics_to_word_scores[curr_bias]
        prev_pagerank = pagerank.copy()
        count = 0
        while count < max_iterations:
            for url in urls:
                bias_factor = 0
                if curr_bias in url_topics[url]:
                    bias_factor = float(1)/biases[curr_bias]
                    print(f"b{bias_factor}")
                print("_______________", url)
                predecessor_sum_score = round(sum((prev_pagerank[source] / outbound_links_count[source]) for source, target in links if target == url and outbound_links_count[source] != 0), 4)
                print(predecessor_sum_score)
                pagerank[url] = round(((1 - damping_factor) * bias_factor + damping_factor * predecessor_sum_score), 3)
                print(pagerank[url])
            # need to go through all urls to see if curr score - prev score < threshold (using all func that takes in iterable)
            converged = all(abs(pagerank[url] - prev_pagerank[url]) < convergence_threshold for url in urls)
            if converged:
                # normalize scores according to sum of scores
                total_sum = sum([score for score in pagerank.values()])
                for curr_url, score in pagerank.items():
                    pagerank[curr_url] /= total_sum
                break

            prev_pagerank = pagerank.copy()
            count += 1
        print(f"Rounds to converge: {count}")
    return topics_to_word_scores

def calculate_final_ranks(query_rel, pagerank_set, biases, urls):
    final = defaultdict(float)
    for url in urls:
        curr_score = 0
        for topic, rel in query_rel.items():
            print(f"{topic}, {url} : {pagerank_set[topic][url]}")
            curr_score += pagerank_set[topic][url] * rel
        final[url] = round(curr_score, 4)
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
