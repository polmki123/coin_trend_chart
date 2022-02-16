# orderbook_0.py
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import time
import os 
from CreonAPI import Client
from binance_coin import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('__file__')))) #상위 경로 추가 
from Dataloader.RT_data import *

