from django.shortcuts import render
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

def search(request, title):
    entries = util.list_entries()
    results = [entry for entry in entries if title.lower() in title.lower()]

    if not results:
        return render(request, "encyclopedia/error.html", {
            "message": "No results found."
        })

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })

