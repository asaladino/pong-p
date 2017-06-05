import tensorflow as tf
# import cv2


# https://github.com/llSourcell/pong_neural_network_live/blob/master/RL.py

class NeuralNetworkController(object):
    def __init__(self, paddle):
        self.paddle = paddle
        self.speed = 2

        # hyper params
        self.ACTIONS = 3  # up,down, stay
        # define our learning rate
        self.GAMMA = 0.99
        # for updating our gradient or training over time
        self.INITIAL_EPSILON = 1.0
        self.FINAL_EPSILON = 0.05
        # how many frames to anneal epsilon
        self.EXPLORE = 500000
        self.OBSERVE = 50000
        # store our experiences, the size of it
        self.REPLAY_MEMORY = 500000
        # batch size to train on
        self.BATCH = 100

        self.create_graph()

    def did_paddle_move(self, event, ball):
        if event is not None:
            return
        if self.paddle.rect.center[1] < ball.rect.center[1]:
            self.paddle.direction = 1
        else:
            self.paddle.direction = -1

    def learn(self, data, score):
        pass

    # create tensorflow graph
    def create_graph(self):

        # first convolutional layer. bias vector
        # creates an empty tensor with all elements set to zero with a shape
        w_conv1 = tf.Variable(tf.zeros([8, 8, 4, 32]))
        b_conv1 = tf.Variable(tf.zeros([32]))

        w_conv2 = tf.Variable(tf.zeros([4, 4, 32, 64]))
        b_conv2 = tf.Variable(tf.zeros([64]))

        w_conv3 = tf.Variable(tf.zeros([3, 3, 64, 64]))
        b_conv3 = tf.Variable(tf.zeros([64]))

        w_fc4 = tf.Variable(tf.zeros([3136, 784]))
        b_fc4 = tf.Variable(tf.zeros([784]))

        w_fc5 = tf.Variable(tf.zeros([784, self.ACTIONS]))
        b_fc5 = tf.Variable(tf.zeros([self.ACTIONS]))

        # input for pixel data
        s = tf.placeholder("float", [None, 84, 84, 4])

        # Computes rectified linear unit activation function on  a 2-D convolution given 4-D input and filter tensors.
        conv1 = tf.nn.relu(tf.nn.conv2d(s, w_conv1, strides=[1, 4, 4, 1], padding="VALID") + b_conv1)

        conv2 = tf.nn.relu(tf.nn.conv2d(conv1, w_conv2, strides=[1, 2, 2, 1], padding="VALID") + b_conv2)

        conv3 = tf.nn.relu(tf.nn.conv2d(conv2, w_conv3, strides=[1, 1, 1, 1], padding="VALID") + b_conv3)

        conv3_flat = tf.reshape(conv3, [-1, 3136])

        fc4 = tf.nn.relu(tf.matmul(conv3_flat, w_fc4) + b_fc4)

        fc5 = tf.matmul(fc4, w_fc5) + b_fc5

        return s, fc5
