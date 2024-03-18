import os

from story import Story
from story_collection import StoryCollection
from dotenv import load_dotenv
from openai import OpenAI

def main():
    story = Story("Pudding thief")

    # story.base_version = ("After an exhausting week at work, John went star gazing. While doing that,"
    #                       "he saw a star growing bigger and bigger, coming straight for him, and said:")
    # story.add_possible_remark("Looks like I forgot to take my pills again.", False,
    #                           "John may actually be taking pills on a regular basis but forgot to take them today,"
    #                           " which would explain this absurd situation")
    # story.add_possible_remark("Well, guess getting squashed by a meteor is not the worst way to die",
    #                           False, "John is simply accepting his fate, because there is no outrunning a meteor")
    # story.add_possible_remark("Oh great, I wanted to die today anyways.", True,
    #                           "Humans do not typically want to die, and there is no indication that John is suicidal")
    # story.add_possible_remark("What the hell is that?", False,
    #                           "John is confused and scared, which is probably a normal reaction upon seeing a meteor coming "
    #                           "straight for you")
    # story.detailed_version = ("After an exhausting week at work, John decided to partake in his favorite hobby: star gazing."
    #                           "Star gazing was always a relaxing activity for John, and he enjoyed the peace and quiet it brought."
    #                           "No matter how stressful his week was, star gazing always managed to calm him down and give him "
    #                           "the energy he needed to face the next week. However, this time was different. As John was looking at the"
    #                           "stars, he saw a star that was growing bigger and bigger. It was coming straight for him!"
    #                           "Seeing that, John said:")
    # story.novel_version = ("John had been working hard all week, and he was exhausted. He decided to go star gazing, as it was his"
    #                        "favorite hobby. Star gazing was always a relaxing activity for John, and he enjoyed the peace and quiet it brought."
    #                        "No matter how stressful his week was, no matter how exhausted he was, looking at the cosmos above"
    #                        "always managed to calm him down. The sense of scale, the beauty of the stars, the knowledge "
    #                        "that in the grand scheme of things his problems insignificant - all of that gave him the peace"
    #                        "of mind he needed to refresh himself and face the next week."
    #                        "This week, just like every other week, John went to his favorite spot to admire the stars."
    #                        "Their scintillating beauty as they hung overhead like smelter pots, dotting the night sky with their"
    #                        "glowing presence, was always a sight to behold. the countless stars, the infinite cosmos, the"
    #                        "vastness of space - looking at all of that always made John feel like he was part of something bigger"
    #                        "and filled him with a sense of awe and wonder, as well as inner peace."
    #                        "However, while John was looking at the stars, he saw a star that was growing bigger and bigger."
    #                        "Not only that, it seemed to be coming straight for him!"
    #                        "Seeing that, John said:"
    #                        )

    # story.base_version = ("Coming home from picking up groceries, John entered the living room and saw his roommate, Jane."
    #                       "Seeing what she was doing, he said:")
    # story.add_possible_remark("That looks fun, mind if I join you?", False,
    #                           "John is simply asking if he can join Jane in whatever she is doing")
    # story.add_possible_remark("Mind helping me with the groceries?", False,
    #                           "John is asking Jane to help him with the groceries,"
    #                           " which is a normal thing to ask of a roommate. Whatever Jane was doing is irrelevant in this context")
    # story.add_possible_remark("Why are you always like this?", False,
    #                           "John is exasperated with Jane's behavior, which seems to be a recurring issue,"
    #                           "but it is not necessarily a sarcastic remark")
    # story.add_possible_remark("So, did I forget to take my pills today, or did you?", True,
    #                           "John is implying that whatever Jane is doing, it is so absurd that it makes him question either "
    #                           "his own sanity or hers")
    # story.detailed_version = ("John went to pick up some groceries for himself and his roomate, Jane, which took him a while."
    #                           "When he came back home, as he headed to the living room, he heard some noises coming from there."
    #                           "Knowing his roommate, he braced himself for the worst and entered the living room."
    #                           "When he saw what she was doing, he said:")
    # story.novel_version = ("John had been out to pick up some groceries for himself and his roommate, Jane."
    #                        "It was a long and arduous task, leading to an epic saga of survival, perseverance, determination,"
    #                        "a battle against the elements and against human nature itself, but he achieved victory nonetheless "
    #                        "and came back home with the groceries."
    #                        "Following his triumphant return, he opened the entryway door,"
    #                        "and as he did so, he heard some noises coming from the living room."
    #                        "John knew his roommate, Jane, and he knew that whatever she was doing, it was going to truly "
    #                        "be something."
    #                        "And so, taking deep breaths and bracing himself for the worst, he entered the living room."
    #                        "Upon entering the living room and seeing what Jane was doing, he said:"
    #                        )

    story_collection = StoryCollection()

    story_collection.load_stories_from_json("stories")

    # story_collection.add_story(story)
    story_collection.save_stories_as_json("stories")
    print(story_collection)
    print(story_collection.stories[0])
    print(story_collection.stories[1])



if __name__ == "__main__":
    main()