from dataset import Dataset
from collections import namedtuple, defaultdict
from pomegranate import HiddenMarkovModel, DiscreteDistribution, State

FakeState = namedtuple("FakeState", "name")

def pair_counts(sequences_A, sequences_B):
    """Return a dictionary keyed to each unique value in the first sequence list
    that counts the number of occurrences of the corresponding value from the
    second sequences list.
    """
    pair_cnts = {tag:defaultdict(int) for tag in sequences_A}
    
    for i in range(len(sequences_A)):
        pair_cnts[sequences_A[i]][sequences_B[i]] += 1
    
    return pair_cnts


def replace_unknown(sequence):
    """Return a copy of the input sequence where each unknown word is replaced
    by the literal string value 'nan'. Pomegranate will ignore these values
    during computation.
    """
    return [w if w in data.training_set.vocab else 'nan' for w in sequence]


def simplify_decoding(X, model):
    """X should be a 1-D sequence of observations for the model to predict"""
    _, state_path = model.viterbi(replace_unknown(X))
    return [state[1].name for state in state_path[1:-1]]


def accuracy(X, Y, model):
    """Calculate the prediction accuracy by using the model to decode each sequence
    in the input X and comparing the prediction with the true labels in Y.
    
    The X should be an array whose first dimension is the number of sentences to test,
    and each element of the array should be an iterable of the words in the sequence.
    The arrays X and Y should have the exact same shape.
    
    X = [("See", "Spot", "run"), ("Run", "Spot", "run", "fast"), ...]
    Y = [(), (), ...]
    """
    correct = total_predictions = 0
    for observations, actual_tags in zip(X, Y):       
        # The model.viterbi call in simplify_decoding will return None if the HMM
        # raises an error (for example, if a test sentence contains a word that
        # is out of vocabulary for the training set). Any exception counts the
        # full sentence as an error (which makes this a conservative estimate).
        try:
            most_likely_tags = simplify_decoding(observations, model)
            correct += sum(p == t for p, t in zip(most_likely_tags, actual_tags))
        except:
            pass
        total_predictions += len(observations)
    return correct / total_predictions


def unigram_counts(sequences):
    """Return a dictionary keyed to each unique value in the input sequence list that
    counts the number of occurrences of the value in the sequences list. The sequences
    collection should be a 2-dimensional array.
    """
    unigrams = defaultdict(int)
    
    for sequence in sequences:
        for item in sequence:
            unigrams[item] += 1
    
    return unigrams


def bigram_counts(sequences):
    """Return a dictionary keyed to each unique PAIR of values in the input sequences
    list that counts the number of occurrences of pair in the sequences list. The input
    should be a 2-dimensional array.
    """

    bigrams = defaultdict(int)
    
    for sequence in sequences:
        for i in range(len(sequence)-1):
            bigrams[(sequence[i],sequence[i+1])] += 1
                
    return bigrams


def starting_counts(sequences):
    """Return a dictionary keyed to each unique value in the input sequences list
    that counts the number of occurrences where that value is at the beginning of
    a sequence.
    """
    startings = defaultdict(int)
    
    for sequence in sequences:
        startings[sequence[0]] += 1
            
    return startings


def ending_counts(sequences):
    """Return a dictionary keyed to each unique value in the input sequences list
    that counts the number of occurrences where that value is at the end of
    a sequence.
    """
    endings = defaultdict(int)
    
    for sequence in sequences:
        endings[sequence[-1]] += 1
    
    return endings


class MFCTagger:
    missing = FakeState(name="<MISSING>")
    def __init__(self, table):
        self.table = defaultdict(lambda: MFCTagger.missing)
        self.table.update({word: FakeState(name=tag) for word, tag in table.items()})
    def viterbi(self, seq):
        return 0., list(enumerate(["<start>"] + [self.table[w] for w in seq] + ["<end>"]))


data = Dataset("tags_universal.txt", "brown_universal.txt", train_test_split=0.8)

# Calculate emission counts
sequences_t = tuple([tag for (word,tag) in data.training_set.stream()])
sequences_w = tuple([word for (word,tag) in data.training_set.stream()])
emission_counts = pair_counts(sequences_t, sequences_w)

# Calculate word counts
word_counts = pair_counts(sequences_w, sequences_t)

# Create a Most Frequent Class tagger instance
mfc_table = dict(map(lambda word:(word,max(word_counts[word],key=word_counts[word].get)),data.training_set.vocab))
mfc_model = MFCTagger(mfc_table)

# Evaluate the accuracy of the tagger on the training and test corp
mfc_training_acc = accuracy(data.training_set.X, data.training_set.Y, mfc_model)
print("training accuracy mfc_model: {:.2f}%".format(100 * mfc_training_acc))
mfc_testing_acc = accuracy(data.testing_set.X, data.testing_set.Y, mfc_model)
print("testing accuracy mfc_model: {:.2f}%".format(100 * mfc_testing_acc))


# Calculate unigram_counts with a list of tag sequences from the training set
tag_unigrams = unigram_counts(data.training_set.Y)
# Calculate bigram_counts with a list of tag sequences from the training set
tag_bigrams = bigram_counts(data.training_set.Y)
# Calculate the count of each tag starting a sequence
tag_starts = starting_counts(data.training_set.Y)
# Calculate the count of each tag ending a sequence
tag_ends = ending_counts(data.training_set.Y)

basic_model = HiddenMarkovModel(name="base-hmm-tagger")

# Create states with emission probability distributions P(word | tag) and add to the model
tag_states = {}

for tag in data.training_set.tagset:
    tag_emissions = DiscreteDistribution({word:emission_counts[tag][word]/tag_unigrams[tag] for word in emission_counts[tag]})
    tag_states[tag] = State(tag_emissions, name=tag)
    basic_model.add_state(tag_states[tag])

# Add edges between states for the observed transition frequencies P(tag_i | tag_i-1)
for tag in data.training_set.tagset:
    basic_model.add_transition(basic_model.start, tag_states[tag], tag_starts[tag]/tag_unigrams[tag])
    for tag1 in data.training_set.tagset:
        basic_model.add_transition(tag_states[tag], tag_states[tag1], tag_bigrams[(tag,tag1)]/tag_unigrams[tag])
    basic_model.add_transition(tag_states[tag], basic_model.end, tag_ends[tag]/tag_unigrams[tag])

# finalize the model
basic_model.bake()

# Evaluate the accuracy of HMM tagger on the training and test corp
hmm_training_acc = accuracy(data.training_set.X, data.training_set.Y, basic_model)
print("training accuracy basic hmm model: {:.2f}%".format(100 * hmm_training_acc))
hmm_testing_acc = accuracy(data.testing_set.X, data.testing_set.Y, basic_model)
print("testing accuracy basic hmm model: {:.2f}%".format(100 * hmm_testing_acc))
