"""로마자 사이 빗금은 로마자 구간 안이다(#1741). 「한국 점자 규정」 제32항 — 로마자표와 종료표 사이는 통일영어점자."""
import pytest

from semojum_braille.encoder.translator import translate_tagged_text
from braille_ascii import ascii_to_unicode


def _ascii(s):
    return ascii_to_unicode(s, backtick="cell")


@pytest.mark.parametrize("text, expect", [
    ("O/X 문제", "0,o_/,x4"),
    ("TCP/IP 통신", "0,,tcp_/,,ip4"),
    ("자녀 2는 ti/ti를", "0ti_/ti4\"!"),            # 2027 gold 생명과학 E26-001 p038
])
def test_로마자_빗금_로마자는_한_구간이다(text, expect):
    assert _ascii(expect) in translate_tagged_text(text)


def test_빗금_뒤_한글이면_종료표를_적는다():
    """규정 예문(재추출 제33항 [다만] 자리) `KTX/새마을호/무궁화호` = `0,,ktx4_/,re<!ju_/em@m7jvju`."""
    assert translate_tagged_text("KTX/새마을호/무궁화호").startswith(_ascii("0,,ktx4_/"))
