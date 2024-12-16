import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.   

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    each_page_probability = {}
    random_value_factor_to_get_to_each_page = (1 - damping_factor) / len(corpus)
    actual_page = corpus[page]
    actual_page_number_of_links = len(actual_page)
    equal_probability = 1 / len(corpus)
    
    if len(actual_page) == 0:
        for key, value in corpus.items():
            each_page_probability[key] = equal_probability
        return each_page_probability
    
    for value in actual_page:
        each_page_probability[value] = ((1 / actual_page_number_of_links) * damping_factor) + random_value_factor_to_get_to_each_page

    for key, _ in corpus.items():
        if key not in each_page_probability:
            each_page_probability[key] = random_value_factor_to_get_to_each_page
    return each_page_probability
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    keys_list = list(corpus.keys())

    random_page = random.choice(keys_list)
    each_page_choice_counter = {}
    each_page_page_rank = {}
    each_page_choice_counter[random_page] = 1

    
    for i in range(n - 1):
        transition_model_result = transition_model(corpus, random_page, damping_factor)
        keys = list(transition_model_result.keys())
        weights = list(transition_model_result.values())
        random_page = random.choices(keys, weights, k=1)[0]
        if random_page in each_page_choice_counter:
            each_page_choice_counter[random_page] += 1
        else:
            each_page_choice_counter[random_page] = 1
    for key, value in each_page_choice_counter.items():
        each_page_page_rank[key] = value / n

    return each_page_page_rank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    each_page_page_rank = {}
    edge_value_to_stop = 0.001
    corpus_len = len(corpus)
    random_probability_value = (1 - damping_factor) / corpus_len
    all_pages_linked = set(corpus.keys())

    for key, value in corpus.items():
        each_page_page_rank[key] = 1 / corpus_len
        if len(value) == 0:
            corpus[key] = all_pages_linked

    stop_range_reached = False

    while not stop_range_reached:
        stop_range_reached = True
        new_ranks = {}
        for page in corpus:
            new_rank = random_probability_value
            for possible_page in corpus:
                if page in corpus[possible_page]:
                    new_rank += damping_factor * each_page_page_rank[possible_page] / len(corpus[possible_page])
            new_ranks[page] = new_rank
            if abs(new_ranks[page] - each_page_page_rank[page]) > edge_value_to_stop:
                stop_range_reached = False
        each_page_page_rank = new_ranks
    
    return each_page_page_rank



if __name__ == "__main__":
    main()
