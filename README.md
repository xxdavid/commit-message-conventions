# commit message conventions
A set of scripts for analyzing commit messages on Github.

## Analyses
* verb form
  * imperative (*add*)
  * gerund (*adding*)
  * past simple (*added*)
  * present simple, 3rd person (*adds*)
* word frequency
* commit message length, number of lines
* beginning with a capital letter
* ending with a dot
* containing only ASCII characters
* written with CAPS LOCK on

## Dependencies
* Python 3.6+
* pyquery
* matplotlib
* numpy

Install with
```bash
pip install -r requirements.txt
```

## Running
Run the scripts in the following order
```bash
./process_verbs.py && ./process_irregular_verbs.py && ./generate_conjugations.py && ./fetch_commits.py yyyy-mm-dd-hh && ./analyze.py && ./plot.py
```

You can substitute `fetch_commits.py yyyy-mm-dd-hh` with `fetch_commits_for_month.py yyyy-mm` or `./fetch_commits_for_year.py yyyy`.

## Results
I analyzed commits from the whole 2017, you can with the charts inside the [results-2017](results-2017/) folder.

## Data sources
* [Github Archive](https://githubarchive.org) – commits
* [WordNet](http://wordnet.princeton.edu/wordnet/download/current-version/) – list of verbs
* [Ted Pedersen](http://www.d.umn.edu/~tpederse/Group01/WordNet/wordnet-stoplist.html) – stop words
* [Wikipedia](https://en.wikipedia.org/wiki/List_of_English_irregular_verbs) – list of irregular verbs
