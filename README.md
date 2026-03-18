# Game Glitch Investigator: The Impossible Guesser

## The Situation

An AI was asked to build a simple "Number Guessing Game" using Streamlit. It wrote the code, ran away, and the game was unplayable:

- You couldn't win because hints pointed the wrong direction.
- The scoring system was inconsistent.
- The secret number's type flipped between int and string on alternating attempts.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`
3. Run tests: `python -m pytest tests/ -v`

## Your Mission (Completed)

1. **Played the game** — observed bugs through the Developer Debug Info panel.
2. **Found the State Bug** — the secret number wasn't changing on submit (session state was handled), but its *type* was flipping between `int` and `str` on even attempts.
3. **Fixed the Logic** — corrected the backwards Higher/Lower hints, removed the type-flipping bug, fixed inconsistent scoring, and corrected the off-by-one attempt counter.
4. **Refactored & Tested** — moved all game logic into `logic_utils.py` and wrote 22 pytest cases covering all functions and edge cases.

## Document Your Experience

- **Game's purpose:** A number guessing game where the player picks a difficulty, gets a range, and tries to guess the secret number within a limited number of attempts. The game provides Higher/Lower hints and tracks a score.
- **Bugs found:**
  1. Hint messages were swapped ("Go HIGHER!" shown when guess was too high).
  2. On even attempts, `secret` was cast to `str`, breaking comparisons.
  3. Score formula for "Too High" added +5 on even attempts instead of always subtracting.
  4. Hard difficulty range (1-50) was easier than Normal (1-100).
  5. Attempts initialized to 1 instead of 0 (off-by-one).
  6. Info banner hardcoded "between 1 and 100" regardless of difficulty.
  7. Invalid guesses still consumed an attempt.
  8. Win score formula used `attempt_number + 1`, double-counting.
- **Fixes applied:**
  - Swapped hint messages so "Too High" says "Go LOWER!" and vice versa.
  - Removed the `str()` conversion and added `int()` casts in `check_guess` for robustness.
  - Made scoring consistently subtract 5 for wrong guesses.
  - Changed Hard range to 1-200.
  - Fixed attempts to start at 0; invalid guesses no longer consume attempts.
  - Info banner now uses dynamic `low` and `high` values.
  - Removed the `+1` from the win score formula.

## Demo

- Screenshot of pytest results (22/22 passing):

```
tests/test_game_logic.py::test_winning_guess PASSED
tests/test_game_logic.py::test_guess_too_high PASSED
tests/test_game_logic.py::test_guess_too_low PASSED
tests/test_game_logic.py::test_hint_message_on_too_high PASSED
tests/test_game_logic.py::test_hint_message_on_too_low PASSED
tests/test_game_logic.py::test_winning_message PASSED
tests/test_game_logic.py::test_parse_valid_integer PASSED
tests/test_game_logic.py::test_parse_float_string PASSED
tests/test_game_logic.py::test_parse_empty_string PASSED
tests/test_game_logic.py::test_parse_none PASSED
tests/test_game_logic.py::test_parse_non_numeric PASSED
tests/test_game_logic.py::test_score_on_win_first_attempt PASSED
tests/test_game_logic.py::test_score_on_win_late_attempt PASSED
tests/test_game_logic.py::test_score_on_too_high PASSED
tests/test_game_logic.py::test_score_on_too_low PASSED
tests/test_game_logic.py::test_score_penalty_consistent_across_attempts PASSED
tests/test_game_logic.py::test_easy_range PASSED
tests/test_game_logic.py::test_normal_range PASSED
tests/test_game_logic.py::test_hard_range_is_harder_than_normal PASSED
tests/test_game_logic.py::test_negative_number_guess PASSED
tests/test_game_logic.py::test_very_large_guess PASSED
tests/test_game_logic.py::test_guess_of_one PASSED
======================== 22 passed in 0.03s ========================
```

## Stretch Features

- Challenge 1 (Advanced Edge-Case Testing) completed: tests include negative numbers, very large values, and boundary guesses.
