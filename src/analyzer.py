class Analyzer:
    def __init__(self, outputs_dir, messages_filename, analyses):
        self.outputs_dir = outputs_dir
        self.messages_path = outputs_dir + '/' + messages_filename
        self.analyses = analyses
        self.authors = {}
        self.total_number = 0
        self.analyzed_number = 0

        self.MAX_COMMITS_BY_AUTHOR = 3

    def analyze(self):
        file = open(self.messages_path)
        with file:
            for line in file:
                [author, repo, lines, message] = line.split("::", 3)
                if author not in self.authors:
                    self.authors[author] = 0
                if self.authors[author] < self.MAX_COMMITS_BY_AUTHOR:
                    for analysis in self.analyses:
                        analysis.analyze_commit(author, repo, lines, message)
                    self.authors[author] += 1
                    self.analyzed_number += 1
                self.total_number += 1

        for analysis in self.analyses:
            analysis.finalize()
            analysis.save()

        print(f"Analyzed {self.analyzed_number} commits (out of {self.total_number}).")
