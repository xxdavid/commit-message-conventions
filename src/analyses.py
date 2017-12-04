from abc import ABC, abstractmethod
from file_utils import save_json, load_txt_into_set
import re
from config import Directories


class Analysis(ABC):
    """
    Abstract analysis class.
    Every analysis analyzes some aspect of a commit message.
    On every commit message it gets, the analysis is performed
    and then the results are eventually written to a file.
    """

    @property
    @abstractmethod
    def name(self):
        """Name of the analysis used in the output filename."""
        pass

    @abstractmethod
    def analyze_commit(self, author, repo, lines, message):
        """
        Run the analysis on a commit.
        :param author: commit author (GitHub username)
        :param repo: repository name
        :param lines: number of lines of the commit message
        :param message: commit message
        """
        pass

    @property
    @abstractmethod
    def state(self):
        """
        Get the current state.
        State should be serializable as it will be encoded to JSON
        and written to a file.
        State should not be accessed before calling finalize().
        """
        pass

    def finalize(self):
        """
        Do final computations.
        For example, sorting or mapping of values can be done here.
        No further input data (commits) should be given after finalizing.
        """
        pass

    def save(self):
        """
        Write the results into a file.
        finalize() should be called before saving.
        """
        save_json(self.state, f"{Directories.json_outputs}/{self.name}.json")


class WordFrequencyAnalysis(Analysis):
    def __init__(self):
        self.words = {}
        self.stopwords =\
            load_txt_into_set(f"{Directories.raw_data}/stopwords.txt")

    @property
    def name(self):
        return 'word_frequency'

    def analyze_commit(self, author, repo, lines, message):
        words = message.split(" ")
        for word in words:
            word = word.lower()
            if word == "" or word in self.stopwords:
                continue

            if word in self.words:
                self.words[word] += 1
            else:
                self.words[word] = 1

    def finalize(self):
        sorted_keys = sorted(self.words, key=self.words.get, reverse=True)
        self.words = [{'word': word, 'count': self.words[word]}
                      for word in sorted_keys]

    @property
    def state(self):
        return self.words


class FirstWordFrequencyAnalysis(WordFrequencyAnalysis):
    @property
    def name(self):
        return 'first_word_frequency'

    def analyze_commit(self, author, repo, lines, message):
        words = message.split(" ")
        word = words[0].lower()

        if word in self.words:
            self.words[word] += 1
        else:
            self.words[word] = 1


class VerbFormAnalysis(Analysis):
    def __init__(self):
        self.forms = [
            'imperative',
            'gerund',
            'third_person',
            'past_tense'
        ]

        self.lists = {}
        for form in self.forms:
            self.lists[form] =\
                load_txt_into_set(f"{Directories.processed_data}/{form}.txt")

        self.counts = {}
        for form in self.forms:
            self.counts[form] = 0
        self.counts['non_verb'] = 0

        self.frequencies = {}
        for form in self.forms:
            self.frequencies[form] = {}

    @property
    def name(self):
        return 'verb_form'

    def analyze_commit(self, author, repo, lines, message):
        word = message.split(" ")[0].lower()
        if not self.analyze_word(word):
            word = re.sub("^.*:\s*", "", message).split(" ")[0].lower()
            if not self.analyze_word(word):
                word = re.sub("^\[.*\]\s*", "", message).split(" ")[0].lower()
                if not self.analyze_word(word):
                    self.counts['non_verb'] += 1

    def analyze_word(self, word):
        for form in self.forms:
            if word in self.lists[form]:
                self.counts[form] += 1
                self.count_frequency(word, form)
                return True
        return False

    def count_frequency(self, word, form):
        if word in self.frequencies[form]:
            self.frequencies[form][word] += 1
        else:
            self.frequencies[form][word] = 1

    def sort_frequencies(self):
        for form in self.forms:
            sorted_keys = sorted(
                self.frequencies[form],
                key=self.frequencies[form].get,
                reverse=True
            )

            self.frequencies[form] = [
                {'word': word, 'count': self.frequencies[form][word]}
                for word in sorted_keys
            ]

    def finalize(self):
        self.sort_frequencies()

    @property
    def state(self):
        return {
            'total_counts': self.counts,
            'frequencies': self.frequencies
        }


class MessageLengthAnalysis(Analysis):
    def __init__(self):
        self.lengths = {}

    @property
    def name(self):
        return 'message_length'

    def analyze_commit(self, author, repo, lines, message):
        length = len(message)
        if length in self.lengths:
            self.lengths[length] += 1
        else:
            self.lengths[length] = 1

    @property
    def state(self):
        return self.lengths


class MessageLineCountAnalysis(Analysis):
    def __init__(self):
        self.lineCounts = {}

    @property
    def name(self):
        return 'message_line_count'

    def analyze_commit(self, author, repo, lines, message):
        if lines in self.lineCounts:
            self.lineCounts[lines] += 1
        else:
            self.lineCounts[lines] = 1

    @property
    def state(self):
        return self.lineCounts


class BinaryAnalyses(Analysis):
    def __init__(self):
        self.analyses = {
            'total': lambda x: True,
            'capital_letter': lambda x: x[0].isupper(),
            'full_stop': lambda x: x[-1] == ".",
            'capslock': lambda x: all(c.isupper() for c in x),
            'non_ascii_chars': lambda x: any(ord(c) > 128 for c in x)
        }

        self.counts = {}
        for analysis in self.analyses:
            self.counts[analysis] = 0

    @property
    def name(self):
        return 'binary'

    def analyze_commit(self, author, repo, lines, message):
        if len(message) > 0:
            for analysis in self.analyses:
                if self.analyses[analysis](message):
                    self.counts[analysis] += 1

    @property
    def state(self):
        return self.counts
