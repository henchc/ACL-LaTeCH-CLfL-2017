from __future__ import unicode_literals  # for python2 compatibility
# -*- coding: utf-8 -*-
# created at UC Berkeley 2015
# Authors: Christopher Hench

# This program cleans texts for analysis.
# Input is any string of text (after it has been opened)


def cleantext(text):

    from string import punctuation

    text = text.lower()  # lowercase
    remove_char = [
        "›"
        "‹"
        "»",
        "«",
        "˃",
        "˂",
        "-",
        "—",
        "〈",
        "〉",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9"]  # remove these characters
    remove_char += list(punctuation)

    for char in remove_char:
        text = text.replace(char, '')

    return (text)
