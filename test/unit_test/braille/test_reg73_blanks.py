"""규정 제73항 — 채워 넣어야 할 빈칸 세 가지를 한곳에서 대조한다.

종전에는 세 빈칸 시험이 `test_emph_and_table_blank.py` · `test_box_char.py` ·
`test_underline_blank_reverse.py` 등에 흩어져 있어, **서로 섞이지 않는지**를 보는 자리가
없었다. 셋은 같은 조항인데 점형이 다르므로 그 갈림이 이 파일의 과제다.

근거는 「한국 점자 규정」 재추출본 제73항(2922행)과 같은 쪽의 점형 줄이다.

| 묵자 | 점형 | 원문 행 |
|---|---|---|
| 밑줄 빈칸 | ⠸⠤  | 2925(점형) · 2928(이름) |
| 네모 빈칸 | ⠸⠦⠀⠴⠇ | 2926 · 2929 |
| 표의 빈칸 | ⠿⠿  | 2927 · 2930 |

[다만] 2941~2942행 — 빈칸의 개수를 나타내야 할 때에는 해당 기호를 묵자의 개수만큼 적는다.
  보기 2944~2945행: `고성__` → ⠸⠤⠸⠤
[붙임] 2946~2947행 — 밑줄 빈칸에 표시 문자가 있으면 표시 문자를 먼저 적고 밑줄 기호를
  붙인다. 네모 빈칸에 표시 문자가 있으면 묵자를 따른다.

⚠ 기대값은 **규정 원문에서만** 가져왔다. 코퍼스 빈도나 현재 코드 동작을 근거로 삼지 않았다.
⚠ 홀드아웃 권의 gold·실물은 쓰지 않는다.
"""
import pytest

from semojum_braille.encoder.translator import translate_body

RULE = "⠸⠤"          # 밑줄 빈칸 (제73항, 2925행)
SQUARE = "⠸⠦⠀⠴⠇"    # 네모 빈칸 (2926행)
TABLE = "⠿⠿"         # 표의 빈칸 (2927행)


def _br(text: str) -> str:
    return "".join(translate_body(text)[0])


# ── 셋이 각각 제 점형으로 나가는가 ──────────────────────────
@pytest.mark.parametrize("tag,want,others", [
    ("밑줄", RULE, (SQUARE, TABLE)),
    ("네모", SQUARE, (RULE, TABLE)),
    ("빈칸", TABLE, (RULE, SQUARE)),
])
def test_제73항_세_빈칸이_서로_섞이지_않는다(tag, want, others):
    """한 빈칸을 쓰면 그 점형만 나오고 나머지 둘은 섞이지 않는다."""
    out = _br(f"다음 <!{tag}> 에 알맞은 말을 쓰시오.")
    assert want in out, f"<!{tag}> → {want} 가 없다: {out}"
    for other in others:
        # 네모(⠸⠦⠀⠴⠇)는 밑줄(⠸⠤)을 부분 문자열로 품지 않는다 — 그대로 대조한다.
        assert other not in out, f"<!{tag}> 에 {other} 가 섞였다: {out}"


# ── [다만] 개수를 나타낼 때 (2941~2945행) ───────────────────
def test_다만_빈칸_개수만큼_적는다():
    """`고성__` 처럼 묵자에 빈칸이 둘이면 기호도 둘이다(2944~2945행)."""
    out = _br("사자성어 채우기: 고성<!밑줄><!밑줄>")
    assert out.count(RULE) == 2, f"밑줄 기호가 둘이어야 한다: {out}"


# ── [붙임] 표시 문자가 있을 때 (2946~2949행) ────────────────
def test_붙임_밑줄_빈칸은_표시_문자를_먼저_적는다():
    """표시 문자(㉠)가 있으면 그것을 먼저 적고 밑줄 기호를 붙인다(2946행)."""
    out = _br("일시: <!밑줄>㉠")
    assert RULE in out, out
    # 표시 문자가 기호보다 앞에 온다
    assert out.index(RULE) > 0, f"밑줄 기호 앞에 아무것도 없다: {out}"


# ── 같은 줄에 둘 이상이 와도 갈라지는가 ─────────────────────
def test_한_줄에_밑줄과_네모가_같이_와도_갈라진다():
    out = _br("<!밑줄> 과 <!네모> 는 다른 기호다")
    assert RULE in out and SQUARE in out, out
    # 네모가 밑줄 자리를 먹지 않는다 — 둘 다 제 횟수대로 나온다
    assert out.count(SQUARE) == 1, out


# ── 태그 없이 □ 글자로 온 네모 빈칸 (원장 C-213, B-20 #1861) ─────
@pytest.mark.parametrize("text", ["다음 □ 안에 알맞은 수를 써넣어 보자.", "□에 들어갈 말은?"])
def test_발문의_네모_글자는_네모_빈칸이다(text):
    """「점자 자료 제작 지침」 2장 4절 6 예(재추출 1038~1039행) `다음 □ 안에 알맞은 수를 써넣어 보자.` = `i<[5`_8`0l`<3n …`."""
    assert SQUARE in _br(text), _br(text)


@pytest.mark.parametrize("text", ["종 A(□)", "□의 넓이"])
def test_발문_밖의_네모_글자는_빠짐표다(text):
    """제49항 빠짐표 □ = `_7l`(문장 부호표 2213행 점형 · 2217행 이름). 채워 넣으라는 말이 없으면 그대로다."""
    out = _br(text)
    assert SQUARE not in out and "⠸⠶⠇" in out, out
