import numpy as np
import math
import random
import time

if __name__ == '__main__':
    start = time.time()
    for i in range(10):
        ls1 = list(range(1, 100000))
    for j in range(len(ls1)):
        ls1[j] = math.sin(ls1[j])

    # print(ls1)
    print(time.time() - start)

    start = time.time()
    for i in range(10):
        ls1 = np.array(np.arange(1, 100000))
    ls1 = np.sin(ls1)

    # print(ls1)
    print(time.time()-start)
