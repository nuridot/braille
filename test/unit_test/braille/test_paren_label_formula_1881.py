"""#1881 · 원장 B-64 — 괄호로 묶은 한글 라벨이 등호 · 연산 기호로 식에 이어지면 라벨까지 한 식(수학 제6항).

기대값은 「한국 점자 규정」 재추출 3129~3130행(`(원의둘레)=(반지름)×2×3.14`)에서 가져온다. 나머지는 꼴만 본다(지어낸 식).
"""
from semojum_braille.encoder.translator import element_type, translate_with_breaks
from braille_ascii import ascii_to_unicode


def _tr(text: str) -> str:
    with element_type("text"):
        return "".join(translate_with_breaks(text)[0]).rstrip("⠀")


def test_규정_예_원의_둘레():
    assert _tr("(원의 둘레)=(반지름)×2×3.14") == ascii_to_unicode('8p3w`i&"n0338^3.o"[50*#b*#c4ad', backtick="space")


def test_라벨과_등호가_붙고_괄호가_갈리지_않는다():
    out = _tr("(좌변)=2")
    assert out.startswith("⠦⠨⠧⠘⠡⠴⠒⠒⠼⠃"), out            # 수학 괄호 ⠦ ⠴ · 등호 ⠒⠒ 붙음
    assert "⠦⠄" not in out and "⠀⠀⠴" not in out          # 종전 꼴: 한글 여는 괄호 · 두 칸 뒤 수식 닫는 괄호
    assert _tr("(우변)= $\\frac{1}{2}$").startswith("⠦⠍⠘⠡⠴⠒⠒⠼⠃⠌⠼⠁")


def test_참조_문자_괄호는_건드리지_않는다():
    from semojum_braille.encoder.translator import _paren_label_formula
    for s in ("(가)=(나)", "(좌변)=☐", "이 식(가정)은 참이다"):
        assert _paren_label_formula(s) == s
