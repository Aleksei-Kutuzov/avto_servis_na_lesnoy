import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/contacts.readonly"]
session = {"token": None}

def get_id_g(e):
    """Shows basic usage of the People API.
    Prints the name of all connections.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if session["token"]:
        creds = Credentials.from_authorized_user_info(session["token"], SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret_file_hv.json", SCOPES
            )
            creds = flow.run_local_server(port=53624)
        # Save the credentials for the next run
        session["token"] = creds.to_json()

    try:
        service = build("people", "v1", credentials=creds)

        # Call the People API
        print("List all connection names")
        # Set pageSize to maximum allowed value to retrieve all contacts
        results = (
            service.people()
            .connections()
            .list(
                resourceName="people/me",
                pageSize=1000,  # Set to a value that exceeds your total contacts
                personFields="names,emailAddresses",
            )
            .execute()
        )
        connections = results.get("connections", [])

        for person in connections:
            names = person.get("names", [])
            emails = person.get("emailAddresses", [])
            if names:
                name = names[0].get("displayName")
                print(name)
            print(emails)
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    get_id_g()
