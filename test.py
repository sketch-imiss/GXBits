import matplotlib.pyplot as plt
import numpy as np
import math


def compute(alpha):
       return math.log(abs(1 - 2 * alpha / sketch)) / math.log(1 - 2 / sketch)

sketch = 100
lst_alpha = []
lst_falpha = []

for alpha in range(0, int(sketch)):
       if alpha != sketch/2:
              lst_alpha.append(alpha)
              falpha = compute(alpha)
              lst_falpha.append(falpha)

fig, ax = plt.subplots()
ax.plot(lst_alpha, lst_falpha)

ax.set(title='sketch=100')

# plt.savefig('sketch100.png')
plt.show()