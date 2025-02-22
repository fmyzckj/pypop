import numpy as np  # engine for numerical computing

from pypop7.benchmarks.base_functions import BaseFunction


def cross_entropy_loss_lr(w, x, y):
    """"Cross-Entropy Loss Function of Logistic Regression (with binary labels/classes {0, 1}).

        Note that this loss function is convex.

        https://web.stanford.edu/~jurafsky/slp3/5.pdf
        https://developer.ibm.com/articles/implementing-logistic-regression-from-scratch-in-python/
        https://jermwatt.github.io/machine_learning_refined/notes/6_Linear_twoclass_classification/6_2_Cross_entropy.html
    ""
    loss = np.empty(len(y))
    for i in range(len(y)):
        p = 1.0/(1.0 + np.exp(-(w[0] + np.dot(x[i], w[1:]))))
        loss[i] = -y[i]*np.log(p) - (1.0 - y[i])*np.log(1.0 - p))
    return np.mean(loss)


class CrossEntropyLossLR(BaseFunction):
    def __call__(self, w, x, y):
        return cross_entropy_loss_lr(w, x, y)
