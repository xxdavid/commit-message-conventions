from abc import ABC, abstractmethod
from file_utils import save_json, load_txt_into_set
import re


class Analysis(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def analyze_commit(self, author, repo, lines, message):
        pass

    @property
    @abstractmethod
    def state(self):
        pass

    @state.setter
    @abstractmethod
    def state(self, value):
        pass

    def finalize(self):
        pass

    def save(self):
        save_json(self.state, f"../outputs/intermediates/{self.name}.json")


class WordFrequencyAnalysis(Analysis):
    def __init__(self):
        self.words = {}
        self.stopwords = load_txt_into_set("../data/raw/stopwords.txt")

    @property
    def name(self):
        return "word_frequency"

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
        self.words = [{'word': word, 'count': self.words[word]} for word in sorted_keys]

    @property
    def state(self):
        return self.words

    @state.setter
    def state(self, value):
        self.words = value


class FirstWordFrequencyAnalysis(WordFrequencyAnalysis):
    @property
    def name(self):
        return "first_word_frequency"

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
            "imperative",
            "gerund",
            "third_person",
            "past_tense"
        ]

        self.lists = {}
        for form in self.forms:
            self.lists[form] = load_txt_into_set(f"../data/processed/{form}.txt")

        self.counts = {}
        for form in self.forms:
            self.counts[form] = 0
        self.counts['non_verb'] = 0

        self.frequencies = {}
        for form in self.forms:
            self.frequencies[form] = {}

    @property
    def name(self):
        return "verb_form"

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
            sorted_keys = \
                sorted(self.frequencies[form], key=self.frequencies[form].get, reverse=True)
            self.frequencies[form] = \
                [{'word': word, 'count': self.frequencies[form][word]} for word in sorted_keys]

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
        return "message_length"

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
        return "message_line_count"

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
        return "binary"

    def analyze_commit(self, author, repo, lines, message):
        if len(message) > 0:
            for analysis in self.analyses:
                if self.analyses[analysis](message):
                    self.counts[analysis] += 1

    @property
    def state(self):
        return self.counts
