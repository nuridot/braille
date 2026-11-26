"""T27 — 상자 안 첫 줄 괄호 제목은 테두리가 아니라 본문 첫 줄(원장 B-15).

지침 1장 2절 5.(4): 제목은 원본 위치대로. 화법과 작문 E26-005 p0157 원본은 `【4문단 초고】` 가
상자 **안** 첫 줄이고 gold 는 `⠿⠛…⠿` / `⠀⠀⠦⠆⠼⠙⠀⠑⠛⠊⠒⠀⠰⠥⠈⠥⠰⠴` / `⠀⠀본문` 이다.
"""
from semojum_braille.encoder import translator as T
from semojum_braille.encoder.layout_braille import _first_indented


def test_괄호_제목은_본문_첫_줄로():
    src = "<!상자>【4문단 초고】<!/상자>\n어떻게 해방될 수 있는가? <!상자끝><!/상자끝>"
    assert T.isolate_border_tags(src).split("\n")[:2] == ["<!상자><!/상자>", "【4문단 초고】"]
    assert T.box_borders_from_source(src)[0] == ("top", 1, "")


def test_맨몸_제목은_테두리_그대로():
    src = "<!상자>보기<!/상자>\nㄱ. 가나다 <!상자끝><!/상자끝>"
    assert "<!상자>보기<!/상자>" in T.isolate_border_tags(src)
    assert T.box_borders_from_source(src)[0][2] == "⠘⠥⠈⠕"


def test_제목_다음_본문도_새_문단():
    border = "⠿" + "⠛" * 30 + "⠿"
    lines = [border, "⠦⠆⠼⠙⠀⠑⠛⠊⠒⠀⠰⠥⠈⠥⠰⠴", "⠎⠠⠊⠎⠴⠈⠝"]
    assert _first_indented(lines) == {1, 2}
    assert _first_indented([border, "⠎⠠⠊⠎⠴⠈⠝", "⠚⠽⠶"]) == {1}   # 종전대로 첫 줄만


def test_지문_구간_라벨은_테두리에_두고_로마자표를_적는다():
    # #1821 — `[A]` ~ `[E]` 는 괄호 제목이어도 위 테두리 제목이다(지침 1장 2절 5.(4)② 재추출 400행).
    #   홀로 선 로마자 제목도 로마자표 ⠴ 를 적는다(「한국 점자 규정」 제29항 1496~1498행 · 예 1505~1506행).
    src = "<!상자>[A]<!/상자>\n가나다 <!상자끝><!/상자끝>"
    assert "<!상자>[A]<!/상자>" in T.isolate_border_tags(src)
    title = T.box_borders_from_source(src)[0][2]
    assert "⠴⠠⠁" in title
    assert title == T._braillify_box_title("[A]")
    assert T.box_borders_from_source("<!상자>[가]<!/상자>\n나 <!상자끝><!/상자끝>")[0][2] == ""   # 한글 괄호 제목은 종전대로 본문
