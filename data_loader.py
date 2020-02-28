import os

import numpy as np
import pandas as pd

tags = ['BD', 'BP', 'PR', 'SP', 'CH', 'ED']
VOCAB_list = ['<PAD>', 'O',]
for tag in tags:
    VOCAB_list.append('I-'+tag)
    VOCAB_list.append('B-'+tag)
VOCAB = tuple(VOCAB_list)
tag2idx = {tag: idx for idx, tag in enumerate(VOCAB)}
idx2tag = {idx: tag for idx, tag in enumerate(VOCAB)}

class NerDataset():
    def __init__(self, fpath):
        """
        fpath: [train|valid|test].txt
        """
        entries = open(fpath, 'r').read().strip().split("\n\n")
        sents, tags_li = [], [] # list of lists
        for entry in entries:
            lines = entry.splitlines()
            words = [line.split()[0] for line in entry.splitlines() if len(line.split()) > 1]
            tags = ([line.split()[-1] for line in entry.splitlines() if len(line.split()) > 1])
            sents.append(["[CLS]"] + words + ["[SEP]"])
            # sents.append(["[CLS]"] + words + ["[SEP]"])
            tags_li.append(["<PAD>"] + tags + ["<PAD>"])
        self.sents, self.tags_li = sents, tags_li

    def __len__(self):
        return len(self.sents)

    def __getitem__(self, idx):
        words, tags = self.sents[idx], self.tags_li[idx] # words, tags: string list
        words = " ".join(words)
        tags = " ".join(tags)
        return words, tags
    
    def append(self, other):
        self.sents.extend(other.sents)
        self.tags_li.extend(other.tags_li)

sample_data = [['[CLS]', 'The', 'character', 'was', 'also', 'shown', 'to', 'have', 'a', 'degree', 'that', 'belies', 'her', 'therapeutic', 'advice', 'and', 'was', 'estranged', 'from', 'her', 'mother', '.', '[SEP]'],
['[CLS]', 'In', '2000', ',', 'in', 'the', 'episode', '"', 'The', 'Midterms', '"', 'on', 'The', 'West', 'Wing', ',', 'the', 'fictional', '"', 'Dr.', 'Jenna', 'Jacobs', '"', 'is', 'scolded', 'by', 'President', 'Bartlet', ',', 'who', 'criticizes', 'her', 'views', 'on', 'homosexuality', ',', 'and', 'points', 'out', 'she', 'is', 'not', 'a', 'doctor', 'in', 'any', 'field', 'related', 'to', 'morality', ',', 'ethics', ',', 'medicine', 'or', 'theology', '.', '[SEP]'], ['[CLS]', 'He', 'quotes', 'from', 'the', 'Bible', 'to', 'point', 'out', 'the', 'inconsistency', 'of', 'condemning', 'certain', 'sins', 'but', 'not', 'others', '.', '[SEP]'], ['[CLS]', 'Show', 'creator', 'Aaron', 'Sorkin', 'admitted', 'to', 'modeling', 'Bartlet', "'s", 'diatribe', 'on', 'an', 'anonymous', '"', 'Letter', 'to', 'Dr.', 'Laura', ',', '"', 'which', 'was', 'a', 'popular', 'viral', 'email', 'at', 'the', 'time', '.', '[SEP]'], ['[CLS]', 'A', 'fictionalised', 'version', 'of', 'Schlessinger', 'is', 'featured', 'as', 'an', 'antagonist', 'in', 'the', '2000', 'animated', 'series', 'Queer', 'Duck', '.', '[SEP]'], ['[CLS]', 'In', '2001', ',', 'Schlessinger', 'was', 'portrayed', 'on', 'the', 'claymation', 'show', 'Celebrity', 'Deathmatch', 'on',
'the', 'episode', ',', 'A', 'Night', 'of', 'Vomit', '.', '[SEP]'], ['[CLS]', 'She', 'was', 'in', 'a', 'fight', 'with', 'Ellen', 'DeGeneres', ';', 'she', 'lost', '.', '[SEP]']]