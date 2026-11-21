"""규정 제73항 — 채워 넣어야 할 빈칸 세 가지를 한곳에서 대조한다.

AI 저장소(`Semojum/AI`)에 같은 시험을 넣었고(이슈 #1747), 사이드카 엔진에도 같은 자리를
둔다. 두 엔진이 같은 점형을 내야 **서버가 낸 점자와 앱이 낸 점자가 같다.**

종전에는 세 빈칸 시험이 `test_underline_blank_reverse.py` · `test_tag_parser.py` 등에
흩어져 있어, **서로 섞이지 않는지**를 보는 자리가 없었다. 셋은 같은 조항인데 점형이
다르므로 그 갈림이 이 파일의 과제다.

| 묵자 | 점형 | 규정 재추출본 행 |
|---|---|---|
| 밑줄 빈칸 | ⠸⠤  | 2925(점형) · 2928(이름) |
| 네모 빈칸 | ⠸⠦⠀⠴⠇ | 2926 · 2929 |
| 표의 빈칸 | ⠿⠿  | 2927 · 2930 |

[다만] 2941~2942행 — 빈칸의 개수를 나타내야 할 때에는 해당 기호를 묵자의 개수만큼 적는다.
  보기 2944~2945행: `고성__` → ⠸⠤⠸⠤
[붙임] 2946~2947행 — 밑줄 빈칸에 표시 문자가 있으면 표시 문자를 먼저 적고 밑줄 기호를
  붙인다. 네모 빈칸에 표시 문자가 있으면 묵자를 따른다.

⚠ 기대값은 **규정 원문에서만** 가져왔다. 코퍼스 빈도나 현재 코드 동작을 근거로 삼지 않았다.
"""
import pytest

from semojum_braille.encoder.translator import translate_body

RULE = "⠸⠤"          # 밑줄 빈칸 (제73항, 2925행)
SQUARE = "⠸⠦⠀⠴⠇"    # 네모 빈칸 (2926행)
TABLE = "⠿⠿"         # 표의 빈칸 (2927행)


def _br(text: str) -> str:
    return "".join(translate_body(text)[0])


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
        assert other not in out, f"<!{tag}> 에 {other} 가 섞였다: {out}"


def test_다만_빈칸_개수만큼_적는다():
    """`고성__` 처럼 묵자에 빈칸이 둘이면 기호도 둘이다(2944~2945행)."""
    out = _br("사자성어 채우기: 고성<!밑줄><!밑줄>")
    assert out.count(RULE) == 2, f"밑줄 기호가 둘이어야 한다: {out}"


def test_붙임_밑줄_빈칸은_표시_문자를_먼저_적는다():
    """표시 문자(㉠)가 있으면 그것을 먼저 적고 밑줄 기호를 붙인다(2946행)."""
    out = _br("일시: <!밑줄>㉠")
    assert RULE in out, out
    assert out.index(RULE) > 0, f"밑줄 기호 앞에 아무것도 없다: {out}"


def test_한_줄에_밑줄과_네모가_같이_와도_갈라진다():
    out = _br("<!밑줄> 과 <!네모> 는 다른 기호다")
    assert RULE in out and SQUARE in out, out
    assert out.count(SQUARE) == 1, out
