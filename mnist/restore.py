# encoding=utf-8
import tensorflow as tf
from PIL import Image,ImageFilter
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

def imageprepare(argv): # 该函数读一张图片，处理后返回一个数组，进到网络中预测
    """
    This function returns the pixel values.
    The imput is a png file location.
    """
    im = Image.open(argv).convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (28, 28), (255))  # creates white canvas of 28x28 pixels

    if width > height:  # check which dimension is bigger
        # Width is bigger. Width becomes 20 pixels.
        nheight = int(round((20.0 / width * height), 0))  # resize height according to ratio width
        if nheight == 0:  # rare case but minimum is 1 pixel
            nheight = 1
            # resize and sharpen
        img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight) / 2), 0))  # caculate horizontal pozition
        newImage.paste(img, (4, wtop))  # paste resized image on white canvas
    else:
        # Height is bigger. Heigth becomes 20 pixels.
        nwidth = int(round((20.0 / height * width), 0))  # resize width according to ratio height
        if (nwidth == 0):  # rare case but minimum is 1 pixel
            nwidth = 1
            # resize and sharpen
        img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth) / 2), 0))  # caculate vertical pozition
        newImage.paste(img, (wleft, 4))  # paste resized image on white canvas

    # newImage.save("sample.png")

    tv = list(newImage.getdata())  # get pixel values

    # normalize pixels to 0 and 1. 0 is pure white, 1 is pure black.
    tva = [(255 - x) * 1.0 / 255.0 for x in tv]
    return tva

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

myGraph = tf.Graph()
with myGraph.as_default():  # 重构相同的网络
    with tf.name_scope('inputsAndLabels'):
        x_raw = tf.placeholder(tf.float32, shape=[None, 784])
        y = tf.placeholder(tf.float32, shape=[None, 10])

    with tf.name_scope('hidden1'):
        x = tf.reshape(x_raw, shape=[-1,28,28,1])
        W_conv1 = weight_variable([5,5,1,32])
        b_conv1 = bias_variable([32])
        l_conv1 = tf.nn.relu(tf.nn.conv2d(x,W_conv1, strides=[1,1,1,1],padding='SAME') + b_conv1)
        l_pool1 = tf.nn.max_pool(l_conv1, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

    with tf.name_scope('hidden2'):
        W_conv2 = weight_variable([5,5,32,64])
        b_conv2 = bias_variable([64])
        l_conv2 = tf.nn.relu(tf.nn.conv2d(l_pool1, W_conv2, strides=[1,1,1,1], padding='SAME')+b_conv2)
        l_pool2 = tf.nn.max_pool(l_conv2, ksize=[1,2,2,1],strides=[1,2,2,1], padding='SAME')

    with tf.name_scope('fc1'):
        W_fc1 = weight_variable([64*7*7, 1024])
        b_fc1 = bias_variable([1024])
        l_pool2_flat = tf.reshape(l_pool2, [-1, 64*7*7])
        l_fc1 = tf.nn.relu(tf.matmul(l_pool2_flat, W_fc1) + b_fc1)
        keep_prob = tf.placeholder(tf.float32)
        l_fc1_drop = tf.nn.dropout(l_fc1, keep_prob)

    with tf.name_scope('fc2'):
        W_fc2 = weight_variable([1024, 10])
        b_fc2 = bias_variable([10])
        y_conv = tf.matmul(l_fc1_drop, W_fc2) + b_fc2

with tf.Session(graph=myGraph) as sess:
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()

    saver.restore(sess,'./model/mnistmodel-1') # restore参数

    array = imageprepare('./7.png') # 读一张包含数字的图片

    prediction = tf.argmax(y_conv, 1) # 预测
    prediction = prediction.eval(feed_dict={x_raw:[array],keep_prob:1.0},session=sess)
    print('The digits in this image is:%d'%prediction[0])