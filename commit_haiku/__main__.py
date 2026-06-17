import sys
from commit_haiku.haiku import generate_haiku, analyze_diff


def main():
    if "--stdin" in sys.argv or "-" in sys.argv:
        diff = sys.stdin.read()
        analysis = analyze_diff()
        if diff:
            analysis["diff"] = diff
    else:
        analysis = analyze_diff()

    haiku = generate_haiku(analysis)
    print()
    print(haiku)
    print()


if __name__ == "__main__":
    main()
