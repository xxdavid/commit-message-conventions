#!/usr/bin/env python3
from config import Directories
from plotters import *
from os import makedirs

makedirs(Directories.charts, exist_ok=True)

plotters = [
    FirstWordFrequencyPlotter(),
    WordFrequencyPlotter(),
    VerbFormOverviewPlotter(),
    ImperativePlotter(),
    GerundWordsPlotter(),
    ThirdPersonWordsPlotter(),
    PastTenseWordsPlotter(),
    MessageLengthPlotter(),
    MessageLinesPlotter(),
    BinaryAnalysesPlotter(),
]

for plotter in plotters:
    plotter.plot()
