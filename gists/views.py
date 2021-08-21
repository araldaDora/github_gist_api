import requests
from django.shortcuts import render
from django.contrib import messages
from .services import (
    githubServices,
    get_gist_information,
    get_gist_forks_information
)


def homepage(request):
    context = {}
    if request.method == "POST":
        while True:
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
                    "description": user_gist.get("description", ""),
                    "forks": []
                }

                # Get the latest forks for the current gist
                gist_id = user_gist.get("id", "")
                gist_forks = githubServices.make_gist_forks_request(gist_id)
                if not gist_forks.ok:
                    gists.append(crt_gist)
                    continue
                try:
                    gist_forks_json = gist_forks.json()
                    gist_forks_json = gist_forks_json[-3:]  # Get the 3 latest forks
                except requests.exceptions.JSONDecodeError:
                    messages.error(request, f"Failed retrieving forks for gist {gist_id} of user {github_user}",
                                   extra_tags="danger")
                    gists.append(crt_gist)
                    break
                crt_gist["forks"] = get_gist_forks_information(gist_forks_json)
                gists.append(crt_gist)

            gists_count = len(user_gists_jsons)
            context = {
                "gist_owner": user_gists_jsons[0].get("owner", {}).get("login", "") if gists_count else "",
                "gist_owner_avatar": user_gists_jsons[0].get("owner", {}).get("avatar_url", ""),
                "gists": gists
            }
            break
    return render(request, "gists/home.html", context=context)
