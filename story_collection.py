import json

from story import Story


class StoryEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Story):
            return obj.__dict__
        else:
            return obj


class StoryCollection:

    def __init__(self):
        self.stories = []
        self.base_version_scores = []
        self.detailed_version_scores = []
        self.novel_version_scores = []
        self.results_dict = {}

    def add_story(self, story):
        story_titles = [story.title for story in self.stories]
        if story.title not in story_titles:
            self.stories.append(story)
        else:
            raise ValueError("Story with the same title already exists")

    def add_base_version_score(self, score, attempts_taken):
        self.base_version_scores.append((score, attempts_taken))

    def add_detailed_version_score(self, score, attempts_taken):
        self.detailed_version_scores.append((score, attempts_taken))

    def add_novel_version_score(self, score, attempts_taken):
        self.novel_version_scores.append((score, attempts_taken))

    def save_stories_as_json(self, filename):
        with open(filename + ".json", "w") as file:
            json.dump(self.stories, file, cls=StoryEncoder)
        file.close()

    def load_stories_from_json(self, filename):
        with open(filename + ".json", "r") as file:
            stories = json.load(file)
        file.close()
        for story in stories:
            new_story = Story.from_json(story)
            self.stories.append(new_story)


    def create_results_dict(self, model_name):
        results_dict = {
            "model_name": model_name,
            "base_version_scores": self.base_version_scores,
            "detailed_version_scores": self.detailed_version_scores,
            "novel_version_scores": self.novel_version_scores
        }
        return results_dict

    def save_results(self, filename, model_name):
        self.results_dict = self.create_results_dict(model_name)
        with open(filename + "_" + model_name + ".json", "w") as file:
            json.dump(self.results_dict, file)

    def load_results(self, filename, model_name):
        with open(filename + "_" + model_name + ".json", "r") as file:
            results_dict = json.load(file)
        file.close()
        self.base_version_scores = results_dict["base_version_scores"]
        self.detailed_version_scores = results_dict["detailed_version_scores"]
        self.novel_version_scores = results_dict["novel_version_scores"]
        self.results_dict = results_dict
        return results_dict["model_name"]

    def __str__(self):
        stories_string = ""
        for i, story in enumerate(self.stories):
            stories_string += f"Story {i + 1}: {story.title}\n"
        return stories_string

