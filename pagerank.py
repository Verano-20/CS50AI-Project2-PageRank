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
    distribution = dict()

    # Add probabilities of choosing a random page
    for everypage in corpus:
        distribution[everypage] = (1 - damping_factor) / len(corpus)

    # Add probablities of choosing each linked page
    for linkedpage in corpus[page]:
        distribution[linkedpage] += damping_factor / len(corpus[page])

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()

    # Add all pages in corpus to pagerank
    for everypage in corpus:
        pagerank[everypage] = 0

    # Get initial page randomly from all pages
    currentpage = random.choice(list(corpus.keys()))

    # Loop until n is reached
    i=0
    while i < n:
        i += 1
        # Add (normalised) one to count of current page in pagerank
        pagerank[currentpage] += 1 / n
        # Get transition model for current page
        transition = transition_model(corpus, currentpage, damping_factor)
        # Choose next page using weighted random selection from transition model of current page
        currentpage = random.choices(list(transition.keys()), weights = list(transition.values()), k=1)[0]

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()

    # Add all pages in corpus to pagerank and give initial vaues 1/N
    for everypage in corpus:
        pagerank[everypage] = 1 / len(corpus)
    
    # Calculate new pagerank values
    while True:
        loop = False
        for p in pagerank.keys():
            # Get starting pagerank to check difference
            startrank = pagerank[p]
            # Probability of randomly landing on page
            PR = (1 - damping_factor / len(corpus))
            # Check all pages in corpus
            for page in corpus.keys():
                # If page has a link to p, update PR
                if p in corpus[page]:
                    PR += damping_factor * (pagerank[page] / len(corpus[page]))
            # Update pagerank
            pagerank[p] = PR
            # If value for any page has changed by more than 0.001, loop again
            if abs(startrank - PR) > 0.001:
                loop = True

        if not loop:
            break

    # Normalise all pagerank values
    alpha = 1 / sum(pagerank.values())
    for page in pagerank:
        pagerank[page] = alpha * pagerank[page]

    return pagerank


if __name__ == "__main__":
    main()
