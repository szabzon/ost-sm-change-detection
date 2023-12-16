class ECDD:
    def __init__(self, alpha = 0.05, warning_threshold=0.1, drift_threshold=0.2):
        self.name = "ECDD"

        self.alpha = alpha
        self.warning_threshold = warning_threshold
        self.drift_threshold = drift_threshold
        self.in_warning_zone = False
        self.in_concept_change = False
        self.ewma = 0

        self.reset()

    def get_name(self):
        return self.name

    def reset(self):
        self.in_warning_zone = False
        self.in_concept_change = False
        self.ewma = 0

    def detected_warning_zone(self):
        return self.in_warning_zone

    def detected_change(self):
        return self.in_concept_change

    def add_element(self, input_value):
        if self.in_concept_change:
            self.reset()
        self.ewma = self.alpha * input_value + (1 - self.alpha) * self.ewma

        if abs(input_value - self.ewma) > self.warning_threshold:
            self.in_warning_zone = True
            if abs(input_value - self.ewma) > self.drift_threshold:
                self.in_concept_change = True
