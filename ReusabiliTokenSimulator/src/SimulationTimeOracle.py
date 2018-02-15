"""@package SimulationTimeOracle
Implementation of a timing oracle
"""


class SimulationTimeOracle(object):
    def __init__(self):
        self.time = 0

    def increment_time(self):
        self.time += 1

    def get_time(self):
        return self.time

