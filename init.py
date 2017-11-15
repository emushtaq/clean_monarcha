import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import pandas as pd
import torch
import tensorflow as tf
import os
!set "KERAS_BACKEND=tensorflow"
import sys
print('__Python VERSION:', sys.version)
print("tensorflow:" + tf.__version__)
print('__pyTorch VERSION:', torch.__version__)
print('__CUDA VERSION')
print('__CUDNN VERSION:', torch.backends.cudnn.version())
print('__Number CUDA Devices:', torch.cuda.device_count())
print('__Devices')
print("OS: ", sys.platform)
print("Python: ", sys.version)
print("PyTorch: ", torch.__version__)
print("Numpy: ", np.__version__)
from multiprocessing import cpu_count
print("cpu_count: ", cpu_count())
# !pip install psutil
import psutil
def cpuStats():
        print(sys.version)
        print(psutil.cpu_percent())
        print(psutil.virtual_memory())  # physical memory usage
        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUse = py.memory_info()[0] / 2. ** 30  # memory use in GB...I think
        print('memory GB:', memoryUse)

cpuStats()
