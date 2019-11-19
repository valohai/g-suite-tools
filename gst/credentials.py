import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow


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
