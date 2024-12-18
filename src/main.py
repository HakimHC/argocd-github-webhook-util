import os
import sys
from .argocd import ArgoCDClient, ArgoClientFactory
from .api import create_flask_app

app = create_flask_app(__name__)

if __name__ == '__main__':
    try:
        argocd_client = ArgoClientFactory.get_instance()
    except (ArgoCDClient.InvalidCredentialsError, ArgoCDClient.EmptyApiUrlError) as e:
        print(
            f'fatal: Couldn\'t authenticate with ArgoCD API because of the following reason: "{str(e)}"',
            file=sys.stderr
        )
        sys.exit(1)

    app.run(host='0.0.0.0', port=8000, debug=True if "true" == os.getenv('FLASK_DEBUG', 'true').lower() else False)
