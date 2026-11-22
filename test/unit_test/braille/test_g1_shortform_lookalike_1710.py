"""#1710: 단축형으로 읽힐 수 있는 글자열 앞 1종 지시자 ⠰(통일영어점자 10.9.5). 한글 없고 영어 산문도 아닌 줄(라벨 · 홀로 선
낱말)에서도 두 글자 이상 약자꼴에는 적고, 홑 낱자는 원장 C-99 대로 안 적는다. 글자열은 UEB 원문에 없는 것으로 골랐다."""
import pytest

from semojum_braille.encoder.translator import translate_with_breaks


def T(s: str) -> str:
    return "".join(translate_with_breaks(s)[0])


@pytest.mark.parametrize("src, want", [
    ("GD", "⠰⠠⠠⠛⠙"),               # 홀로 선 대문자 약어 = 단축형 good 의 셀
    ("QK", "⠰⠠⠠⠟⠅"),
    ("Brlova", "⠰⠠⠃⠗⠇⠕⠧⠁"),        # 첫 글자만 대문자인 낱말이 brl(braille)로 시작
    ("Grtek", "⠰⠠⠛⠗⠞⠑⠅"),           # grt(great)로 시작
])
def test_라벨_줄의_여러_글자_약자꼴에_적는다(src, want):
    assert T(src) == want


@pytest.mark.parametrize("src, want", [
    ("B", "⠠⠃"),                    # 홑 낱자 라벨은 C-99 대로 안 적는다
    ("Blake", "⠠⠃⠇⠁⠅⠑"),            # bl 뒤가 모음이면 단축형으로 안 읽힌다
    ("3ab", "⠼⠉⠀⠁⠃"),              # 수 뒤 a~j 는 띄움으로 가른다(C5 방어), 홀로 선 자리가 아니다
])
def test_라벨_줄이라도_안_적는다(src, want):
    assert T(src) == want


def test_한글_문장_속_고유명사도_머리를_본다():
    assert "⠴⠰⠠⠛⠗⠞⠑⠅" in T("이름은 Grtek 이다")
