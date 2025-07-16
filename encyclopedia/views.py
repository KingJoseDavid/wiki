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

