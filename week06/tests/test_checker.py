"""No-key tests for the checker: the code that compares a critique with the requirements
(spec.md, Week 6 behaviors 1-8).

    python3 -m pytest week06/tests -v     # from the repository root; well under a second
"""
from critique import check, disagreements, extract_json, text_matches

REQS = ["There is exactly one mug in the image", "The mug is white", "The background is plain white"]


def critique_with(*met):
    return {"checks": [{"requirement": r, "met": m, "evidence": "x"} for r, m in zip(REQS, met)]}


def test_all_met_is_ok():
    assert check(REQS, critique_with(True, True, True)) == {"ok": True, "problems": [], "unmet": [], "missing": [], "extra": []}


def test_unmet_requirement_is_reported_by_name():
    result = check(REQS, critique_with(True, False, True))
    assert not result["ok"]
    assert result["unmet"] == ["The mug is white"]


def test_anything_but_true_is_unmet():
    c = critique_with(True, True, True)
    c["checks"][2]["met"] = "yes"                       # a string is not a verdict
    assert check(REQS, c)["unmet"] == ["The background is plain white"]


def test_missing_requirement_is_a_problem_even_if_the_rest_pass():
    partial = {"checks": [{"requirement": REQS[0], "met": True}, {"requirement": REQS[1], "met": True}]}
    result = check(REQS, partial)
    assert not result["ok"]
    assert result["missing"] == [REQS[2]]


def test_invented_requirement_is_flagged():
    c = critique_with(True, True, True)
    c["checks"].append({"requirement": "The lighting is dramatic", "met": True})
    result = check(REQS, c)
    assert result["extra"] == ["The lighting is dramatic"]
    assert not result["ok"]


def test_requirement_text_is_matched_loosely():
    c = {"checks": [{"requirement": "there is exactly one mug in the image.", "met": True},
                    {"requirement": "The mug is WHITE", "met": True},
                    {"requirement": "The background is plain white!", "met": True}]}
    assert check(REQS, c)["ok"]


def test_non_json_reply_is_a_failed_critique_not_a_crash():
    result = check(REQS, extract_json("Sorry, I can't see any image."))
    assert not result["ok"]
    assert result["missing"] == REQS
    assert check(REQS, extract_json(None))["ok"] is False


def test_json_without_a_checks_list_is_a_failed_critique():
    assert not check(REQS, {"verdict": "looks great"})["ok"]


def test_json_inside_prose_and_fences_is_extracted():
    text = 'Here you go:\n```json\n{"checks": [{"requirement": "a", "met": true}]}\n```\nHope that helps.'
    assert extract_json(text) == {"checks": [{"requirement": "a", "met": True}]}


def test_text_match_ignores_case_and_punctuation():
    assert text_matches("MORNING", "  morning. ")
    assert not text_matches("MORNING", "MORNlNG")        # lower-case L for I: the misread the code must catch
    assert not text_matches("MORNING", "MORNING COFFEE")  # extra words are a mismatch
    assert not text_matches("MORNING", None)


def test_disagreements_between_two_critics():
    a = [{"name": "mug-01", "critique": critique_with(True, True, True), "text_read": "MORNING"}]
    b = [{"name": "mug-01", "critique": critique_with(True, False, True), "text_read": "MORNlNG"}]
    d = disagreements(a, b)
    assert len(d) == 1
    assert {x["requirement"] for x in d[0]["diffs"]} == {REQS[1], "<text read>"}
    assert disagreements(a, a) == []
