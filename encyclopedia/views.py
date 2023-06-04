from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from . import util
import markdown2
from random import choice

class NewSearchForm(forms.Form):
    query = forms.CharField(label="Search Encyclopedia...")
class NewTitleForm(forms.Form):
    title = forms.CharField(label="Enter title:")

def index(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the query from the 'cleaned' version of form data
            query = form.cleaned_data["query"]

            # Look if the query corresponds to an existing entry
            if query in util.list_entries():
                return render(request, "encyclopedia/entry.html", {
                    "form": NewSearchForm(),
                    "entry": markdown2.markdown(util.get_entry(query)),
                    "atitle": query})

            matching = []
            for entry in util.list_entries():
                if query in entry:
                    matching.append(entry)
                else:
                    continue

            # If the query is a substring of an existing entry title
            if matching:
                return render(request, "encyclopedia/search_results.html", {
                    "form": NewSearchForm(),
                    "atitle": query,
                    "matching": matching})
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/index.html", {
                "form": form
            })

    return render(request, "encyclopedia/index.html", {
        "form": NewSearchForm(),
        "entries": util.list_entries(),
        })


def display_entry(request, atitle):
    # Look if the query corresponds to an existing entry
    if (atitle in util.list_entries()):
        return render(request, "encyclopedia/entry.html", {
        "form": NewSearchForm(),
        "entry": markdown2.markdown(util.get_entry(atitle)),
        "atitle": atitle})
    else:
        return render(request, "encyclopedia/error.html", {
            "form": NewSearchForm(),
            "atitle": atitle})

def create_new_page(request):
    return render(request, "encyclopedia/create.html", {
        "form": NewSearchForm(),
        "titleform": NewTitleForm(),
    })

def save_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if title not in util.list_entries():
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:entry", args=(title,)))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": NewSearchForm(),
                "titleform": NewTitleForm(),
                "title": title,
                "content": content,
                "error_message":
                    "<b>Error</b> : an entry with your chosen title already exists; Please enter a new one.",
            })
    else:
        return HttpResponseRedirect(reverse("wiki:create"))

def edit_page(request, atitle):
    return render(request, "encyclopedia/edit.html", {
        "form": NewSearchForm(),
        "atitle": atitle,
        "content": util.get_entry(atitle),
    })

def save_edit(request, atitle):
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(atitle, content)
        return HttpResponseRedirect(reverse("wiki:entry", args=(atitle,)))

def random_page(request):
    random_entry = ''.join([choice(util.list_entries())])
    return render(request, "encyclopedia/entry.html", {
        "form": NewSearchForm(),
        "entry": markdown2.markdown(util.get_entry(random_entry)),
        "atitle": random_entry})
