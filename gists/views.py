import requests
from django.shortcuts import render
from django.contrib import messages
from .services import githubServices


def homepage(request):
    context = {}
    while True:
        if request.method == "POST":
            github_user = request.POST.get("github_user", "")
            user_gists = githubServices.make_user_gist_request(github_user)
            if not user_gists.ok:
                break

            try:
                user_gists_jsons = user_gists.json()
            except requests.exceptions.JSONDecodeError:
                messages.error(request, f"Failed retrieving gists for user {github_user}", extra_tags="danger")
                break

            gists = []
            for user_gist in user_gists_jsons:
                crt_gist = {
                    "files": [file_data for _, file_data in user_gist.get("files", {}).items()],
                    "owner_login": user_gist.get("owner", {}).get("login", ""),
                    "owner_avatar": user_gist.get("owner", {}).get("avatar_url", "")
                }
                gists.append(crt_gist)
            context = {
                "gists": gists
            }
            break
    return render(request, "gists/home.html", context=context)
