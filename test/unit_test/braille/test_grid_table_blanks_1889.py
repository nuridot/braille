"""원장 C-220(B-21 #1889) — 격자 표(칸 구분선 ⠐⠐⠐)는 위아래 빈 줄 없이 붙고, 칸 구분선 없는 표(상자형 지문 · 펼친 꼴)는 종전대로 띈다.

근거: 지침 표 예(도서-3-2 · 3-4 · 3-5 · 3-6 짝)와 2027 gold — 우리 격자 표 자리 앞 붙음 225 · 빈 줄 26 · 뒤 211 : 38,
구분선 없는 표 자리 앞 222 : 290 · 뒤 62 : 303(띄움). 셀은 지어낸 것이다.
"""
from semojum_braille.encoder import layout_braille as LB

_TOP = LB._BOX_LEVELS[1]["top"][0] + LB._BOX_LEVELS[1]["top"][1] * (LB._COLS - 2) + LB._BOX_LEVELS[1]["top"][2]
_BOT = LB._BOX_LEVELS[1]["bottom"][0] + LB._BOX_LEVELS[1]["bottom"][1] * (LB._COLS - 2) + LB._BOX_LEVELS[1]["bottom"][2]
_SEP = "⠐" * LB._COLS


def _around(lines, monkeypatch, switch=None):
    if switch:
        monkeypatch.setenv("TABLE_BLANKS", switch)
    else:
        monkeypatch.delenv("TABLE_BLANKS", raising=False)
    lb = LB.LayoutBraille.__new__(LB.LayoutBraille)
    formatted = [(0, "text", ["⠁⠁"]), (0, "table", lines), (0, "text", ["⠃⠃"])]
    body = [l for page in lb._assemble_pages(formatted, "", "", 1) for l in page]
    return body[body.index(lines[0]) - 1], body[body.index(lines[-1]) + 1]


def test_격자_표는_붙는다(monkeypatch):
    assert _around([_TOP, "⠞⠞", _SEP, "⠞⠞", _BOT], monkeypatch) == ("⠁⠁", "⠃⠃")


def test_구분선_없는_표는_띈다(monkeypatch):
    assert _around([_TOP, "⠞⠞", "⠞⠞", _BOT], monkeypatch) == ("", "")


def test_되돌리기_스위치는_격자_표도_띈다(monkeypatch):
    assert _around([_TOP, "⠞⠞", _SEP, "⠞⠞", _BOT], monkeypatch, "1") == ("", "")

