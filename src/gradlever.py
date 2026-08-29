#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path

# scoop install "gradle@$(& gradlever)"

ROOT = Path.cwd()


def get_wrapper_version():
    wrapper = ROOT / "gradle" / "wrapper" / "gradle-wrapper.properties"

    if not wrapper.exists():
        return None

    text = wrapper.read_text()

    match = re.search(r"gradle-([0-9][^-/]*)-", text)
    if match:
        return match.group(1)

    return None


def get_gradlew_version():
    gradlew = ROOT / "gradlew"

    if not gradlew.exists():
        return None

    try:
        result = subprocess.run(
            ["./gradlew", "--version"],
            capture_output=True,
            text=True,
            timeout=20,
        )

        match = re.search(r"Gradle (\S+)", result.stdout)
        if match:
            return match.group(1)

    except Exception:
        pass

    return None


def get_android_gradle_plugin():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix not in {".gradle", ".kts"}:
            continue

        try:
            text = path.read_text(errors="ignore")

            match = re.search(
                r"com\.android\.tools\.build:gradle:([0-9.]+)",
                text,
            )

            if match:
                return match.group(1)

        except Exception:
            pass

    return None


def main():
    version = get_wrapper_version()

    if version:
        print(f"{version}")
        return 0

    version = get_gradlew_version()

    if version:
        print(f"{version}")
        return 0

    agp = get_android_gradle_plugin()

    if agp:
        return 1


if __name__ == "__main__":
    main()
