import markdown2
from random import choice

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
from .forms import NewEntryForm, EditEntryForm

ENTRIES_PATH = "entries/"

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if entry not in util.list_entries():
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/entry.html", {
        "entry_name": entry,
        "entry_content": markdown2.markdown(util.get_entry(entry))
    })

def search(request):
    query = request.GET.get('q', None)
    if query not in util.list_entries():
        similar_entries = []
        for entry in util.list_entries():
            if query.upper() in entry.upper():
                similar_entries.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": similar_entries
        })

    return HttpResponseRedirect(reverse("entry_page", args=[query]))

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title, content = form.cleaned_data["title"], form.cleaned_data["content"]
            with open(ENTRIES_PATH + title + ".md", "w") as f:
                f.write(content)
            return HttpResponseRedirect(reverse("entry_page", args=[form.cleaned_data["title"]]))
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form,
            })
        
    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm(),
    })

def edit(request, entry):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            with open(ENTRIES_PATH + entry + ".md", "w") as f:
                f.write(content)
            return HttpResponseRedirect(reverse("entry_page", args=[entry]))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form,
            })
    
    return render(request, "encyclopedia/edit.html", {
        "form": EditEntryForm(data={"content": util.get_entry(entry)}),
        "entry": entry
    })

def random(request):
    entry = choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry_page", args=[entry]))

