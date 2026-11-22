"""빗금으로 이은 한 글자 단위(#1739). 「한국 점자 규정」 제69항(재추출 2680 · 2691행): 로마자 단위는 ⠴ … ⠲,
빗금으로 이은 단위는 한 구간(`160㎎/㎗` = `#afj0mg_/dl4`). 2027 gold `36m/s의` = `#cf0m_/s4w`."""
import pytest

from semojum_braille.encoder.translator import translate_tagged_text
from braille_ascii import ascii_to_unicode


@pytest.mark.parametrize("text, expect", [
    ("36m/s의", "#cf0m_/s4w"),            # gold(BRF 소문자 · 백틱 없음)
    ("속력은 10 m/s이다.", "#aj 0m_/s4oi4"),
    ("9.8m/s²", "#i4h0m_/s~#b"),          # 위 첨자 앞은 종료표 없음(gold `#aj0m_/s^#b`)
])
def test_빗금_한_글자_단위는_한_구간이다(text, expect):
    assert ascii_to_unicode(expect, backtick="cell").replace("⠀", " ") in translate_tagged_text(text).replace("⠀", " ")


def test_빗금_없는_한_글자는_종전대로():
    """`3 m` · `5g` 은 변수와 같은 글자라 이 규칙 밖이다(빗금이 있을 때만 단위로 읽는다)."""
    assert "⠴⠍⠸⠌" not in translate_tagged_text("x=3 m")
