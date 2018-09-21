import numpy as np

def add_bias(array, axis=0):
    pad = ((0, 1), (0, 0)) if axis == 0 else ((0, 0), (0, 1))
    return np.pad(array, pad, 'constant', constant_values=1e-3)

def remove_bias(array, axis=0):
    return array[:-1] if axis == 0 else array[:, :-1]

def one_of_k(pos, length):
    array = np.zeros((length))
    array[pos] = 1
    return array

def tanh_prime(x):
    return 1 - np.square(np.tanh(x))

def psh(arrays):
    for a in arrays: print (np.shape(a))

def expand(array):
    return np.expand_dims(array, axis=1)
