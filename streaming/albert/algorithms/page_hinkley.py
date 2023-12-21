# Page-Hinkley Implementation
class PageHinkley:
    def __init__(self, min_instances=30, delta=0.005, threshold=50, alpha=1-0.0001):
        self.min_instances = min_instances
        self.delta = delta
        self.threshold = threshold
        self.alpha = alpha
        self.cum_sum = 0
        self.mean = 0
        self.n = 0

    def add_element(self, value):
        if self.n < self.min_instances:
            self.n += 1
            self.mean = self.mean + (value - self.mean) / self.n
            return False

        self.cum_sum = max(0, self.alpha * self.cum_sum + (value - self.mean - self.delta))

        self.mean = self.mean + (value - self.mean) / self.n
        self.n += 1

        if self.cum_sum > self.threshold:
            self.cum_sum = 0
            return True

        return False