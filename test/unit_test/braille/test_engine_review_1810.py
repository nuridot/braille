"""#1810 전수 점검 엔진 몫: 평문 결합 윗줄 선분 · 해설 권 문항 머리 앞 빈 줄.

기대값 근거(「한국 점자 규정」 재추출 행): 수학 제35항 선분 `A̅B̅ ⠈⠉⠠⠠⠁⠃`(3729~3730) · 제23항 평균 `x̅ ⠭⠈⠉`(3631~3632) ·
제12항 1 수식은 로마자표 없이 앞뒤 두 칸(`이 방정식의 해는 x=1 이다` 3256~3257).
"""
from semojum_braille.encoder import layout_braille as L
from semojum_braille.encoder.translator import translate_tagged_text


def test_plain_overline_segment_goes_math_path():
    out = translate_tagged_text("선분 AB̅의 길이")
    assert "⠀⠀⠈⠉⠠⠠⠁⠃⠀⠀" in out           # 선분표가 앞, 수식이라 두 칸
    assert "⠴" not in out and "⠲⠈⠉" not in out  # 로마자표 · 뒤에 붙은 윗줄표 없음


def test_plain_overline_on_each_letter_and_mean_bar():
    assert "⠈⠉⠠⠠⠁⠃" in translate_tagged_text("변 A̅B̅와")
    assert "⠭⠈⠉" in translate_tagged_text("평균 x̅는")


def test_explanation_question_head_gets_lead_blank():
    assert L._q_blanks(["⠀⠀⠼⠚⠋⠀⠨⠝"], "  06 제4차 십자군 전쟁의 전개 이해") == (frozenset(), True)
    # 글 속 숫자로 여는 문장 · 여러 줄 요소는 머리가 아니다
    assert L._q_blanks(["⠀⠀⠼⠃⠚"], "  20 세기 초에 많은 변화가 일어났다.") == (frozenset(), False)
    assert L._q_blanks(["⠀⠀⠼⠃⠚", "⠀⠀⠁"], "  20 세기 초\n이어지는 글") == (frozenset(), False)


def test_furniture_is_not_explanation_head():
    # 단원 꼬리말(`01 지수와 로그`)은 쪽 머리 꼬리말이라 문항 머리 빈 줄을 안 받는다(사이드카 force_roman 시험이 잡음)
    assert L._q_blanks(["⠼⠚⠁⠀⠨⠕"], "01 지수와 로그", "header_footer") == (frozenset(), False)
    assert L._q_blanks(["⠼⠚⠁⠀⠨⠕"], "01 지수와 로그", "text") == (frozenset(), True)
