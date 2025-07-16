from django.shortcuts import render, redirect
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    content = util.get_entry(title)

    if content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Error 404, page not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()

    if query in entries:
        return entry(request, query)

    results = [entry for entry in entries if query.lower() in entry.lower()]

    if not results:
        return render(request, "encyclopedia/error.html", {
            "message": "No results found."
        })

    return render(request, "encyclopedia/search.html", {
        "result": results
    })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        entries = util.list_entries()

        if any (entry.lower() == title.lower() for entry in entries):
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with that title already exists."
            })

        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "POST":
        new_content = request.POST["content"]
        util.save_entry(title, new_content)
        return redirect("entry", title=title)

    content = util.get_entry(title)
    
    return render(request, "encyclopedia/edit.html", {
    "title": title,
    "content": content
})


def random(request):
    import random
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect("entry", title=title)
