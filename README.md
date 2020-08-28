# CS50AI-Project2-PageRank

My solution for CS50AI project 2 - PageRank.

The Pagerank algorithm, developed by Google's co-founders, enables webpages to be ranked by 'importance'. A webpage is ranked as more important if it is linked to by other important webpages, and less important if it is only linked to by less important webpages.

This program calculates a pagerank for a set of webpages using a Random Surfer Model, and an Iterative Algorithm method.

The Random Surfer Model defines a transition model and samples *n* pages, where the next page is chosen from links in the current page based on the probabilities defined in the transition model. Aftet *n* samples, the pagerank is given by the total number of visits to each page.

The Iterative Algorithm methos uses the following algorithm:

<img src="https://github.com/Verano-20/CS50AI-Project2-PageRank/blob/master/pagrank%20formula.png" alt="pagerank formula" />

By iterating over this algorithm many times probabilities for each webpage converge, and the pagerank can be defined.
