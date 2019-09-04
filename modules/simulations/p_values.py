import time
from os.path import dirname, abspath
from playsound import playsound





if __name__ == '__main__':
    SOUNDS_PATH = dirname(dirname(dirname(abspath(__file__))))
    p_value_sonata([0.3, 0.005, 0.56, 0.06])
