"""요구사항 07: 크기별 MAC 연산 시간 측정."""
import time

REPEAT = 10
WARMUP = 5


def measure_ms(func, *args, repeat=REPEAT):
    """func(*args) 호출 구간만 repeat회 측정해 평균(ms) 반환.

    I/O(input/print/파일 읽기)는 측정 구간에 넣지 않는다.
    첫 호출의 캐시/초기화 영향을 줄이기 위해 WARMUP회 먼저 실행한 뒤 측정한다.
    """
    for _ in range(WARMUP):  # 워밍업 (측정 제외)
        func(*args)
    elapsed = 0.0
    for _ in range(repeat):
        t0 = time.perf_counter()
        func(*args)
        elapsed += time.perf_counter() - t0
    return elapsed / repeat * 1000


def print_perf_table(rows, repeat=REPEAT):
    """rows: [(n, avg_ms), ...] → 크기 / 평균 시간 / 연산 횟수(N²) 표."""
    print("\n[성능 분석] (각 크기 %d회 반복 평균)" % repeat)
    print("%-10s %14s %14s" % ("크기(N×N)", "평균 시간(ms)", "연산 횟수(N²)"))
    print("-" * 42)
    for n, ms in rows:
        print("%-10s %14.4f %14d" % ("%dx%d" % (n, n), ms, n * n))
