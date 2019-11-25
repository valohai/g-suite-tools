import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def get_credentials(key, scopes):
    cached_credentials_file = f"./{key}.credentials.pickle"
    if os.path.isfile(cached_credentials_file):
        with open(cached_credentials_file, "rb") as infp:
            return pickle.load(infp)
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes=scopes
    )
    credentials = flow.run_console()
    with open(cached_credentials_file, "wb") as fp:
        pickle.dump(credentials, fp)
    return credentials


def get_directory_read_client():
    credentials = get_credentials(
        key="get_directory_read_client",
        scopes=[
            "https://www.googleapis.com/auth/admin.directory.group.readonly",
            "https://www.googleapis.com/auth/admin.directory.user.readonly",
        ],
    )
    return build("admin", "directory_v1", credentials=credentials)
