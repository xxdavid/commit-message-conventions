from abc import ABC, abstractmethod
from file_utils import save_json, load_txt_into_set


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


class VerbFormAnalysis(Analysis):
    def __init__(self):
        self.n_infinitive = 0
        self.n_gerund = 0
        self.n_third_person = 0
        self.n_past_tense = 0
        self.n_non_verb = 0

        self.infinitive_list = load_txt_into_set("../data/processed/infinitive.txt")
        self.gerund_list = load_txt_into_set("../data/processed/gerund.txt")
        self.third_person_list = load_txt_into_set("../data/processed/third_person.txt")
        self.past_tense_list = load_txt_into_set("../data/processed/past_tense.txt")

    @property
    def name(self):
        return "verb_form"

    def analyze_commit(self, author, repo, lines, message):
        word = message.split(" ")[0].strip().lower()
        if word in self.infinitive_list:
            self.n_infinitive += 1
        elif word in self.gerund_list:
            self.n_gerund += 1
        elif word in self.third_person_list:
            self.n_third_person += 1
        elif word in self.past_tense_list:
            self.n_past_tense += 1
        else:
            self.n_non_verb += 1

    @property
    def state(self):
        return {
            'infinitive': self.n_infinitive,
            'gerund': self.n_gerund,
            'third_person': self.n_third_person,
            'past_tense': self.n_past_tense,
            'non_verb': self.n_non_verb
        }
