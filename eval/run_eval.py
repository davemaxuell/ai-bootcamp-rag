import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from answerer import answer
from retriever import retrieve


def main() -> int:
    path = Path(__file__).parent / "gold_questions.yaml"
    items = yaml.safe_load(path.read_text(encoding="utf-8"))
    passed = 0
    for item in items:
        docs = retrieve(item["q"])
        result = answer(item["q"], docs)
        sources = " ".join(citation["source"] for citation in result["citations"])
        ok = (
            item["expect_source_contains"].casefold() in sources.casefold()
            and bool(result["text"].strip())
        )
        print(f"[{'PASS' if ok else 'FAIL'}] {item['q'][:30]} -> {sources[:80]}")
        passed += int(ok)
    print(f"{passed}/{len(items)} passed")
    return 0 if passed == len(items) else 1


if __name__ == "__main__":
    raise SystemExit(main())
