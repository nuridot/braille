"""한글 없는 영어 줄의 로마자표 다시 열기(#1223, 원장 C-164 · B-29).

- C-164: 구판 gold 영어책 4권은 영어 줄 화살표를 한글 꼴 ⠒⠕ 로 적고 뒤 영어에 로마자표 ⠴ 를 다시 열었다(274/288).
  #1698 에서 규정형으로 돌렸다. 한글 없는 영어 산문 줄은 통째로 로마자 구간이라 화살표도 통일영어점자 꼴 ⠰⠳⠕ 이고
  (「한국 점자 규정」 제32항 재추출 1650~1651행 위임 · UEB 3.2.1 1548~1557행) 구간이 안 끊겨 ⠴ 를 다시 열지 않는다.
  2027 gold EBS-E26-008 영어 줄 화살표 44 곳(줄머리 2 포함)이 모두 이 꼴이다(판본 역전).
- B-29: 띄어 쓴 줄표 · 빈칸 뒤에는 ⠴ 를 덧붙이지 않는다. gold 빈칸 뒤 0/2,261 · 줄표 뒤 12/385.
기대값은 gold BRF 원문 줄을 그대로 옮긴 것이다(BRF ASCII → 유니코드 점자). 화살표 두 줄은 줄머리 `3o 0` 을 규정형 `;\\o ` 로 바꿨다.
"""
import pytest

from semojum_braille.encoder.translator import translate_tagged_text

_BRF = " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="


def _u(brf: str) -> str:
    return "".join(chr(0x2800 + _BRF.index(c.upper())) for c in brf)


@pytest.mark.parametrize("text,gold", [
    # MS-REF-007 ans p0087 174행(구판 gold `3o 0,if …`)
    ("→ If you turn to the left, you will", ";\\o ,if y turn to ! left1 y w"),
    # HS-REF-007 ans p0016 27행(구판 gold `3o 0wond]+ …`)
    ("→ wondering who had the nerve to", ";\\o wond]+ :o _h ! n]ve to"),
])
def test_영어_줄_화살표는_통일영어점자_꼴이고_로마자표를_다시_안_연다(text: str, gold: str) -> None:
    assert translate_tagged_text(text) == _u(gold)


@pytest.mark.parametrize("text,gold", [
    # MS-REF-007 body p0016 11행
    ("<!밑줄> at history, and she is interested", ".- at hi/ory1 & %e is 9t]e/$"),
    # MS-REF-007 body p0004 50행
    ("might, must, should - Check-up Test.", "mi<t1 m/1 %d - ,*eck-up ,te/4"),
])
def test_띄어_쓴_빈칸_줄표_뒤에_로마자표를_안_붙인다(text: str, gold: str) -> None:
    assert translate_tagged_text(text) == _u(gold)


def test_붙인_붙임표_뒤는_종전대로_연다() -> None:
    # 한글 줄 `-UN-` = ⠤⠴⠠⠠⠥⠝⠤ (사회문화 p100 · 108 관행, _emit_mixed 주석)
    assert "⠤⠴⠠⠠⠥⠝⠤" in translate_tagged_text("사과 -UN- 기구")


def test_원소_반응식_화살표는_안_연다() -> None:
    # 과학 점자 제1항 꼴(test_back_roundtrip.TestBareElementLine) — 영어 산문 줄이 아니다
    assert "⠴" not in translate_tagged_text("H, Cl → HCl")
