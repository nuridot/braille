"""#1698: 한글 없는 영어 산문 줄의 화살표 · 괄호 · 쌍점 · % · ° 는 통일영어점자 꼴이다.

근거: 「한국 점자 규정」 제32항(재추출 1650~1651행)이 로마자 구간을 「통일영어점자 규정」에 맡기고, 제33항(1667~1669행)은
로마자와 **한글 사이**의 , : ; ― 만 한글 꼴로 적게 한다. 한글 없는 영어 줄은 통째로 로마자 구간이다.
점형: 화살표 ⠰⠳⠕(UEB 3.2.1, 1548~1557행) · ° ⠘⠚(3.11, 1771행) · % ⠨⠴(3.21, 1996행) · 숫자 뒤 쌍점은 ⠒ 이고 숫자 모드가
끝나 뒤 숫자에 수표를 다시 적는다(6.3.1, 2923~2927행) · 괄호 ⠐⠣ ⠐⠜(제32항 예 1664~1666행). 글은 모두 지어낸 것이다.
"""
from __future__ import annotations

import pytest

from semojum_braille.encoder.translator import translate_tagged_text

B = "⠀"


def _t(text: str) -> str:
    return translate_tagged_text(text)


def test_영어_줄_화살표는_통일영어점자_꼴이고_로마자표가_없다():
    out = _t("Do you want to join the club today? (M) → Sorry, I have to finish my homework. (W)")
    assert "⠰⠳⠕" in out and "⠒⠕" not in out
    assert "⠴" not in out                                  # 구간이 안 끊긴다(한글 꼴 화살표 뒤 ⠴ 다시 열기 없음)
    assert "⠐⠣⠰⠠⠍⠐⠜" in out and "⠐⠣⠰⠠⠺⠐⠜" in out          # 줄 가운데 화자 표시는 구간 안 괄호


def test_줄_가운데_홑_낱자_괄호는_구간_안_괄호():
    assert "⠐⠣⠰⠠⠺⠐⠜" in _t("the red bench (W) → the blue one")     # 구 뒤 화자 표시(듣기 메모)
    out = _t("Choose the answer (A) or (B).")
    assert "⠐⠣⠠⠁⠐⠜" in out and "⠐⠣⠰⠠⠃⠐⠜" in out and "⠶" not in out


@pytest.mark.parametrize("text,cells", [
    ("About 90% of the members voted.", "⠼⠊⠚⠨⠴"),
    ("It was 30°C in the morning.", "⠼⠉⠚⠘⠚⠠⠉"),
    ("The bus leaves at 7:30 every day.", "⠼⠛⠒⠼⠉⠚"),
])
def test_영어_줄_숫자_뒤_기호(text: str, cells: str):
    assert cells in _t(text)


@pytest.mark.parametrize("text", ["The ticket costs \\$15 for adults.", "The ticket costs $15 for adults."])
def test_영어_줄_달러는_통일영어점자_꼴(text: str):
    out = _t(text)                                         # UEB 3.10(1734~1745행 `$6` = `@s#f`)
    assert "⠈⠎⠼⠁⠑" in out and "⠴⠈⠎" not in out and "⠸⠡" not in out


@pytest.mark.parametrize("text", ["3 C \\$9 Bamboo 4", "(B) 300g, \\$15"])
def test_로마자가_든_한글_없는_줄의_달러도_통일영어점자_꼴(text: str):
    out = _t(text)                                         # 표 행 · 무게와 값 줄(산문 문턱 밖)
    assert "⠈⠎⠼" in out and "⠴⠈⠎" not in out


@pytest.mark.parametrize("text", ["Emma: <!밑줄>", "Emma: <!밑줄> <!밑줄>", "Emma:"])
def test_받아쓰기_화자_줄은_통일영어점자_쌍점과_빈칸(text: str):
    out = _t(text)
    assert out.startswith("⠠⠑⠍⠍⠁⠒") and "⠐⠂" not in out and "⠸⠤" not in out
    assert out.count("⠨⠤") == text.count("<!밑줄>")


@pytest.mark.parametrize("text,head", [
    ("Ms. Parker: <!밑줄> <!밑줄>", "⠠⠏⠜⠅⠻⠒"),           # 두 낱말 이름은 산문 길로 가도 화자 쌍점이다
    ("Tour Guide: <!밑줄>", "⠠⠛⠥⠊⠙⠑⠒"),
    ("Mr. Kim:", "⠠⠅⠊⠍⠒"),
])
def test_두_낱말_화자_줄도_통일영어점자_쌍점(text: str, head: str):
    out = _t(text)
    assert head in out and "⠐⠂" not in out and out.count("⠨⠤") == text.count("<!밑줄>")


@pytest.mark.parametrize("text,keep", [
    ("가격이 45% 올랐다.", "⠴⠏"),                        # 한글 줄은 한글 꼴(제69항 단위)
    ("온도는 28°C 이다.", "⠴⠙"),
    ("가 → 나", "⠒⠕"),
    ("H, Cl → HCl", "⠒⠕"),                              # 반응식 줄은 산문이 아니다
    ("dis(= not) + agree → disagree", "⠒⠕"),            # 어원 줄(`=` · `+`)은 종전대로
    ("(a) The cat sat on the mat.", "⠶⠁⠶"),             # 줄머리 보기 표지는 원장 C-165 A-2 관행 그대로
    ("(B) The dog ran to the park.", "⠶⠰⠠⠃⠶"),
    ("humble <!밑줄>", "⠸⠤"),                           # 단어장 뜻 칸
    ("A: O  X  X", "⠐⠂"),                               # 홑 글자 이름표
    ("가격은 \\$10 이다.", "⠴⠈⠎⠼⠁⠚"),                     # 한글 줄 달러는 제65항 화폐 꼴(2594~2620행)
    ("① \\$40", "⠴⠈⠎⠼⠙⠚"),                              # 수 · 달러만 든 선택지 줄은 원장 C-202 보류(규정 꼴)
])
def test_영어_산문_줄_밖은_종전대로(text: str, keep: str):
    assert keep in _t(text)
