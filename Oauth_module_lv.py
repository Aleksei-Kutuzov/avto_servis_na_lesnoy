from Imports_module import *
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "864007838994-ia4jimu5qvikqdmvlkvg6lre32lovvni.apps.googleusercontent.com"
YANDEX_CLIENT_ID = 'ed17771a6b6642b89f0933cfd56c5763'
YANDEX_CLIENT_SECRET = '986369e541da45cc84ecaa6a0c080cf0'
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret_file_lv.json")

scopes = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
]
flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
                                     scopes=scopes,
                                     redirect_uri="http://127.0.0.1:5000")
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper
