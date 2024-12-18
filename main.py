from argocd import ArgoCDClient
import sys

if __name__ == '__main__':
    try:
        argocd_client = ArgoCDClient()
    except (ArgoCDClient.InvalidCredentialsError, ArgoCDClient.EmptyApiUrlError) as e:
        print(
            f'fatal: Couldn\'t authenticate with ArgoCD API because of the following reason: "{str(e)}"',
            file=sys.stderr
        )
        sys.exit(1)

    print(argocd_client.list_applications())
