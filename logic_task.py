import numpy as np
from utils import *

class Task:
    def __init__(self, batch_size):
        xs, ys, texts = [], [], []
        chars = ['A', 'B', 'C', '⇒', '¬', '(', ')', '|', '-', ',']
        char_to_i = {char: i for i, char in enumerate(chars)}
        lines = open('training/unique_logic.txt', 'r').readlines()

        #calculamos la sentencia más larga para determinar qué tan
        # grande tiene que ser la input layer de la red neuronal (NN).
        largest_sen = 0
        for line in lines[:-1]:
            x1, x2, _ = line.split(' ')
            largest_sen = max(largest_sen, len(x1 + x2) + 1)

        #traducimos 'A>B!AB A>B!A!B' a algo que la NN pueda entender
        for line in lines:
            x1, x2, y = line.strip().split(' ')
            #Ponemos | entre las dos enunciados para que la NN sepa diferenciar
            # entre ellos. ljust agrega el char '-' hasta que la sentencia mida
            # largest_sen de largo (para que todas los inputs midan lo mismo.)
            x = (x1 + '|' + x2).ljust(largest_sen, '-')
            x = [char_to_i[c] for c in x]
            x = [one_of_k(i, len(chars)) for i in x]
            x = np.array(x).flatten()
            xs.append(x)
            y = float(y) * 2 - 1
            ys.append([y])
            texts.append(x1 + ' ' + x2)

        self.batch_size = batch_size
        self.input_size = largest_sen * len(chars)
        self.xs, self.ys, self.texts = np.array(xs[1:-1000]), np.array(ys[1:-1000]), np.array(texts[1:-1000])
        self.val_xs, self.val_ys = np.array(xs[-1000:]), np.array(ys[-1000:])
        self.val_texts = np.array(texts[-1000:])
        self.test_xs, self.test_ys = np.array(xs[0:1]), np.array(ys[0:1])
        self.test_texts = np.array(texts[0:1])

    def next_batch(self):
        ids = np.random.randint(len(self.xs), size=self.batch_size)
        return self.xs[ids], self.ys[ids], self.texts[ids]

    def val_data(self):
        return self.val_xs, self.val_ys, self.val_texts

    def test_data(self):
        return self.test_xs, self.test_ys, self.test_texts

'''
TODO:
Try removing the '|'. It's redundant, but it may help the nn
'''
