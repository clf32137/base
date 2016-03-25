if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath('__file__'))))

sys.dont_write_bytecode = True

import sys, os
from numpy import *
from matplotlib.pyplot import *

overnight = True

matplotlib.rcParams['savefig.dpi'] = 100

from msushkov_rnnlm import RNNLM

################################
#Gradient check on toy data for speed.
################################
random.seed(10)
wv_dummy = random.randn(10,50)
model = RNNLM(L0 = wv_dummy, U0 = wv_dummy, alpha=0.005, rseed=10, bptt=4)
model.grad_check(array([1,2,3]), array([2,3,4]))


################################
#Prepare vocabulary
################################

from data_utils import utils as du
import pandas as pd

# Load the vocabulary
vocab = pd.read_table("../data/lm/vocab.ptb.txt", header=None, sep="\s+",
                     index_col=0, names=['count', 'freq'], )

# Choose how many top words to keep
if overnight:
    vocabsize = 5000
else:
    vocabsize = 2000

num_to_word = dict(enumerate(vocab.index[:vocabsize]))
word_to_num = du.invert_dict(num_to_word)
##
# Below needed for 'adj_loss': DO NOT CHANGE
fraction_lost = float(sum([vocab['count'][word] for word in vocab.index
                           if (not word in word_to_num) 
                               and (not word == "UUUNKKK")]))
fraction_lost /= sum([vocab['count'][word] for word in vocab.index
                      if (not word == "UUUNKKK")])
print "Retained %d words from %d (%.02f%% of all tokens)" % (vocabsize, len(vocab),
                                                             100*(1-fraction_lost))

################################
#Load datasets
################################

# Load the training set
docs = du.load_dataset('../data/lm/ptb-train.txt')
S_train = du.docs_to_indices(docs, word_to_num)
X_train, Y_train = du.seqs_to_lmXY(S_train)

# Load the dev set (for tuning hyperparameters)
docs = du.load_dataset('../data/lm/ptb-dev.txt')
S_dev = du.docs_to_indices(docs, word_to_num)
X_dev, Y_dev = du.seqs_to_lmXY(S_dev)

# Load the test set (final evaluation only)
docs = du.load_dataset('../data/lm/ptb-test.txt')
S_test = du.docs_to_indices(docs, word_to_num)
X_test, Y_test = du.seqs_to_lmXY(S_test)

# Display some sample data
print " ".join(d[0] for d in docs[7])
print S_test[7]
#Do these indices correspond to actual sentences?
print [num_to_word[i] for i in S_test[5]]


################################
#Initialize the model
################################
if overnight:
    hdim = 150
else:
    hdim = 100 # dimension of hidden layer = dimension of word vectors


random.seed(10)
L0 = zeros((vocabsize, hdim)) # replace with random init, 
                              # or do in RNNLM.__init__()

if overnight:
    model = RNNLM(L0, U0 = L0, alpha=0.1, rseed=10, bptt=7)
else:
    model = RNNLM(L0, U0 = L0, alpha=0.1, rseed=10, bptt=3)


# Gradient check is going to take a *long* time here
# since it's quadratic-time in the number of parameters.
# run at your own risk...
#model.grad_check(array([1,2,3]), array([2,3,4])) #spoiler - it passed.
#print "long grad check done"

################################
#Train the model.
################################
ntrain = len(Y_train)
X = X_train[:ntrain]
Y = Y_train[:ntrain]

k = 5
indices = range(ntrain)

# A random schedule of N/k minibatches of size k, sampled with replacement from the training set.
def idxiter_batches():
    num_batches = ntrain / k
    for i in xrange(num_batches):
        yield random.choice(indices, k)

print "##########################"
model_output = model.train_sgd(X=X, y=Y, idxiter=idxiter_batches(), printevery=5000, costevery=100000)
#Took 1810.33 secs on desktop. For msushkov, it had taken 3697.97 secs while for dengfy it took 15000 secs or 5 hours!
print "##########################"

## DO NOT CHANGE THIS CELL ##
# Report your numbers, after computing dev_loss above.

dev_loss = model.compute_mean_loss(X_dev, Y_dev)
#Now lets exclude the loss for Unknowns.
def adjust_loss(loss, funk):
    return (loss + funk * log(funk))/(1 - funk)

print "Unadjusted: %.03f" % exp(dev_loss)
print "Adjusted for missing vocab: %.03f" % exp(adjust_loss(dev_loss, fraction_lost))


##
# Save to .npy files; should only be a few MB total
assert(min(model.sparams.L.shape) <= 100) # don't be too big
assert(max(model.sparams.L.shape) <= 5000) # don't be too big
save("rnnlm.L.npy", model.sparams.L)
save("rnnlm.U.npy", model.params.U)
save("rnnlm.H.npy", model.params.H)

################################
#Now lets generate some sentences.
################################
def seq_to_words(seq):
    return [num_to_word[s] for s in seq]

seq, J = model.generate_sequence(word_to_num["<s>"],
                                 word_to_num["</s>"],
                                 maxlen=100)
print J
# print seq
print " ".join(seq_to_words(seq))


# Replace UUUNKKK with a random unigram,
# drawn from vocab that we skipped
from nn.math import MultinomialSampler, multinomial_sample

def fill_unknowns(words):
    #### YOUR CODE HERE ####
    word_list = list(vocab.index)
    word_freqs = vocab.freq
    words_and_freqs = zip(word_list, word_freqs)
    new_words = []
    new_freqs = []
    for (w, f) in words_and_freqs:
        if w not in word_to_num:
            new_words.append(w)
            new_freqs.append(f)
    
    # normalize new_freqs
    s = sum(new_freqs)
    new_freqs = [x / float(s) for x in new_freqs]
    
    ret = []
    
    for word in words:
        curr = None
        if word == 'UUUNKKK':
            curr = random.choice(new_words, p = new_freqs)
        else:
            curr = word
        ret.append(curr)
    #### END YOUR CODE ####
    return ret
    
print " ".join(fill_unknowns(seq_to_words(seq)))


