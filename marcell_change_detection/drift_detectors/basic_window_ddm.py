class BasicWindowDDM:
    def __init__(self, expected_value=1, window_size=20, warning_diff=0.3, out_control_diff=0.5):
        self.id = 3

        self.sample_count = None
        self.window_size = window_size
        self.window = None
        self.window_avg = None
        self.expected_value = expected_value

        self.warning_diff = warning_diff
        self.out_control_diff = out_control_diff
        self.in_warning_zone = False
        self.in_concept_change = False

        self.reset()

    def get_id(self):
        return self.id

    def reset(self):
        self.window = []
        self.window_avg = 0
        self.sample_count = 0
        self.in_warning_zone = False
        self.in_concept_change = False

    def detected_warning_zone(self):
        return self.in_warning_zone

    def detected_change(self):
        return self.in_concept_change

    def add_element(self, input_value):
        if self.in_concept_change:
            self.reset()
        # shift the window: add new element
        self.window.append(input_value)
        # subtract the oldest element from the window average
        self.window_avg += input_value / self.window_size
        # increase sample_count
        self.sample_count += 1

        # shift the window: remove oldest
        if len(self.window) > self.window_size:
            # subtract the oldest element from the window average
            self.window_avg -= self.window[0] / self.window_size
            self.window.pop(0)

        # do not do drift detection if the window size is not sufficient i.e. at the beginning
        elif len(self.window) < self.window_size:
            return

        # do the warning detection:
        if abs(self.window_avg - self.expected_value) > self.warning_diff:
            self.in_warning_zone = True
            # do the drift detection
            if abs(self.window_avg - self.expected_value) > self.out_control_diff:
                self.in_concept_change = True
