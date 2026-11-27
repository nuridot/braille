"""#1887 — 숫자 앞에 붙은 × 는 곱셈표 ⠡(「한국 점자 규정」 수학 곱셈 기호), 맞고 틀림 가위표 X(⠴⠠⠭)가 아니다.

맞고 틀림 표시 · 숨김표 자리는 그대로인지도 본다(원장 C-14 · #945). 식은 지어낸 것이다.
"""
from semojum_braille.encoder.translator import element_type, translate_with_breaks


def _tr(text: str) -> str:
    with element_type("text"):
        return "".join(translate_with_breaks(text)[0])


def test_수_앞_곱셈표():
    assert "⠡⠼⠛" in _tr("가 ×7 나") and "⠴⠠⠭" not in _tr("가 ×7 나")
    assert "⠡⠼⠃" in _tr("값은 ×2배")


def test_맞고_틀림_표시와_숨김표는_그대로():
    assert "⠴⠠⠭" in _tr("3. ◯  4. ×")
    assert _tr("2026년 ×월").count("⠸⠭⠇") == 1
