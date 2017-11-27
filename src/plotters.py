from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np

from config import Directories
from file_utils import load_json


class Plotter(ABC):
    def __init__(self):
        self.data = load_json(f"{Directories.json_outputs}/{self.input_file_name}.json")

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    def input_file_name(self):
        return self.name

    @property
    @abstractmethod
    def title(self):
        pass

    @property
    @abstractmethod
    def x_label(self):
        pass

    @property
    def y_label(self):
        return "Occurrences [%]"

    @abstractmethod
    def init_plot(self):
        pass

    @property
    def text_color(self):
        return "#EAE3CB"

    def plot(self):
        plt.rcParams['axes.labelcolor'] = self.text_color
        plt.rcParams['xtick.color'] = self.text_color
        plt.rcParams['ytick.color'] = self.text_color

        self.init_plot()

        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        title = plt.title(self.title)
        plt.setp(title, color=self.text_color)

        plt.tight_layout()

        plt.savefig(f"{Directories.charts}/{self.name}.png", transparent=True)
        plt.savefig(f"{Directories.charts}/{self.name}.svg")
        plt.close()


class BarPlotter(Plotter):
    @abstractmethod
    def compute_values(self):
        pass

    @property
    def bar_color(self):
        return "#259286"

    def init_plot(self):
        values = self.compute_values()

        [x, y] = list(zip(*values))

        ind = np.arange(len(x))
        width = .8
        plt.bar(ind, y, width=width, color=self.bar_color)
        plt.xticks(ind, x, rotation=self.rotation)
        plt.tick_params(bottom='off')

    @property
    def rotation(self):
        return 70


class LinePlotter(Plotter):
    @abstractmethod
    def compute_values(self):
        pass

    def init_plot(self):
        values = self.compute_values()

        [x, y] = list(zip(*values))

        plt.plot(x, y)


class WordFrequencyPlotter(BarPlotter):
    @property
    def name(self):
        return "word_frequency"

    @property
    def title(self):
        return "The most frequent words"

    @property
    def x_label(self):
        return "Word"

    @property
    def n_top_words(self):
        return 10

    def compute_values(self):
        total_count = sum(x['count'] for x in self.data)

        top_words = self.data[:self.n_top_words]
        values = [(x['word'], x['count'] * 100 / total_count) for x in top_words]

        return values


class FirstWordFrequencyPlotter(WordFrequencyPlotter):
    @property
    def name(self):
        return "first_word_frequency"

    @property
    def title(self):
        return "The most frequent first words"


class VerbFormOverviewPlotter(BarPlotter):
    @property
    def name(self):
        return "verb_form_overview"

    @property
    def input_file_name(self):
        return "verb_form"

    @property
    def title(self):
        return "Overview of verb conjugation use"

    @property
    def x_label(self):
        return "Verb form"

    def compute_values(self):
        counts = self.data['total_counts']
        total_count = sum(counts.values())

        values = [(x.replace("_", " ").capitalize(), counts[x] * 100 / total_count)
                  for x in counts]
        values.sort(key=lambda x: x[1], reverse=True)

        return values


class VerbFormWordsPlotter(WordFrequencyPlotter, ABC):
    @property
    @abstractmethod
    def form(self):
        pass

    @property
    def name(self):
        return f"verb_form_{self.form}_frequency"

    @property
    def input_file_name(self):
        return "verb_form"

    @property
    def title(self):
        form_title = self.form.replace("_", " ").capitalize()
        return f"{form_title}: the most frequent first words"

    def compute_values(self):
        total_count = self.data['total_counts'][self.form]

        top_words = self.data['frequencies'][self.form][:self.n_top_words]
        values = [(x['word'], x['count'] * 100 / total_count) for x in top_words]

        return values


class ImperativePlotter(VerbFormWordsPlotter):
    @property
    def form(self):
        return "imperative"


class GerundWordsPlotter(VerbFormWordsPlotter):
    @property
    def form(self):
        return "gerund"


class ThirdPersonWordsPlotter(VerbFormWordsPlotter):
    @property
    def form(self):
        return "third_person"


class PastTenseWordsPlotter(VerbFormWordsPlotter):
    @property
    def form(self):
        return "past_tense"


class MessageLengthPlotter(LinePlotter):
    @property
    def name(self):
        return "message_length"

    @property
    def title(self):
        return "Length of the first line"

    @property
    def x_label(self):
        return "Length"

    def compute_values(self):
        total_count = sum(self.data.values())

        values = [(int(x), self.data[x] * 100 / total_count) for x in self.data]
        values.sort(key=lambda x: x[0])
        values = values[:100]

        return values


class MessageLinesPlotter(LinePlotter):
    @property
    def name(self):
        return "message_line_count"

    @property
    def title(self):
        return "Number of lines"

    @property
    def x_label(self):
        return "Line count"

    def compute_values(self):
        total_count = sum(self.data.values())

        values = [(int(x), self.data[x] * 100 / total_count) for x in self.data]
        values.sort(key=lambda x: x[0])
        values = values[:7]

        return values


class BinaryAnalysesPlotter(BarPlotter):
    @property
    def name(self):
        return "binary"

    @property
    def title(self):
        return "Miscellaneous binary analyses"

    @property
    def x_label(self):
        return "Condition"

    @property
    def rotation(self):
        return 10

    def compute_values(self):
        total_count = self.data['total']

        labels = {
            'capital_letter': 'Capital letter',
            'full_stop': 'Full stop',
            'capslock': 'CAPSLOCK ON',
            'non_ascii_chars': 'Contains non-ASCII chars'
        }

        values = [
            (labels[x], self.data[x] * 100 / total_count)
            for x in self.data
            if x != 'total'
        ]
        values.sort(key=lambda x: x[1], reverse=True)

        return values

