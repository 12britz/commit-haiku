import random
import re
import subprocess
from collections import Counter

ADD_TEMPLATES = [
    ("New code takes its place", 5, "a gentle offering"),
    ("A function is born", 5, "from keystrokes and endless thought"),
    ("Lines of logic flow", 5, "into the waiting codebase"),
]

FIX_TEMPLATES = [
    ("The bug crawls no more", 5, "squashed beneath careful hands"),
    ("A subtle mistake", 5, "corrected with patient grace"),
    ("What once was broken", 5, "now stands repaired and ready"),
]

REMOVE_TEMPLATES = [
    ("Old code fades away", 5, "making room for what will be"),
    ("Lines are swept aside", 5, "dead branches from the live tree"),
    ("We let go of this", 5, "to make the whole system clean"),
]

REFACTOR_TEMPLATES = [
    ("Twisted paths unwind", 5, "the shape of code refined"),
    ("What was tangled once", 5, "now flows clear and organized"),
    ("Shapes shift and reshape", 5, "the structure finds its form"),
]

GENERAL_TEMPLATES = [
    ("A quiet commit", 5, "speaks louder than words can say"),
    ("Keys tap in the dark", 5, "building castles from commands"),
    ("The cursor blinks once", 5, "a universe takes its breath"),
    ("Changes ripple out", 5, "through branches yet to be named"),
    ("This small delta now", 5, "carries the weight of purpose"),
    ("Pull requests await", 5, "the judgment of peers and time"),
    ("Merge conflicts resolved", 5, "peace settles on the codebase"),
    ("In the terminal", 5, "a developer finds their flow"),
    ("The test suite turns green", 5, "like spring after winter's end"),
    ("One file at a time", 5, "we shape the digital world"),
]

LINE_TEMPLATES = [
    (5, 7, 5),  # standard haiku
    (5, 5, 5),  # variant
    (3, 5, 3),  # mini
]

def get_git_diff():
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--stat"],
            capture_output=True, text=True, check=False
        )
        if result.stdout.strip():
            return result.stdout

        result = subprocess.run(
            ["git", "diff", "--stat", "HEAD"],
            capture_output=True, text=True, check=False
        )
        if result.stdout.strip():
            return result.stdout

        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            capture_output=True, text=True, check=False
        )
        if result.stdout.strip():
            return result.stdout

        return ""
    except FileNotFoundError:
        return ""


def parse_diff_stats(diff_output):
    if not diff_output:
        return []

    files = []
    for line in diff_output.strip().split("\n"):
        if "|" in line and ("changed" in line or line.strip().startswith(" ")):
            continue
        match = re.match(r"\s*(.+?)\s*\|\s*(\d+)", line)
        if match:
            files.append(match.group(1).strip())
    return files


def analyze_diff():
    diff = get_git_diff()
    if not diff:
        return {}

    files = parse_diff_stats(diff)

    lines = diff.strip().split("\n")
    total_changes = 0
    for line in lines:
        m = re.search(r"\|\s*(\d+)", line)
        if m:
            total_changes += int(m.group(1))

    full_diff = ""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True, text=True, check=False
        )
        if not result.stdout.strip():
            result = subprocess.run(
                ["git", "diff", "HEAD"],
                capture_output=True, text=True, check=False
            )
        full_diff = result.stdout
    except FileNotFoundError:
        pass

    added = len(re.findall(r"^\+", full_diff, re.MULTILINE))
    removed = len(re.findall(r"^\-", full_diff, re.MULTILINE))

    keywords = []
    if full_diff:
        kw_match = re.findall(r"\b(fix|bug|hotfix|patch|repair|broken)\b", full_diff, re.IGNORECASE)
        keywords.extend(kw_match)
    if keywords:
        kind = "fix"
    elif added > removed * 3:
        kind = "add"
    elif removed > added * 3:
        kind = "remove"
    elif added + removed > 50:
        kind = "refactor"
    else:
        kind = "general"

    return {
        "files": files,
        "file_count": len(files),
        "changes": total_changes,
        "added": added,
        "removed": removed,
        "kind": kind,
        "keywords": keywords,
        "diff": full_diff,
    }


def count_syllables(text):
    text = text.lower().strip()
    if not text:
        return 0
    text = re.sub(r"[^a-z\s]", "", text)
    vowels = "aeiouy"
    count = 0
    prev_char = ""
    for char in text:
        if char in vowels:
            if prev_char not in vowels:
                count += 1
        prev_char = char
    if text.endswith("e"):
        count = max(count - 1, 1)
    if text.endswith("le") and len(text) > 2 and text[-3] not in vowels:
        count += 1
    return max(count, 1)


def build_haiku_line(text, target_syllables):
    words = text.split()
    if not words:
        return text

    result = []
    current_syllables = 0

    for word in words:
        syl = count_syllables(word)
        if current_syllables + syl <= target_syllables:
            result.append(word)
            current_syllables += syl
        elif current_syllables < target_syllables:
            alt = find_syllable_match(word, target_syllables - current_syllables)
            if alt:
                result.append(alt)
                break
            break
        else:
            break

    return " ".join(result)


def find_syllable_match(word, target):
    synonyms = {
        "adding": "new", "creates": "makes", "removes": "drops",
        "fixing": "mends", "changes": "tweaks", "updating": "revises",
        "features": "things", "function": "routine", "implementation": "code",
        "refactoring": "rework", "configuration": "setup", "beautiful": "clean",
        "wonderful": "great", "complicated": "complex", "everything": "all",
        "application": "app", "additional": "more", "necessary": "needed",
        "substantial": "large", "foundation": "base", "interface": "UI",
    }
    word_lower = word.lower()
    if word_lower in synonyms:
        s = count_syllables(synonyms[word_lower])
        if s <= target:
            return synonyms[word_lower]
    return None


def get_random_line(syllable_count, words_pool):
    random.shuffle(words_pool)
    line = []
    remaining = syllable_count
    for word in words_pool:
        s = count_syllables(word)
        if s <= remaining:
            line.append(word)
            remaining -= s
        if remaining == 0:
            break
    return " ".join(line) if line else "code is art"


def generate_haiku(analysis=None):
    if analysis is None:
        analysis = analyze_diff()

    kind = analysis.get("kind", "general")
    files = analysis.get("files", [])
    file_count = analysis.get("file_count", 0)

    template_pool = GENERAL_TEMPLATES.copy()
    if kind in ("add",):
        template_pool = ADD_TEMPLATES + template_pool
    elif kind == "fix":
        template_pool = FIX_TEMPLATES + template_pool
    elif kind == "remove":
        template_pool = REMOVE_TEMPLATES + template_pool
    elif kind == "refactor":
        template_pool = REFACTOR_TEMPLATES + template_pool

    l1, l3 = random.choice(template_pool)[:2], random.choice(template_pool)[2]
    if isinstance(l1, tuple):
        l1 = l1[0]

    if files:
        file_word = random.choice(files).replace("_", " ").replace("-", " ")
        file_word = re.sub(r"\..*$", "", file_word)
        file_syl = count_syllables(file_word)
        if file_syl <= 5:
            l1 = file_word.capitalize() + " " + " ".join(l1.split()[1:])
            l1 = build_haiku_line(l1, 5)

    line1 = l1 if count_syllables(l1) <= 7 else build_haiku_line(l1, 5)
    line1 = build_haiku_line(l1, 5)

    line3 = l3 if isinstance(l3, str) else l3[1]
    line3 = build_haiku_line(line3, 5)

    middle_words = []
    if files:
        middle_words.append("code")
    if analysis.get("changes", 0) > 0:
        middle_words.append(str(analysis["changes"]))
    middle_words.extend(["lines", "changes", "files", "commits", "patches",
                         "branches", "fixes", "diffs", "merges", "pushes"])
    if kind == "fix":
        middle_words.extend(["bugs", "errors", "crashes"])
    elif kind == "add":
        middle_words.extend(["features", "functions"])
    elif kind == "remove":
        middle_words.extend(["removals", "cleanup"])
    elif kind == "refactor":
        middle_words.extend(["structure", "design"])

    line2 = get_random_line(7, middle_words)

    return f"{line1}\n{line2}\n{line3}"



