from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# ── check_guess tests ──────────────────────────────────────────────

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_hint_message_on_too_high():
    _, message = check_guess(75, 50)
    assert "LOWER" in message


def test_hint_message_on_too_low():
    _, message = check_guess(25, 50)
    assert "HIGHER" in message


def test_winning_message():
    _, message = check_guess(42, 42)
    assert "Correct" in message


# ── parse_guess tests ──────────────────────────────────────────────

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_float_string():
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None


def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert "Enter" in err


def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None


def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert "not a number" in err


# ── update_score tests ─────────────────────────────────────────────

def test_score_on_win_first_attempt():
    score = update_score(0, "Win", 1)
    assert score == 90


def test_score_on_win_late_attempt():
    score = update_score(0, "Win", 10)
    assert score == 10


def test_score_on_too_high():
    score = update_score(100, "Too High", 1)
    assert score == 95


def test_score_on_too_low():
    score = update_score(100, "Too Low", 1)
    assert score == 95


def test_score_penalty_consistent_across_attempts():
    score_even = update_score(50, "Too High", 2)
    score_odd = update_score(50, "Too High", 3)
    assert score_even == score_odd == 45


# ── get_range_for_difficulty tests ─────────────────────────────────

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


def test_hard_range_is_harder_than_normal():
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high


# ── edge-case tests ───────────────────────────────────────────────

def test_negative_number_guess():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5


def test_very_large_guess():
    outcome, _ = check_guess(999999, 50)
    assert outcome == "Too High"


def test_guess_of_one():
    outcome, _ = check_guess(1, 1)
    assert outcome == "Win"
