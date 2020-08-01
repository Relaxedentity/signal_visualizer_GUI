# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

data = np.load('data_copper.npy')

print(data.shape)

print(data.dtype)

plt.imshow(data[...,5,10])
plt.show()

plt.imshow(data[100,200])
plt.show()