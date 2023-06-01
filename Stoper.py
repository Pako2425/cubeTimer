import time

class Stoper():
    def __init__(self):
        self.startTime = 0.0
        self.measuredTime = 0.0

    def start(self):
        self.startTime = time.time()
        self.measuredTime = 0.0

    def read(self):
        self.measuredTime = time.time() - self.startTime
        return self.measuredTime

    def reset(self):
        self.measuredTime = 0.0
        self.startTime = time.time()