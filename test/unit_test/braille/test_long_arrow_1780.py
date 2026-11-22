"""긴 꼴 화살표(⟺ ⟹ ⟶ ⟷)는 짧은 꼴과 같은 점형이다(#1780).

종전에는 기호표에 없어 빠짐 표시 ⣿ 로 나갔다. 기대값은 「한국 점자 규정」 재추출본(유니코드 점자 파일 같은 행)의
수학 논리 기호 예문이다. 묵자 예문은 짧은 꼴이고, 긴 꼴은 같은 기호의 글꼴 차이다(LaTeX `\\iff` 가 찍는 글자가 ⟺).
"""
import uuid

import pytest

from semojum_braille.encoder.formula_braille import FormulaBraille
from semojum_braille.encoder.translator import dropped_symbols, translate_tagged_text
from semojum_braille.schemas import LLMOutput

CASES = [
    ("r ⟺ s", "⠗⠀⠪⠒⠒⠕⠀⠎"),   # 필요충분(⇔) 4167~4169행
    ("p ⟹ q", "⠏⠀⠒⠒⠕⠀⠟"),   # 항진명제(⇒) 4156 · 4161행
    ("p ⟶ q", "⠏⠀⠒⠕⠀⠟"),     # 조건문(→) 4154~4155행
    ("p ⟷ q", "⠏⠀⠪⠒⠕⠀⠟"),   # 쌍조건문(↔) 4164~4166행
]


def _formula(text: str) -> str:
    o = LLMOutput(element_id=uuid.uuid4(), corrected_text=text, render_mode="formula_block", routing_tier="ZERO")
    return "".join(FormulaBraille().translate([o])[0].braille_lines)


@pytest.mark.parametrize("src,reg", CASES)
def test_긴_화살표는_규정_예문대로(src, reg):
    assert translate_tagged_text(src) == reg                       # 글 길
    assert translate_tagged_text(f"<!수식>{src}<!/수식>") == reg  # 수식 태그 길
    assert _formula(src) == reg                                    # 수식 요소 길


@pytest.mark.parametrize("latex,reg", [
    (r"$p \implies q$", "⠏⠀⠒⠒⠕⠀⠟"),            # 4161행
    (r"$p \Longrightarrow q$", "⠏⠀⠒⠒⠕⠀⠟"),     # 4161행
    (r"$p \longleftrightarrow q$", "⠏⠀⠪⠒⠕⠀⠟"),  # 4166행
])
def test_긴_화살표_LaTeX_명령도_같다(latex, reg):
    assert translate_tagged_text(latex) == reg


def test_긴_화살표는_빠진_글자로_안_센다():
    """종전엔 빠짐 셈(R17 · ⣿)에 들었다. 점형이 나가므로 이제 안 센다."""
    assert "⟺" not in dropped_symbols("g(x) ⟺ f(x)")
