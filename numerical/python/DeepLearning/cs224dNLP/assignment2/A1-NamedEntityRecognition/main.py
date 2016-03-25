if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath('__file__'))))

sys.dont_write_bytecode = True


import sys, os
from numpy import *
from matplotlib.pyplot import *

matplotlib.rcParams['savefig.dpi'] = 100


from misc import random_weight_matrix
random.seed(10)
print random_weight_matrix(3,5)


import data_utils.utils as du
import data_utils.ner as ner


# Load the starter word vectors
wv, word_to_num, num_to_word = ner.load_wv('data/ner/vocab.txt',
                                           'data/ner/wordVectors.txt')
tagnames = ["O", "LOC", "MISC", "ORG", "PER"]
num_to_tag = dict(enumerate(tagnames))
tag_to_num = du.invert_dict(num_to_tag)


# Set window size
windowsize = 3

# Load the training set
docs = du.load_dataset('data/ner/train')
X_train, y_train = du.docs_to_windows(docs, word_to_num, tag_to_num,
                                      wsize=windowsize)

# Load the dev set (for tuning hyperparameters)
docs = du.load_dataset('data/ner/dev')
X_dev, y_dev = du.docs_to_windows(docs, word_to_num, tag_to_num,
                                  wsize=windowsize)

# Load the test set (dummy labels only)
docs = du.load_dataset('data/ner/test.masked')
X_test, y_test = du.docs_to_windows(docs, word_to_num, tag_to_num,
                                    wsize=windowsize)



from softmax_example import SoftmaxRegression
sr = SoftmaxRegression(wv=zeros((10,100)), dims=(100,5))

##
# Automatic gradient checker!
# this checks anything you add to self.grads or self.sgrads
# using the method of Assignment 1
sr.grad_check(x=5, y=4)


#from nerwindow import WindowMLP
from nerwindow_msushkov import WindowMLP
clf = WindowMLP(wv, windowsize=windowsize, dims=[None, 100, 5],
                reg=0.001, alpha=0.01)
clf.grad_check(X_train[0], y_train[0]) # gradient check on single point


nepoch = 5
N = nepoch * len(y_train)
k = 5 # minibatch size

random.seed(10)
########################
## training schedules
########################
indices = range(len(y_train))

# An "epoch" schedule that just iterates through the training set, in order, nepoch times
idxiter_epoch = nepoch * indices

# A random schedule of N examples sampled with replacement from the training set.
idxiter_N = random.choice(indices, N)

# A random schedule of N/k minibatches of size k, sampled with replacement from the training set.
def idxiter_batches():
    num_batches = N / k
    for i in xrange(num_batches):
        yield random.choice(indices, k)


from nerwindow import full_report, eval_performance

# Tune training schedule
#schedules = [idxiter_epoch, idxiter_N, idxiter_batches()]
schedules = [idxiter_epoch]

for i, train_sched in enumerate(schedules):
    print "===== Training schedule %d:" % i
    clf = WindowMLP(wv, windowsize=3, dims=[None, 100, 5], reg=0.001, alpha=0.01)
    clf.train_sgd(X=X_train, y=y_train, idxiter=train_sched, printevery=250000, costevery=25000)
    yp = clf.predict(X_dev)
    full_report(y_dev, yp, tagnames)
    eval_performance(y_dev, yp, tagnames)


