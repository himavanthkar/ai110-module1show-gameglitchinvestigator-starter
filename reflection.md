# Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the game, it looked like a normal Streamlit guessing game with a text input, submit button, and a debug panel. However, within a couple of guesses it became clear the game was deeply broken. **Bug 1: The hints were backwards** — when I guessed too high, the game said "Go HIGHER!" instead of "Go LOWER!", making it impossible to converge on the answer. **Bug 2: The secret number's type flipped on even attempts** — on every other guess, the secret was silently converted to a string (`str(secret)`), which caused comparisons to fail because Python compares strings and integers differently. **Bug 3: The score was inconsistent** — on even-numbered attempts, a "Too High" outcome actually *added* 5 points instead of subtracting, making the scoring unreliable. I also noticed the attempts counter started at 1 instead of 0, meaning the "Attempts left" display was always off by one, and the info banner always said "between 1 and 100" regardless of which difficulty was selected.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used **Claude** (via Cursor IDE) as my primary AI tool for this project. I referenced the full codebase context by pointing Claude at `app.py` and `logic_utils.py` together, and asked it to identify bugs, propose fixes, and refactor the game logic into `logic_utils.py` across multiple files in one step. I also used Claude's inline chat to highlight specific lines and ask "Explain this logic step-by-step" when I wasn't sure what a block of code was doing.

**Correct suggestion:** When I asked Claude to analyze the `check_guess()` function, it correctly identified that the hint messages were swapped — "Go HIGHER!" was paired with the `guess > secret` branch and "Go LOWER!" with `guess < secret`. Claude suggested flipping the messages so "Too High" shows "Go LOWER!" and "Too Low" shows "Go HIGHER!". I verified this by writing a pytest (`test_hint_message_on_too_high`) that checks `check_guess(60, 50)` returns a message containing "LOWER" — the test passed, confirming the fix was correct.

**Incorrect/misleading suggestion:** When I asked Claude about the type-flipping bug (where even-numbered attempts converted the secret to a string), it initially suggested simply removing the `str()` conversion on those lines without explaining *why* the original code had a `TypeError` catch in `check_guess` that attempted string comparison as a fallback. That catch was masking the real bug rather than fixing it. Claude's initial suggestion was technically correct in removing the symptom, but it didn't address the root cause — `check_guess` needed `int()` casts on both arguments to handle any type safely. I rejected the surface-level fix and instead asked Claude to also update `check_guess` to cast both inputs to `int`. I verified the full fix by running pytest with both integer and string inputs, and all tests passed.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed by using a two-step verification: first running targeted pytest cases, then manually playing the Streamlit app to confirm the user experience matched expectations.

For example, I wrote `test_hint_message_on_too_high` which calls `check_guess(75, 50)` and asserts that the returned message contains "LOWER". Before the fix, this test would have failed because the original code returned "Go HIGHER!" for a guess that was too high. After fixing the messages, the test passed, confirming the hints now point the player in the correct direction. I also wrote `test_score_penalty_consistent_across_attempts` which verifies that a "Too High" penalty is the same on both even and odd attempts — this caught the original bug where even attempts added points instead of subtracting.

The AI helped me design tests by suggesting edge cases I hadn't considered, like negative number inputs and very large guesses. It generated the test structure and I reviewed each assertion to make sure it tested the right behavior.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit works differently from a traditional app — every time you interact with the page (click a button, type in a field), the entire Python script runs again from top to bottom. This means any regular variable you create gets reset to its initial value on every interaction. To keep data between reruns (like the secret number, the score, or how many attempts you've made), you use `st.session_state`, which is like a persistent dictionary that survives reruns. If you write `secret = random.randint(1, 100)` without session state, the secret changes every time you click Submit. But with `if "secret" not in st.session_state: st.session_state.secret = random.randint(1, 100)`, it only generates once and stays the same until you explicitly reset it. This was the root cause of one of the biggest bugs — you have to guard every piece of persistent data with a session state check.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to carry forward is **writing targeted pytest cases immediately after fixing a bug**, before moving on. It forces me to confirm the fix actually works and creates a safety net if I accidentally break it later. I also liked the practice of separating logic from UI — putting pure functions in a utility module makes them independently testable.

Next time, I would be more skeptical of AI suggestions that only address symptoms rather than root causes. When the AI said "just remove the `str()` conversion," that was technically a fix, but it didn't address the fragile type handling in `check_guess`. I should always ask the AI "why was this code here in the first place?" before accepting a removal.

This project taught me that AI-generated code can look perfectly reasonable while hiding subtle logic bugs (like swapped hint messages or inconsistent scoring rules). The code ran without errors, but the *behavior* was wrong — and that's the hardest kind of bug to catch. It reinforced that I need to always test AI code against expected behavior, not just check that it runs.
