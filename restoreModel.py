#!/home/chaochao/anaconda2/bin
# -*- coding: utf-8 -*-
# Created by jiachaochao on 17-9-1 上午10:07
import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
from PIL import Image, ImageFilter


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

# mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
# batch = mnist.train.next_batch(50)
# x_image = np.array(batch[0][0:1, :], dtype=np.float32)
# y_label = np.array(batch[1][0:1, :], dtype=np.float32)
x_image = imageprepare("./eight.png")
print(np.array([1 if n > 0 else 0 for n in x_image]).reshape([28, 28]))
x_image = tf.reshape(x_image, [-1, 28, 28, 1])


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

sess = tf.Session()

saver = tf.train.import_meta_graph('./model/model.ckpt.meta')
saver.restore(sess, tf.train.latest_checkpoint('./model'))

graph = tf.get_default_graph()
x = graph.get_tensor_by_name("input:0")

W_conv1 = graph.get_tensor_by_name("W_conv1:0")
b_conv1 = graph.get_tensor_by_name("b_conv1:0")


h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = graph.get_tensor_by_name("W_conv2:0")
b_conv2 = graph.get_tensor_by_name("b_conv2:0")

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = graph.get_tensor_by_name("W_fc1:0")
b_fc1 = graph.get_tensor_by_name("b_fc1:0")

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)


W_fc2 = graph.get_tensor_by_name("W_fc2:0")
b_fc2 = graph.get_tensor_by_name("b_fc2:0")

y_conv = tf.add(tf.matmul(h_fc1, W_fc2), b_fc2, name="conv")

# print(x_image)
print(np.argmax(sess.run(y_conv)))
print("DONE")