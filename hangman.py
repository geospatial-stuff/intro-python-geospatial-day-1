# Hangman script to demonstrate conditionals
#
# David O'Sullivan
# Originally written March 2005
# Lightly modified several times since

# Updated to Python 3 March 2019

# the random module allows for randomization functions
import random

def get_matches(letter, word):
    matches = [i for i in range(len(word)) if word[i] == letter]
    return matches

def replace_letters(indexes, letter, word):
    w = list(word)
    for i in indexes:
        w[i] = letter
    return "".join(w)

if __name__ == "__main__":
    # open and read a file of words
    with open("hangmanWords.txt") as f:
        wordlist = f.readlines()

    # strip of trailing linefeed and convert to upper case
    wordlist = [w.strip().upper() for w in wordlist]

    max_guesses = 10

    # Whole program nested in infinite loop
    # break from loop to end program
    while True:
        wrong_guesses = 0
        unused_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # select a word at random from the file
        word = random.choice(wordlist).upper()
        # make a string of the same number of dashes
        user_word = '-' * len(word)
        # Greet the player and tell them what to do
        print(f"""\nI'm thinking of a word.  You have {str(max_guesses)} wrong guesses to get all its letters.\nI'll let you know when you guess a letter right.  You can enter more than one letter each time.\n\n
        Enter * to end.\n\nThe word looks like this:\n\n\t{user_word}
        """)

        while True:
            # Get the next guess from the player
            guesses = input(f"Wrong guesses   : {wrong_guesses}\n" +
                            f"Unused letters  : {unused_letters}\n" +
                            "Enter next guess: ")
            # handle the * case -- which indicates player wants to finish
            if guesses == "*":
                print()
                break  # exits the game guess loop
            if guesses == "":
                print()
                continue

            # convert the guess to upper case
            guesses = guesses.upper()
            # check that guesses are letters
            if not guesses.isalpha():
                print("Your guess should be all letters.\n")
                continue
            guess_list = [g for g in guesses if g in unused_letters]
            if len(guess_list) == 0:
                print("You have already tried all those letters. Try again.\n")
                continue
            print('\n')

            correct_guesses = 0
            # remove duplicates by converting to a set
            for guess in set(guess_list):
                # update the unused letters list
                unused_letters = unused_letters.replace(guess, '-')
                # make a list from the current guess word
                matches = get_matches(guess, word)
                if len(matches) > 0:
                    correct_guesses += len(matches)
                    user_word = replace_letters(matches, guess, user_word)
                else:
                    wrong_guesses += 1

            # Tell user what happened
            if correct_guesses > 0:
                print(f"Good guess. Progress so far:\n\n\t{user_word}\n")
                if user_word == word:
                    print(f"""Congratulations! You got the word with just {wrong_guesses} guess{'es' if wrong_guesses > 1 else ''}!\n""")
                    break
            else:
                print(f"""The word doesn't contain {guesses}. Try again.\n\n\t{user_word}\n""")
                if wrong_guesses > max_guesses:
                    print(f"""Bad luck, you ran out of guesses. The word was: {word.upper()}\n""")
                    break

        again = input("Another game (Y/N)? ")
        if again.lower() == "y":
            print()
            continue  # goes again
        else:
            print("\nBye!\n")
            break  # exits completely
