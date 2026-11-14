"""Text matching primitives used by the oracle (ground truth) and detectors."""
from __future__ import annotations
import re


def norm(s: str) -> str:
    """Lowercase, keep only [a-z0-9]."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def contains_verbatim(text: str, needle: str) -> bool:
    pat = r"(?<![A-Za-z0-9])" + re.escape(needle) + r"(?![A-Za-z0-9])"
    return re.search(pat, text, re.I) is not None


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def approx_contains(ntext: str, npat: str, k: int = 2) -> bool:
    """True if npat occurs in ntext with <= k edits (Sellers). Pattern must be >= 7 chars."""
    m = len(npat)
    if m < 7:
        return False
    parts = k + 1
    size = m // parts
    pieces = [npat[i * size:(i + 1) * size if i < parts - 1 else m] for i in range(parts)]
    if not any(p in ntext for p in pieces):  # pigeonhole prefilter
        return False
    col = list(range(m + 1))
    for ch in ntext:
        new = [0]
        for j in range(1, m + 1):
            new.append(min(col[j] + 1, new[j - 1] + 1, col[j - 1] + (npat[j - 1] != ch)))
        if new[m] <= k:
            return True
        col = new
    return False


_NUM = re.compile(r"\d[\d,._ ]*\d|\d")


def numbers_in(text: str) -> set[str]:
    """Digit strings of every number in text with separators removed and trailing zeros stripped."""
    out = set()
    for m in _NUM.finditer(text):
        d = re.sub(r"[^0-9]", "", m.group(0)).rstrip("0")
        if d:
            out.add(d)
    return out


RANK = {"verbatim": 0, "reformatted": 1, "paraphrase": 2}


def match_secret(text: str, secret) -> str | None:
    """Return flow class in {verbatim, reformatted, paraphrase} or None.

    secret.kind: code (identifier / codename), number (amount), semantic (keyword groups).
    """
    t = text or ""
    if secret.kind == "semantic":
        low = t.lower()
        if all(any(alt in low for alt in grp) for grp in secret.semantic):
            return "paraphrase"
        return None
    if contains_verbatim(t, secret.text):
        return "verbatim"
    if secret.kind == "number":
        want = re.sub(r"[^0-9]", "", secret.text).rstrip("0")
        return "reformatted" if want in numbers_in(t) else None
    n, nt = norm(secret.text), norm(t)
    if len(n) >= 7:
        if n in nt or n[::-1] in nt or approx_contains(nt, n, 2):
            return "reformatted"
    return None


def best_class(text: str, secrets) -> tuple[str | None, list[str]]:
    best, hit = None, []
    for s in secrets:
        c = match_secret(text, s)
        if c:
            hit.append(s.sid)
            if best is None or RANK[c] < RANK[best]:
                best = c
    return best, hit
