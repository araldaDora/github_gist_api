import requests


class GithubServices:
    def __init__(self):
        self.user_gists_base_path = "https://api.github.com/users"

    def make_request(self, url):
        response = requests.get(url)
        return response

    def make_user_gist_request(self, user):
        request_url = f"{self.user_gists_base_path}/{user}/gists"
        return self.make_request(request_url)


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
