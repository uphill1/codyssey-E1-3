"""Mini NPU Simulator 진입점 (요구사항 09: 실행 흐름)."""
import os
import sys

from src import mode_input, mode_json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.join(BASE_DIR, "data.json")


def select_mode():
    print("===== Mini NPU Simulator =====")
    print("1. 사용자 입력 (3×3)")
    print("2. data.json 분석")
    while True:
        choice = input("모드를 선택하세요 (1/2): ").strip()
        if choice in ("1", "2"):
            return choice
        print("1 또는 2를 입력하세요.")


def main():
    # 다른 데이터 파일로 검증하고 싶으면: python main.py samples/broken_data.json
    data_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA
    try:
        if select_mode() == "1":
            mode_input.run()
        else:
            mode_json.run(data_path)
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")


if __name__ == "__main__":
    main()
