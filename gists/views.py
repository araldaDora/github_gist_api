import requests
from django.shortcuts import render
from django.contrib import messages
from .services import githubServices, get_gist_information


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
                files = [file_json_info for _, file_json_info in user_gist.get("files", {}).items()]
                files, tags = get_gist_information(files)
                crt_gist = {
                    "files": files,
                    "file_tags": tags,
                    "description": user_gist.get("description", "")
                }
                gists.append(crt_gist)
            gists_count = len(user_gists_jsons)
            context = {
                "gist_owner": user_gists_jsons[0].get("owner", {}).get("login", "") if gists_count else "",
                "gist_owner_avatar": user_gists_jsons[0].get("owner", {}).get("avatar_url", ""),
                "gists": gists
            }
            break
    return render(request, "gists/home.html", context=context)
