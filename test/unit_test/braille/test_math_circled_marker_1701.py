"""#1701: 수식 구분자 안에 원문자 하나만 든 자리는 수식이 아니라 원문자다.

MinerU 가 받아쓰기 번호 ❶ 을 윗첨자 `$^{①}$` 로 감싸 낸다. 수식으로 점역하면 윗첨자표가 붙고(수학 제18항, 재추출 3528행
위첨자 기호 ^ = ⠘), 줄이 수식 조각에서 갈려 화자 쌍점 · 밑줄 빈칸이 한글 꼴로 나간다. 글은 지어낸 것이다.
"""
from __future__ import annotations

import pytest

from semojum_braille.encoder.translator import translate_tagged_text as _t


@pytest.mark.parametrize("wrapped", ["$^{①}$", "$①$", "$_{①}$", "$^①$"])
def test_원문자_하나만_감싼_수식은_원문자와_같다(wrapped: str):
    plain = _t("He wanted to ① <!밑줄> <!밑줄> at the park.")
    assert _t(f"He wanted to {wrapped} <!밑줄> <!밑줄> at the park.") == plain
    assert "⠼⠂" in plain


def test_감싼_원문자가_든_받아쓰기_줄은_한_줄로_점역된다():
    out = _t("M: Kate $^{②}$ <!밑줄> <!밑줄> every weekend.")
    assert out.startswith("⠰⠠⠍⠒")                            # 화자 쌍점이 구간 안 쌍점(⠐⠂ 아님)
    assert out.count("⠨⠤") == 2 and "⠸⠤" not in out


def test_다른_것이_든_수식은_그대로_수식이다():
    assert "⠘" in _t("$x^{①}$")                              # 윗첨자표가 남는다
