def calculate_delay_of_detection(true_change_points, detected_change_points):
    total_delay = 0
    count = 0

    for true_point in true_change_points:
        detected_point = min([dp for dp in detected_change_points if dp >= true_point], default=None)
        if detected_point is not None:
            total_delay += (detected_point - true_point)
            count += 1

    return total_delay / count if count else None


def calculate_false_detection_rate(true_change_points, detected_change_points):
    false_detections = [dp for dp in detected_change_points if dp not in true_change_points]
    return len(false_detections) / len(detected_change_points) if detected_change_points else 0



def calculate_miss_detection_rate(true_change_points, detected_change_points):
    missed_detections = [tp for tp in true_change_points if tp not in detected_change_points]
    return len(missed_detections) / len(true_change_points) if true_change_points else 0



def calculate_error_rate(true_labels, predicted_labels):
    incorrect_predictions = sum(1 for true, pred in zip(true_labels, predicted_labels) if true != pred)
    return incorrect_predictions / len(true_labels) if true_labels else 0