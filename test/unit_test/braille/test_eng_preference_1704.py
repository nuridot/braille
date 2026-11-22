"""#1704: 겹치는 영어 약자는 「통일영어점자 규정」 10.10 Preference 차례로 고른다(`통일영어점자 규정_UEB2013.txt` 5666~5809행).

셀 수가 적은 쪽이 먼저(10.10.2)이고, 같으면 머리글자 · 끝 묶음 약자보다 윗칸 · 아래칸 묶음 약자(10.10.7) · 강약자(10.10.3)를
쓴다. 곁 규칙 넷(10.7.2 · 10.6.1 · 10.11.2 · 10.8.4)도 같이 본다. 낱말은 규정 예에 없는 것으로 골랐고 기대값은 조항에서 손으로
셌다(셀 수는 주석).
"""
import pytest

from semojum_braille.encoder.eng_braille import translate_word


@pytest.mark.parametrize("word, want", [
    ("laziness", "⠇⠁⠵⠊⠰⠎"),          # 10.10.2: lazi + ness 6칸. 종전 왼쪽 긴 것 먼저는 in + ess 로 7칸
    ("emptiness", "⠑⠍⠏⠞⠊⠰⠎"),
    ("aesthetic", "⠁⠑⠎⠮⠞⠊⠉"),        # 10.10.2: s + the 7칸. st + h 는 8칸
    ("inhered", "⠔⠓⠻⠫"),              # 10.10.7: in here d 와 in h er ed 가 4칸으로 같으면 er · ed
    ("farther", "⠋⠜⠮⠗"),              # 10.10.3: ar the r 와 ar th er 가 같으면 강약자 the
])
def test_10_10_선호_차례(word: str, want: str):
    assert translate_word(word) == want


def test_10_7_2_these_는_낱말_뜻이_남을_때만():
    assert translate_word("prostheses") == "⠏⠗⠕⠎⠮⠎⠑⠎"     # these 약자(⠘⠮)를 쓰면 7칸이지만 뜻이 안 남는다


def test_10_6_1_con_뒤가_묵음_e_뿐이면_첫_음절이_아니다():
    assert translate_word("cones") == "⠉⠐⠕⠎"               # c + one + s. con(⠒) 아님


def test_10_11_2_ng_뒤_h_는_gh_로_묶지_않는다():
    assert translate_word("longhorn") == "⠇⠰⠛⠓⠕⠗⠝"


def test_10_8_4_ain_뒤_여성_어미_ess_는_ness_가_아니다():
    assert translate_word("villainess") == "⠧⠊⠇⠇⠁⠔⠑⠎⠎"
    assert translate_word("laziness").endswith("⠰⠎")         # 여성 어미가 아닌 ness 는 그대로
