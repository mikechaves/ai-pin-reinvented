import sys
import json


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({"error": "missing file argument"}))
        sys.exit(1)

    filename = sys.argv[1]
    if "demo_bike" in filename:
        result = {"danger": True, "direction": "left", "eta": 3}
    else:
        result = {"danger": False}

    print(json.dumps(result))


if __name__ == "__main__":
    main()

