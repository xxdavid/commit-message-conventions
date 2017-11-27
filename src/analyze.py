#!/usr/bin/env python3
from analyzer import Analyzer
from analyses import *

Analyzer("../data/processed/commits.txt", [
    WordFrequencyAnalysis(),
    FirstWordFrequencyAnalysis(),
    VerbFormAnalysis(),
    MessageLengthAnalysis(),
    MessageLineCountAnalysis(),
    BinaryAnalyses(),
]).analyze()
