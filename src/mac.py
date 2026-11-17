"""요구사항 05: MAC(Multiply-Accumulate) 연산. 외부 라이브러리 사용 금지."""


def mac(pattern, filt):
    """같은 위치끼리 곱해서(Multiply) 모두 누적(Accumulate)한 점수.

    N×N 이면 곱셈/덧셈이 각각 N²번 → O(N²).
    """
    total = 0
    n = len(pattern)
    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filt[i][j]
    return total


def mac_flat(pattern_flat, filt_flat):
    """보너스 1: 1차원(길이 N²) 리스트용 MAC. 이중 인덱싱 없이 단일 반복문."""
    total = 0
    for k in range(len(pattern_flat)):
        total += pattern_flat[k] * filt_flat[k]
    return total
