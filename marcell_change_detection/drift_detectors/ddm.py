# implement basic ddm change detector
import numpy as np


class DDM:
    """ Drift Detection Method for evolving data streams."""

    def __init__(self, min_num_instances=30, warning_level=2.0, out_control_level=3.0):
        self.id = 1

        self.in_concept_change = None
        self.in_warning_zone = None
        self.estimation = None
        self.delay = None

        self.sample_count = None
        self.miss_prob = None
        self.miss_std = None
        self.miss_prob_sd_min = None
        self.miss_prob_min = None
        self.miss_sd_min = None
        self.min_instances = min_num_instances
        self.warning_level = warning_level
        self.out_control_level = out_control_level

        self.reset()

    def get_id(self):
        return self.id

    def reset(self):
        """ reset

        Resets the change detector parameters.

        """
        self.in_concept_change = False
        self.in_warning_zone = False
        self.estimation = 0.0
        self.delay = 0.0

        self.sample_count = 1
        self.miss_prob = 1.0
        self.miss_std = 0.0
        self.miss_prob_sd_min = float("inf")
        self.miss_prob_min = float("inf")
        self.miss_sd_min = float("inf")

    def detected_change(self):
        """ detected_change
        This function returns whether concept drift was detected or not.
        """
        return self.in_concept_change

    def detected_warning_zone(self):
        """ detected_warning_zone
        This function returns whether it's inside the warning zone or not.
        """
        return self.in_warning_zone

    def get_length_estimation(self):
        """ get_length_estimation

        Returns the length estimation.

        Returns
        -------
        int
            The length estimation

        """
        return self.estimation

    def add_element(self, prediction):
        """ Add a new element to the statistics

        Parameters
        ----------
        prediction: int (either 0 or 1)
            This parameter indicates whether the last sample analyzed was
            correctly classified or not. 1 indicates an error (miss-classification).

        Notes
        -----
        After calling this method, to verify if change was detected or if
        the learner is in the warning zone, one should call the super method
        detected_change, which returns True if concept drift was detected and
        False otherwise.

        """
        if self.in_concept_change:
            self.reset()

        self.miss_prob = self.miss_prob + (prediction - self.miss_prob) / float(self.sample_count)
        self.miss_std = np.sqrt(self.miss_prob * (1 - self.miss_prob) / float(self.sample_count))
        self.sample_count += 1

        self.estimation = self.miss_prob
        self.in_concept_change = False
        self.in_warning_zone = False
        self.delay = 0

        if self.sample_count < self.min_instances:
            return

        if self.miss_prob + self.miss_std <= self.miss_prob_sd_min:
            self.miss_prob_min = self.miss_prob
            self.miss_sd_min = self.miss_std
            self.miss_prob_sd_min = self.miss_prob + self.miss_std

        if self.miss_prob + self.miss_std > self.miss_prob_min + self.out_control_level \
                * self.miss_sd_min:
            self.in_concept_change = True

        elif self.miss_prob + self.miss_std > self.miss_prob_min + self.warning_level \
                * self.miss_sd_min:
            self.in_warning_zone = True

        else:
            self.in_warning_zone = False