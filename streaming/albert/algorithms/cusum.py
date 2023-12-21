class CUSUM:
    def __init__(self, threshold=10, drift_threshold=5):
        self.threshold = threshold
        self.drift_threshold = drift_threshold
        self.sum = 0
        self.reference = 0
        self.change_detected = False

    def add_element(self, value):
        deviation = value - self.reference
        self.sum = max(0, self.sum + deviation - self.threshold)

        if self.sum > self.drift_threshold:
            self.change_detected = True
            self.sum = 0
        else:
            self.change_detected = False

        self.reference += self.threshold

        return self.change_detected
