#!/usr/bin/env python3
from plotters import *
from os import makedirs

makedirs("../outputs/charts", exist_ok=True)

FirstWordFrequencyPlotter().plot()
WordFrequencyPlotter().plot()
VerbFormOverviewPlotter().plot()
ImperativePlotter().plot()
GerundWordsPlotter().plot()
ThirdPersonWordsPlotter().plot()
PastTenseWordsPlotter().plot()
MessageLengthPlotter().plot()
MessageLinesPlotter().plot()
BinaryAnalysesPlotter().plot()
