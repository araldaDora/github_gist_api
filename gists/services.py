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


def get_gists_for_user(github_user):
    status = -1
    user_gists_jsons = []
    user_gists = githubServices.make_user_gist_request(github_user)
    if user_gists.ok:
        try:
            user_gists_jsons = user_gists.json()
            status = 0
        except requests.exceptions.JSONDecodeError:
            print("Failed decoding gist json")
    return status, user_gists_jsons


def get_latest_forks_for_gist(gist_id, fork_count):
    status = -1
    gist_forks_json = []
    gist_forks = githubServices.make_gist_forks_request(gist_id)
    if gist_forks.ok:
        try:
            gist_forks_json = gist_forks.json()
            gist_forks_json = gist_forks_json[-fork_count:]  # Get the latest forks
            status = 0
        except requests.exceptions.JSONDecodeError:
            print("Failed decoding fork json")
    return status, gist_forks_json


def get_gist_file_contents(gist_file_raw_url):
    gist_file = githubServices.make_request(gist_file_raw_url)
    if gist_file.ok:
        return gist_file.text
    return "Error retrieving gist file"


def get_gist_information(gist):
    tags = set()
    files = []
    gist_files = [file_json for _, file_json in gist.get("files", {}).items()]
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
