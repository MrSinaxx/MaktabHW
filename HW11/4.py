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
    print(f"The secret number was {secret_number}")
    


def main():
    parser = argparse.ArgumentParser(description='Number Guessing Game')
    parser.add_argument('-s', dest='start', type=int, default=0, help='start range')
    parser.add_argument('-e', dest='end', type=int, default=100, help='end range')
    parser.add_argument('-g', dest='max_guesses', type=int, default=5, help='maximum number of guesses')

    args = parser.parse_args()

    play_game(args.start, args.end, args.max_guesses)

if __name__ == '__main__':
    main()