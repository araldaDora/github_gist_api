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
