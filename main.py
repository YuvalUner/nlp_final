from story_collection import StoryCollection
from dotenv import load_dotenv
from compute_statistics import *
from tests import (test_zero_shot_no_explanations, test_zero_shot_with_explanations, few_shot_test,
                   few_shot_chain_of_thought, zero_shot_chain_of_thought)
import pandas as pd



def main():
    load_dotenv()
    story_collection = StoryCollection()

    story_collection.load_stories_from_json("stories")
    print(story_collection)

    # test_zero_shot_with_explanations("detailed", story_collection)
    # story_collection.reset()
    # test_zero_shot_no_explanations("base", story_collection)
    # story_collection.reset()
    # test_zero_shot_no_explanations("detailed", story_collection)
    # story_collection.reset()
    # test_zero_shot_no_explanations("novel", story_collection)
    # story_collection.reset()
    # test_zero_shot_with_explanations("base", story_collection)
    # story_collection.reset()
    # test_zero_shot_with_explanations("detailed", story_collection)
    # story_collection.reset()
    # test_zero_shot_with_explanations("novel", story_collection)
    # story_collection.reset()
    # few_shot_test("base", story_collection)
    # story_collection.reset()
    # few_shot_test("detailed", story_collection)
    # story_collection.reset()
    # few_shot_test("novel", story_collection)
    # story_collection.reset()

    # story_collection.reset()
    # few_shot_chain_of_thought("base", story_collection)
    # story_collection.reset()
    # few_shot_chain_of_thought("detailed", story_collection)
    # story_collection.reset()
    # few_shot_chain_of_thought("novel", story_collection)
    # story_collection.reset()

    story_collection.reset()
    zero_shot_chain_of_thought("base", story_collection)
    story_collection.reset()
    zero_shot_chain_of_thought("detailed", story_collection)
    story_collection.reset()
    zero_shot_chain_of_thought("novel", story_collection)




if __name__ == "__main__":
    main()