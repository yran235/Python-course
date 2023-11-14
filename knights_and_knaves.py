# Written by Yuan for COMP9021
#

import sys
from os.path import exists
from pathlib import Path
from collections import defaultdict
from itertools import product

names = []
roles_list = ['Knave', 'Knight']
role_of_everyone = []
speaker_and_quote = defaultdict(list)

def get_file_name():
    file_name = input('Which text file do you want to use for the puzzle? '
                    ).removesuffix('\n')
    if not exists(file_name):
        print('Incorrect input, giving up.')
        sys.exit()
    return file_name

def get_puzzle(file_name):
    L = ''
    with open(file_name) as file:
        for line in file:
            if not line.isspace():
                L = L + line.replace('\n', ' ')
    return L

def split_words_and_delet_marks(text):
    text_by_word = text.split()
    result = []
    for word in text_by_word:
        word = strip_all_marks(word)
        result.append(word)
    return result

def get_sorted_names(text):
    i = 0
    sorted_names = []
    while i < len(text):
        if text[i] == 'Sir':
            sorted_names.append(text[i+1])
        elif text[i] == 'Sirs':
            b = 1
            while i < len(text):
                sorted_names.append(text[i+b])
                if text[i+b+1] == 'and' or text[i+b+1] == 'or':
                    sorted_names.append(text[i+b+2])
                    break
                b += 1
        i += 1
    sorted_names = sorted(set(sorted_names))
    return sorted_names

def puzzle_sentence_split(text):
    sentences = []
    sentence = []
    for word in text.split():
        sentence.append(word)
        if word.endswith(('.', '!', '?', '."', '?"', '!"')):
            sentences.append(' '.join(sentence))
            sentence = []
    return sentences
    
def strip_all_marks(string):
    stripped_string = string.strip(''.join([c for c in string if not c.isalpha()]))
    return stripped_string

def get_speakers_and_quotes():
    for sentence in puzzle_sentences:
        words = sentence.split()
        speaker = None
        quote = ''
        in_quote = False
        i = 0
        current_quote = ''
        while i < len(words):
            if '"' in words[i]:
                if in_quote:
                    current_quote += ' '+words[i]
                    quote = current_quote
                    current_quote = ''
                    in_quote = False
                else:
                    in_quote = True
            if in_quote:
                    current_quote += ' '+words[i]
            if words[i] == 'Sir' and not in_quote:
                for name in names:
                    if words[i+1].startswith(name):
                        speaker = name
                        break
            i += 1
        if speaker and quote:
            quote = strip_all_marks(quote)
            speaker_and_quote[speaker].append(quote)

def give_results(result):
    print('The Sirs are: ' + ' '.join(names))
    if not result:
        print('There is no solution.')
    elif result == 1:
        print('There is a unique solution:')
        i = 0
        while i<len(names):
            print('Sir '+names[i]+' is a '+roles_list[role_of_everyone[0][i]]+'.')
            i += 1
    else:
        print('There are', str(len(role_of_everyone)), 'solutions.')

def solve_puzzle():
    for speaker, quotes in speaker_and_quote.items():
        for quote in quotes:
            Q = split_words_and_delet_marks(quote)
            mentioned_names = []
        
            if 'us' in Q:
                for name in names:
                    mentioned_names.append(name)
            else:    
                for name in names:
                    if name in Q:
                        mentioned_names.append(name)
                    elif name == speaker and 'I' in Q:
                        mentioned_names.append(speaker)
            to_remove = []
            for current_roles in role_of_everyone:
                sum_of_mentioned_names = 0
                for name1 in mentioned_names:
                    sum_of_mentioned_names += current_roles[names.index(name1)]
                if current_roles == (0,1,1,0):
                    pass
        
                if "least" in Q:
                    if 'Knave' in Q:
                        if current_roles[names.index(speaker)] == 1 and sum_of_mentioned_names < len(mentioned_names):
                            continue
                        elif current_roles[names.index(speaker)] == 0 and sum_of_mentioned_names == len(mentioned_names):
                            continue
                    else:
                        if current_roles[names.index(speaker)] == 1 and sum_of_mentioned_names > 0:
                            continue
                        elif  current_roles[names.index(speaker)] == 0 and sum_of_mentioned_names == 0:
                            continue
        
                elif "most" in Q:
                    if 'Knave' in Q:
                        if current_roles[names.index(speaker)] == 1 and sum_of_mentioned_names >= len(mentioned_names)-1:
                            continue
                        elif current_roles[names.index(speaker)] == 0 and sum_of_mentioned_names < len(mentioned_names)-1:
                            continue
                    else:
                        if current_roles[names.index(speaker)] == 1 and sum_of_mentioned_names <= 1:
                            continue
                        elif current_roles[names.index(speaker)] == 0 and sum_of_mentioned_names > 1:
                            continue
        
                elif "exactly" in Q or "Exactly" in Q:
                    if 'Knave' in Q:
                        if current_roles[names.index(speaker)] == 1 and sum_of_mentioned_names == len(mentioned_names)-1:
                            continue
                        elif current_roles[names.index(speaker)] == 0 and sum_of_mentioned_names != len(mentioned_names)-1:
                            continue
                    else:
                        if current_roles[names.index(speaker)] == 1 and sum_of_mentioned_names == 1:
                            continue
                        elif current_roles[names.index(speaker)] == 0 and sum_of_mentioned_names != 1:
                            continue
        
                elif "all" in Q or "All" in Q:
                    if 'Knaves' in Q:
                        if current_roles[names.index(speaker)] == 0 and sum(i for i in current_roles) > 0:
                            continue
                    else:
                        if sum(i for i in current_roles) == len(current_roles) or current_roles[names.index(speaker)] == 0:
                            continue
        
                elif Q[1] == "am":
                    if 'Knave' in Q:
                        role_of_everyone.clear()
                        return 0
                    else:
                        continue
        
                elif Q[0] == "Sir" and Q[2] == "is":
                    if 'Knave' in Q:
                        if current_roles[names.index(mentioned_names[0])] + current_roles[names.index(speaker)] == 1:
                            continue
                    else:
                        if current_roles[names.index(mentioned_names[0])] + current_roles[names.index(speaker)] != 1:
                            continue
                
                elif 'or' in Q:
                    if 'Knave' in Q:
                        if current_roles[names.index(speaker)] == 1 and sum_of_mentioned_names < len(mentioned_names):
                            continue
                        elif current_roles[names.index(speaker)] == 0 and sum_of_mentioned_names == len(mentioned_names):
                            continue
                    else:
                        if current_roles[names.index(speaker)] == 1 and sum_of_mentioned_names > 0:
                            continue
                        elif current_roles[names.index(speaker)] == 0 and sum_of_mentioned_names == 0:
                            continue
        
                elif 'and' in Q and 'are' in Q:
                    if 'Knaves' in Q:
                        if current_roles[names.index(speaker)] == 1 and sum_of_mentioned_names == 0:
                            continue
                        elif current_roles[names.index(speaker)] == 0 and sum_of_mentioned_names > 0:
                            continue
                    else:
                        if current_roles[names.index(speaker)] == 1 and sum_of_mentioned_names == len(mentioned_names):
                            continue
                        elif current_roles[names.index(speaker)] == 0 and sum_of_mentioned_names < len(mentioned_names):
                            continue

                to_remove.append(role_of_everyone.index(current_roles))
        
            for i in reversed(to_remove):
                role_of_everyone.pop(i)
        
    return len(role_of_everyone)

# file_name = get_file_name()
file_name = Path('E:/python_code/assignment1/test_cases/logic_puzzle_40.txt')
puzzles = get_puzzle(file_name)

puzzles_by_word = split_words_and_delet_marks(puzzles)
names = get_sorted_names(puzzles_by_word)
role_of_everyone = list(product([0, 1], repeat=len(names)))

puzzle_sentences = puzzle_sentence_split(puzzles)
get_speakers_and_quotes()

result = solve_puzzle()
give_results(result)