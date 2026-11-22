"""수식 안 ASCII 마침표 셋 `...` 은 줄임표 ⠠⠠⠠ 다(#1758, 원장 B-62).

종전에는 `\\cdots` · `\\ldots` · `…` 만 ⠠⠠⠠ 이고 마침표 셋은 ⠲⠲⠲ 로 나갔다. 기대값은 「한국 점자 규정」 재추출본
(유니코드 점자 파일 같은 행)의 예문이다.
"""
from semojum_braille.encoder.translator import translate_tagged_text


def test_수열_나열의_줄임표는_규정_예문대로():
    """수학 제12항 [붙임 1](3326행) "줄임표는 ⠠⠠⠠으로 적는다" · 예문 3327~3329행(묵자가 마침표 셋이다)."""
    out = translate_tagged_text("a₁,a₂,a₃,...라 하자.")
    assert out.lstrip("⠀") == "⠁⠰⠼⠁⠐⠀⠁⠰⠼⠃⠐⠀⠁⠰⠼⠉⠐⠀⠠⠠⠠⠀⠀⠐⠣⠀⠚⠨⠲"


def test_무한소수의_줄임표도_수_바로_뒤에_붙는다():
    """제11항 예 3242~3243행 `0.1999⋯` = ⠼⠚⠲⠁⠊⠊⠊⠠⠠⠠. 마침표 셋으로 와도 같다."""
    assert translate_tagged_text("<!수식>0.1999...<!/수식>") == "⠼⠚⠲⠁⠊⠊⠊⠠⠠⠠"
    assert translate_tagged_text("<!수식>0.1999...<!/수식>") == translate_tagged_text("<!수식>0.1999\\cdots<!/수식>")


def test_마침표_셋은_cdots_와_같다():
    for latex in ("a_1, a_2, ...", "1+2+...+n"):
        dots = translate_tagged_text(f"<!수식>{latex}<!/수식>")
        cdots = translate_tagged_text("<!수식>" + latex.replace("...", "\\cdots") + "<!/수식>")
        assert dots == cdots and "⠲⠲⠲" not in dots, latex
