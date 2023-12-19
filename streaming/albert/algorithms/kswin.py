
import numpy as np
from sklearn.metrics.pairwise import pairwise_kernels


# KSWIN Implementation
class KSWIN:
    def __init__(self, window_size=30, alpha=0.01, kernel='linear'):
        self.window_size = window_size
        self.alpha = alpha
        self.kernel = kernel
        self.data_buffer = []
        self.change_detected = False

    def add_element(self, value):
        self.data_buffer.append(value)

        if len(self.data_buffer) > self.window_size:
            self.data_buffer.pop(0)

            if self.change_detected:
                return True

            kernel_matrix = pairwise_kernels([value], self.data_buffer, metric=self.kernel)[0]
            mean_kernel = np.mean(kernel_matrix)
            var_kernel = np.var(kernel_matrix)

            if var_kernel > 0:
                stat = (1 / var_kernel) * (mean_kernel - np.mean(kernel_matrix))
                self.change_detected = stat > np.percentile(np.random.normal(0, 1, 1000), 100 * (1 - self.alpha))

                if self.change_detected:
                    return True

        return False
