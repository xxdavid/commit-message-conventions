class Analyzer:
    def __init__(self, outputs_dir, messages_filename, analyses):
        self.outputs_dir = outputs_dir
        self.messages_path = outputs_dir + '/' + messages_filename
        self.analyses = analyses

    def analyze(self):
        file = open(self.messages_path)
        with file:
            for line in file:
                [author, repo, lines, message] = line.split("::", 3)
                for analysis in self.analyses:
                    analysis.analyze_commit(author, repo, lines, message)

        for analysis in self.analyses:
            analysis.finalize()
            analysis.save()

