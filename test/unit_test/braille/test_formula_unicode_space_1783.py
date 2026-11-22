"""수식 속 유니코드 빈칸은 ASCII 빈칸과 같다(#1783).

종전에는 `convert_latex` 가 ASCII 빈칸만 빈칸으로 다뤄, NBSP 같은 글자가 날 글자 그대로 점자 줄에 남았다(점자 블록 밖).
점형 문제가 아니라 빈칸 정규화라 기대값은 같은 식을 ASCII 빈칸으로 적은 출력이다.
"""
import uuid

import pytest

from semojum_braille.encoder.formula_braille import FormulaBraille
from semojum_braille.encoder.translator import translate_tagged_text
from semojum_braille.schemas import LLMOutput

SPACES = [" ", " ", "　", " ", " "]


def _formula(text: str) -> str:
    o = LLMOutput(element_id=uuid.uuid4(), corrected_text=text, render_mode="formula_block", routing_tier="ZERO")
    return "".join(FormulaBraille().translate([o])[0].braille_lines)


def _in_block(s: str) -> bool:
    return all("⠀" <= c <= "⣿" for c in s)


@pytest.mark.parametrize("sp", SPACES, ids=[f"U+{ord(c):04X}" for c in SPACES])
def test_유니코드_빈칸은_ASCII_빈칸과_같다(sp):
    for src in ("x{}=1", "a=1{}b=2"):
        out = _formula(src.format(sp))
        assert _in_block(out) and out == _formula(src.format(" "))
        tagged = translate_tagged_text("$" + src.format(sp) + "$")
        assert _in_block(tagged) and tagged == translate_tagged_text("$" + src.format(" ") + "$")
