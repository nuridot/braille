"""옛한글 방점(「한국 점자 규정」 제27항, 재추출 1298~1302행) 거성 · = ⠸⠂ · 상성 ： = ⠸⠅ (#1896, B-20)."""
from semojum_braille.encoder.translator import element_type, translate_with_breaks


def _tr(s: str) -> str:
    with element_type("text"):
        return "".join(translate_with_breaks(s)[0])


def test_방점은_거성_상성_점형으로_적는다():
    # 예(1317 · 1320행) `나·랏 ：말ᄊᆞ·미` = `c_1"<'`_ke1,,"#_1eo`
    assert _tr("나·랏 ：말ᄊᆞ·미") == "⠉⠸⠂⠐⠣⠄⠀⠸⠅⠑⠂⠠⠠⠐⠼⠸⠂⠑⠕"


def test_한자와_독음_사이_방점은_한자를_빼고_남긴다():
    # 예(1317 · 1321행) `文문字·ᄍᆞᆼ` = `eg_1,."#"7`
    assert _tr("文문字·ᄍᆞᆼ") == "⠑⠛⠸⠂⠠⠨⠐⠼⠐⠶"


def test_현대_글_가운뎃점은_그대로다():
    assert _tr("사과·배") == "⠇⠈⠧⠐⠆⠘⠗"
