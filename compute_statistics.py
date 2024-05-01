import json


def load_results(filename):
    with open(filename, "r") as file:
        results_dict = json.load(file)
    file.close()
    return results_dict

def compute_accuracy(results_dict):
    """
    Accuracy is computed as the number of times the model got the correct answer on the first attempt divided by the total
    :param results_dict:
    :return:
    """
    total_correct = 0
    total_attempts = 0
    for story_results in results_dict["Results"]:
        if story_results["Correct on Attempt"] == 1:
            total_correct += 1
        total_attempts += 1
    return total_correct / total_attempts

def compute_average_attempts_for_success(results_dict):
    """
    Average attempts is computed as the sum of the number of attempts the model took to get the correct answer divided by the total
    :param results_dict:
    :return:
    """
    total_attempts = 0
    success_count = 0
    for story_results in results_dict["Results"]:
        total_attempts += story_results["Correct on Attempt"] if story_results["Correct on Attempt"] != -1 else 0
        if story_results["Correct on Attempt"] != -1:
            success_count += 1
    return total_attempts / success_count


def compute_average_attempts_overall(results_dict):
    """
    Average attempts is computed as the sum of the number of attempts the model took to get the correct answer divided by the total
    :param results_dict:
    :return:
    """
    total_attempts = 0
    for story_results in results_dict["Results"]:
        total_attempts += story_results["Correct on Attempt"] if story_results["Correct on Attempt"] != -1 else 4
    return total_attempts / len(results_dict["Results"])

def compute_success_rate(results_dict):
    """
    Success rate is computed as the number of times the model got the correct answer divided by the total
    :param results_dict:
    :return:
    """
    total_correct = 0
    total_attempts = 0
    for story_results in results_dict["Results"]:
        if story_results["Correct on Attempt"] != -1:
            total_correct += 1
        total_attempts += 1
    return total_correct / total_attempts