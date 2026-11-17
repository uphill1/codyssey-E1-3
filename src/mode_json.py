"""요구사항 03·06·08: 모드 2 - data.json 분석."""
import json

from src.judge import EPSILON, UNDECIDED, judge, normalize_label
from src.mac import mac, mac_flat
from src.matrix import describe_shape, flatten, is_square, make_cross
from src.perf import measure_ms, print_perf_table

PERF_SIZES = [3, 5, 13, 25]

# 실패 원인 분류
CAT_SCHEMA = "데이터/스키마"
CAT_LOGIC = "로직"
CAT_NUMERIC = "수치 비교"


def load_data(path):
    """파일 없음 / JSON 손상 시 안내 후 None 반환 (비정상 종료 방지)."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("오류: '%s' 파일을 찾을 수 없습니다." % path)
        return None
    except json.JSONDecodeError as e:
        print("오류: JSON 파싱 실패 (%s)" % e)
        return None
    if not isinstance(data, dict):
        print("오류: 최상위 구조가 객체({})가 아닙니다.")
        return None
    return data


def parse_size_from_key(key):
    """'size_13' 또는 'size_13_2' → 13. 규칙 위반 시 None."""
    parts = str(key).split("_")
    if len(parts) < 2 or parts[0] != "size":
        return None
    try:
        n = int(parts[1])
    except ValueError:
        return None
    return n if n > 0 else None


def load_filters(raw_filters):
    """filters 섹션을 {N: {'Cross': 행렬, 'X': 행렬}} 로 정규화.

    문제가 있는 필터는 건너뛰고 경고 목록에 기록한다.
    """
    filters, warnings = {}, []
    if not isinstance(raw_filters, dict):
        return filters, ["filters 섹션이 없거나 객체가 아님"]

    for key, group in raw_filters.items():
        n = parse_size_from_key(key)
        if n is None:
            warnings.append("필터 키 '%s'가 size_N 규칙에 맞지 않음" % key)
            continue
        if not isinstance(group, dict):
            warnings.append("필터 '%s'의 값이 객체가 아님" % key)
            continue
        normalized = {}
        for label_key, matrix in group.items():
            label = normalize_label(label_key)
            if label is None:
                warnings.append("필터 '%s'의 라벨 '%s'를 알 수 없음" % (key, label_key))
                continue
            if not is_square(matrix, n):
                warnings.append("필터 '%s.%s' 크기 불일치 (기대 %dx%d, 실제 %s)"
                                % (key, label_key, n, n, describe_shape(matrix)))
                continue
            normalized[label] = matrix
        filters[n] = normalized
    return filters, warnings


def _fail(result, category, reason):
    result.update(status="FAIL", category=category, reason=reason)
    return result


def run_case(case_id, case, filters):
    """패턴 1건 판정. 예외를 밖으로 던지지 않고 FAIL + 사유로 기록한다."""
    result = {"id": case_id, "score_cross": None, "score_x": None,
              "verdict": "-", "expected": "-", "status": "PASS",
              "category": "", "reason": ""}

    n = parse_size_from_key(case_id)
    if n is None:
        return _fail(result, CAT_SCHEMA, "키가 size_N_idx 규칙에 맞지 않음")
    if not isinstance(case, dict):
        return _fail(result, CAT_SCHEMA, "케이스 값이 객체가 아님")

    expected = normalize_label(case.get("expected"))
    result["expected"] = expected or repr(case.get("expected"))
    if expected is None:
        return _fail(result, CAT_SCHEMA,
                     "알 수 없는 expected 라벨: %r" % case.get("expected"))

    group = filters.get(n)
    if not group or "Cross" not in group or "X" not in group:
        return _fail(result, CAT_SCHEMA, "size_%d 필터(Cross/X)를 찾을 수 없음" % n)

    pattern = case.get("input")
    if not is_square(pattern, n):
        return _fail(result, CAT_SCHEMA, "패턴 크기 불일치 (기대 %dx%d, 실제 %s)"
                     % (n, n, describe_shape(pattern)))

    score_cross = mac(pattern, group["Cross"])
    score_x = mac(pattern, group["X"])
    verdict = judge(score_cross, score_x)
    result.update(score_cross=score_cross, score_x=score_x, verdict=verdict)

    if verdict == expected:
        return result
    if verdict == UNDECIDED:
        return _fail(result, CAT_NUMERIC, "동점 (|%r - %r| = %.1e < %g)"
                     % (score_cross, score_x, abs(score_cross - score_x), EPSILON))
    return _fail(result, CAT_LOGIC, "판정 %s ≠ expected %s" % (verdict, expected))


def _fmt(score):
    return "-" if score is None else "%.6g" % score


def print_case_table(results):
    print("\n[케이스별 판정]")
    print("%-12s %10s %10s %11s %9s %6s"
          % ("케이스", "Cross", "X", "판정", "expected", "결과"))
    print("-" * 64)
    for r in results:
        print("%-12s %10s %10s %11s %9s %6s"
              % (r["id"], _fmt(r["score_cross"]), _fmt(r["score_x"]),
                 r["verdict"], r["expected"], r["status"]))


def run_performance(filters):
    """3×3은 생성기로, 5/13/25는 data.json 필터 + 생성한 십자가 패턴으로 측정."""
    rows, bonus = [], []
    for n in PERF_SIZES:
        pattern = make_cross(n)
        filt = filters.get(n, {}).get("Cross") or make_cross(n)
        rows.append((n, measure_ms(mac, pattern, filt)))
        # 보너스 1: 동일 입력, 동일 반복 횟수로 1차원 버전 측정 (평탄화는 측정 밖)
        p_flat, f_flat = flatten(pattern), flatten(filt)
        bonus.append((n, rows[-1][1], measure_ms(mac_flat, p_flat, f_flat)))
    print_perf_table(rows)
    return bonus


def print_bonus_table(bonus):
    print("\n[보너스] 2차원 vs 1차원 MAC 비교 (동일 입력, 각 10회 평균)")
    print("%-10s %12s %12s %10s" % ("크기(N×N)", "2차원(ms)", "1차원(ms)", "개선율"))
    print("-" * 48)
    for n, ms_2d, ms_1d in bonus:
        gain = (1 - ms_1d / ms_2d) * 100 if ms_2d > 0 else 0.0
        print("%-10s %12.4f %12.4f %9.1f%%" % ("%dx%d" % (n, n), ms_2d, ms_1d, gain))


def print_summary(results):
    passed = [r for r in results if r["status"] == "PASS"]
    failed = [r for r in results if r["status"] == "FAIL"]
    print("\n[결과 요약] 전체 %d / 통과 %d / 실패 %d"
          % (len(results), len(passed), len(failed)))
    if not failed:
        print("실패 케이스 없음")
        return
    counts = {}
    for r in failed:
        print("  - %s [%s] %s" % (r["id"], r["category"], r["reason"]))
        counts[r["category"]] = counts.get(r["category"], 0) + 1
    print("실패 분류: " + ", ".join("%s %d건" % kv for kv in counts.items()))


def run(path):
    data = load_data(path)
    if data is None:
        return

    # 1. 필터 로드
    filters, warnings = load_filters(data.get("filters"))
    print("\n[필터 로드] " + ", ".join(
        "size_%d(%s)" % (n, "/".join(sorted(g))) for n, g in sorted(filters.items())))
    for w in warnings:
        print("  경고:", w)

    # 2~4. 패턴 로드/검증 → MAC → 판정/PASS-FAIL
    patterns = data.get("patterns")
    if not isinstance(patterns, dict):
        print("오류: patterns 섹션이 없거나 객체가 아닙니다.")
        patterns = {}
    results = [run_case(cid, case, filters) for cid, case in patterns.items()]
    print_case_table(results)

    # 5. 성능 분석 (+ 보너스 비교)
    bonus = run_performance(filters)
    print_bonus_table(bonus)

    # 6. 결과 요약
    print_summary(results)
