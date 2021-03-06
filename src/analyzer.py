from config import Directories


class Analyzer:
    """Class that reads commits and runs analyses on them."""

    def __init__(self, analyses):
        self.analyses = analyses
        self.authors = {}
        self.total_number = 0
        self.analyzed_number = 0

        self.MAX_COMMITS_BY_AUTHOR = 3

    def analyze(self):
        file = open(f"{Directories.processed_data}/commits.txt")
        with file:
            for line in file:
                try:
                    [author, repo, lines, message] = line.split("::", 3)
                    if author not in self.authors:
                        self.authors[author] = 0
                    if self.authors[author] < self.MAX_COMMITS_BY_AUTHOR:
                        message = message.strip()
                        for analysis in self.analyses:
                            analysis.analyze_commit(author, repo, lines, message)
                        self.authors[author] += 1
                        self.analyzed_number += 1
                except ValueError:
                    print("ValueError, skipping.")
                self.total_number += 1

        for analysis in self.analyses:
            analysis.finalize()
            analysis.save()

        print(f"Analyzed {self.analyzed_number} commits"
              f" (out of {self.total_number}).")
