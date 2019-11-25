import argparse
import json
from itertools import chain


def format_csv(stream, users):
    for user in users:
        primary_email = user["primaryEmail"]
        emails = [e["address"] for e in user.get("emails", [])]
        other_emails = list(
            sorted(
                email
                for email in emails
                if email != primary_email and "test-google-a.com" not in email
            )
        )

        print(";".join(chain([primary_email], other_emails)), file=stream)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True, type=argparse.FileType(mode="r"))
    ap.add_argument("--write-csv", "-w", type=argparse.FileType(mode="w"))
    args = ap.parse_args()
    users = json.load(args.json)
    if args.write_csv:
        format_csv(args.write_csv, users)


if __name__ == "__main__":
    main()
