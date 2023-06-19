import random
import argparse

def play_game(start, end, max_guesses):
    secret_number = random.randint(start, end)
    guesses_taken = 0

    while guesses_taken < max_guesses:
        guess = int(input("Enter your guess: "))

        if guess < secret_number:
            print("Enter a higher number.")
        elif guess > secret_number:
            print("Enter a lower number.")
        else:
            print("Congratulations! You guessed the correct number.")
            return

        guesses_taken += 1

    print("Game over. You ran out of guesses.")