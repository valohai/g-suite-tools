import argparse
import json
from functools import partial

from gst.uhtml import write_tag


def get_thing_short_name(user_or_group):
    name = user_or_group.get("email") or user_or_group.get("id") or repr(user_or_group)
    return name.partition("@")[0]


def format_markdown(stream, groups):
    for group in groups:
        header = group["email"]
        if group.get("aliases"):
            aliases_str = ", ".join(sorted(group["aliases"]))
            header += f" ({aliases_str})"
        print(f"# {header}", file=stream)
        print(file=stream)
        for member in group["_members"]:
            line = f"{get_thing_short_name(member)}"
            if member["role"] != "MEMBER":
                line += f" ({member['role']})"
            print(f"  * {line}", file=stream)
        print(file=stream)


role_emojis = {
    "owner": "\U0001f451",
    "member": "\u2705",
    "manager": "\U0001f477",
}


def format_membership(member):
    role = member["role"].lower()
    return role, role_emojis.get(role, role)


def format_membership_matrix_html(stream, groups):
    tag = partial(write_tag, stream=stream)
    groups_with_members = [g for g in groups if g.get("_members", ())]
    all_member_ids = set()
    for group in groups:
        all_member_ids.update(
            get_thing_short_name(member) for member in group["_members"]
        )
    with tag("style"):
        print(
            """
            body{font-family:sans-serif}
            table {border-collapse:collapse}
            th, td {text-align:left;border:1px solid black;padding:3px}
            thead>tr>th{writing-mode:vertical-lr;transform:rotate(180deg)}
            td {line-height:1;vertical-align:middle}
            """,
            file=stream,
        )
    with tag("table"):
        with tag("thead"):
            with tag("tr"):
                with tag("th"):
                    pass
                for group in groups_with_members:
                    with tag("th"):
                        print(get_thing_short_name(group), file=stream)
        with tag("tbody"):
            for member_id in sorted(all_member_ids):
                with tag("tr"):
                    with tag("th"):
                        print(member_id, file=stream)
                    for group in groups_with_members:
                        group_short_name = get_thing_short_name(group)
                        with tag("td"):
                            for member in group["_members"]:
                                if get_thing_short_name(member) == member_id:
                                    role, role_emoji = format_membership(member)
                                    desc = (
                                        f"{member_id} is {role} in {group_short_name}"
                                    )
                                    with tag("span", attrs={"title": desc}):
                                        print(role_emoji, file=stream)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True, type=argparse.FileType(mode="r"))
    ap.add_argument("--write-markdown", type=argparse.FileType(mode="w"))
    ap.add_argument("--write-membership-matrix-html", type=argparse.FileType(mode="w"))
    args = ap.parse_args()
    groups = json.load(args.json)
    if args.write_markdown:
        format_markdown(args.write_markdown, groups)
    if args.write_membership_matrix_html:
        format_membership_matrix_html(args.write_membership_matrix_html, groups)


if __name__ == "__main__":
    main()
