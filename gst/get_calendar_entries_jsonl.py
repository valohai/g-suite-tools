import argparse
import json

from gst.credentials import get_calendar_read_client
from gst.utils import get_paginated


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calendar-id", required=True)
    # ap.add_argument("--start-date", type=datetime.date.fromisoformat, required=True)
    # ap.add_argument("--end-date", type=datetime.date.fromisoformat, required=True)
    args = ap.parse_args()
    crc = get_calendar_read_client()

    for events_resp in get_paginated(
        crc.events().list,
        {
            "calendarId": args.calendar_id,
            "timeMin": args.start_date.isoformat() + "T00:00:00Z",
            "timeMax": args.end_date.isoformat() + "T23:59:59Z",
        },
    ):
        for event in events_resp.get("items", []):
            print(json.dumps(event, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
