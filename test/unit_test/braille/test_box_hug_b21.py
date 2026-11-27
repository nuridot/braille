"""B-21 · 원장 C-217 — 점역자 주 줄 바로 뒤 글상자 · 상자 바로 뒤 출처 줄은 빈 줄 없이 붙는다.

「점자 도서 제작 지침」 1장 2절 5. 2)(6)(재추출 489~490행)은 글상자 위아래에 빈 줄을 두지만, 같은 지침의 그래프 · 표 예는 그래프 주 머리와
자료 상자 · 상자와 출처 줄을 붙인다. gold(2027 dev · val) 도 주 줄 → 위 테두리 6:0 · 아래 테두리 → 출처 · 자료 4:0 으로 붙인다. 글은 지어낸 것이다.
"""
from semojum_braille.encoder import layout_braille as lb
from semojum_braille.encoder.translator import translate_with_breaks

TOP = lb._BOX_LEVELS[1]["top"][0] + lb._BOX_LEVELS[1]["top"][1] * (lb._COLS - 2) + lb._BOX_LEVELS[1]["top"][2]
BOT = lb._BOX_LEVELS[1]["bottom"][0] + lb._BOX_LEVELS[1]["bottom"][1] * (lb._COLS - 2) + lb._BOX_LEVELS[1]["bottom"][2]


def _cells(text: str) -> str:
    return "".join(translate_with_breaks(text)[0])


def test_그래프_주_머리_뒤_상자는_붙는다():
    head = _cells("<!주>막대 그래프<!/주>:")
    assert lb._box_kind(TOP) == "top" and lb._is_tn_head_line(head)
    assert lb._hugs_prev(TOP, head)
    at, _lead, _tail = lb._box_blanks([head, TOP, _cells("가 10"), BOT], off=False)
    assert 1 not in at


def test_상자_뒤_출처_줄은_붙는다():
    src = _cells("출처: 가나 통계")
    assert lb._hugs_prev(src, BOT)
    at, _lead, _tail = lb._box_blanks([TOP, _cells("가 10"), BOT, src], off=False)
    assert 3 not in at


def test_그_밖의_글은_종전대로_띄운다():
    body = _cells("다음 글을 읽는다")
    assert not lb._hugs_prev(TOP, body) and not lb._hugs_prev(body, BOT)
    at, _lead, _tail = lb._box_blanks([body, TOP, _cells("가 10"), BOT, body], off=False)
    assert at == frozenset({1, 4})


def test_홑_점역자_주_줄_뒤_상자는_띄운다():
    # 「그림 생략」 처럼 쌍점 없는 주 줄은 앞 그림의 주다. 뒤에 따로 오는 상자를 이끌지 않는다(eval E-44 회차 11).
    note = _cells("<!주>그림 생략<!/주>")
    assert not lb._is_tn_head_line(note) and not lb._hugs_prev(TOP, note)
    at, _lead, _tail = lb._box_blanks([note, TOP, _cells("가 10"), BOT], off=False)
    assert 1 in at
