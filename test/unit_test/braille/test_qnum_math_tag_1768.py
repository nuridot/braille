"""문항 번호 바로 뒤가 `<!수식>` 태그면 `$…$` 와 같이 번호에 마침표를 안 붙인다(#1768, 원장 C-41 열한째).

종전에는 C-41 여섯째 가드가 `$` 만 수식 시작으로 보고 `<` 는 `<!강조>` 단원 소제목 때문에 일부러 뺐다. 그래서 앱 수식 넣기
단추 · #1759 가 낸 `1 <!수식>x+1=2<!/수식>` 이 `⠼⠁⠲…` 로 나갔다(eval E-02). 근거는 「점자 도서 제작 지침」 제2장 7. 1)(1)
(재추출 1247행) "본문의 번호 체계는 원본 자료의 형태를 따르는 것을 원칙으로 한다". 글은 지어낸 것이다.
"""
import uuid

from semojum_braille.encoder.text_braille import TextBraille
from semojum_braille.schemas import LLMOutput


def _tb(text: str) -> str:
    opt = LLMOutput(element_id=uuid.uuid4(), corrected_text=text, render_mode="text_only", routing_tier="ZERO")
    return "".join(TextBraille().translate([opt])[0].braille_lines)


def test_번호_뒤_수식_태그엔_마침표가_없다():
    """`1` = ⠼⠁(제40항 수표) · 수식 앞 두 칸(수학 제11항 3235행) · `x+1=2` 는 제12항 예 3313~3314행 `ax+b=0` = ⠁⠭⠢⠃⠒⠒⠼⠚ 꼴."""
    assert _tb("  1 <!수식>x+1=2<!/수식>") == "⠼⠁⠀⠀⠭⠢⠼⠁⠒⠒⠼⠃"
    assert _tb("  1 <!수식>x+1=2<!/수식>") == _tb("  1 $x+1=2$")


def test_다른_태그와_본문은_종전대로_마침표를_받는다():
    """열한째는 `<!수식>` 하나만 뺀다. 여섯째가 일부러 남긴 `<!강조>` 단원 소제목 · 한글 본문 번호는 그대로다."""
    assert _tb("  6 <!강조>근대적 생활 방식의 확산<!/강조>").startswith("⠼⠋⠲")
    assert _tb("  1 철수는 학교에 갔다.").startswith("⠼⠁⠲")
