import sys, os

#Expand Python classes path with your app's path
sys.path.insert(0, os.path.dirname(__file__))
from app import app as application
