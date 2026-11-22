"""구분자 없는 평문 속 함수 표기 `f(x)` 는 수식이다(#1762, 원장 B-61).

종전에는 강한 신호 목록에 홑 글자 함수 표기가 없어 `f(x),g(x)` 가 로마자표 · 한글 소괄호로 나갔다(수식 쪽이어도 같았다).
기대값은 「한국 점자 규정」 재추출본(유니코드 점자 파일 같은 행)의 예문이다.
"""
import pytest

from semojum_braille.encoder.translator import translate_tagged_text


def test_두_연속함수_예문은_규정대로():
    """수학 제11항 2호(3321행) "국어 문장 안에 로마자가 포함된 수학적 표기는 수식에 따른다" · 예문 3323~3325행."""
    reg = "⠀⠀⠊⠍⠀⠡⠠⠭⠚⠢⠠⠍⠀⠀⠋⠦⠭⠴⠐⠀⠛⠦⠭⠴⠀⠀⠫⠀⠊⠣⠪⠢⠀⠨⠥⠈⠾⠮⠀⠑⠒⠨⠭⠠⠕⠋⠟⠊⠲"
    assert translate_tagged_text("두 연속함수 f(x),g(x)가 다음 조건을 만족시킨다.").lstrip("⠀") == reg.lstrip("⠀")


@pytest.mark.parametrize("text", ["함수 f(x)의 값", "h(t)는 시간", "이때 f(x)>0이므로"])
def test_함수_표기는_로마자표_없이_수식이다(text):
    """제12항 1호(3308~3309행) 수식의 로마자는 로마자표 ⠴ 를 적지 않고 앞뒤를 두 칸 띄운다. 수식 소괄호는 ⠦ … ⠴(제6항)."""
    out = translate_tagged_text(text)
    assert "⠦⠄" not in out and "⠴⠋" not in out and "⠴⠓" not in out
    assert "⠀⠀" in out


@pytest.mark.parametrize("text", ["P(A)의 확률", "f(가)는"])
def test_대문자_앞_글자나_괄호_안_한글은_건드리지_않는다(text):
    """오탐 막기 — 이 고침은 f · g · h 소문자 + 한글 없는 괄호만 본다. 글 경로는 한글 소괄호 ⠦⠄ (2156행)."""
    assert "⠦⠄" in translate_tagged_text(text)
