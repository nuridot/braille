"""#1877 — 화학 반응식 상태 표시 (aq)(s)(l)(g) 괄호는 한글 소괄호 + 로마자표(과학 점자 제18항 3., 재추출 4834~4843행).

기대값은 규정 BRF 그대로다. 대문자 구절표의 효력은 괄호를 건너 이어진다.
"""
from semojum_braille.encoder.translator import element_type, translate_with_breaks
from braille_ascii import ascii_to_unicode


def _tr(text: str) -> str:
    with element_type("text"):
        return "".join(translate_with_breaks(text)[0]).rstrip("⠀")


def _brf(*lines: str) -> str:
    return "⠀".join(ascii_to_unicode(x, backtick="space") for x in lines)


def test_고체_기체_상태():          # 4836~4838행
    assert _tr("2S(s) + 3O₂(g) → 2SO₃(g)") in (_brf("#b,s8'0s,0`5`#c,o;#b8'0g,0`3o", "#b,s,o;#c8'0g,0"),
                                                  _brf("#b,s8'0s,0`5`#c,o;#b8'0g,0`3o") + _brf("#b,s,o;#c8'0g,0"))


def test_수용액_액체_상태와_구절표():   # 4839~4843행
    got = _tr("H₂CO₃(aq) + H₂O(l) ⇄ H₃O⁺(aq) + HCO₃⁻(aq)")
    assert got.replace("⠀", "") == _brf(",,,h;#b\"co;#c8'0aq,0`5", "h;#bo8'0l,0`[7o`h;#co^58'0aq,0`5",
                                         "hco;#c^9,'8'0aq,0").replace("⠀", "")


def test_화학식_밖의_괄호_낱자는_그대로():
    assert "⠦⠄⠴⠎⠠⠴" in _tr("함수 f의 (s) 값")          # 본문 로마자 괄호(종전 꼴)


def test_화살표_뒤_화학식도_원소마다_대문자표():      # #1879 · 과학 제18항 2.(재추출 4826~4828행)
    got = _tr("H₂SO₄ + Zn → ZnSO₄ + H₂↑").replace("⠀", "")
    assert got == _brf(",,,h;#bso;#d,'`5`,zn`3o", ",zn,s,o;#d`5`,h;#b;3o").replace("⠀", "")
