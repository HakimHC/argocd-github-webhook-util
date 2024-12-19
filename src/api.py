from __future__ import annotations

from pathlib import Path

from flask import Blueprint
from flask import Flask
from flask import request

from .argocd import ArgoCDClient
from .argocd import ArgoClientFactory
from .repo import Repo
from .utils import get_affected_argocd_applications
from .utils import get_changed_files


def create_webhook_blueprint(argocd_client: ArgoCDClient):
    webhook_bp = Blueprint("webhook", __name__)

    @webhook_bp.route("/whoami", methods=["GET"])
    def whoami():
        return argocd_client.user_info(), 200

    @webhook_bp.route("/webhook", methods=["POST"])
    def webhook():
        # misc
        data = request.get_json()
        head_commit = data.get("head_commit", {})
        if not head_commit:
            return "Bad Request", 400

        if not data.get("repository"):
            return "Bad Request", 400
        if not data["repository"].get("ssh_url"):
            return "Bad Request", 400

        url = data["repository"]["ssh_url"]
        repo = Repo(url)
        repo.clone()
        files = get_changed_files(head_commit)

        affected_apps = get_affected_argocd_applications(
            clone_path=Path(repo.clone_path), changed_files=files
        )
        print(f"Affected apps: {affected_apps}")
        for app in affected_apps:
            argocd_client.refresh_application(app)
        return "OK", 200

    return webhook_bp


def create_flask_app(name: str):
    app = Flask(name)
    argocd_client = ArgoClientFactory.get_instance()
    app.register_blueprint(create_webhook_blueprint(argocd_client))
    return app
