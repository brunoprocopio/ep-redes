"""
Arquivo de configuração
"""

import socket
import threading
import sys
import time
from random import randint
import fileIO

BYTE_SIZE = 1024
HOST = '127.0.0.1'
PORT = 5000
PEER_BYTE_DIFFERENTIATOR = b'\X11'
RAND_TIME_START = 1
RAND_TIME_END = 2
REQUEST_STRING = "req"
