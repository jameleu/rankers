import sys
from collections import defaultdict

def read_topics(filename):  # topic, query relevance
    topic_dict = {}  # topic : query relevance
    with open(filename, 'r') as f:
        for line in f:
            curr_line = line.strip().split()
            topic_dict[curr_line[0]] = curr_line[1]
    return topic_dict
def count_topic_totals(filename):  # topic, count
    biases = defaultdict(int)
    urls = set()
    with open(filename, 'r') as f:
        for line in f:
            curr_line = line.strip().split()
            topic_dict[curr_line[0]] += 1
            urls.add((curr_line[0], curr_line[1]))
    return biases, urls
def read_links(filename):
    """Read link pairs (source_URL, URL) from a file."""
    with open(filename, 'r') as f:
        links = []
        for line in f:
            curr_line = line.strip().split()
            links.append(tuple(curr_line))
    return links

def calculate_pagerank(urls, links, biases, convergence_threshold, damping_factor=0.85):
    # Default 0.25 starting scores
    prev_pagerank = pagerank.copy()  # basically starts at default scores, too; need separate because are modifying pagerank with each url and want last round's info, not curr
    N = len(urls)
    # get outbound links count
    outbound_links_count = defaultdict(int)
    for url in urls:
        for source, target in links:
            if source == url:
                outbound_links_count[url] += 1
    count = 0
    topics_to_word_scores = defaultdict(dict)
    for curr_bias in biases.keys():
        topics_to_word_scores[curr_bias] = {url: 0.25 for url in urls}
        pagerank = topics_to_word_scores[curr_bias]
        while True:
            for url, bias in urls:
                bias_factor = 0
                if bias == curr_bias:
                    bias_factor = biases[bias]
                predecessor_sum_score = sum(prev_pagerank[source] / outbound_links_count[source] for source, target in links if target == url and outbound_links_count[source] != 0)

                pagerank[url] = (1 - damping_factor) * bias_factor + damping_factor * predecessor_sum_score

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
    return pagerank

def calculate_final_ranks(query_rel, pagerank_set, biases, urls):
    final = defauldict(float)
    for url in urls:
        curr_score = 0
        for topic, rel in query_rel.items():
            curr_score += pagerank_set[topic][url] * rel
        final[url] = curr_score
    return final
        
def write_pagerank(filename, pagerank):
    """Write sorted PageRank scores to a file."""
    with open(filename, 'w') as f:
        for url, score in sorted(pagerank.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{url} {score}\n")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python pagerank.py <links_file> <topics_file> <url_association_file> <d> <convergence_threshold>")
        sys.exit(1)

    # urls_file = sys.argv[1]
    links_file = sys.argv[1]
    topics_file = sys.argv[2]
    url_association_file = sys.argv[3]  # what topic each node associates with
    damping_factor = sys.argv[4]
    convergence_threshold = float(sys.argv[5])

    # list of urls
    # urls = read_urls(urls_file)
    # list of tuples (source, target)
    links = read_links(links_file)
    query_rel = read_topics(topics_file)
    biases, urls = count_topics_total(url_association_file)

    pagerank = calculate_pagerank(urls, links, biases, convergence_threshold, damping_factor=damping_factor)
    ranks = calculate_final_ranks(pagerank, query_rel)
    write_pagerank("pagerank.output", ranks)
