"""문항 번호 바로 뒤가 구분자 없는 평문 수식이면 `$…$` 와 같이 번호에 마침표를 안 붙이고 번호와 수식을 두 칸으로 가른다
(#1771, 원장 C-41 열두째 · 부록9).

근거는 「점자 도서 제작 지침」 제2장 7. 1)(1)(재추출 1247행) "본문의 번호 체계는 원본 자료의 형태를 따르는 것을 원칙으로
한다"(지침). 마침표만 빼면 번호가 수식에 빨려 들어가 계수가 되므로(`1x+1=2`) 첫 수식 토막을 태그로 감싼다. 글은 지어낸 것이다.
"""
import uuid

import pytest

from semojum_braille.encoder.text_braille import TextBraille
from semojum_braille.schemas import LLMOutput


def _tb(text: str) -> str:
    opt = LLMOutput(element_id=uuid.uuid4(), corrected_text=text, render_mode="text_only", routing_tier="ZERO")
    return "".join(TextBraille().translate([opt])[0].braille_lines)


def test_번호_뒤_평문_수식은_달러_꼴과_같다():
    """`1` = ⠼⠁(제40항) · 수식 앞 두 칸(수학 제11항 3235행) · `x+1=2` 는 제12항 예 3313~3314행 `ax+b=0` = ⠁⠭⠢⠃⠒⠒⠼⠚ 꼴."""
    assert _tb("  1 x+1=2") == "⠼⠁⠀⠀⠭⠢⠼⠁⠒⠒⠼⠃"
    assert _tb("  9 ∠AOB=α라 하면") == _tb("  9 $∠AOB=α$라 하면")


@pytest.mark.parametrize("text,head", [
    ("  1 철수는 학교에 갔다.", "⠼⠁⠲"),     # 한글 본문 번호(C-41 관행 그대로)
    ("  1 x축 위의 점", "⠼⠁⠲"),             # 홑 로마자 + 한글은 수식 아님
    ("  2 CO₂가 발생한다", "⠼⠃⠲"),         # 화학식 토큰은 gold 근거가 없어 종전대로
])
def test_수식이_아닌_첫_토막은_종전대로_마침표(text, head):
    assert _tb(text).startswith(head)
