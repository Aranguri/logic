import numpy as np
from logic_task import Task
from utils import *

learning_rate = 1e-2
task = Task(batch_size=3)
#Cada elemento de size representa la cantidad de neuronas en una layer
#(eg, si len(size) = 4 entonces la red neuronal tiene cuatro capas).
#Empieza con las neuronas necesarias para leer el input y termina con una neurona.
size = [task.input_size, 30, 10, 1]
ws = [np.random.randn(m + 1, n) * 1e-2 for m, n in zip(size, size[1:])]
smooth_loss = .5

while True:
    x, y, texts = task.next_batch()
    xs, zs, dws = [x], {}, np.zeros_like(ws)

    #generamos output a partir de output
    for t, w in enumerate(ws):
        xs[t] = add_bias(xs[t], axis=1)#el bias está adentro del weight
        zs[t] = xs[t].dot(w)
        next_x = np.tanh(zs[t])
        xs.append(next_x)

    #backpropagation. generamos la derivada del costo con respecto a los weights
    #dx (o dz o dw) representa dC/dx (o dC/dz o dC/dw) con C siendo el costo y las d
    #siendo el operador de derivada.
    dx = xs[-1] - y
    for t in reversed(range(len(size) - 1)):
        dz = tanh_prime(zs[t]) * dx
        dws[t] = xs[t].T.dot(dz)
        dx = dz.dot(ws[t].T)
        dx = remove_bias(dx, axis=1)

    #gradient descent
    for w, dw in zip(ws, dws):
        w -= learning_rate * dw

    loss = (np.square(xs[-1] - y) / 2).sum()
    #smootheamos la loss para que sea más lindo y entendible
    smooth_loss = smooth_loss * .999 + loss * .001
    print ('{:.4f} {:.4f} {} {}'.format(smooth_loss, xs[-1][0][0], y[0][0], texts[0]))
