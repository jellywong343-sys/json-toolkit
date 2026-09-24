from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def render(data: Any, compact: bool = False, sort_keys: bool = False) -> str:
    if compact:
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=sort_keys)
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=sort_keys) + "\n"


def differences(left: Any, right: Any, path: str = "$") -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    if type(left) is not type(right):
        return [{"path": path, "kind": "type", "left": left, "right": right}]
    if isinstance(left, dict):
        left_keys, right_keys = set(left), set(right)
        for key in sorted(left_keys - right_keys):
            output.append({"path": f"{path}.{key}", "kind": "removed", "left": left[key]})
        for key in sorted(right_keys - left_keys):
            output.append({"path": f"{path}.{key}", "kind": "added", "right": right[key]})
        for key in sorted(left_keys & right_keys):
            output.extend(differences(left[key], right[key], f"{path}.{key}"))
    elif isinstance(left, list):
        common = min(len(left), len(right))
        for index in range(common):
            output.extend(differences(left[index], right[index], f"{path}[{index}]"))
        for index in range(common, len(left)):
            output.append({"path": f"{path}[{index}]", "kind": "removed", "left": left[index]})
        for index in range(common, len(right)):
            output.append({"path": f"{path}[{index}]", "kind": "added", "right": right[index]})
    elif left != right:
        output.append({"path": path, "kind": "changed", "left": left, "right": right})
    return output


def query(data: Any, expression: str) -> Any:
    current = data
    for token in expression.replace("[", ".").replace("]", "").split("."):
        if not token:
            continue
        if isinstance(current, list):
            current = current[int(token)]
        elif isinstance(current, dict):
            current = current[token]
        else:
            raise KeyError(f"Cannot access {token!r} in a scalar value")
    return current


def write_or_print(text: str, output: str | None) -> None:
    if output:
        Path(output).write_text(text, encoding="utf-8")
        print(f"Written to {output}")
    else:
        sys.stdout.write(text)
        if text and not text.endswith("\n"):
            sys.stdout.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Format, validate, query, and compare JSON.")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("format", "minify", "sort"):
        item = sub.add_parser(command)
        item.add_argument("file")
        item.add_argument("--output", "-o")
    validate = sub.add_parser("validate")
    validate.add_argument("files", nargs="+")
    diff = sub.add_parser("diff")
    diff.add_argument("left")
    diff.add_argument("right")
    diff.add_argument("--output", "-o")
    find = sub.add_parser("query")
    find.add_argument("file")
    find.add_argument("expression", help="Dot path such as user.name or items[0].id")
    find.add_argument("--output", "-o")
    args = parser.parse_args()

    try:
        if args.command == "validate":
            failed = False
            for name in args.files:
                try:
                    load_json(Path(name))
                    print(f"OK {name}")
                except (json.JSONDecodeError, OSError) as exc:
                    failed = True
                    print(f"INVALID {name}: {exc}")
            raise SystemExit(1 if failed else 0)
        if args.command == "diff":
            result = differences(load_json(Path(args.left)), load_json(Path(args.right)))
            write_or_print(render(result), args.output)
            raise SystemExit(1 if result else 0)
        data = load_json(Path(args.file))
        if args.command == "format":
            write_or_print(render(data), args.output)
        elif args.command == "minify":
            write_or_print(render(data, compact=True), args.output)
        elif args.command == "sort":
            write_or_print(render(data, sort_keys=True), args.output)
        elif args.command == "query":
            write_or_print(render(query(data, args.expression)), args.output)
    except (json.JSONDecodeError, OSError, KeyError, IndexError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2)

if __name__ == "__main__":
    main()
