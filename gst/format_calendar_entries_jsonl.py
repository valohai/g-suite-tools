import argparse
import datetime
import sys
import zoneinfo

from gst.utils import read_jsonl

IGNORED_KEYS_FOR_ICAL = (
    "attachments",
    "attendees",
    "colorId",
    "conferenceData",
    "created",
    "creator",
    "endTimeUnspecified",  # Should this be handled?
    "etag",
    "eventType",
    "extendedProperties",
    "guestsCanInviteOthers",
    "guestsCanModify",
    "guestsCanSeeOtherGuests",
    "hangoutLink",
    "htmlLink",
    "id",  # handled above
    "kind",
    "organizer",
    "originalStartTime",  # for recurring events
    "privateCopy",
    "recurrence",
    "recurringEventId",  # for recurring events
    "reminders",
    "sequence",
    "status",
    "transparency",  # ???
    "updated",
    "visibility",
)


def get_datetime_or_date(s):
    if "dateTime" in s:
        tz = zoneinfo.ZoneInfo(s["timeZone"])
        return datetime.datetime.fromisoformat(s["dateTime"]).astimezone(tz)
    if "date" in s:
        return datetime.date.fromisoformat(s["date"])
    raise ValueError(f"Unexpected start time: {s}")


def get_datetime(s):
    datetime_or_date = get_datetime_or_date(s)
    if not isinstance(datetime_or_date, datetime.datetime):
        return datetime.datetime.combine(datetime_or_date, datetime.datetime.min.time())
    return datetime_or_date


def compact_dict(d):
    return {k: v for k, v in d.items() if v is not None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--format", choices=("tsv", "ical"), required=True)
    args = ap.parse_args()
    events = sorted(
        (
            event
            for event in read_jsonl(sys.stdin)
            if "start" in event and event["status"] != "cancelled"
        ),
        key=lambda event: get_datetime(event["start"]).timestamp(),
    )
    if args.format == "tsv":
        dump_tsv(events)
    elif args.format == "ical":
        dump_ical(events)
    else:
        raise NotImplementedError(f"Unexpected format: {args.format}")


def dump_tsv(events):
    for event in events:
        start = get_datetime(event["start"])
        end = get_datetime(event["end"])
        print(start, end, event.get("summary"), sep="\t")


def dump_ical(events):
    import icalendar

    ic = icalendar.Calendar()
    ic.add("version", "2.0")

    for event in events:
        event = event.copy()
        uid = event.pop("iCalUID") or event.pop("id")
        iev = icalendar.Event(uid=uid)
        iev.start = get_datetime(event.pop("start"))
        iev.end = get_datetime(event.pop("end"))
        for key in ("summary", "location", "description"):
            value = event.pop(key, None)
            if value:
                iev.add(key, value)
        for key in IGNORED_KEYS_FOR_ICAL:
            event.pop(key, None)
        if event:
            raise ValueError(f"Unexpected keys: {event.keys()}")
        ic.add_component(iev)
    sys.stdout.buffer.write(ic.to_ical())


if __name__ == "__main__":
    main()
