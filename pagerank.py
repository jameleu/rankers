import sys
from collections import defaultdict

def read_urls(filename):
    """Read URLs from a file."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

def read_links(filename):
    """Read link pairs (source_URL, URL) from a file."""
    with open(filename, 'r') as f:
        links = []
        urls = set()
        for line in f:
            curr_line = line.strip().split()
            # account for the weird urls with spaces in them by combining them if there are more than 0 spaced words after the second url per pair
            if len(curr_line) > 2:
                for i in range(2, len(curr_line)):
                    curr_line[1] += curr_line[i]
                links.append((curr_line[0], curr_line[1]))
                if curr_line[0] not in urls:
                    urls.add(curr_line[0])
                if curr_line[1] not in urls:
                    urls.add(curr_line[1])
            else:
                links.append(tuple(curr_line))
                if curr_line[0] not in urls:
                    urls.add(curr_line[0])
                if curr_line[1] not in urls:
                    urls.add(curr_line[1])
    return (links, urls)

def calculate_pagerank(urls, links, convergence_threshold, max_iterations, damping_factor=0.85):
    # Default 0.25 starting scores
    pagerank = {url: 0.25 for url in urls}
    prev_pagerank = pagerank.copy()  # basically starts at default scores, too; need separate because are modifying pagerank with each url and want last round's info, not curr
    N = len(urls)
    # get outbound links count
    outbound_links_count = defaultdict(int)
    for source, target in links:
        outbound_links_count[source] += 1
    count = 0
    while count < max_iterations:
        for url in urls:
            # for each predecessor (j of IN(v_i)), add score / its outgoing links to sum  (ingoing means coming to curr url, so target is curr url)
            predecessor_sum_score = sum(prev_pagerank[source] / outbound_links_count[source] for source, target in links if target == url and outbound_links_count[source] != 0)

            # pagerank for this url is (1-d) / N + d * predecessor sum score
            pagerank[url] = (1 - damping_factor) / N + damping_factor * predecessor_sum_score

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

def write_pagerank(filename, pagerank):
    """Write sorted PageRank scores to a file."""
    with open(filename, 'w') as f:
        for url, score in sorted(pagerank.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{url} {score}\n")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python pagerank.py <links_file> <d> <convergence_threshold> <max_iterations>")
        sys.exit(1)

    # urls_file = sys.argv[1]
    links_file = sys.argv[1]
    damping_factor = float(sys.argv[2])
    convergence_threshold = float(sys.argv[3])

    # list of urls
    # urls = read_urls(urls_file)
    # list of tuples (source, target)
    links, urls = read_links(links_file)

    pagerank = calculate_pagerank(urls, links, convergence_threshold, max_iterations, damping_factor=damping_factor)

    write_pagerank("pagerank.output", pagerank)
