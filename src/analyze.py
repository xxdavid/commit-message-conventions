#!/usr/bin/env python3
from analyzer import Analyzer
from analyses import *

Analyzer("../outputs", "messages.txt", [
    WordFrequencyAnalysis(),
    FirstWordFrequencyAnalysis()
]).analyze()
