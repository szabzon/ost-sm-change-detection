class ECDD:
    def __init__(self, alpha=0.05, warning_threshold=0.8, drift_threshold=0.95, expected_value=1, min_num_instances=20):
        self.id = 4

        self.alpha = alpha
        self.warning_threshold = warning_threshold
        self.drift_threshold = drift_threshold
        self.in_warning_zone = False
        self.in_concept_change = False
        self.ewma = 0
        self.expected_value = 1 - expected_value
        self.min_num_instances = min_num_instances
        self.sample_count = 0

        self.reset()

    def get_id(self):
        return self.id

    def reset(self):
        self.in_warning_zone = False
        self.in_concept_change = False
        self.ewma = 0
        self.sample_count = 0

    def detected_warning_zone(self):
        return self.in_warning_zone

    def detected_change(self):
        return self.in_concept_change

    def add_element(self, input_value):
        if self.in_concept_change:
            self.reset()

        input_value = 1 - input_value
        self.ewma = self.alpha * input_value + (1 - self.alpha) * self.ewma
        self.sample_count += 1
        if self.sample_count < self.min_num_instances:
            pass

        if abs(self.ewma - self.expected_value) > self.warning_threshold:
            self.in_warning_zone = True
            if abs(self.ewma - self.expected_value) > self.warning_threshold:
                self.in_concept_change = True
