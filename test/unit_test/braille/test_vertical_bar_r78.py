"""원장 R-78 · #1868 — 본문 · 목록 요소의 세로줄 `|` 는 제71항 ⠸⠳, 그 밖 요소는 종전대로 빈칸.

「한국 점자 규정」 제71항(재추출 2855~2856행) `저자 | 홍길동` = `.s.`_|`j=@o1i=`. 머리글(`언어 | 음운`)은 header_footer 로 오고
정답 책은 그 자리를 안 적는다(ai A-40). 예문 말고는 지어낸 글이다.
"""
import uuid

from semojum_braille.encoder.text_braille import TextBraille
from semojum_braille.encoder.translator import element_type, translate_with_breaks
from semojum_braille.schemas import LLMOutput
from braille_ascii import ascii_to_unicode

BAR = "⠀⠸⠳⠀"


def _one(etype: str, text: str) -> str:
    eid = uuid.uuid4()
    out = TextBraille({eid: etype}).translate(
        [LLMOutput(element_id=eid, corrected_text=text, render_mode="text_only", routing_tier="ZERO")])
    return "".join(out[0].braille_lines)


def test_본문_요소의_세로줄은_제71항_꼴이다():
    assert _one("text", "저자 | 홍길동") == ascii_to_unicode(".s.`_|`j=@o1i=", backtick="space")     # 2856행
    assert BAR in _one("list_item", "출판 | 가나다")


def test_머리글_제목_종류_모름은_종전대로_빈칸이다():
    for etype in ("header_footer", "title", ""):
        assert "⠸⠳" not in _one(etype, "단원 | 소제목"), etype
    assert "⠸⠳" not in "".join(translate_with_breaks("단원 | 소제목")[0])     # 표 칸 등 element_type 밖


def test_박스_표제는_종류와_무관하게_붙임표로_감싼다():
    with element_type("text"):
        assert "".join(translate_with_breaks("|정답|")[0]) == "".join(translate_with_breaks("-정답-")[0])
