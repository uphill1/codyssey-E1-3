"""요구사항 01: n×n 2차원 패턴/필터 데이터 구조."""


def make_matrix(n, fill=0):
    """n×n 행렬 생성.

    [[fill] * n] * n 으로 만들면 모든 행이 같은 리스트를 가리키므로
    컴프리헨션으로 행마다 새 리스트를 만든다.
    """
    return [[fill for _ in range(n)] for _ in range(n)]


def get_value(matrix, row, col):
    """특정 위치의 값 읽기."""
    return matrix[row][col]


def set_value(matrix, row, col, value):
    """특정 위치에 값 저장."""
    matrix[row][col] = value


def is_number(value):
    """int/float 여부 (bool은 int의 하위 타입이라 명시적으로 제외)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_square(matrix, n=None):
    """정사각 n×n 이고 모든 원소가 숫자인지 검사.

    n을 주면 그 크기와도 일치해야 한다.
    """
    if not isinstance(matrix, list) or len(matrix) == 0:
        return False
    size = len(matrix) if n is None else n
    if len(matrix) != size:
        return False
    for row in matrix:
        if not isinstance(row, list) or len(row) != size:
            return False
        for value in row:
            if not is_number(value):
                return False
    return True


def describe_shape(matrix):
    """오류 메시지용 실제 크기 문자열 (예: '5x4')."""
    if not isinstance(matrix, list):
        return "배열 아님"
    rows = len(matrix)
    cols = len(matrix[0]) if rows and isinstance(matrix[0], list) else 0
    return "%dx%d" % (rows, cols)


def flatten(matrix):
    """보너스 1: 2차원 → 길이 N² 1차원 리스트."""
    return [value for row in matrix for value in row]


def make_cross(n, on=1.0, off=0.0):
    """보너스 2: N×N 십자가 패턴 생성 (가운데 행/열이 on)."""
    c = n // 2
    return [[on if (i == c or j == c) else off for j in range(n)]
            for i in range(n)]


def make_x(n, on=1.0, off=0.0):
    """보너스 2: N×N X 패턴 생성 (두 대각선이 on)."""
    return [[on if (i == j or i + j == n - 1) else off for j in range(n)]
            for i in range(n)]
