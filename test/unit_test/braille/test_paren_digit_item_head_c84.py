"""괄호 숫자 글자 `⑴` ~ `⒇` 로 여는 4단계 제목도 항목 머리라 3칸에서 시작한다(원장 C-84).

사회 네 권은 소항목 머리를 `⑴` 한 글자로 적는다. `_ITEM_HEAD_NUM` 이 `(1)` 꼴만 잡아 5칸(앞 빈칸 4)으로 나갔다.
gold 세계사 본책 p0041 3행 = `⠀⠀⠦⠄⠼⠁⠠⠴⠀⠕⠠⠮⠐⠣⠢⠈⠬⠺⠀⠠⠻⠐⠕⠃`(⑴ 이슬람교의 성립), 37행 ⑵ 도 2칸.
"""
from uuid import uuid4

import pytest

from semojum_braille.encoder.layout_braille import LayoutBraille
from semojum_braille.schemas import BrailleOutput


def _indent(text: str) -> int:
    bo = BrailleOutput(element_id=uuid4(), braille_lines=["⠦⠄⠼⠁⠠⠴⠀⠕⠠⠮⠐⠣⠢⠈⠬⠺"], corrected_text=text)
    return LayoutBraille()._first_indent(bo, "title", True, 4)


@pytest.mark.parametrize("text", ["⑴\t이슬람교의 성립", "⑵ 이슬람 제국의 발전", "⒇ 마지막", "(1) 괄호 꼴"])
def test_괄호_숫자_머리는_3칸에서(text):
    assert _indent(text) == 2


def test_단원_제목은_종전대로_5칸에서():
    assert _indent("이슬람 세계의 형성과 발전") == 4


# #1829 — 글머리 기호 하나 + 빈칸으로 여는 제목도 문단 머리라 3칸이다.
#   「점자 도서 제작 지침」 2장 3절 5. 1)(재추출 1434행) 「문단 시작 위치의 글머리 기호는 3칸에 표기」.
@pytest.mark.parametrize("text", ["• 낱말", "•낱말", "○ 낱말", "● 낱말", "□ 낱말", "△ 낱말"])
def test_글머리_기호로_여는_제목은_3칸에서(text):
    assert _indent(text) == 2


@pytest.mark.parametrize("text", ["○○의 생애", "△△일보"])
def test_빈칸_자리표시_제목은_종전대로_5칸에서(text):
    assert _indent(text) == 4
