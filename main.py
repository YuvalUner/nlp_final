import os

from story import Story
from story_collection import StoryCollection
from dotenv import load_dotenv
from openai import OpenAI

def main():
    story = Story("Rescuing the princess from the dragon")

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

    # story.base_version = ("Hunting down the dragon that is thought to have kidnapped the princess, the knight finally "
    #                       "reached the dragon's castle. The knight condemned the dragon for his crime, to which the "
    #                       "dragon responded:")
    # story.add_possible_remark("Your princess is in another castle.", False, "This is a reference to the Super Mario game series,"
    #                                                                         "where the princess is always in another castle")
    # story.add_possible_remark("Yeah, I'm not the kidnapper, it's some other dragon. You should leave.", False, "The dragon is"
    #                                                                                          "either really innocent or just"
    #                                                                                          "playing dumb")
    # story.add_possible_remark("Hey, I'm just trying to make a living here. Do you how lucrative princess kidnapping is?",
    #                           False, "The dragon is just trying to make a living,"
    #                                  "and princess kidnapping may really be a lucrative business. There isn't "
    #                                  "necessarily any sarcasm here")
    # story.add_possible_remark("Oh, now that you say that, I realize how terrible that was. I am ever so sorry.", True,
    #                           "The dragon is being sarcastic here, as it is highly unlikely that the dragon is"
    #                           " actually sorry for kidnapping the princess after just being condemned for it by the knight")
    # story.detailed_version = ("""
    # The knight had been on a quest to rescue the princess for weeks now.
    # He had faced many challenges and fought many battles, but he had finally reached the castle where the
    # dragon who was said to have kidnapped the princess lived.
    # Upon entering the castle and confronting the dragon, the knight condemned the dragon for his crime.
    # The dragon, however, responded in a way that the knight did not expect, saying:
    # """)
    # story.novel_version = (
    #     """
    #     A tragedy had befallen the kingdom. The princess had been kidnapped by a fearsome dragon, and the king had
    #     dispatched his bravest and mightiest knight to rescue her.
    #     The knight had faced many dangers and perils on his journey, overcoming countless obstacles in his path,
    #     surpassing his limit many times over, vanquishing all evil that stood in his way.
    #     And now, after a long and arduous journey, the knight had finally reached the dragon's castle.
    #     The castle loomed before him, a dark and foreboding structure, its walls towering high above him, its gates
    #     hiding behind them what may well be the most fearsome creature in all the land.
    #     Gathering his courage, the knight entered the castle, his sword drawn, his shield raised, ready to face
    #     whatever lay ahead.
    #     And there, in the heart of the castle, he found the dragon.
    #     The dragon, a massive and terrifying beast, stood before him, its scales gleaming in the dim light, its eyes
    #     a molten gold, each larger than he is tall, its claws sharp and daggers, and the very air around it seemed to
    #     tremble with its presence.
    #     The knight, undaunted, condemned the dragon for its crime, accusing it of kidnapping the princess and bringing
    #     sorrow and despair to the kingdom.
    #     The dragon, however, responded in a way that the knight did not expect, saying:
    #     """
    #     )

    story_collection = StoryCollection()

    story_collection.load_stories_from_json("stories")
    # story_collection.add_story(story)

    # story_collection.add_story(story)
    # story_collection.save_stories_as_json("stories")
    print(story_collection)



if __name__ == "__main__":
    main()