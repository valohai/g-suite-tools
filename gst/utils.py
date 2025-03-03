import json


def get_paginated(func, base_kwargs):
    page_token = None
    while True:
        resp = func(**base_kwargs, pageToken=page_token).execute()
        yield resp
        page_token = resp.get("nextPageToken")
        if not page_token:
            break


def read_jsonl(stream):
    for line in stream:
        yield json.loads(line)
