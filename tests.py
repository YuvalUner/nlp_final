# This file is an example of programming horror, but oh well, it works and was fast to write.

import json
import os
import random
import spacy

from openai import OpenAI

from story_collection import StoryCollection


def request_from_model(chat_messages: list):
    client = OpenAI(
        api_key=os.environ.get("TOGETHER_API_KEY"),
        base_url="https://api.together.xyz/v1",
    )
    chat_completion = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=chat_messages,
        temperature=1,
        max_tokens=2000,
    )
    response = chat_completion.choices[0].message.content.strip()
    return response

def test_zero_shot_no_explanations(version_type: str, story_collection: StoryCollection):
    """
    Tests the model on zero shot prompting, where the model is not given any explanations for why its previous response was incorrect
    :param version_type:
    :param story_collection:
    :return:
    """
    results_dict = {
        "Version Type": version_type,
        "Results": []
    }

    for i, story in enumerate(story_collection):
        attempt_num = 1
        story_results = {
            "Title": story_collection[i].title,
        }
        if version_type == "base":
            story_content = story.get_base_version_string_for_model()
        elif version_type == "detailed":
            story_content = story.get_detailed_version_string_for_model()
        elif version_type == "novel":
            story_content = story.get_novel_version_string_for_model()
        else:
            raise ValueError("Invalid version type")
        system_content = """You will be presented with a story, followed by a list of possible remarks the character in the story could make.
Your task is to choose the sarcastic remark from the list.
Reply only with the number of the sarcastic remark. Your response must be a single number, and nothing else. Do not apologize, explain, or ask questions.
Your answers will be checked automatically, so writing anything other than the number of the sarcastic remark will be automatically marked as incorrect and you will 
fail and be penalized.
If you answer incorrectly, you will be asked to try again. You will have a limited number of attempts to get the correct answer. 
In all of your responses, including the follow up ones, please only reply with the number of the sarcastic remark. Do not
copy the remark, or add any additional text.
"""
        user_content = f"""The story is as follows:
'''
{story_content}
'''
        """
        chat_messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]
        response = request_from_model(chat_messages)
        correct, text, _ = story.check_model_output(response)
        story_results[f"Attempt {attempt_num}"] = {
            "Correct": correct,
            "Response": text,
            "Model Response": response
        }
        while not correct:
            attempt_num += 1
            # If the model would have to make more attempts than there are possible remarks, then it is considered
            # to have failed the story
            if attempt_num == len(story.possible_remarks):
                break
            chat_messages.append({"role": "assistant", "content": response})
            chat_messages.append({"role": "user", "content": "Wrong answer. Please try again. Remember to reply only with the number of the sarcastic remark."
                                                             "Do not apologize, explain , or ask questions. Your response must be a single number, and nothing else."})
            response = request_from_model(chat_messages)
            correct, text, _ = story.check_model_output(response)
            story_results[f"Attempt {attempt_num}"] = {
                "Correct": correct,
                "Response": text,
                "Model Response": response
            }
        story_results["Correct on Attempt"] = attempt_num if correct else -1

        results_dict["Results"].append(story_results)
        print(f"Story {i + 1} completed, {f'correct on attempt {attempt_num}' if correct else 'failed'}.")
    with open("results/results_zero_shot_zero_explanations_" + version_type + ".json", "w") as file:
        json.dump(results_dict, file)


def test_zero_shot_with_explanations(version_type: str, story_collection: StoryCollection):
    """
    Tests the model on zero shot prompting, but this time the model receives an explanation of why the previous response was incorrect
    :param version_type:
    :param story_collection:
    :return:
    """
    results_dict = {
        "Version Type": version_type,
        "Results": []
    }

    for i, story in enumerate(story_collection):
        attempt_num = 1
        story_results = {
            "Title": story_collection[i].title,
        }
        if version_type == "base":
            story_content = story.get_base_version_string_for_model()
        elif version_type == "detailed":
            story_content = story.get_detailed_version_string_for_model()
        elif version_type == "novel":
            story_content = story.get_novel_version_string_for_model()
        else:
            raise ValueError("Invalid version type")
        system_content = """You will be presented with a story, followed by a list of possible remarks the character in the story could make.
Your task is to choose the sarcastic remark from the list.
Reply only with the number of the sarcastic remark. Your response must be a single number, and nothing else. Do not apologize, explain, or ask questions.
Your answers will be checked automatically, so writing anything other than the number of the sarcastic remark will be automatically marked as incorrect and you will 
fail and be penalized.
If you answer incorrectly, you will be asked to try again. You will have a limited number of attempts to get the correct answer. 
In all of your responses, including the follow up ones, please only reply with the number of the sarcastic remark. Do not
copy the remark, or add any additional text.
        """
        user_content = f"""The story is as follows:
'''
{story_content}
'''
"""
        chat_messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]
        response = request_from_model(chat_messages)
        correct, text, explanation = story.check_model_output(response)
        story_results[f"Attempt {attempt_num}"] = {
            "Correct": correct,
            "Response": text,
            "Model Response": response,
            "Explanation": explanation
        }
        while not correct:
            attempt_num += 1
            # If the model would have to make more attempts than there are possible remarks, then it is considered
            # to have failed the story
            if attempt_num == len(story.possible_remarks):
                break
            chat_messages.append({"role": "assistant", "content": response})
            chat_messages.append({"role": "user", "content": "Wrong answer. "
                                                             "Reason: " + explanation +
                                                             " Please try again. Remember to reply only with the number of the sarcastic remark."
                                                             "Do not apologize, explain , or ask questions. Your response must be a single number, and nothing else."})
            response = request_from_model(chat_messages)
            correct, text, explanation = story.check_model_output(response)
            story_results[f"Attempt {attempt_num}"] = {
                "Correct": correct,
                "Response": text,
                "Model Response": response,
                "Explanation": explanation
            }
        story_results["Correct on Attempt"] = attempt_num if correct else -1

        results_dict["Results"].append(story_results)
        print(f"Story {i + 1} completed, {f'correct on attempt {attempt_num}' if correct else 'failed'}.")
    with open("results/results_zero_shot_with_explanations_" + version_type + ".json", "w") as file:
        json.dump(results_dict, file)

def few_shot_test(version_type: str, story_collection: StoryCollection):
    """
    Tests the model on few shot prompting, where the model is given some examples of sarcastic remarks before being tested
    :param version_type:
    :param story_collection:
    :return:
    """
    results_dict = {
        "Version Type": version_type,
        "Results": []
    }

    for i, story in enumerate(story_collection):
        attempt_num = 1
        story_results = {
            "Title": story_collection[i].title,
        }
        paired_indexes = random.sample(range(len(story_collection)), 2)
        while i in paired_indexes:
            paired_indexes = random.sample(range(len(story_collection)), 2)
        pair_first = story_collection[paired_indexes[0]]
        pair_second = story_collection[paired_indexes[1]]
        if version_type == "base":
            story_content = story.get_base_version_string_for_model()
            pair_first_content = pair_first.get_base_version_string_for_model()
            pair_second_content = pair_second.get_base_version_string_for_model()
        elif version_type == "detailed":
            story_content = story.get_detailed_version_string_for_model()
            pair_first_content = pair_first.get_detailed_version_string_for_model()
            pair_second_content = pair_second.get_detailed_version_string_for_model()
        elif version_type == "novel":
            story_content = story.get_novel_version_string_for_model()
            pair_first_content = pair_first.get_novel_version_string_for_model()
            pair_second_content = pair_second.get_novel_version_string_for_model()
        else:
            raise ValueError("Invalid version type")
        system_content = """You will be presented with a story, followed by a list of possible remarks the character in the story could make.
You will be presented with a story, followed by a list of possible remarks the character in the story could make.
Your task is to choose the sarcastic remark from the list.
Reply only with the number of the sarcastic remark. Your response must be a single number, and nothing else. Do not apologize, explain, or ask questions.
Your answers will be checked automatically, so writing anything other than the number of the sarcastic remark will be automatically marked as incorrect and you will 
fail and be penalized.
If you answer incorrectly, you will be asked to try again. You will have a limited number of attempts to get the correct answer. 
In all of your responses, including the follow up ones, please only reply with the number of the sarcastic remark. Do not
copy the remark, or add any additional text.
        """
        user_content = f"""First, let's look at several examples for you to learn from.
First story:
{pair_first_content}
Answer: {pair_first.sarcastic_index + 1}

Second story:
{pair_second_content}
Answer: {pair_second.sarcastic_index + 1}

Now, let's move on to the story you will be tested on.
The story is as follows:
'''
{story_content}
'''
Answer:
        """
        chat_messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]
        response = request_from_model(chat_messages)
        correct, text, explanation = story.check_model_output(response)
        story_results[f"Attempt {attempt_num}"] = {
            "Correct": correct,
            "Response": text,
            "Model Response": response,
            "Explanation": explanation
        }
        while not correct:
            attempt_num += 1
            # If the model would have to make more attempts than there are possible remarks, then it is considered
            # to have failed the story
            if attempt_num == len(story.possible_remarks):
                break
            chat_messages.append({"role": "assistant", "content": response})
            chat_messages.append({"role": "user", "content": "Wrong answer. "
                                                             "Reason: " + explanation +
                                                             " Please try again. Remember to reply only with the number of the sarcastic remark."
                                                             "Do not apologize, explain , or ask questions. Your response must be a single number, and nothing else."})
            response = request_from_model(chat_messages)
            correct, text, explanation = story.check_model_output(response)
            story_results[f"Attempt {attempt_num}"] = {
                "Correct": correct,
                "Response": text,
                "Model Response": response,
                "Explanation": explanation
            }
        story_results["Correct on Attempt"] = attempt_num if correct else -1

        results_dict["Results"].append(story_results)
        print(f"Story {i + 1} completed, {f'correct on attempt {attempt_num}' if correct else 'failed'}.")
    with open("results/results_few_shot_" + version_type + ".json", "w") as file:
        json.dump(results_dict, file)


def few_shot_chain_of_thought(version_type: str, story_collection: StoryCollection):
    """
    Tests the model on few shot prompting, where the model is given some examples of sarcastic remarks before being tested.
    In this version, the model is also requested to make its thought process explicit.
    :param version_type:
    :param story_collection:
    :return:
    """
    results_dict = {
        "Version Type": version_type,
        "Results": []
    }

    for i, story in enumerate(story_collection):
        attempt_num = 1
        story_results = {
            "Title": story_collection[i].title,
        }
        paired_indexes = random.sample(range(len(story_collection)), 2)
        while i in paired_indexes:
            paired_indexes = random.sample(range(len(story_collection)), 2)
        pair_first = story_collection[paired_indexes[0]]
        pair_second = story_collection[paired_indexes[1]]
        if version_type == "base":
            story_content = story.get_base_version_string_for_model()
            pair_first_content = pair_first.get_base_version_string_for_model()
            pair_second_content = pair_second.get_base_version_string_for_model()
        elif version_type == "detailed":
            story_content = story.get_detailed_version_string_for_model()
            pair_first_content = pair_first.get_detailed_version_string_for_model()
            pair_second_content = pair_second.get_detailed_version_string_for_model()
        elif version_type == "novel":
            story_content = story.get_novel_version_string_for_model()
            pair_first_content = pair_first.get_novel_version_string_for_model()
            pair_second_content = pair_second.get_novel_version_string_for_model()
        else:
            raise ValueError("Invalid version type")
        pair_first_explanations = pair_first.get_explanations()
        pair_second_explanations = pair_second.get_explanations()
        system_content = """You will be presented with a story, followed by a list of possible remarks the character in the story could make.
You will be presented with a story, followed by a list of possible remarks the character in the story could make.
Your task is to choose the sarcastic remark from the list.
Show your thought process while doing so.
Your answers will be checked automatically, and so it is of paramount importance that you heed the following instruction:
Make sure that the very last letter of your response is the number of the remark that you believe is sarcastic, or the 
very last letter is that number followed by a single period.
Failure to do so will result in an automatic failure, and you will be penalized.
        """
        user_content = f"""First, let's look at several examples for you to learn from.
First story:
{pair_first_content}
Thought process: {pair_first_explanations}
Therefore, the answer is {pair_first.sarcastic_index + 1}

Second story:
{pair_second_content}
Thought process: {pair_second_explanations}
Therefore, the answer is {pair_second.sarcastic_index + 1}

Now, let's move on to the story you will be tested on.
The story is as follows:
'''
{story_content}
'''
Thought process:
        """

        chat_messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]
        response = request_from_model(chat_messages)
        # Extract the last letter of the response if it is a number, otherwise extract the last sentence
        response = response.strip()
        response = response.replace(".", "")
        response = response[-1] if response[-1].isdecimal() else response.split("\n")[-1]
        correct, text, explanation = story.check_model_output(response)
        story_results[f"Attempt {attempt_num}"] = {
            "Correct": correct,
            "Response": text,
            "Model Response": response,
            "Explanation": explanation
        }
        while not correct:
            attempt_num += 1
            # If the model would have to make more attempts than there are possible remarks, then it is considered
            # to have failed the story
            if attempt_num == len(story.possible_remarks):
                break
            chat_messages.append({"role": "assistant", "content": response})
            chat_messages.append({"role": "user", "content": "Wrong answer. "
                                                             "Reason: " + explanation +
                                                             " Please try again. Remember that the last letter of your "
                                                             "response must be the number of the remark that you believe is sarcastic."})
            response = request_from_model(chat_messages)
            response = response.strip()
            response = response.replace(".", "")
            response = response[-1] if response[-1].isdecimal() else response.split("\n")[-1]
            correct, text, explanation = story.check_model_output(response)
            story_results[f"Attempt {attempt_num}"] = {
                "Correct": correct,
                "Response": text,
                "Model Response": response,
                "Explanation": explanation
            }
        story_results["Correct on Attempt"] = attempt_num if correct else -1

        results_dict["Results"].append(story_results)
        print(f"Story {i + 1} completed, {f'correct on attempt {attempt_num}' if correct else 'failed'}.")
    with open("results/results_few_shot_chain_of_thought_" + version_type + ".json", "w") as file:
        json.dump(results_dict, file)


def few_shot_chain_of_thought_with_coreference(version_type: str, story_collection: StoryCollection):
    """
    Tests the model on few shot chain of thought prompting, where the model is given some examples of sarcastic remarks before being tested.
    In this version, the model is also requested to make its thought process explicit, as well as provided with
    the coreferences other stories, to help it perform coreference analysis and understand the context of the story.
    :param version_type:
    :param story_collection:
    :return:
    """
    print(f"Starting few shot, chain of thought with coreference analysis, version type: {version_type}...")
    nlp = spacy.load('en_core_web_trf')
    nlp.add_pipe('coreferee')
    results_dict = {
        "Version Type": version_type,
        "Results": []
    }

    for i, story in enumerate(story_collection):
        attempt_num = 1
        story_results = {
            "Title": story_collection[i].title,
        }
        paired_indexes = random.sample(range(len(story_collection)), 2)
        while i in paired_indexes:
            paired_indexes = random.sample(range(len(story_collection)), 2)
        pair_first = story_collection[paired_indexes[0]]
        pair_second = story_collection[paired_indexes[1]]
        if version_type == "base":
            story_content = story.get_base_version_string_for_model()
            pair_first_content = pair_first.get_base_version_string_for_model()
            pair_second_content = pair_second.get_base_version_string_for_model()
            first_story_text = pair_first.base_version
            second_story_text = pair_second.base_version
        elif version_type == "detailed":
            story_content = story.get_detailed_version_string_for_model()
            pair_first_content = pair_first.get_detailed_version_string_for_model()
            pair_second_content = pair_second.get_detailed_version_string_for_model()
            first_story_text = pair_first.detailed_version
            second_story_text = pair_second.detailed_version
        elif version_type == "novel":
            story_content = story.get_novel_version_string_for_model()
            pair_first_content = pair_first.get_novel_version_string_for_model()
            pair_second_content = pair_second.get_novel_version_string_for_model()
            first_story_text = pair_first.novel_version
            second_story_text = pair_second.novel_version
        else:
            raise ValueError("Invalid version type")
        pair_first_explanations = pair_first.get_explanations()
        pair_second_explanations = pair_second.get_explanations()

        pair_first_coref = nlp(first_story_text)
        pair_second_coref = nlp(second_story_text)


        # Format the coreference chains for the model
        pair_first_coref_pretty = pair_first_coref._.coref_chains.pretty_representation
        num_chains_first = len(pair_first_coref._.coref_chains)
        pair_second_coref_pretty = pair_second_coref._.coref_chains.pretty_representation
        num_chains_second = len(pair_second_coref._.coref_chains)
        # Pretty representation has a single line, of the form: "0: word1(1), word2(2), word3(5), 1: word4(7), word5(13)"
        # We need to split this into multiple lines, each line corresponding to a coreference cluster
        for j in range(1, num_chains_first):
            pair_first_coref_pretty = pair_first_coref_pretty.replace(f"{i}: ", f"\n{i}: ")
        for j in range(1, num_chains_second):
            pair_second_coref_pretty = pair_second_coref_pretty.replace(f"{i}: ", f"\n{i}: ")


        system_content = """You will be presented with a story, followed by a list of possible remarks the character in the story could make.
You will be presented with a story, followed by a list of possible remarks the character in the story could make.
Your task is to choose the sarcastic remark from the list.
Perform coreference analysis on the story to better understand the context, then show your thought process when you reason through the possible remarks.
Your answers will be checked automatically, and so it is of paramount importance that you heed the following instruction:
Make sure that the very last letter of your response is the number of the remark that you believe is sarcastic, or the 
very last letter is that number followed by a single period.
Failure to do so will result in an automatic failure, and you will be penalized.
        """

        user_content = f"""First, let's look at several examples for you to learn from.
First story:
{pair_first_content}
Observe the coreferences in the story, to better understand the context.
The numbers at the beginning of each line indicate the coreference cluster that the words belongs to, while the numbers in the brackets next to each word indicates the index of the word in the story. Both use 0-indexing.
The coreferences are as follows:
{pair_first_coref_pretty}

Logical reasoning about story and remarks: {pair_first_explanations}
Therefore, the answer is {pair_first.sarcastic_index + 1}

Second story:
{pair_second_content}
Observe the coreferences in the story, to better understand the context.
The numbers at the beginning of each line indicate the coreference cluster that the words belongs to, while the numbers in the brackets next to each word indicates the index of the word in the story. Both use 0-indexing.
The coreferences are as follows:
{pair_second_coref_pretty}

Logical reasoning about story and remarks: {pair_second_explanations}
Therefore, the answer is {pair_second.sarcastic_index + 1}

Now, let's move on to the story you will be tested on.
The story is as follows:
'''
{story_content}
'''
Observe the coreferences in the story, to better understand the context:
        """
        chat_messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]
        response = request_from_model(chat_messages)
        # Extract the last letter of the response if it is a number, otherwise extract the last sentence
        response = response.strip()
        response = response.replace(".", "")
        response = response[-1] if response[-1].isdecimal() else response.split("\n")[-1]
        correct, text, explanation = story.check_model_output(response)
        story_results[f"Attempt {attempt_num}"] = {
            "Correct": correct,
            "Response": text,
            "Model Response": response,
            "Explanation": explanation
        }
        while not correct:
            attempt_num += 1
            # If the model would have to make more attempts than there are possible remarks, then it is considered
            # to have failed the story
            if attempt_num == len(story.possible_remarks):
                break
            chat_messages.append({"role": "assistant", "content": response})
            chat_messages.append({"role": "user", "content": "Wrong answer. "
                                                             "Reason: " + explanation +
                                                             " Please try again. Remember that the last letter of your "
                                                             "response must be the number of the remark that you believe is sarcastic."})
            response = request_from_model(chat_messages)
            response = response.strip()
            response = response.replace(".", "")
            response = response[-1] if response[-1].isdecimal() else response.split("\n")[-1]
            correct, text, explanation = story.check_model_output(response)
            story_results[f"Attempt {attempt_num}"] = {
                "Correct": correct,
                "Response": text,
                "Model Response": response,
                "Explanation": explanation
            }
        story_results["Correct on Attempt"] = attempt_num if correct else -1

        results_dict["Results"].append(story_results)
        print(f"Story {i + 1} completed, {f'correct on attempt {attempt_num}' if correct else 'failed'}.")

    with open("results/results_few_shot_chain_of_thought_with_coreference_" + version_type + ".json", "w") as file:
        json.dump(results_dict, file)


def zero_shot_chain_of_thought(version_type: str, story_collection: StoryCollection):
    """
    Tests the model on zero shot chain of thought prompting, where the model is not given any examples of sarcastic remarks
    before being tested, but is requested to make its thought process explicit.
    :param version_type:
    :param story_collection:
    :return:
    """
    results_dict = {
        "Version Type": version_type,
        "Results": []
    }

    for i, story in enumerate(story_collection):
        attempt_num = 1
        story_results = {
            "Title": story_collection[i].title,
        }
        if version_type == "base":
            story_content = story.get_base_version_string_for_model()
        elif version_type == "detailed":
            story_content = story.get_detailed_version_string_for_model()
        elif version_type == "novel":
            story_content = story.get_novel_version_string_for_model()
        else:
            raise ValueError("Invalid version type")
        system_content = """You will be presented with a story, followed by a list of possible remarks the character in the story could make.
You will be presented with a story, followed by a list of possible remarks the character in the story could make.
Your task is to choose the sarcastic remark from the list.
Show your thought process while doing so.
Your answers will be checked automatically, and so it is of paramount importance that you heed the following instruction:
Make sure that the very last letter of your response is the number of the remark that you believe is sarcastic, or the 
very last letter is that number followed by a single period.
Failure to do so will result in an automatic failure, and you will be penalized.
        """
        user_content = f"""The story is as follows:
'''
{story_content}
'''
Use the following format to reply:
1 is sarcastic / not sarcastic, because: [reason], 2 is sarcastic / not sarcastic, because: [reason], etc.
Therefore, the answer is: 
"""
        chat_messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]
        response = request_from_model(chat_messages)
        # Extract the last letter of the response if it is a number, otherwise extract the last sentence
        response = response.strip()
        response = response.replace(".", "")
        response = response[-1] if response[-1].isdecimal() else response.split("\n")[-1]
        correct, text, explanation = story.check_model_output(response)
        story_results[f"Attempt {attempt_num}"] = {
            "Correct": correct,
            "Response": text,
            "Model Response": response,
            "Explanation": explanation
        }
        while not correct:
            attempt_num += 1
            # If the model would have to make more attempts than there are possible remarks, then it is considered
            # to have failed the story
            if attempt_num == len(story.possible_remarks):
                break
            chat_messages.append({"role": "assistant", "content": response})
            chat_messages.append({"role": "user", "content": "Wrong answer. "
                                                             "Reason: " + explanation +
                                                             " Please try again. Remember that the last letter of your "
                                                             "response must be the number of the remark that you believe is sarcastic."})
            response = request_from_model(chat_messages)
            response = response.strip()
            response = response.replace(".", "")
            response = response[-1] if response[-1].isdecimal() else response.split("\n")[-1]
            correct, text, explanation = story.check_model_output(response)
            story_results[f"Attempt {attempt_num}"] = {
                "Correct": correct,
                "Response": text,
                "Model Response": response,
                "Explanation": explanation
            }
        story_results["Correct on Attempt"] = attempt_num if correct else -1

        results_dict["Results"].append(story_results)
        print(f"Story {i + 1} completed, {f'correct on attempt {attempt_num}' if correct else 'failed'}.")

    with open("results/results_zero_shot_chain_of_thought_" + version_type + ".json", "w") as file:
        json.dump(results_dict, file)

