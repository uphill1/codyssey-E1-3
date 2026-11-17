"""요구사항 04·06: 라벨 정규화와 허용오차(epsilon) 기반 판정."""

EPSILON = 1e-9
UNDECIDED = "UNDECIDED"

# 원본 표기 → 표준 라벨. 프로그램 내부에서는 Cross / X 두 가지만 사용한다.
_LABEL_MAP = {
    "+": "Cross",
    "cross": "Cross",
    "x": "X",
}


def normalize_label(raw):
    """'+', 'cross', 'x' 등 원본 라벨을 'Cross' / 'X'로 표준화.

    알 수 없는 값은 None을 반환하고, 호출한 쪽에서 FAIL로 처리한다.
    """
    if raw is None:
        return None
    key = str(raw).strip().lower()
    return _LABEL_MAP.get(key)


def is_tie(a, b, eps=EPSILON):
    """부동소수점 오차를 고려한 동점 여부."""
    return abs(a - b) < eps


def judge(score_a, score_b, label_a="Cross", label_b="X"):
    """두 점수를 비교해 label_a / label_b / UNDECIDED 반환."""
    if is_tie(score_a, score_b):
        return UNDECIDED
    return label_a if score_a > score_b else label_b
