import math
import random


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
        random.shuffle(self.possible_remarks)
        for i in range(len(self.possible_remarks)):
            if self.possible_remarks[i][1]:
                self.sarcastic_index = i
                break

    def __str__(self):
        self.__randomize_remarks()
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
        for i, remark in enumerate(self.possible_remarks):
            remarks_string += f"{i + 1}. {remark[0]}\n"
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
        try:
            model_output = int(model_output)
            if model_output == self.sarcastic_index + 1:
                correct = True
            text = self.possible_remarks[model_output - 1][0]
        except ValueError:
            # Remove numbers from the model output
            model_output = ''.join([i for i in model_output if not i.isdigit()])
            # Remove the initial dot and space from the model output
            model_output = model_output[2:]
            # Compare the model output to the sarcastic remark
            if model_output == self.possible_remarks[self.sarcastic_index][0]:
                correct = True
            text = model_output
        return correct, text

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
