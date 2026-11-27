"""한글 낱말에 붙은 단위 · 유전자형 괄호 뒤 연산 기호는 한글 사이 연산이다(#1894, B-20).

「한국 점자 규정」 제46항 예(재추출 2071행) `(신장(m) × 신장(m))` = 글 괄호 ⠦⠄⠴m⠠⠴ · × 앞뒤 한 칸.
종전엔 `(m) ×` 를 평문 수식으로 감싸 수식 괄호 ⠦m⠴ 와 앞뒤 두 칸이 나갔다.
"""
from semojum_braille.encoder import inline_math
from semojum_braille.encoder.translator import element_type, translate_with_breaks


def _tr(s: str) -> str:
    with element_type("text"):
        return "".join(translate_with_breaks(s)[0])


def test_단위_괄호_뒤_곱셈표는_수식으로_감싸지_않는다():
    assert inline_math.wrap("(신장(m) × 신장(m))") == "(신장(m) × 신장(m))"
    # 규정 2071행 셋째 줄 · 둘째 줄 끝: `,q.78'0m,0`*`,q.78'0m,0,0`
    assert _tr("(신장(m) × 신장(m))") == "⠦⠄⠠⠟⠨⠶⠦⠄⠴⠍⠠⠴⠀⠡⠀⠠⠟⠨⠶⠦⠄⠴⠍⠠⠴⠠⠴"


def test_한글에_안_붙은_괄호식은_그대로_수식이다():
    assert inline_math.wrap("f(x) × g(x)") == "<!수식>f(x) × g(x)<!/수식>"
