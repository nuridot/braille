"""유전자형 위첨자(원장 B-22 · R-104 (나)).

성염색체 · ABO 유전자형의 대립유전자 위첨자를 점역이 버리거나(유니코드 `ᴬ` · `ᵃ`) 글자마다 대문자표를 달던 것을 고쳤다.
기대값의 근거:
- 「과학 점자」 제23항(재추출 4923~4925행) 대문자가 2개 이상 붙어 나오면 대문자 단어표 ⠠⠠, 예 `RRyy` = `,,rr,'yy`(4933~4934행)는
  단어표 범위 뒤 소문자 앞에 대문자 종료표 ⠠⠄.
- 「수학 점자」 제18항 1(3528~3530행) 위첨자 기호 ⠘ 뒤에 첨자를 적고, [붙임](3540행) 곱은 묶음 괄호 ⠷ … ⠾(예 `a^(#cm5#bn)` 3544행).
- 제11항(3235행) 수식 앞뒤 두 칸, 제54항(2406행) 여는 괄호 뒤 · 닫는 괄호 앞은 붙여 쓴다(원장 R-104 (나)).
- 위첨자 글자의 대문자는 단어표 범위 밖이라 글자마다 ⠠ 를 단다: 규정에 예가 없어 gold 관행(생명과학 001 단어표 꼴 171 : 대문자마다 ⠠ 꼴 10).
입력 문장은 지어 썼다.
"""
from semojum_braille.encoder.kor_math_rules import is_genotype
from semojum_braille.encoder.translator import convert_latex, translate_with_breaks


def _tr(text: str) -> str:
    return "".join(translate_with_breaks(text)[0])


def test_유니코드_위첨자_대립유전자를_버리지_않는다():
    out = _tr("유전자형은 XᴬXᵃ이다.")
    assert "⠀⠀⠠⠠⠭⠘⠠⠁⠭⠘⠁⠀⠀" in out          # 단어표 · 위첨자 ⠘ · 위첨자 대문자 ⠠ · 앞뒤 두 칸


def test_홑_유전자형도_위첨자를_살린다():
    assert "⠀⠀⠠⠭⠘⠠⠁⠀⠀" in _tr("어머니는 Xᴬ 또는 Y를 가진다.")   # 두 글자 토막도 수식 구간(제11항 두 칸)
    assert "⠀⠀⠠⠠⠭⠘⠠⠁⠭⠘⠁⠀⠀" in _tr("딸은 Xᴬ \u2009Xᵃ이다.")      # 위첨자 뒤 가는 빈칸(첨자 폭 잔재)은 붙인다


def test_여러_글자_위첨자는_묶음_괄호():
    assert convert_latex("X^{Ab}Y") == "⠠⠠⠭⠘⠷⠠⠁⠃⠾⠽"
    assert convert_latex("X^{AB}Y") == "⠠⠠⠭⠘⠷⠠⠠⠁⠃⠾⠽"   # 묶음 안 대문자 둘도 단어표


def test_단어표_범위_뒤_소문자_앞은_종료표():
    assert convert_latex("X^{A}X^{a}Bb") == "⠠⠠⠭⠘⠠⠁⠭⠘⠁⠃⠠⠄⠃"
    assert convert_latex("AaX^{B}Y") == "⠠⠁⠁⠠⠠⠭⠘⠠⠃⠽"     # 홑 대문자 A 는 ⠠ 하나, 뒤 X · Y 가 단어표
    assert convert_latex("I^{A}I^{B}") == "⠠⠠⠊⠘⠠⠁⠊⠘⠠⠃"
    assert convert_latex("I^{A}i") == "⠠⠊⠘⠠⠁⠊"


def test_글_괄호_안_유전자형은_괄호에_붙인다():
    out = _tr("자녀(XᵃXᵃ, XᵃY)는 정상이다.")
    assert "⠦⠄⠠⠠⠭⠘⠁⠭⠘⠁⠐⠀⠠⠠⠭⠘⠁⠽⠠⠴" in out
    assert "⠦⠄⠀" not in out and "⠀⠠⠴" not in out


def test_괄호_앞_번호와_쉼표_뒤_개체_이름은_글로_둔다():
    out = _tr("개체 3(XᴬXᵃBb)와 개체 4를 비교한다.")
    assert "⠼⠉⠦⠄⠠⠠⠭⠘⠠⠁⠭⠘⠁⠃⠠⠄⠃⠠⠴" in out          # 번호 · 글 괄호에 붙임
    out = _tr("P는 XᵃYBb, Q는 XᴬXᵃBb이다.")
    assert "⠠⠠⠭⠘⠁⠽⠃⠠⠄⠃⠐⠀⠴⠠⠟" in out               # 쉼표는 식에 붙이고(#1653) Q 는 로마자표를 단 글


def test_홑_소문자_대립유전자가_낀_묶음도_글_괄호():
    out = _tr("대립유전자(Iᴬ, Iᴮ, i)를 쓴다.")
    assert "⠦⠄⠠⠊⠘⠠⠁⠐⠀⠠⠊⠘⠠⠃⠐⠀⠊⠠⠴" in out


def test_유전자형_아닌_위첨자는_그대로():
    assert not is_genotype("X^{2}") and not is_genotype("x^{a}") and not is_genotype("A^{B}")
    assert is_genotype("XᴬXᵃ/Bd/bD") and is_genotype("Iᴮ i")
