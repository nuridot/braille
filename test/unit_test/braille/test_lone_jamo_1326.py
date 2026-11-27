"""#1326 — 홀로 쓴 자음자를 첫가끝 초성(U+1100~)으로 받아도 온표 + 받침꼴로 점역한다(제8항)."""
from semojum_braille.encoder import translator as T


def test_첫가끝_초성으로_쓴_홀로_자음도_온표와_받침꼴이다():
    # 「한국 점자 규정」 제8항 예(재추출 479~480행): `삼각형 ㄱㄴㄷ` = l5$aj}`=a=3=9(규정 BRF 백틱은 빈칸)
    assert T.translate_tagged_text("삼각형 ᄀᄂᄃ") == "⠇⠢⠫⠁⠚⠻⠀⠿⠁⠿⠒⠿⠔"
    # gold 언어와 매체 본책 p0014 `‘ㄴ’ 첨가` — 한컴 글자층은 ㄴ 을 U+1102 로 싣는다(종전 ⠉ = 약자 '나')
    assert T.translate_tagged_text("‘ᄂ’ 첨가").startswith("⠠⠦⠿⠒⠴⠄⠀⠰⠎⠢⠫")


def test_중성이_이어지는_옛한글_초성은_건드리지_않는다():
    for s in ("하ᄂᆞᆯ히", "말ᄊᆞ미", "나"):
        assert T._LONE_CHO_RE.search(s) is None, s


def test_홀로_쓴_자모_뒤_두_음절_조사도_온표다():
    # B-20 #1861. 「점자 자료 제작 지침」 [예 2-26](재추출 1416 · 1420~1421행)
    #   `ㄱ에서 ㅎ까지 … ㅏ~ㅣ까지` = `=an,s` · `=0,$.o` · `=<@9=o,$.o`. braillify 는 뒤가 두 음절이면 제10항 `_` 로 냈다
    out = T.translate_tagged_text("ㄱ에서 ㅎ까지, ㅏ~ㅣ까지")
    assert out.startswith("⠿⠁⠝⠠⠎⠀⠿⠴⠠⠫⠨⠕"), out
    assert "⠿⠣⠈⠔⠿⠕⠠⠫⠨⠕" in out, out
    # 제10항 — 단어에 붙은 자음자는 그대로 `_`(재추출 523~524행 `Roma [ㄹㄹ로마]`)
    assert "⠦⠆⠸⠂⠸⠂⠐⠥⠑⠰⠴" in T.translate_tagged_text("Roma [ㄹㄹ로마]")   # 524행 `82_1_1"ue;0`


def test_홀로_쓴_아래아는_온표다():
    # 제25항 ㆍ = `"#`(재추출 1239 · 1247행) + 제8항 온표. 지침 [예 2-26](1413 · 1417행) `아래아(ㆍ)` = `<"r<8'="#,0`
    assert T.translate_tagged_text("아래아(ㆍ)") == "⠣⠐⠗⠣⠦⠄⠿⠐⠼⠠⠴"
    assert T.translate_tagged_text("개인적ㆍ사회적") == T.translate_tagged_text("개인적·사회적")   # 한글 사이는 가운뎃점 대용
