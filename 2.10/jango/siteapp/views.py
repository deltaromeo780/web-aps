from django.shortcuts import render, redirect
from .models import Author, Quote, Tag
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
from django.http import HttpResponse
from .paths import authors_file_path, quotes_file_path, tags_file_path
import json


# Create your views here.
def main(request):
    quotes = Quote.objects.all()
    return render(request, "siteapp/quotes.html", {"quotes": quotes})


def author(request, author_fullname):
    author = Author.objects.filter(fullname=author_fullname).first()
    return render(request, "siteapp/author_details.html", {"author": author})


@login_required
def add_author(request):

    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save()

            return redirect(to="siteapp:main")
        else:
            return render(request, "siteapp/add_author.html", {"form": form})

    return render(request, "siteapp/add_author.html", {"form": AuthorForm()})


@login_required
def add_quote(request):
    authors = Author.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            author = Author.objects.filter(fullname=request.POST.get("author")).get()
            new_quote.author = author
            new_quote.save()

            return redirect(to="siteapp:main")
        else:
            return render(
                request, "siteapp/add_quote.html", {"authors": authors, "form": form}
            )

    return render(
        request, "siteapp/add_quote.html", {"authors": authors, "form": QuoteForm()}
    )


def load_author(author: dict):
    author_in_db = Author.objects.filter(fullname=author["fullname"]).first()
    if author_in_db != None:
        author_in_db.delete()

    author_to_db = Author(
        fullname=author["fullname"],
        born_date=author["born_date"],
        born_location=author["born_location"],
        description=author["description"],
    )
    author_to_db.save()


def load_tag(tag: str):
    tag_in_db = Tag.objects.filter(name=tag).first()

    if tag_in_db != None:
        tag_in_db.delete()

    tag_to_db = Tag(name=tag)
    tag_to_db.save()


def load_quote(quote: dict):
    quote_in_db = Quote.objects.filter(quote=quote).first()

    if quote_in_db != None:
        quote_in_db.delete()

    author = Author.objects.filter(fullname=quote["author"]).first()
    tags = Tag.objects.filter(name__in=quote["tags"]).all()

    quote_to_db = Quote(quote=quote["quote"], author=author)

    quote_to_db.save()
    quote_to_db.tags.set(tags)


def load(request):

    try:

        with open(authors_file_path, "r") as fh:
            authors_from_scrapping = json.load(fh)

        with open(quotes_file_path, "r") as fh:
            quotes_from_scrapping = json.load(fh)

        with open(tags_file_path, "r") as fh:
            tags_from_scrapping = json.load(fh)

        # load authors
        for author in authors_from_scrapping:
            load_author(author)

        # load tags
        for tag in tags_from_scrapping:
            load_tag(tag)

        # load quotes
        for quote in quotes_from_scrapping:
            load_quote(quote)

        message = "Everything works"

    except Exception as e:
        print(e)
        message = f"Something went wrong"

    return HttpResponse(message)
