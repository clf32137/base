if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath('__file__'))))

sys.dont_write_bytecode = True


import os
import nltk
import operator
import numpy
from numpy import *
import itertools
import re

from data_utils import utils as du
from msushkov_rnnlm import RNNLM

overnight = True

################################
#Read in the files and construct vocabulary.
################################
rootdir = "..\\data\\mydata"

a = []

word_vocab = {}

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        f = open(filepath)

        for i in f:
            a.append(i)
            #Remove non ascii characters
            txt = ''.join(l for l in i if ord(l)<128)
            tokens = nltk.word_tokenize(txt)
            for j in tokens:
                char = j
                #if j.isdigit():
                #    char = "DGGGGG"
                if char in word_vocab:
                    word_vocab[char] += 1
                else:
                    word_vocab[char] = 1


word_to_num = {}
j = 0
dropped = 0
for i in word_vocab.keys():
    if word_vocab[i] < 5:
        dropped += word_vocab[i]
    else:
        if i not in word_to_num:
            word_to_num[i] = j
            j = j + 1
mx = j

print "dropped: " +  str(float(dropped)/sum(word_vocab.values()))

num_to_word = du.invert_dict(word_to_num)
vocabsize = len(num_to_word) + 2 #One for line ending and one for unknown


################################
#Prepare data for training.
################################

X_train = []
Y_train = []

for i in a:
    txt = ''.join(l for l in i if ord(l)<128)
    temparr = []        
    for j in nltk.word_tokenize(txt):
        if j in word_to_num:
            temparr.append(word_to_num[j])
        else:
            temparr.append(mx+1) #mx is period and mx+1 is unknown
    if temparr:
        temparr_y = temparr[1:]
        temparr_y.append(mx)
        temparr = numpy.array(temparr)
        temparr_y = numpy.array(temparr_y)
        X_train.append(temparr)
        Y_train.append(temparr_y) #Add the stop word.


X_train = numpy.array(X_train)
Y_train = numpy.array(Y_train)


################################
#Initialize the model
################################
if overnight:
    hdim = 150
else:
    hdim = 100 # dimension of hidden layer = dimension of word vectors


L0 = zeros((vocabsize, hdim)) # replace with random init, 
                              # or do in RNNLM.__init__()

if overnight:
    model = RNNLM(L0, U0 = L0, alpha=0.1, rseed=10, bptt=15)
else:
    model = RNNLM(L0, U0 = L0, alpha=0.1, rseed=10, bptt=3)


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

################################
#Train the model.
################################
print "##########################"
model_output = model.train_sgd(X = X, y = Y, idxiter = idxiter_batches(), printevery = 5000, costevery = 100000)
#Took 18711 secs or 5 hours on desktop.
print "##########################"


################################
#Generate a random sequence.
################################
num_to_word[max(num_to_word.keys()) + 1] = "</s>"
num_to_word[max(num_to_word.keys()) + 1] = "UNKKK"


def seq_to_words(seq):
    return [num_to_word[s] for s in seq]

seq, J = model.generate_sequence(word_to_num[","],
                                 word_to_num["cliffs"],
                                 maxlen=40)
print J
# print seq
print " ".join(seq_to_words(seq))




