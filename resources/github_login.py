from flask_restful import Resource
from flask import url_for, render_template, g, request
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel
from oa import github


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github().authorize_redirect(url_for("github.authorize", _external=True))
        # return github().authorize_redirect("http://localhost:5000/login/github/authorized")


class GithubAuthorize(Resource):
    # They already gave us authorization to get details,
    # now we want to access the token...
    @classmethod
    def get(cls):
        resp = github().authorize_access_token()
        if resp is None or resp.get("access_token") is None:
            error_response = {
                "error": request.args["error"],
                "error_description": request.args["error_description"]
            }
            return error_response

        g.access_token = resp["access_token"]  # Not useful line.
        github_user = github().get("user").json()
        github_username = github_user["login"]

        user = UserModel.find_by_username(github_username)
        if not user:
            user = UserModel(username=github_username, password=None)
            user.save_to_db()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200