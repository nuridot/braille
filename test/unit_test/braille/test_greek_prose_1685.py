"""#1685: 그리스 글자가 낀 영어 산문을 식으로 감싸지 않는다.

「한국 점자 규정」 제30항(재추출 1508행) 그리스 문자는 「통일영어점자 규정」에 따라 적는다.
예 `α or β` = `.a`or`.b`(1637~1638행) · α `.a`(1513행) · β `.b`(1518행) · θ `.?`(1548행).
평문 수식 감지가 그리스 글자 하나를 강한 수식 신호로 보고 한글 없는 줄을 통째로 감싸, 수식 길에서 `\\alpha` 명령 뒤
빈칸이 먹혔다(`⠨⠁⠕⠗`). 연산 · 관계 기호와 첨자 없이 함수 이름 아닌 소문자 낱말(두 글자 이상)이 끼면 식이 아니다.
글은 규정 예 하나 말고는 지어 썼다.
"""
from semojum_braille.encoder import inline_math
from semojum_braille.encoder.translator import translate_tagged_text


def test_규정_예_그리스_글자_사이_영어_낱말():
    assert inline_math.wrap("α or β") == "α or β"
    assert translate_tagged_text("α or β") == "⠨⠁⠀⠕⠗⠀⠨⠃"          # 1638행 `.a`or`.b`


def test_영어_문장_속_그리스_글자_뒤_빈칸():
    t = "the angle θ is small"
    assert inline_math.wrap(t) == t
    assert "⠨⠹⠀" in translate_tagged_text(t)                         # θ 뒤 빈칸이 남는다


def test_연산_기호나_함수_이름이_있으면_종전대로_식():
    assert inline_math.wrap("sin θ") == "<!수식>\\sin θ<!/수식>"
    assert inline_math.wrap("θ+φ") == "<!수식>θ+φ<!/수식>"
    assert inline_math.wrap("x=θ or x=φ").startswith("<!수식>")
