# -*- coding: utf-8 -*-
from model_ori import CGAN
from utils import input_setup

import numpy as np
import tensorflow as tf
from tensorflow.python.keras import backend as K

import pprint
import os
import time

# for i in range(5):
#       time.sleep(1)
#       print(5-i)

flags = tf.app.flags
flags.DEFINE_integer("epoch", 30, "Number of epoch [10]")
flags.DEFINE_integer("batch_size", 48, "The size of batch images [128]") #32
flags.DEFINE_integer("image_size", 120, "The size of image to use [33]")  #132
flags.DEFINE_integer("label_size", 120, "The size of label to produce [21]")
flags.DEFINE_float("learning_rate", 1e-4, "The learning rate of gradient descent algorithm [1e-4]")
flags.DEFINE_integer("c_dim", 1, "Dimension of image color. [1]")
flags.DEFINE_integer("scale", 3, "The size of scale factor for preprocessing input image [3]")
flags.DEFINE_integer("stride", 14, "The size of stride to apply input image [14]")
flags.DEFINE_string("checkpoint_dir", "checkpoint_20", "Name of checkpoint directory [checkpoint]")
flags.DEFINE_string("sample_dir", "sample", "Name of sample directory [sample]")
flags.DEFINE_string("summary_dir", "log", "Name of log directory [log]")
flags.DEFINE_boolean("is_train", True, "True for training, False for testing [True]")
FLAGS = flags.FLAGS

pp = pprint.PrettyPrinter()

def main(_):
  os.environ['CUDA_VISIBLE_DEVICES']='0'
  log_device_placement=True
  allow_soft_placement=True
  tf.ConfigProto(log_device_placement=True,allow_soft_placement=True)
  config = tf.ConfigProto()
  config.gpu_options.per_process_gpu_memory_fraction = 0.99
  config.gpu_options.allow_growth = True
  K.set_session(tf.Session(graph=tf.get_default_graph(),config=config))
  
  pp.pprint(flags.FLAGS.__flags)

  if not os.path.exists(FLAGS.checkpoint_dir):
    os.makedirs(FLAGS.checkpoint_dir)
  if not os.path.exists(FLAGS.sample_dir):
    os.makedirs(FLAGS.sample_dir)

  with tf.Session() as sess:
    srcnn = CGAN(sess, 
                  image_size=FLAGS.image_size, 
                  label_size=FLAGS.label_size, 
                  batch_size=FLAGS.batch_size,
                  c_dim=FLAGS.c_dim, 
                  checkpoint_dir=FLAGS.checkpoint_dir,
                  sample_dir=FLAGS.sample_dir)
    
    
    srcnn.train(FLAGS)
    
if __name__ == '__main__':
  tf.app.run()
