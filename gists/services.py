import requests


class GithubServices:
    def __init__(self):
        self.user_gists_base_path = "https://api.github.com/users"
        self.gist_forks_base_path = "https://api.github.com/gists"

    def make_request(self, url):
        response = requests.get(url)
        return response

    def make_user_gist_request(self, user):
        request_url = f"{self.user_gists_base_path}/{user}/gists"
        return self.make_request(request_url)

    def make_gist_forks_request(self, gist_id):
        requests_url = f"{self.gist_forks_base_path}/{gist_id}/forks"
        return self.make_request(requests_url)


githubServices = GithubServices()


def get_gist_information(gist_files):
    tags = set()
    files = []
    for f in gist_files:
        crt_file = {
            "filename": f.get("filename", ""),
            "raw_url": f.get("raw_url", "")
        }
        file_type = f.get("type", "")
        tags.add(str(file_type))
        files.append(crt_file)

    tags = list(tags)
    tags.sort(key=len)
    return files, tags


def get_gist_forks_information(gist_forks):
    fork_information = []
    for crt_fork in gist_forks:
        crt_fork_information = {
            "fork_owner": crt_fork.get("owner", {}).get("login", ""),
            "fork_owner_avatar": crt_fork.get("owner", {}).get("avatar_url", "")
        }
        fork_information.append(crt_fork_information)
    return fork_information
