from keras.src.datasets import mnist
import numpy as np
from sps.config import Config

def get_mnist_data():
    """
    Returns desired set of images and labels from MNIST dataset.
    Output based on module sps/Config.
    """

    # Raw dataset size:
    # train_data = 3-D matrix [60.000 x 28 x 28] of images (used to train the model)
    # train_label = 1-D array [60.000] of labels (used to train the model)
    # test_data = 3-D matrix [10.000 x 28 x 28] of images (used to test accuracy)
    # test_label = 1-D array [10.000] of labels (used to test accuracy)
    (train_data, train_label), (test_data, test_label) = mnist.load_data()

    # Slicing images and labels of dataset according to Config settings
    train_data = train_data[:Config.TRAIN_SIZE]
    train_label = train_label[:Config.TRAIN_SIZE]
    test_data = test_data[:Config.TEST_SIZE]
    test_label = test_label[:Config.TEST_SIZE]

    # Converting pixel data type to uint8 
    train_q = train_data.astype(np.uint8)
    test_q = test_data.astype(np.uint8)

    # Optionally inverting white-black encoding according to Config settings
    if Config.INVERT:
        train_q = 255 - train_q
        test_q = 255 - test_q

    return train_q, train_label, test_q, test_label