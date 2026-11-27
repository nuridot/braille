"""식 뒤 줄임표 + 번호(식 번호 · 조건 번호)의 빈칸(#1898, B-20).

「한국 점자 규정」 수학 제6항 예(재추출 3104~3109행) `b(x−1)(1≤x≤2)⋯②` = `b8x9#a0`8#a66x66#b0`,,,`#2`:
줄임표 앞뒤 한 칸(묵자는 붙였다). 글 속 `$식$ …… ㉠` 도 식 뒤 한 칸이다(2027 gold 009 한 칸 26 : 두 칸 0).
"""
from semojum_braille.encoder.kor_math_rules import convert_latex
from semojum_braille.encoder.translator import element_type, translate_with_breaks


def _tr(s: str) -> str:
    with element_type("text"):
        return "".join(translate_with_breaks(s)[0])


def test_수식_안_줄임표_번호는_앞뒤_한_칸():
    assert convert_latex(r"(0\le x\le 1)\cdots ①") == "⠦⠼⠚⠖⠖⠭⠖⠖⠼⠁⠴⠀⠠⠠⠠⠀⠼⠂"   # 3107~3108행 `8#j66x66#a0`,,,`#1`


def test_수식_안_다른_줄임표는_그대로():
    assert convert_latex(r"1+2+\cdots+n") == "⠼⠁⠢⠼⠃⠢⠀⠠⠠⠠⠀⠢⠝"


def test_식_뒤_줄임표_번호는_한_칸():
    assert _tr("<!수식>x=2<!/수식> …… ①") == "⠭⠒⠒⠼⠃⠀⠠⠠⠠⠀⠼⠂"


def test_식_뒤_줄임표_다음_글은_두_칸_그대로():
    assert _tr("<!수식>x=2<!/수식> …… 그러므로").startswith("⠭⠒⠒⠼⠃⠀⠀⠠⠠⠠")
