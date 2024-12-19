from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown
import random 

from . import util

# Convert Markdown File into  HTML document
def convert_markdown_to_html(title):
    markdowner = markdown.Markdown()
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        return markdowner.convert(content)

# List out the whole entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Display Entry with their Titles
def title(request, title):
    html_file = convert_markdown_to_html(title)
    if html_file == None:
        return render(request, "encyclopedia/error.html", {
            "message": html_file
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_file
        })
        
# Search for an entry through a Form    
def search(request):
    if request.method == "POST":
        search_input = request.POST['q']
        html_file = convert_markdown_to_html(search_input)
        if html_file is not None:
            return render(request, "encyclopedia/entry.html", {
            "title": search_input,
            "content": html_file
            })
        else:
            all_wiki_entries = util.list_entries()
            user_recommedation = []
            for entry in all_wiki_entries:
                if search_input.lower() in entry.lower():
                    user_recommedation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "user_recommedation": user_recommedation
            })
    
# Create a new Entry
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        title_already_exit = util.get_entry(title)
        if title_already_exit is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Page already exit"
            })
        else:
            html_file = convert_markdown_to_html(title)
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_file
            })

# Edit an entry        
def edit_page(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
# Save Entry
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_file = convert_markdown_to_html(title)
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_file
        })
    
def random_choice(request):
    allEntries = util.list_entries()
    random_entry = random.choice(allEntries)
    html_file = convert_markdown_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_file
    })
