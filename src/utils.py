from pathlib import Path
import os


def get_files_in_directory(directory: Path):
    return [f.name for f in directory.iterdir() if f.is_file()]


def get_changed_files(commit: dict) -> list[str]:
    files = []
    changes_keys = ['added', 'removed', 'modified']
    for key in changes_keys:
        files += commit.get(key, [])
    return files


def get_argocd_app_from_path(base_path: Path, root_dir: Path) -> str | None:
    current_dir = base_path.parent
    application_file_name = os.getenv('APPLICATION_FILE_NAME', '')
    while current_dir != root_dir:
        files = get_files_in_directory(current_dir)
        if application_file_name in files:
            with open(current_dir / application_file_name, 'r') as f:
                return f.read().strip()
        current_dir = current_dir.parent
    return None


def get_affected_argocd_applications(clone_path: Path, changed_files: list[str]) -> set[str]:
    affected_apps = set()
    for file in changed_files:
        argo_app_name = get_argocd_app_from_path(clone_path / file, clone_path)
        if argo_app_name:
            affected_apps.add(argo_app_name)
    return affected_apps


if __name__ == '__main__':
    print(get_files_in_directory(Path.cwd()))
