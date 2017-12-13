#!/usr/bin/env python3
import sys

from fetch_commits_for_month import fetch_and_parse_commits_for_month


def fetch_and_parse_commits_for_year(year):
    """
    Fetch and parse commits for a given year.
    :param year: year in yyyy format
    """
    for month in range(1, 13):
            fetch_and_parse_commits_for_month(year, month)


if __name__ == '__main__':
    fetch_and_parse_commits_for_year(sys.argv[1])
