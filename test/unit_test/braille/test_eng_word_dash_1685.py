"""#1685: 한글 없는 줄의 영어 낱말이 하나여도 낱말에 붙은 줄표는 통일영어점자 줄표 ⠠⠤ 다.

「통일영어점자 규정」 10.4.1 예 `er– ],-`(er 묶음 약자 ⠻ + 줄표 ⠠⠤). 종전에는 영어 산문 줄(영어 낱말 둘 이상)만 맡겨
낱말 하나 줄은 한글 줄표 ⠤⠤ 로 나갔다. 글은 지어낸 것이다(규정 예 `er—` 는 그대로 썼다).
"""
import pytest

from semojum_braille.encoder.translator import translate_with_breaks


def _br(text: str) -> str:
    return "".join(translate_with_breaks(text)[0])


def test_낱말_하나_뒤_줄표는_통일영어점자_줄표():
    assert _br("er—") == "⠻⠠⠤"                     # 10.4.1 예
    assert _br("word—").endswith("⠠⠤")


@pytest.mark.parametrize("text", ["10–12", "가나—다", "x=1—", "—"])
def test_영어_낱말이_아니거나_식이면_그대로(text):
    assert "⠠⠤" not in _br(text)
