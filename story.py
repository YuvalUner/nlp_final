import math
import numpy as np


class Story:
    """
    A class to represent a story in the LLM sarcasm detection database.
    Contains:
    1. title: the title of the story
    2. base_version: the base, bare-bones version of the story
    3. detailed_version: a detailed version of the bare-bones story, containing more information
    4. novel_version: a novel version of the story, containing more information and more complex language
    base version should be a sentence or two, detailed version should be a paragraph,
    and novel version should be a few paragraphs.
    5. possible_remarks: a list of (string, boolean, explanation) tuples, where the string is a possible remark and the
    boolean is whether the remark is sarcastic. Only one of the remarks should be sarcastic.
    Explanation is a string explaining why the remark is sarcastic or not.
    """

    def __init__(self, title=""):
        self.title = title
        self.base_version = ""
        self.detailed_version = ""
        self.novel_version = ""
        self.possible_remarks = []
        self.sarcastic_index = -1

    def add_base_version(self, base_version):
        self.base_version = base_version

    def add_detailed_version(self, detailed_version):
        self.detailed_version = detailed_version

    def add_novel_version(self, novel_version):
        self.novel_version = novel_version

    def add_possible_remark(self, remark, sarcastic, explanation):
        self.possible_remarks.append((remark, sarcastic, explanation))

    def __randomize_remarks(self):
        """
        Randomizes the order of the possible remarks and sets the sarcastic index.
        This should be called before getting the string for the model.
        This prevents the model from learning the order of the remarks.
        :return:
        """
        np.random.shuffle(self.possible_remarks)
        for i in range(len(self.possible_remarks)):
            _, sarcastic, _ = self.possible_remarks[i]
            if sarcastic:
                self.sarcastic_index = i
                break

    def __str__(self):
        return (f"Base Version: {self.base_version}\n\nDetailed Version: {self.detailed_version}\n"
                f"\nNovel Version: {self.novel_version}\n\nRemarks: {self.possible_remarks}\n\nSarcastic"
                f" Index: {self.sarcastic_index}\n\nStringified remarks:\n{self.__stringify_remarks()}\n\n")

    def __stringify_remarks(self):
        """
        Returns a string of the possible remarks.
        The string is formatted as:
        1. remark1
        2. remark2
        ...
        :return:
        """
        remarks_string = ""
        for i in range(len(self.possible_remarks)):
            remark, _, _ = self.possible_remarks[i]
            remarks_string += f"{i + 1}. {remark}\n"
        return remarks_string

    def get_base_version_string_for_model(self):
        """
        Returns a string of the base version of the story, followed by the possible remarks.
        :return:
        """
        self.__randomize_remarks()
        return f"""{self.base_version}\n\n{self.__stringify_remarks()}
        """

    def get_detailed_version_string_for_model(self):
        """
        Returns a string of the detailed version of the story, followed by the possible remarks.
        :return:
        """
        self.__randomize_remarks()
        return f"""{self.detailed_version}\n\n{self.__stringify_remarks()}
        """

    def get_novel_version_string_for_model(self):
        """
        Returns a string of the novel version of the story, followed by the possible remarks.
        :return:
        """
        self.__randomize_remarks()
        return f"""{self.novel_version}\n\n{self.__stringify_remarks()}
        """

    def check_model_output(self, model_output):
        """
        Checks if the model output is the sarcastic remark.
        :param model_output:
        :return: True if the model output is the number of the sarcastic remark or the sarcastic remark itself, False otherwise.
        Also returns the text of the answer the model chose.
        """
        correct = False
        explanation = ""
        text = ""
        try:
            model_output = int(model_output)
            if model_output == (self.sarcastic_index + 1):
                correct = True
            text = self.possible_remarks[model_output - 1][0]
            explanation = self.possible_remarks[model_output - 1][2]
        except ValueError:
            # Remove numbers from the model output
            model_output = ''.join([i for i in model_output if not i.isdigit()])
            # Find the index of the remark that matches the model output
            idx = -1
            for i, remark in enumerate(self.possible_remarks):
                # Check if the model output contains the remark, in case the model output is a sentence instead of a number
                if remark[0].lower() in model_output.lower():
                    if i == self.sarcastic_index:
                        correct = True
                    idx = i
                    text = remark[0]
                    explanation = remark[2]
                    break
            if idx == -1:
                text = model_output
                explanation = "Invalid answer. Please choose a number from the list."
        return correct, text, explanation

    def score_model_output(self, attempt_number):
        """
        Scores the model output. The score is computed as 1 / 2^(attempt_number - 1) if the attempt number is less than
        the number of possible remarks, and 0 otherwise.
        :param attempt_number: the number of attempts the model took to get the right answer
        :return: the score
        """
        return 1 / math.pow(2, attempt_number - 1) if attempt_number < len(self.possible_remarks) else 0

    @staticmethod
    def from_json(json):
        """
        Initializes the story from a JSON object.
        :param json: the JSON object
        :return:
        """
        story = Story()
        story.base_version = json["base_version"]
        story.detailed_version = json["detailed_version"]
        story.novel_version = json["novel_version"]
        story.possible_remarks = json["possible_remarks"]
        story.sarcastic_index = json["sarcastic_index"]
        story.title = json["title"]
        return story

    def get_explanations(self):
        """
        Returns a string of the explanations for the possible remarks.
        :return:
        """
        explanations = ""
        for i, remark in enumerate(self.possible_remarks):
            explanations += f"{i + 1} is {'sarcastic' if remark[1] else 'not sarcastic'}, because: {remark[2]}\n"
        return explanations

    def get_explanation(self, index):
        """
        Returns the explanation for a specific remark.
        :param index: the index of the remark
        :return:
        """
        return self.possible_remarks[index][2]