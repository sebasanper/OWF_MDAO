from simanneal import Annealer
import call_workflow_once as wf
from random import choice, randint


class TimeScore(Annealer):
    def move(self):
        a = randint(0, len(self.state) - 1)
        if a == 0:
            self.state[a] = randint(2, 25)
        elif a == 1:
            self.state[a] = choice([30.0, 60.0, 90.0, 120.0, 180.0])
        elif a == 2:
            while self.state[a] > self.state[1]:
                self.state[a] = choice([1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0])
            self.state[a] = self.state[a]
        elif a == 3:
            self.state[a] = randint(0, 2)
        elif a == 4:
            self.state[a] = randint(0, 2)
        elif a == 5:
            self.state[a] = randint(0, 5)
        elif a == 6:
            self.state[a] = randint(0, 3)
        elif a == 7:
            self.state[a] = randint(0, 3)
        elif a == 8:
            self.state[a] = randint(0, 3)
        elif a == 9:
            self.state[a] = randint(0, 4)
        elif a == 10:
            self.state[a] = randint(0, 3)
        elif a == 11:
            self.state[a] = randint(0, 1)
        elif a == 12:
            self.state[a] = randint(0, 1)

    def energy(self):
        return wf.score_median_workflow(self.state)[2]

if __name__ == '__main__':
    initial_state = [21, 90.0, 30.0, 2, 2, 0, 0, 3, 3, 2, 1, 0, 0]
    optimize_time = TimeScore(initial_state)
    optimize_time.Tmax = 10.0
    optimize_time.steps = 50
    optimize_time.updates = 50
    results = optimize_time.anneal()
    print results
