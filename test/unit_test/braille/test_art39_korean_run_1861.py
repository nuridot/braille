"""제39항 영어 문장 판정 — 한글 낱말이 잇달면(한국어 문장) 영어 문장 속 한글이 아니다(#1861, eval E-44 회차 8).

듣기 대본처럼 영어 대화 뒤에 한글 번역이 같은 줄에 붙은 꼴을 받아, 한글 낱말마다 한글표 ⠸⠷…⠸⠾ 로 감쌌다.
"""
from semojum_braille.encoder.translator import _english_sentence_with_hangul, translate_with_breaks


def test_영어_대화_뒤_한글_번역은_영어_문장이_아니다():
    s = "W: Don't worry too much. You'll do just fine. 너무 걱정하지 마. 넌 정말 잘할 거야."
    assert not _english_sentence_with_hangul(s)
    assert "⠸⠷" not in "".join(translate_with_breaks(s)[0])


def test_영어_문장_속_한글_낱말_하나는_그대로():
    # 「점자 자료 제작 지침」 [예 2-37](재추출 1672~1676행) · 「한국 점자 규정」 제39항 예(1896 · 1901행)
    for s in ("I love 떡갈비.", "What is 김치 in English?",
              "Banchan (Korean: 반찬) are small side dishes served along with cooked rice in Korean cuisine."):
        assert _english_sentence_with_hangul(s), s
