from django.shortcuts import render
from django.contrib import messages
from .services import (
    get_gists_for_user,
    get_latest_forks_for_gist,
    get_gist_information,
    get_gist_forks_information,
    get_gist_file_contents
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
                "gist_id": user_gist.get("id", ""),
            }
            gists.append(crt_gist)
        request.session["gists"] = gists  # Set this so that we can filter without requesting the data again

        gists_count = len(user_gists_jsons)
        if gists_count:
            context = {
                "gist_owner": user_gists_jsons[0].get("owner", {}).get("login", "") if gists_count else "",
                "gist_owner_avatar": user_gists_jsons[0].get("owner", {}).get("avatar_url", ""),
                "gists": gists
            }
    return render(request, "gists/home.html", context=context)


def display_gist_file_content(request):
    context = {}
    if request.method == "POST":
        gist_file_owner = request.POST.get("gist_file_owner", "")
        gist_file_owner_avatar = request.POST.get("gist_file_owner_avatar", "")
        gist_file_name = request.POST.get("gist_file_name", "")
        gist_file_raw_url = request.POST.get("gist_file_raw_url", "")

        gist_file_contents = get_gist_file_contents(gist_file_raw_url)
        gist_file_contents = str(gist_file_contents)
        context = {
            "gist_owner": gist_file_owner,
            "gist_owner_avatar": gist_file_owner_avatar,
            "gist_file_name": gist_file_name,
            "gist_file_contents": gist_file_contents
        }
    return render(request, "gists/display_gist_file.html", context=context)


def display_latest_forks_for_gist(request):
    context = {}
    if request.method == "POST":
        gist_id = request.POST.get("gist_id", "")
        gist_file_owner = request.POST.get("gist_file_owner", "")
        gist_file_owner_avatar = request.POST.get("gist_file_owner_avatar", "")

        status, gist_forks_json = get_latest_forks_for_gist(gist_id, 3)
        if status != 0:
            gist_forks_json = []
            messages.error(request, f"Failed retrieving forks for gist {gist_id} of user {gist_file_owner}",
                           extra_tags="danger")
        latest_forks = get_gist_forks_information(gist_forks_json)
        context = {
            "gist_id": gist_id,
            "gist_owner": gist_file_owner,
            "gist_owner_avatar": gist_file_owner_avatar,
            "gist_latest_forks": latest_forks,
            "latest_forks_count": len(latest_forks)
        }
    return render(request, "gists/display_latest_forks.html", context=context)


def display_filtered_gists(request):
    context = {}
    if request.method == "POST":
        selected_tag = request.POST.get("selected_tag", "")
        gist_file_owner = request.POST.get("gist_file_owner", "")
        gist_file_owner_avatar = request.POST.get("gist_file_owner_avatar", "")

        gists = request.session["gists"]
        filtered_gists = []
        for gist in gists:
            if selected_tag in gist.get("file_tags", []):
                filtered_gists.append(gist)
        context = {
            "gist_owner": gist_file_owner,
            "gist_owner_avatar": gist_file_owner_avatar,
            "gists": filtered_gists
        }
    return render(request, "gists/home.html", context=context)