from django.shortcuts import render
from django.contrib import messages
from .services import (
    get_gists_for_user,
    get_latest_forks_for_gist,
    get_gist_information,
    get_gist_forks_information
)


def homepage(request):
    context = {}
    if request.method == "POST":
        github_user = request.POST.get("github_user", "")
        status, user_gists_jsons = get_gists_for_user(github_user)
        if status != 0:
            user_gists_jsons = []
            messages.error(request, f"Failed retrieving gists for {github_user}", extra_tags="danger")
        gists = []
        for user_gist in user_gists_jsons:
            files, tags = get_gist_information(user_gist)
            crt_gist = {
                "files": files,
                "file_tags": tags,
                "description": user_gist.get("description", ""),
                "forks": []
            }
            # Get the latest forks for the current gist
            gist_id = user_gist.get("id", "")
            status, gist_forks_json = get_latest_forks_for_gist(gist_id, 3)
            if status != 0:
                gist_forks_json = []
                messages.error(request, f"Failed retrieving forks for gist {gist_id} of user {github_user}",
                               extra_tags="danger")
            crt_gist["forks"] = get_gist_forks_information(gist_forks_json)
            gists.append(crt_gist)

        gists_count = len(user_gists_jsons)
        if gists_count:
            context = {
                "gist_owner": user_gists_jsons[0].get("owner", {}).get("login", "") if gists_count else "",
                "gist_owner_avatar": user_gists_jsons[0].get("owner", {}).get("avatar_url", ""),
                "gists": gists
            }
    return render(request, "gists/home.html", context=context)
