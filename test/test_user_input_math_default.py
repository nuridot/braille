"""점역사가 앱에서 친 글의 수식 판단 — 쪽 문맥이 없는 기본값(`math_page` 거짓)에서 무엇을 수식으로 보는가.

앱은 블록을 벗어나거나 엔터를 칠 때 블록 하나를 사이드카 `translate` 로 넘긴다(2026-11-21 대표 결정).
사람이 친 글에는 쪽 PDF 가 없어 수식 쪽 신호(한컴 수식 글꼴 비율)를 못 재므로 `math_page` 는 기본 거짓이다.
이 값에서는 **강한 신호**(그리스 문자 · 첨자 · 함수 이름 · 연산자 낀 등식)만 수식으로 잡고 `p-q` · `(x, y)` ·
`a>1` · `(t>0)` 같은 약한 신호는 글로 둔다. 한글 본문을 수식으로 잘못 잡으면 점역사가 지우고 다시 쳐야 해서
빠뜨리는 쪽이 낫다는 판단이다(V2 `temp/n488/Braille_prompt.md` B-1). 이 시험이 그 기본값을 굳힌다.
"""
import pytest

from semojum_braille import sidecar

# 「한국 점자 규정」 수학 제11항 2호(재추출 3321행) "국어 문장 안에 로마자가 포함된 수학적 표기는 수식에 따른다",
# 제12항 1호(3308~3309행) 로마자표 없이 앞뒤 두 칸. 묵자 · 점자는 그 예문(유니코드 점자 파일 같은 행).
_STRONG = [
    ("이 방정식의 해는 x=1 이다.", "⠀⠀⠕⠀⠘⠶⠨⠻⠠⠕⠁⠺⠀⠚⠗⠉⠵⠀⠀⠭⠒⠒⠼⠁⠀⠀⠕⠊⠲"),   # 3315~3316행 · 등식
    ("일반항 aₙ의 값", "⠕⠂⠘⠒⠚⠶⠀⠀⠁⠰⠝⠀⠀⠺⠀⠫⠃⠄"),                          # 3322행 · 아래 첨자
    ("2⁴⁰은 몇 자리 정수인가?", "⠀⠀⠼⠃⠘⠼⠙⠚⠀⠀⠵⠀⠑⠱⠆⠀⠨⠐⠕⠀⠨⠻⠠⠍⠟⠫⠦"),            # 3246~3247행 · 위 첨자
]


@pytest.mark.parametrize("text,reg", _STRONG)
def test_강한_신호는_쪽_문맥_없이도_규정대로_수식이다(text, reg):
    cells = sidecar.translate(text)["cells"]
    assert cells.lstrip("⠀") == reg.lstrip("⠀")
    assert cells == sidecar.translate(text, math_page=True)["cells"]      # 쪽 문맥과 무관


# 약한 신호. 수식 쪽이면 수식(로마자표 없음 · 수식 소괄호)이고, 기본값이면 글이다 — 글의 로마자는 로마자표 ⠴
# (「한국 점자 규정」 제29항, 수학 제12항 1호 3308행이 '수식에서는 적지 않는다'는 그 ⠴), 글의 소괄호는 ⠦⠄ … ⠠⠴(2156~2157행).
@pytest.mark.parametrize("text,text_mark", [
    ("두 수의 차 p-q가 양수이다.", "⠴"),
    ("a>1일 때", "⠴"),
    ("점 (x, y)를 지난다.", "⠦⠄"),
    ("조건 (t>0)에서", "⠦⠄"),
])
def test_약한_신호는_수식_쪽에서만_수식이다(text, text_mark):
    plain = sidecar.translate(text)["cells"]
    math = sidecar.translate(text, math_page=True)["cells"]
    assert plain != math
    assert text_mark in plain and text_mark not in math
    assert sidecar.translate(text)["cells"] == plain                     # 켠 값이 다음 요청으로 새지 않는다


def test_한글_문장은_수식으로_잡지_않는다():
    """오탐 방지 — 수 범위 · 로마자 낱말은 기본값에서 글이다(수식 두 칸이 안 붙는다)."""
    for text in ("3-4쪽을 펴서 읽는다.", "우리 반은 A팀이다."):
        cells = sidecar.translate(text)["cells"]
        assert "⠀⠀⠀" not in cells.lstrip("⠀"), (text, cells)
        assert cells == sidecar.translate(text, math_page=True)["cells"], text
