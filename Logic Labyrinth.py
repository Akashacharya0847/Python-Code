import random


def generate_code():
    """Generate a unique 4-digit code (digits 1-6, no repeats)."""
    digits = [str(i) for i in range(1, 7)]
    random.shuffle(digits)
    return ''.join(digits[:4])


def get_feedback(secret, guess):
    """Return feedback: correct position (A), wrong position (B)."""
    a_count = sum(1 for i in range(4) if guess[i] == secret[i])
    b_count = sum(1 for digit in guess if digit in secret) - a_count
    return f"{a_count}A{b_count}B"


def play_game():
    secret = generate_code()
    score = 100  # Starting score
    attempts = 0
    max_attempts = 10

    print("🔍 Welcome to Logic Labyrinth!")
    print("Guess the 4-digit code (1-6, no repeats).")
    print("Feedback: XA YB (X=correct position, Y=present but wrong spot)\n")

    while attempts < max_attempts:
        guess = input(f"Attempt {attempts + 1}/{max_attempts} - Enter guess: ").strip()

        if len(guess) != 4 or not guess.isdigit():
            print("❌ Invalid: Must be 4 digits (1-6). Try again.\n")
            continue

        digits = set(guess)
        if len(digits) != 4 or not all(d in '123456' for d in guess):
            print("❌ Invalid: Digits 1-6, no repeats.\n")
            continue

        attempts += 1
        feedback = get_feedback(secret, guess)
        print(f"Feedback: {feedback}")

        if feedback == "4A0B":
            print(f"\n🎉 Victory! Code was {secret}")
            print(f"Attempts: {attempts} | Score: {score - (attempts - 1) * 5}")
            return

        score -= 5  # Penalty per attempt

        # Hint every 3 attempts
        if attempts % 3 == 0:
            hint_digit = random.choice(secret)
            print(f"💡 Hint: '{hint_digit}' is in the code.\n")

    print(f"\n💀 Game Over! Secret code: {secret}")
    print(f"Final Score: {max(score, 0)}")


if __name__ == "__main__":
    play_game()
