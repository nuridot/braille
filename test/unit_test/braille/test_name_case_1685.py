"""#1685: 이름꼴 낱말(대문자마다 소문자가 이어지는 낱말)에도 약자를 쓴다.

「통일영어점자 규정」 10.4.3(재추출 4626행) ing 약자는 낱말 첫머리가 아니면 쓴다, 예 `SmithInge` = `,smi?,+e`(4638행).
10.7.4 예 `McKeever` = `,mc,keev]`(5211행). 종전에는 대소문자가 섞인 낱말을 모두 약어(mV · pH)로 보아 약자를 안 썼다.
원소 기호 · 유전자형 · 단위는 종전대로 글자마다 적는다(대문자 앞 ⠠, UEB 8.3).
"""
import pytest

from semojum_braille.encoder.eng_braille import translate_word
from braille_ascii import ascii_to_unicode


def _letters(word: str) -> str:
    return "".join(("⠠" if c.isupper() else "") + ascii_to_unicode(c.lower()) for c in word)


def test_규정_예_이름꼴_낱말():
    assert translate_word("SmithInge") == ascii_to_unicode(",smi?,+e")
    assert translate_word("McKeever") == ascii_to_unicode(",mc,keev]")


@pytest.mark.parametrize("word", ["HCl", "NaCl", "AaBb", "AaBbdd", "AaBbccdd", "mV", "pH"])
def test_원소_기호_유전자형_단위는_글자마다(word):
    assert translate_word(word) == _letters(word)


def test_영어_1급은_약자_없이():
    assert translate_word("SmithInge", uncontracted=True) == _letters("SmithInge")
