import argparse
import json


def format_markdown(stream, groups):
    for group in groups:
        header = group["email"]
        if group.get("aliases"):
            aliases_str = ", ".join(sorted(group["aliases"]))
            header += f" ({aliases_str})"
        print(f"# {header}", file=stream)
        print(file=stream)
        for member in group["_members"]:
            line = f'{member.get("email") or member.get("id")}'
            if member["role"] != "MEMBER":
                line += f" ({member['role']})"
            print(f"  * {line}", file=stream)
        print(file=stream)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True, type=argparse.FileType(mode="r"))
    ap.add_argument("--write-markdown", type=argparse.FileType(mode="w"))
    args = ap.parse_args()
    groups = json.load(args.json)
    if args.write_markdown:
        format_markdown(args.write_markdown, groups)


if __name__ == "__main__":
    main()
