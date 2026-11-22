"""#1705: 점역에서 빠지는 글자 자리에 공통 표시 ⣿(U+28FF, 8점 모두) 하나를 둔다. 셈 = 표시.

검토 표시(R15 글꼴 사설영역 · R17 기호 · 한자 · 그 밖 글자 · 수식 명령 · R18 옛한글)가 세는 수와 점자에 든 ⣿ 수가 같아야
점역사가 몇 자가 빠졌는지 점자에서 바로 안다. 셈과 표시는 같은 자리 함수를 쓴다. 글은 지어낸 것이다.
"""
import pytest

from semojum_braille.encoder.translator import (dropped_hanja, dropped_latex, dropped_old_jamo, dropped_pua, dropped_symbols,
                                       dropped_unknown, translate_body)

_COUNTERS = (dropped_pua, dropped_symbols, dropped_hanja, dropped_unknown, dropped_latex, dropped_old_jamo)


def _count(text: str) -> int:
    return sum(sum(f(text).values()) for f in _COUNTERS)


def _marks(text: str) -> int:
    return "".join(translate_body(text)[0]).count("⣿")


@pytest.mark.parametrize("text", [
    "가▶나 그리고 ★표",              # 기호
    "가[漢]나 乚 다",                   # 한자(한자만 든 병기 괄호가 아님)
    "가나",                       # 글꼴 사설영역
    "가́나 가�나",            # 빈 점자를 내는 결합 부호 · 폴백이 지우는 글자
    "$a \\vert b$ 와 $c$",             # 모르는 수식 명령
    "하ᄀᆞᄋᆉ다",                         # 점형 없는 옛한글 음절
    "x ⊳ y\n둘째 줄 가⃞나 끝",         # 여러 줄 · 홀로 선 네모
])
def test_셈과_표시_수가_같다(text: str):
    assert _count(text) >= 1
    assert _marks(text) == _count(text)


@pytest.mark.parametrize("text", [
    "학교(學校)에 갔다",           # 한자만 든 병기 괄호는 통째로 걷는다(지침 2.5.2 (2))
    "▲ 첫째 줄머리",              # 줄머리 ▲ 는 점형이 나온다
    "보통 글 ABC 123",
    "정⃞답⃞ 을 고른다",           # 장식 배지 네모는 일부러 지운다(원장 C-16-3)
    "國귁ᄋᆡ 말ᄊᆞᄆᆡ",              # 옛한글 인용 속 한자는 독음과 함께 적혀 일부러 지운다(규정 제25항 예 1272~1277행)
])
def test_빠짐이_없으면_표시도_없다(text: str):
    assert _count(text) == 0
    assert _marks(text) == 0
