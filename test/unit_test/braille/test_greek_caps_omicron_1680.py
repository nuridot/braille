"""#1680: 그리스 오미크론과 대문자 그리스 낱말.

「한국 점자 규정」 제30항 표(재추출 1587 · 1589행) `ο` = `.o`(⠨⠕) · `Ο` = `,.o`(⠠⠨⠕) 가 기호표에 없어, 오미크론이 든 런을
제31항 한글 문맥 감싸기가 놓쳤다. 제30항 예(1641행) `ΔΕΛΦΟΙ` = `,,.d.e.l.f.o.i` 는 한글 없는 줄에서도 대문자 단어표 ⠠⠠ 하나에
글자마다 ⠨ 다. `ΦΟΙ는` 은 지어낸 글이다.
"""
import pytest

from semojum_braille.encoder.translator import translate_with_breaks


def _br(text: str) -> str:
    return "".join(translate_with_breaks(text)[0])


@pytest.mark.parametrize("text,want", [
    ("ο", "⠨⠕"),                                   # 제30항 1587행 `.o`
    ("Ο", "⠠⠨⠕"),                                  # 제30항 1589행 `,.o`
    ("ΔΕΛΦΟΙ", "⠠⠠⠨⠙⠨⠑⠨⠇⠨⠋⠨⠕⠨⠊"),             # 제30항 1641행 `,,.d.e.l.f.o.i`
    ("ΦΒΚ의", "⠴⠠⠠⠨⠋⠨⠃⠨⠅⠲⠺"),                    # 제31항 예 `0,,.f.b.k4w`(종전에도 맞음)
])
def test_규정_예(text, want):
    assert _br(text) == want


def test_오미크론이_든_런도_한글_문맥에서_감싼다():
    assert _br("ΦΟΙ는") == "⠴⠠⠠⠨⠋⠨⠕⠨⠊⠲⠉⠵"


@pytest.mark.parametrize("text", ["ΔA", "x-ΔΣ"])
def test_로마자가_붙거나_연산_기호_뒤면_대문자_단어표를_안_쓴다(text):
    assert "⠠⠠" not in _br(text)
