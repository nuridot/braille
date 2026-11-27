"""#839 · #1840 — 격자 표의 행 머리 뒤 구분자.

#1840(대표 결정 P-17, 2026-11-26, 원장 C-140): 행 머리 뒤는 **늘 쌍점**이다.
  「점자 도서 제작 지침」 3장 2절 1)(1)③(재추출 1770~1772행) "행 제목과 항목 사이는 쌍점 "1으로 구분한다".
  쌍점 점형 ⠐⠂ 은 「한국 점자 규정」 제49항 표(재추출 2133행), 뒤 한 칸은 제51항(2346행).
  값과 값 사이는 지침 1647행 "표의 셀과 셀 사이는 두 칸을 띄어 구분한다".
  1773~1774행 [다만](단순한 표는 두 칸 허용)은 기본이 아니라 허용이다.
종전 판정(`_sep_word_level`, 칸 중앙값 ≤14 면 두 칸)은 `TABLE_GRID_SEP=auto` 로 되돌린다.
표는 모두 지어낸 것이다.
"""
import importlib
import os

import pytest

from semojum_braille.encoder import table_braille as tb

# 낱말 수준 — 종전 판정은 두 칸이었다.
WORD_TABLE = "구분|2020|2021\n첫째|88.9|89.2\n둘째|11.1|10.8"

# 문장 수준 — 중앙값 셀이 14셀을 넘는다.
SENT_TABLE = ("구분|설명\n"
              "계층 이동의 의미|한 개인이나 집단의 사회적 위치가 바뀌는 현상을 뜻한다\n"
              "수직 이동의 특징|계층적 위치가 상승하거나 하강하는 이동을 가리킨다\n"
              "수평 이동의 특징|같은 계층 안에서 자리만 옮겨 가는 이동을 가리킨다")

COLON = "⠐⠂⠀"     # 쌍점(제49항 2133행) + 뒤 한 칸(제51항 2346행)


@pytest.fixture(autouse=True)
def _default(monkeypatch):
    monkeypatch.delenv("TABLE_GRID_SEP", raising=False)


def _body(text: str) -> list[str]:
    """테두리·행 구분선을 뺀 내용 줄."""
    return [ln for ln in tb._render_grid(text)
            if ln.strip("⠀") and not ln.startswith(("⠿", "⠐⠐"))]


def _row(text: str, head: str) -> str:
    return next(ln for ln in _body(text) if ln.startswith("⠀⠀" + tb._translate(head)))


class TestGridRowHeadSeparator:
    def test_낱말_수준도_행_머리_뒤는_쌍점(self) -> None:
        row = _row(WORD_TABLE, "첫째")
        assert tb._translate("첫째") + COLON + tb._translate("88.9") in row, row

    def test_문장_수준도_쌍점(self) -> None:
        row = _row(SENT_TABLE, "계층 이동의 의미")
        assert tb._translate("계층 이동의 의미") + COLON in row, row

    def test_값_사이는_두_칸이다(self) -> None:
        row = _row(WORD_TABLE, "첫째")
        assert tb._translate("88.9") + "⠀⠀" + tb._translate("89.2") in row, row

    def test_auto_는_종전_판정으로_돌아간다(self, monkeypatch) -> None:
        monkeypatch.setenv("TABLE_GRID_SEP", "auto")
        assert not any("⠐⠂" in ln for ln in _body(WORD_TABLE)), "auto 에서 낱말 표가 두 칸이 아니다"
        assert any("⠐⠂" in ln for ln in _body(SENT_TABLE)), "auto 에서 문장 표 쌍점이 사라졌다"
        # 스위치를 내리면 곧바로 쌍점 기본으로 — 임포트 때 굳지 않는다.
        monkeypatch.delenv("TABLE_GRID_SEP")
        assert any(COLON in ln for ln in _body(WORD_TABLE))

    def test_auto_에서_두_렌더러가_같은_판정을_쓴다(self, monkeypatch) -> None:
        """`TABLE_GRID_SEP=auto` 의 `_render_grid` 는 `_render_unfold` 와 같은 `_sep_word_level` 을 쓴다(#839 원인)."""
        monkeypatch.setenv("TABLE_GRID_SEP", "auto")
        for text in (WORD_TABLE, SENT_TABLE):
            rows = [[c.strip() for c in r.split("|")] for r in text.splitlines() if r.strip()]
            want_colon = not tb._sep_word_level(rows)
            got_colon = any("⠐⠂" in ln for ln in _body(text))
            assert got_colon is want_colon, f"판정과 출력이 어긋난다: {text.splitlines()[0]!r}"


class TestRegulationMode:
    @pytest.fixture()
    def regulation(self):
        os.environ["BRAILLE_STYLE"] = "regulation"
        importlib.reload(tb)
        yield tb
        os.environ.pop("BRAILLE_STYLE", None)
        importlib.reload(tb)

    def test_규정_모드도_행_머리_뒤는_쌍점(self, regulation) -> None:
        """지침 1770~1772행 기본이 쌍점이라 규정 모드도 같다."""
        row = next(ln for ln in regulation._render_grid(WORD_TABLE)
                   if ln.startswith("⠀⠀" + regulation._translate("첫째")))
        assert regulation._translate("첫째") + COLON in row, row
