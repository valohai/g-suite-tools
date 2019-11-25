import argparse
import json
import sys
from typing import List

import tqdm

from gst.credentials import get_directory_read_client
from gst.utils import get_paginated


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", required=True)
    ap.add_argument("--write-json", type=argparse.FileType(mode="w"))
    args = ap.parse_args()
    directory_client = get_directory_read_client()
    domain = args.domain

    users = get_domain_users(directory_client, domain)
    print(f"{len(users)} users.")

    if args.write_json:
        json.dump(users, args.write_json)
        print(f"Wrote JSON to {args.write_json}", file=sys.stderr)


def get_domain_users(directory_client, domain) -> List[dict]:
    users = []
    for users_resp in tqdm.tqdm(
        get_paginated(directory_client.users().list, {"domain": domain}),
        desc="retrieving users",
    ):
        users.extend(users_resp["users"])
    return users


if __name__ == "__main__":
    main()
