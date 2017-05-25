'''This function takes as input a text file of strophe separated by one blank space,
or a python list of stanzas. It yields tagged syllables with endings and weights
as well as ratios for each stanza'''


def process(filepath=False, stanza_text=False):

    import sys
    from syllabipymhg import syllabipymhg
    from get_features import syllableend
    from get_features import syllableweight
    from clean_text import cleantext
    from process_for_syll_feats import process

    def flatten(seq, levels):
        for x in range(levels):
            seq = [item for sublist in seq for item in sublist]
        return seq

    if filepath:
        with open(filepath, "r") as f:
            raw_text = f.read()
        stanza_text = raw_text.split('\n\n')

    elif stanza_text:
        stanza_text = stanza_text.split('\n\n')

    stanzas_lines = [stanza.split('\n') for stanza in stanza_text]
    stanza_lengths = [len(l) for l in stanzas_lines]
    stanzas_words = [[cleantext(line).split()
                      for line in stanza] for stanza in stanzas_lines]

    stanzas_words_sylls = [[[syllabipymhg(
        word) for word in line] for line in stanza] for stanza in stanzas_words]

    stanzas_words_sylls_feats = [[[[(syll, syllableend(syll), syllableweight(syll)) for syll in word]
                                   for word in line] for line in stanza]
                                 for stanza in stanzas_words_sylls]

    by_stanza = [flatten(stanza, 2) for stanza in stanzas_words_sylls_feats]
    by_stanza = [x for x in by_stanza if len(x) > 0]

    ratios_end = []
    ratios_weight = []
    for s in by_stanza:
        line_ratios_end = []
        line_ratios_weight = []
        for syll in s:
            line_ratios_end.append(syll[1])
            line_ratios_weight.append(syll[2])
        ratios_end.append(line_ratios_end)
        ratios_weight.append(line_ratios_weight)

    from collections import Counter
    ratios_end = [Counter(s) for s in ratios_end]
    ratios_weight = [Counter(s) for s in ratios_weight]

    percent_end = [x['O'] / (x['C'] + x['O']) for x in ratios_end]
    percent_weight = [x['L'] / (x['H'] + x['L']) for x in ratios_weight]

    percent_end_ordered = list(zip(stanza_text, percent_end))
    percent_weight_ordered = list(zip(stanza_text, percent_weight))
    percent_end_sorted = sorted(percent_end_ordered, key=lambda tup: tup[1])
    percent_weight_sorted = sorted(
        percent_weight_ordered,
        key=lambda tup: tup[1])

    return (
        stanzas_words_sylls_feats,
        percent_end_ordered,
        percent_end_sorted,
        percent_weight_ordered,
        percent_weight_sorted,
        stanza_lengths,
        list(zip(stanza_text, percent_end)))
