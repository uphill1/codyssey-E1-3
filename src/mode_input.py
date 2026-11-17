"""요구사항 02: 모드 1 - 3×3 사용자 입력."""
from src.judge import judge, UNDECIDED
from src.mac import mac
from src.perf import measure_ms, print_perf_table

ERR_COUNT = "입력 형식 오류: 각 줄에 %d개의 숫자를 공백으로 구분해 입력하세요."
ERR_NUMBER = "입력 형식 오류: 숫자만 입력할 수 있습니다. (예: 0 1 0 또는 0.5 1 0)"


def parse_number(text):
    """int를 먼저 시도하고, 실패하면 float으로 변환 (5.0 대신 5로 표시)."""
    try:
        return int(text)
    except ValueError:
        return float(text)  # 여기서도 실패하면 ValueError가 호출자로 전달됨


def read_matrix(name, n=3):
    """n×n 행렬을 한 줄씩 입력받는다. 형식 오류 시 안내 후 처음부터 재입력."""
    while True:
        print("\n%s (%d×%d)를 한 줄씩 입력하세요. 예: 0 1 0" % (name, n, n))
        rows, ok = [], True
        for i in range(n):
            parts = input("  %d행: " % (i + 1)).split()
            if len(parts) != n:
                print(ERR_COUNT % n)
                ok = False
                break
            try:
                rows.append([parse_number(p) for p in parts])
            except ValueError:
                print(ERR_NUMBER)
                ok = False
                break
        if ok:
            return rows
        print("→ %s를 처음부터 다시 입력합니다." % name)


def _to_ab(verdict):
    """내부 판정(A/B/UNDECIDED)을 모드 1 출력 문구로 변환."""
    return "판정 불가 (동점)" if verdict == UNDECIDED else verdict


def run():
    filter_a = read_matrix("필터 A")
    print("필터 A 저장 완료:", filter_a)
    filter_b = read_matrix("필터 B")
    print("필터 B 저장 완료:", filter_b)
    pattern = read_matrix("패턴")
    print("패턴 저장 완료:", pattern)

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    ms_a = measure_ms(mac, pattern, filter_a)
    ms_b = measure_ms(mac, pattern, filter_b)
    verdict = judge(score_a, score_b, "A", "B")

    print("\n[결과]")
    print("필터 A 점수: %s  (평균 %.4f ms)" % (score_a, ms_a))
    print("필터 B 점수: %s  (평균 %.4f ms)" % (score_b, ms_b))
    print("판정: %s" % _to_ab(verdict))

    print_perf_table([(3, (ms_a + ms_b) / 2)])
