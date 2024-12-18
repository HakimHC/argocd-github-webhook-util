import time
import re
import subprocess


class Repo:
    def __init__(self, url: str):
        self.url = url
        self.full_name = self.__get_repo_name()
        self.clone_path = None

    def clone(self):
        now = str(int(time.time()))
        name = self.full_name.split('/')[-1]
        clone_path = f'/tmp/{name}-{now}'
        r = subprocess.run(['git', 'clone', self.url, clone_path], capture_output=True)
        if r.returncode != 0:
            raise Repo.GitCloneError(r.stderr.decode('utf-8'))
        print(f'Cloned repo to: {clone_path}')
        self.clone_path = clone_path

    def __get_repo_name(self) -> str | None:
        # TODO: implement parsing for https scheme
        if re.match(r'^git@.*:.*\.git$', self.url):
            return self.__parse_repo_name_ssh()
        if re.match(r'^https?://.*/.*/.*\.git$', self.url):
            return self.__parse_repo_name_https()
        return None
        # raise NotImplementedError()

    def __parse_repo_name_ssh(self):
        return re.findall(r'^git@.*:(.*)\.git$', self.url)[0]

    def __parse_repo_name_https(self):
        return re.findall(r'^https?://.*/(.*/.*).git$', self.url)[0]

    class GitCloneError(Exception):
        def __init__(self, message: str):
            super().__init__(message)


if __name__ == '__main__':
    repo = Repo('git@github.com:HakimHC/homelab.git')
    repo.clone()
