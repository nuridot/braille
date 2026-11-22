"""띄어 쓴 두 식은 따로 감싼다(#1737). 수학 제11항(재추출 3235행) "수식은 앞뒤를 두 칸씩"."""
from semojum_braille.encoder import inline_math as IM
from semojum_braille.encoder.translator import translate_tagged_text


def test_두_식은_따로_감싸고_수가_안_붙는다():
    assert IM.wrap("2×3=6 6÷2=3") == "<!수식>2×3=6<!/수식> <!수식>6÷2=3<!/수식>"
    assert "⠼⠋⠀⠀⠼⠋" in translate_tagged_text("2×3=6 6÷2=3")      # 종전 ⠼⠋⠋(=66)


def test_gold_세_식():
    """수학 E26-009 p004 gold `a55#j  a33#j  a99#j`."""
    assert IM.wrap("a>0  a=0  a<0").count("<!수식>") == 3


def test_한_식은_안_가른다():
    for t in ("sin x = 1/2", "f(x) = 2x + 1", "Sn=A n", "p-2a (x-p-a)=0", "an=a+(n-1)d (n=1, 2, 3)"):
        assert IM.wrap(t).count("<!수식>") <= 1, t
