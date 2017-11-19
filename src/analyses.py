from abc import ABC, abstractmethod
from file_utils import save_json, load_txt_into_dict


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

    @abstractmethod
    def finalize(self):
        pass

    def save(self):
        save_json(self.state, f"../outputs/intermediates/{self.name}.json")


class WordFrequencyAnalysis(Analysis):
    def __init__(self):
        self.words = {}
        self.stopwords = load_txt_into_dict("../data/raw/stopwords.txt")

    @property
    def name(self):
        return "word_frequency"

    def analyze_commit(self, author, repo, lines, message):
        words = message.split(" ")
        for word in words:
            word = word.strip().lower()
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
        word = words[0].strip().lower()

        if word in self.words:
            self.words[word] += 1
        else:
            self.words[word] = 1


