import tensorflow as tf

import pygame
import numpy as np  # math
import random  # random
import cv2
from collections import deque  # queue data structure. fast appends. and pops. replay memory


# https://github.com/llSourcell/pong_neural_network_live/blob/master/RL.py

class NeuralNetworkController(object):
    def __init__(self, paddle):
        self.paddle = paddle

        # define hyper parameters
        self.ACTIONS = 3  # up, down, stay
        self.GAMMA = 0.99  # define our learning rate
        self.INITIAL_EPSILON = 1.0  # for updating our gradient or training over time
        self.FINAL_EPSILON = 0.05  # final value of epsilon
        self.OBSERVE = 1000  # time steps to observe before training
        self.EXPLORE = 1000  # frames over which to anneal epsilon
        self.REPLAY_MEMORY = 250000  # store our experiences, the size of it (test, how much your ram can fit!)
        self.BATCH = 32  # batch size to train on
        self.T_MAX = 1000000  # number of training iterations
        self.S_MAX = 100  # the score our agent shall reach

        self.input = None
        self.output = None
        # create session
        self.sess = tf.InteractiveSession()

        self.arg_max = None
        self.gt = None
        self.train_step = None

        # create a queue for experience replay to store policies
        self.deque = deque()
        # action do nothing
        self.arg_max_t = np.zeros([self.ACTIONS])
        self.arg_max_t[0] = 1

        self.inp_t = None
        # saver
        self.saver = None
        self.stats_log = open("logs/stats.log", "w")

        # total game score
        self.score = 0

        self.t = 0
        self.epsilon = self.INITIAL_EPSILON

    def create_graph(self):
        """
        create tensorflow graph
        input layer and output layer by creating graph
        :return:
        """

        # network weights
        weighted_conv1 = tf.Variable(tf.truncated_normal([8, 8, 4, 32], stddev=0.01))
        bias_conv1 = tf.Variable(tf.constant(0.01, shape=[32]))

        weighted_conv2 = tf.Variable(tf.truncated_normal([4, 4, 32, 64], stddev=0.01))
        bias_conv2 = tf.Variable(tf.constant(0.01, shape=[64]))

        weighted_conv3 = tf.Variable(tf.truncated_normal([3, 3, 64, 64], stddev=0.01))
        bias_conv3 = tf.Variable(tf.constant(0.01, shape=[64]))

        weighted_fully_connected4 = tf.Variable(tf.truncated_normal([1600, 512], stddev=0.01))
        bias_fully_connected4 = tf.Variable(tf.constant(0.01, shape=[512]))

        weighted_fully_connected5 = tf.Variable(tf.truncated_normal([512, self.ACTIONS], stddev=0.01))
        bias_fully_connected5 = tf.Variable(tf.constant(0.01, shape=[self.ACTIONS]))

        # input layer for pixel data
        self.input = tf.placeholder("float", [None, 80, 80, 4])

        # Computes rectified linear unit activation fucntion (relu) on a 2-D convolution
        #  given 4-D input and filter tensors
        conv1 = tf.nn.relu(tf.nn.conv2d(self.input, weighted_conv1, strides=[1, 4, 4, 1], padding="SAME") + bias_conv1)
        pool1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

        conv2 = tf.nn.relu(tf.nn.conv2d(pool1, weighted_conv2, strides=[1, 2, 2, 1], padding="SAME") + bias_conv2)
        conv3 = tf.nn.relu(tf.nn.conv2d(conv2, weighted_conv3, strides=[1, 1, 1, 1], padding="SAME") + bias_conv3)

        conv3_flat = tf.reshape(conv3, [-1, 1600])
        fully_connected4 = tf.nn.relu(tf.matmul(conv3_flat, weighted_fully_connected4) + bias_fully_connected4)
        fully_connected5 = tf.matmul(fully_connected4, weighted_fully_connected5) + bias_fully_connected5

        self.output = fully_connected5

    def did_paddle_move(self, event, ball):
        pass

    def did_paddle_move_alone(self, ball):
        if self.argmax_t is not None:
            if self.argmax_t[2] == 1:
                self.paddle.direction = 1
            elif self.argmax_t[1] == 1:
                self.paddle.direction = -1

    def train_graph(self, frame):
        """
        deep q network. feed in pixel data to graph session
        train our graph on input and output with session variables
        :return: None
        """
        # to calculate the arg_max, we multiply the predicted output with a vector with one value 1 and rest as 0
        self.arg_max = tf.placeholder("float", [None, self.ACTIONS])
        self.gt = tf.placeholder("float", [None])  # ground truth

        # action
        action = tf.reduce_sum(tf.multiply(self.output, self.arg_max), axis=1)
        # cost function we will reduce through backpropagation
        cost = tf.reduce_mean(tf.square(self.gt - action))

        # optimization function to reduce our minimize our cost function
        self.train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)

        # initial frame
        # frame = self.pong.GetFrame(self.arg_max_t)[1]
        # convert rgb to gray scale for processing
        frame = cv2.cvtColor(cv2.resize(frame, (80, 80)), cv2.COLOR_BGR2GRAY)
        # binary colors, black or white
        frame = cv2.threshold(frame, 1, 255, cv2.THRESH_BINARY)[1]
        # stack frames, that is our input tensor
        self.inp_t = np.stack((frame, frame, frame, frame), axis=2)

        self.saver = tf.train.Saver()
        self.sess.run(tf.global_variables_initializer())
        checkpoint = tf.train.get_checkpoint_state("saved_networks")
        if checkpoint and checkpoint.model_checkpoint_path:
            self.saver.restore(self.sess, checkpoint.model_checkpoint_path)
            print("Successfully loaded:", checkpoint.model_checkpoint_path)
        else:
            print("Could not find saved networks")

    def learn(self, frame, reward_t):
        """
        :param image_data:
        :param reward_t: reward tensor if score is positive
        """
        # output tensor
        out_t = self.output.eval(feed_dict={self.input: [self.inp_t]})[0]
        # arg_max function
        arg_max_t = np.zeros([self.ACTIONS])

        if random.random() <= self.epsilon or self.t <= self.OBSERVE:
            max_index = random.randrange(self.ACTIONS)
            r_dec = "True"  # optional for logging, True if randomly decided
        else:
            max_index = np.argmax(out_t)
            r_dec = "False"
        arg_max_t[max_index] = 1

        # scale down epsilon
        if self.epsilon > self.FINAL_EPSILON and self.t > self.OBSERVE:
            self.epsilon -= (self.INITIAL_EPSILON - self.FINAL_EPSILON) / self.EXPLORE

        # reward tensor if score is positive
        # reward_t, frame = self.pong.GetFrame(arg_max_t)

        # get frame pixel data
        frame = cv2.cvtColor(cv2.resize(frame, (80, 80)), cv2.COLOR_BGR2GRAY)
        ret, frame = cv2.threshold(frame, 1, 255, cv2.THRESH_BINARY)
        frame = np.reshape(frame, (80, 80, 1))

        # new input tensor
        inp_t1 = np.append(frame, self.inp_t[:, :, 0:3], axis=2)

        # add our input tensor, arg_max tensor, reward and updated tensor to stack of experiences
        self.deque.append((self.inp_t, arg_max_t, reward_t, inp_t1))

        # if we run out of replay memory, make room
        if len(self.deque) > self.REPLAY_MEMORY:
            self.deque.popleft()

        # training iteration
        if self.t > self.OBSERVE:
            # get values from our replay memory
            mini_batch = random.sample(self.deque, self.BATCH)

            inp_batch = [d[0] for d in mini_batch]
            arg_max_batch = [d[1] for d in mini_batch]
            reward_batch = [d[2] for d in mini_batch]
            inp_t1_batch = [d[3] for d in mini_batch]

            gt_batch = []
            out_batch = self.output.eval(feed_dict={self.input: inp_t1_batch})

            # add values to our batch
            for i in range(0, len(mini_batch)):
                gt_batch.append(reward_batch[i] + self.GAMMA * np.max(out_batch[i]))

            # train on that
            self.train_step.run(feed_dict={
                self.gt: gt_batch,
                self.arg_max: arg_max_batch,
                self.input: inp_batch
            })

        # update our input tensor the next frame
        self.inp_t = inp_t1
        self.t += 1

        # print out where we are
        if self.t <= self.OBSERVE:
            state = "observe"
        elif self.OBSERVE < self.t < self.OBSERVE + self.EXPLORE:
            state = "explore"
        else:
            state = "train"

        self.score += reward_t

        stats = "TIMESTEP {:7} | SCORE: {: 5} | STATE {:7} | EPSILON {:6.4f} |" \
                " ACTION {} | R_DEC {:5} | REWARD {:2d} | Q_MAX {: e}".format(self.t, self.score, state,
                                                                              self.epsilon,
                                                                              max_index, r_dec, reward_t,
                                                                              np.max(out_t))
        print(stats)
        # write into file
        self.stats_log.write(stats + "\n")

        # save our session every 10000 steps
        if self.t % 10000 == 0:
            self.saver.save(self.sess, "saved_networks/pong_game-dqn.chk", global_step=self.t)
            print("Session saved.")

    def resign(self):
        self.sess.close()
