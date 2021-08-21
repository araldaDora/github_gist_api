import requests


class GithubServices:
    def __init__(self):
        self.user_gists_base_path = "https://api.github.com/users"
        self.gist_forks_base_path = "https://api.github.com/gists"

    def make_request(self, url):
        response = requests.get(url)
        return response

    def make_user_gist_request(self, user, page=1):
        request_url = f"{self.user_gists_base_path}/{user}/gists?page={page}"
        return self.make_request(request_url)

    def make_gist_forks_request(self, gist_id, page=1):
        requests_url = f"{self.gist_forks_base_path}/{gist_id}/forks?page={page}"
        return self.make_request(requests_url)


githubServices = GithubServices()


def get_gists_for_given_page(github_user, page):
    status = -1
    user_gists_jsons = []
    user_gists = githubServices.make_user_gist_request(github_user, page)
    if user_gists.ok:
        try:
            user_gists_jsons = user_gists.json()
            status = 0
        except requests.exceptions.JSONDecodeError:
            print("Failed decoding gist json")
    return status, user_gists, user_gists_jsons


def get_gists_for_user(github_user):
    status = -1
    user_gists_jsons = []
    status, user_gists, user_gists_jsons = get_gists_for_given_page(github_user, 1)
    previous_page = 0
    crt_page = 1
    while "next" in user_gists.links and previous_page != crt_page:
        link = user_gists.links
        next_page_url = link.get("next", {}).get("url", "")
        if next_page_url == "":
            break
        page_nb_index = next_page_url.rfind("=") + 1
        next_page = int(next_page_url[page_nb_index:])
        status, _, next_user_gists_jsons = get_gists_for_given_page(github_user, next_page)
        user_gists_jsons.extend(next_user_gists_jsons)

        previous_page = crt_page
        crt_page = next_page
    return status, user_gists_jsons


def get_forks_for_given_page(gist_id, page):
    status = -1
    gist_forks_json = []
    gist_forks = githubServices.make_gist_forks_request(gist_id, page)
    if gist_forks.ok:
        try:
            gist_forks_json = gist_forks.json()
            status = 0
        except requests.exceptions.JSONDecodeError:
            print("Failed decoding fork json")
    return status, gist_forks, gist_forks_json


def get_latest_forks_for_gist(gist_id, fork_count):
    status = -1
    gist_forks_json = []
    previous_gist_forks_json = []
    status, gist_forks, gist_forks_json = get_forks_for_given_page(gist_id, fork_count)
    if status == 0:
        link = gist_forks.links
        if link:
            last_page_url = link.get("last", {}).get("url", "")
            if last_page_url != "":
                page_nb_index = last_page_url.rfind("=") + 1
                last_page = int(last_page_url[page_nb_index:])
                # Get the newest forks --> from the last page
                status, _, gist_forks_json = get_forks_for_given_page(gist_id, last_page)
                if status == 0 and len(gist_forks_json) < 3 and last_page != 1:
                    status, _, previous_gist_forks_json = get_forks_for_given_page(gist_id, last_page-1)
    if status == 0:
        previous_gist_forks_json.extend(gist_forks_json)
        gist_forks_json = previous_gist_forks_json[-3:]
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
