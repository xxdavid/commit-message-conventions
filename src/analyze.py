#!/usr/bin/env python3
from analyzer import Analyzer
from analyses import *

Analyzer([
    WordFrequencyAnalysis(),
    FirstWordFrequencyAnalysis(),
    VerbFormAnalysis(),
    MessageLengthAnalysis(),
    MessageLineCountAnalysis(),
    BinaryAnalyses(),
]).analyze()
