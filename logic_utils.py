def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Swapped Hard range to 1-200 so it's actually harder than Normal (1-100).
    # Previously Hard was 1-50, which was easier. Refactored from app.py using Cursor Agent mode.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome: "Win", "Too High", or "Too Low"
    """
    # FIX: Corrected the hint messages — previously "Too High" said "Go HIGHER!"
    # and "Too Low" said "Go LOWER!", which was backwards and misleading.
    # Refactored from app.py into logic_utils.py using Cursor Agent mode.
    if int(guess) == int(secret):
        return "Win", "🎉 Correct!"

    if int(guess) > int(secret):
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: Removed the +1 offset in the win formula (was double-counting attempts)
    # and removed the inconsistent even/odd bonus on "Too High" outcomes.
    # Refactored from app.py using Cursor Agent mode.
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
