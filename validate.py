import csv, json, re, sys
from pathlib import Path
root = Path(__file__).parent
rows = json.loads((root / "words.json").read_text(encoding="utf-8"))
assert len(rows) == 1000, f"Expected 1000 cards, got {len(rows)}"
assert len({x["w"] for x in rows}) == 1000, "Duplicate headwords found"
assert sorted({x["day"] for x in rows}) == list(range(1, 21)), "Day numbering mismatch"
for day in range(1, 21):
    count = sum(1 for x in rows if x["day"] == day)
    assert count == 50, f"Day {day} has {count} cards"
for i, x in enumerate(rows, 1):
    assert all(x.get(k) for k in ("w", "r", "m", "p")), f"Empty field at row {i}"
    assert re.fullmatch(r"[\u3040-\u309F\u30A0-\u30FFー・]+", x["r"]), f"Non-kana reading at row {i}: {x['r']}"
html = (root / "index.html").read_text(encoding="utf-8")
assert "STORE='n1WordLibrary1000V2'" in html
assert "e.code==='Space'" in html and "ArrowRight" in html and "ArrowLeft" in html
assert html.count('"w":') == 1000
print("PASS: 1,000 unique cards; 20 Days × 50; all readings kana; keyboard handler present.")
