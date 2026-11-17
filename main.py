import os
from sps import network
from sps.config import Config

# Disabling oneDNN CPU optimizations in TensorFlow.
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

Config.compute_k_range()
print("---starting mnist classification---")
network.launch_mnist()

