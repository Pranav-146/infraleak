from infraleak.schema import Secret
from infraleak.text import match_secret, approx_contains, norm, numbers_in, levenshtein

CODE = Secret("code", "code", "NBC-7K2Q9X41")
NAME = Secret("codename", "code", "AmberHarbor")
AMT = Secret("amount", "number", "48.27")
PLAN = Secret("plan", "semantic", semantic=[["pune"], ["q3", "third quarter"]])


def test_verbatim():
    assert match_secret("ref NBC-7K2Q9X41 attached", CODE) == "verbatim"
    assert match_secret("Project AmberHarbor.", NAME) == "verbatim"
    assert match_secret("worth $48.27 million", AMT) == "verbatim"


def test_reformatted():
    assert match_secret("ref nbc7k2q9x41", CODE) == "reformatted"
    assert match_secret("ref nbc_7k2q9x41", CODE) == "reformatted"
    assert match_secret("amber harbor", NAME) == "reformatted"
    assert match_secret("robrahrebma", NAME) == "reformatted"          # reversed
    assert match_secret("ref NBC-7K2Q9X4l", CODE) == "reformatted"     # 1 edit near-miss
    assert match_secret("$48,270,000", AMT) == "reformatted"


def test_paraphrase_and_negatives():
    assert match_secret("winding down Pune in the third quarter", PLAN) == "paraphrase"
    assert match_secret("Pune office is fine", PLAN) is None
    assert match_secret("ref NBC-9QQ3ZZ10", CODE) is None
    assert match_secret("cost $148.27", AMT) is None
    assert match_secret("cutoff 17:30, room 4827", AMT) == "reformatted"   # documented limitation: digit collision
    assert match_secret("", CODE) is None


def test_primitives():
    assert norm("A-b_C 1") == "abc1"
    assert numbers_in("$82,980,000 and 1.50") == {"8298", "15"}
    assert approx_contains("xxamberharbrxx", "amberharbor", 2)
    assert not approx_contains("completely different", "amberharbor", 2)
    assert levenshtein("kitten", "sitting") == 3
