import os

from flask import g
from authlib.integrations.flask_client import OAuth

oauth = OAuth()


def github():
    oauth.register(
        name="github",
        client_id=os.getenv("GITHUB_CONSUMER_KEY"),
        client_secret=os.getenv("GITHUB_CONSUMER_SECRET"),
        access_token_url="https://github.com/login/oauth/access_token",
        access_token_params=None,
        authorize_url="https://github.com/login/oauth/authorize",
        authorize_params=None,
        api_base_url="https://api.github.com/",
        client_kwargs={
            "scope": "user:email",
            "token_endpoint_auth_method": "client_secret_basic",
        },
    )

    return oauth.create_client('github')


"""
@github.tokengetter
def get_github_token():
    if "access_token" in g:
        return g.access_token
"""


