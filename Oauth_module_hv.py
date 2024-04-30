from Imports_module import *
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "864007838994-dgesnrqgns0p66k3s4prlrsdaeundjcs.apps.googleusercontent.com"
YANDEX_CLIENT_ID = '25117d154a7a4b4c91a0df19bc5b3db0'
YANDEX_CLIENT_SECRET = 'a0731ee4be4a4b33aad0845577cd4780'
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret_file_hv.json")

scopes = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
]
flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
                                     scopes=scopes,
                                     redirect_uri="https://avtoservisnalesnoj.ru/loginwithgoogle")
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper
