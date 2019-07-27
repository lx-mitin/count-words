import random
from collections import namedtuple, OrderedDict
from itertools import chain

Sentence = namedtuple("Sentence", "words tags")

def read_tags(filename):
    """Read a list of word tag classes"""
    with open(filename, 'r') as f:
        tags = f.read().split("\n")
    return frozenset(tags)


def read_data(filename):
    """Read tagged sentence data"""
    with open(filename, 'r') as f:
        sentence_lines = [l.split("\n") for l in f.read().split("\n\n")]
    return OrderedDict(((s[0], Sentence(*zip(*[l.strip().split("\t")
                        for l in s[1:]]))) for s in sentence_lines if s[0]))


class Dataset(namedtuple("_Dataset", "sentences keys vocab X tagset Y training_set testing_set N stream")):
    def __new__(cls, tagfile, datafile, train_test_split=0.8, seed=112890):
        tagset = read_tags(tagfile)
        sentences = read_data(datafile)
        keys = tuple(sentences.keys())
        wordset = frozenset(chain(*[s.words for s in sentences.values()]))
        word_sequences = tuple([sentences[k].words for k in keys])
        tag_sequences = tuple([sentences[k].tags for k in keys])
        N = sum(1 for _ in chain(*(s.words for s in sentences.values())))
        
        # split data into train/test sets
        _keys = list(keys)
        if seed is not None: random.seed(seed)
        random.shuffle(_keys)
        split = int(train_test_split * len(_keys))
        training_data = Subset(sentences, _keys[:split])
        testing_data = Subset(sentences, _keys[split:])
        stream = tuple(zip(chain(*word_sequences), chain(*tag_sequences)))
        return super().__new__(cls, dict(sentences), keys, wordset, word_sequences, tagset,
                               tag_sequences, training_data, testing_data, N, stream.__iter__)
    def __len__(self):
        return len(self.sentences)
    def __iter__(self):
        return iter(self.sentences.items())

class Subset(namedtuple("BaseSet", "sentences keys vocab X tagset Y N stream")):
    def __new__(cls, sentences, keys):
        word_sequences = tuple([sentences[k].words for k in keys])
        tag_sequences = tuple([sentences[k].tags for k in keys])
        wordset = frozenset(chain(*word_sequences))
        tagset = frozenset(chain(*tag_sequences))
        N = sum(1 for _ in chain(*(sentences[k].words for k in keys)))
        stream = tuple(zip(chain(*word_sequences), chain(*tag_sequences)))
        return super().__new__(cls, {k: sentences[k] for k in keys}, keys, wordset, word_sequences,
                               tagset, tag_sequences, N, stream.__iter__)
    def __len__(self):
        return len(self.sentences)
    def __iter__(self):
        return iter(self.sentences.items())
