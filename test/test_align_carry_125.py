# -*- coding: utf-8 -*-
"""정렬 태그는 그 줄 전체부터 다음 정렬 태그 앞까지 이어진다(#125, 대표 지시 2026-11-16).

실로암브레일 Pro 2 에서 같은 글을 출력용 점자 문서로 만들어 본 동작과 같다.
`ab<sc>cd` 는 `abcd` 한 줄 전체가 가운데이고, 다음 줄도 다음 코드가 나올 때까지 가운데다.
"""
from semojum_braille import assist, sidecar
from semojum_braille.assist import carry_aligns

COLS = 32
SP = "⠀"


def _lead(line: str) -> int:
    return len(line) - len(line.lstrip(SP))


def _job(*blocks):
    return {"sources": [{"orig_page": 1, "blocks": [dict(b, order=i) for i, b in enumerate(blocks)]}],
            "opts": {"page_row_pages": "none"}}


def _block(text: str) -> dict:
    r = sidecar.translate(text, blank_lines=False)
    b = {"braille": r["cells"], "breaks": r["breaks"]}
    if "line_alignment" in r:
        b["line_alignments"] = r["line_alignment"]
    return b


def test_대표_예시_세_줄():
    """네모<!가운데정렬>치킨 / 바보 / 부자<!오른쪽정렬> → 가운데 · 가운데 · 오른쪽."""
    page = assist.build_pages_from_job(_job(_block("네모<!가운데정렬>치킨\n바보\n부자<!오른쪽정렬>")))[0]
    one, two, three = page[:3]
    assert _lead(one) == (COLS - len(one.strip(SP))) // 2       # 네모치킨 가운데
    assert _lead(two) == (COLS - len(two.strip(SP))) // 2       # 바보도 가운데(이어짐)
    assert len(three) == COLS and _lead(three) == COLS - len(three.strip(SP))   # 부자 오른쪽


def test_태그는_줄_중간에_있어도_그_줄_전체에_걸린다():
    r = sidecar.translate("네모<!가운데정렬>치킨", blank_lines=False)
    assert r["line_alignment"][0]["align"] == "center"
    assert r["line_alignment"][0]["source_start"] == 0 and r["line_alignment"][0]["source_end"] == 4


def test_정렬은_다음_블록으로_이어진다():
    page = assist.build_pages_from_job(_job(_block("<!오른쪽정렬>제목"), _block("본문 한 줄")))[0]
    assert _lead(page[1]) == COLS - len(page[1].strip(SP))


def test_왼쪽정렬이_나오면_거기서_끊긴다():
    page = assist.build_pages_from_job(
        _job(_block("<!가운데정렬>제목"), _block("<!왼쪽정렬>둘째"), _block("셋째")))[0]
    assert _lead(page[0]) > 0
    assert _lead(page[1]) == 0 and _lead(page[2]) == 0     # 왼쪽은 들여쓰기도 걷는다


def test_태그가_한_번도_없으면_받은_그대로다():
    """정렬 태그가 없는 문서는 종전과 바이트로 같다(들여쓰기 유지)."""
    plain = _block("본문 한 줄")
    assert "line_alignments" not in plain
    page = assist.build_pages_from_job(_job(plain))[0]
    assert page[0] == plain["braille"]


def test_정렬은_원본_쪽을_넘어_이어진다():
    job = {"sources": [{"orig_page": 1, "blocks": [dict(_block("<!가운데정렬>첫 쪽"), order=0)]},
                       {"orig_page": 2, "blocks": [dict(_block("둘째 쪽"), order=0)]}],
           "opts": {"page_row_pages": "none", "show_change_line": False}}
    page = assist.build_pages_from_job(job)[0]
    body = [ln for ln in page if ln.strip(SP)]
    assert all(_lead(ln) == (COLS - len(ln.strip(SP))) // 2 for ln in body[:2])


def test_옛_align_칸은_그_블록_첫_줄_태그로_읽고_이어진다():
    job = _job({"braille": "⠁⠃", "align": "center"}, {"braille": "⠉⠙"})
    page = assist.build_pages_from_job(job)[0]
    assert _lead(page[0]) == 15 and _lead(page[1]) == 15


def test_carry_aligns_는_블록마다_줄별_값을_낸다():
    blocks = [{"text": "⠁\n⠃", "line_alignments": [{"braille_start": 2, "align": "right"}]},
              {"text": "⠉"}, {"text": "⠙", "align": "left"}]
    eff, state = carry_aligns(blocks)
    assert eff == [["", "right"], ["right"], ["left"]] and state == "left"


def test_줄이_안_맞으면_line_alignment_를_내지_않는다():
    assert sidecar.line_alignment("가\n나", "⠁") is None


def test_line_alignment_좌표는_앞_빈칸을_지난다():
    rows = sidecar.line_alignment("<!가운데정렬>가\n나", "⠀⠀⠁\n⠃")
    assert rows[0]["braille_start"] == 2 and rows[0]["braille_end"] == 3
    assert rows[1] == {"source_start": 2, "source_end": 3, "braille_start": 4, "braille_end": 5,
                       "align": "", "effective": "center"}


def test_머리말_안_정렬_태그는_줄_정렬이_아니다():
    r = sidecar.translate("<!머리말><!오른쪽정렬>머리<!/머리말>본문", blank_lines=False)
    assert "line_alignment" not in r


def test_translate_page_도_line_alignment_를_낸다():
    res = sidecar.translate_page([{"text": "<!가운데정렬>가운데"}, {"text": "본문"}])
    first, second = res["elements"]
    assert first["line_alignment"][0]["align"] == "center"
    assert "line_alignment" not in second
