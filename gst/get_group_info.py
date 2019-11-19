import argparse
import json
import sys
from typing import List

import tqdm
from googleapiclient.discovery import build

from gst.credentials import get_credentials
from gst.utils import get_paginated


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", required=True)
    ap.add_argument("--write-json", type=argparse.FileType(mode="w"))
    args = ap.parse_args()
    credentials = get_credentials(
        "group_report.py",
        scopes=[
            "https://www.googleapis.com/auth/admin.directory.group.readonly",
            "https://www.googleapis.com/auth/admin.directory.user.readonly",
        ],
    )
    directory_client = build("admin", "directory_v1", credentials=credentials)
    domain = args.domain

    groups = get_domain_groups(directory_client, domain)
    print(f"{len(groups)} groups.")
    populate_groups_members(directory_client, groups)

    if args.write_json:
        json.dump(groups, args.write_json)
        print(f"Wrote JSON to {args.write_json}", file=sys.stderr)


def populate_groups_members(directory_client, groups: List[dict]) -> None:
    for group in tqdm.tqdm(groups, desc="retrieving members"):
        group["_members"] = members = []
        for members_resp in get_paginated(
            directory_client.members().list, {"groupKey": group["id"]}
        ):
            members.extend(members_resp["members"])


def get_domain_groups(directory_client, domain) -> List[dict]:
    groups = []
    for groups_resp in tqdm.tqdm(
        get_paginated(directory_client.groups().list, {"domain": domain}),
        desc="retrieving groups",
    ):
        groups.extend(groups_resp["groups"])
    return groups


if __name__ == "__main__":
    main()
