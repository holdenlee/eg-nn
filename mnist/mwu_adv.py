#DONT USE

import tensorflow as tf
from functools import *
import itertools
import inspect
from datetime import datetime
import re
import os
import os.path
import time
import numpy as np
#from six.moves import xrange
from cleverhans.utils_mnist import data_mnist
from cleverhans.attacks import fgsm

from utils import *
from tf_utils.tf_vars import *
from tf_utils.tf_utils import *
from .adv_model import *
from mwu.mwu import *

def mnist_mwu_model_adv(adv_f, f):
    m = f()
    #THIS MUST BE OUTSIDE otherwise 2 copies will be made!
    def model(x,y):
        predictions= m(x)
        loss = cross_entropy(y, predictions, 0.00001)
        #loss = tf.Print(loss, [y, predictions, logt(predictions,0.00001), y*logt(predictions,0.0001)], 'actual and true:', summarize=10)
        #loss = tf.Print(loss, [y, predictions], 'actual and true:', summarize=10)
        loss = tf.identity(loss, name="loss")
        acc = accuracy2(y, predictions)
        tf.add_to_collection('losses', loss)
        return {'loss': loss, 'inference': predictions, 'accuracy': acc}
        #NEED TO COMMUNICATE Ws and bs.
        #Use collections instead.
    x = tf.placeholder(tf.float32, shape=(None, 28, 28, 1))
    y = tf.placeholder(tf.float32, shape=(None, 10))
    adv_model, epsilon = make_adversarial_model(model, adv_f, x, y)
    ph_dict = {'x': x, 'y': y, 'epsilon': epsilon}
    return adv_model, ph_dict, epsilon
