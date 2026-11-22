"""선분 · 벡터 기호 안 점 이름에 첨자 · 프라임이 들어도 기호가 앞에 남는다(#1756, 원장 B-63).

종전에는 `\\overline{…}` · `\\overrightarrow{…}` 인자 안에 중괄호가 또 있으면(`B_{1}` · `A^{\\prime}`) 정규식이 안 걸려 명령이
남고 버려졌다(R17). 선분 B₁H₁ 의 길이가 곱 B₁ × H₁ 로 읽혔다. 중괄호 없는 `B_1H_1` 은 걸렸지만 연속 대문자 판정이 첨자를
몰라 제23항 켤레 가로바처럼 **뒤에** 붙었다.

기대값은 「한국 점자 규정」 재추출본(유니코드 점자 파일 같은 행)의 예문이다.
"""
import pytest

from semojum_braille.encoder.translator import translate_tagged_text


def _m(latex: str) -> str:
    return translate_tagged_text(f"<!수식>{latex}<!/수식>")


@pytest.mark.parametrize("latex,reg", [
    (r"\overline{AB}", "⠈⠉⠠⠠⠁⠃"),                          # 제35항 3728~3730행
    (r"\overline{A'B'}", "⠈⠉⠠⠠⠁⠤⠃⠤"),                      # 제35항 [붙임] 3731~3734행
    (r"\overline{A^{\prime}B^{\prime}}", "⠈⠉⠠⠠⠁⠤⠃⠤"),      # 같은 예문, 추출이 내는 꼴
    (r"\overline{\mathrm{A^{\prime}B^{\prime}}}", "⠈⠉⠠⠠⠁⠤⠃⠤"),
    (r"\overleftrightarrow{AB}", "⠪⠒⠕⠠⠠⠁⠃"),               # 제37항 3738~3742행
    (r"\overrightarrow{AB}", "⠒⠕⠠⠠⠁⠃"),                    # 제38항 3743~3746행
])
def test_선분_직선_반직선은_규정_예문대로(latex, reg):
    assert _m(latex) == reg


@pytest.mark.parametrize("latex,content", [
    (r"\overline{B_{1}H_{1}}", r"B_{1}H_{1}"),
    (r"\overline {{\mathrm{B} _ {1} \mathrm{H} _ {1}}}", r"B_{1}H_{1}"),
    (r"\overline{B_1H_1}", r"B_1H_1"),
    (r"\overline{\mathrm{AB}_{1}}", r"AB_{1}"),
])
def test_첨자_낀_점_이름의_선분표는_앞에_하나(latex, content):
    """첨자 낀 대문자 연속의 셀 꼴은 규정 예문 · gold 에 없어 자문 대상이다(원장 B-63). 여기서는 선분표 ⠈⠉ 가 앞에 하나
    오고 나머지가 점 이름 그대로인 것만 본다(제35항 3728행 '선분은 ⠈⠉ 으로 적는다')."""
    out = _m(latex)
    assert out == "⠈⠉" + _m(content)
    assert "⣿" not in out and not out.endswith("⠈⠉")


@pytest.mark.parametrize("latex,content,mark", [
    (r"\overrightarrow{A_{1}B}", r"A_{1}B", "⠒⠕"),
    (r"\vec{a_{1}}", r"a_{1}", "⠒⠕"),
])
def test_첨자_낀_벡터도_기호가_앞에_남는다(latex, content, mark):
    assert _m(latex) == mark + _m(content)


def test_대문자_하나나_식_위_가로바는_지금처럼_뒤에_붙는다():
    """제23항 1호 가 켤레 복소수(3626~3629행 `―a+bi` = ⠷⠁⠢⠃⠊⠾⠈⠉) · 나 평균(3630~3632행 `―x` = ⠭⠈⠉)."""
    assert _m(r"\overline{a+bi}") == "⠷⠁⠢⠃⠊⠾⠈⠉"
    assert _m(r"\bar{x}") == "⠭⠈⠉"
    out = _m(r"\overline{B_{1}}")
    assert out.endswith("⠈⠉") and not out.startswith("⠈⠉")
