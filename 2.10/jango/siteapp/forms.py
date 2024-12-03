from django.forms import ModelForm, CharField, TextInput, DateField, DateInput
from .models import Tag, Quote, Author


class TagForm(ModelForm):

    name = CharField(min_length=2, max_length=30, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]


class AuthorForm(ModelForm):

    fullname = CharField(min_length=2, max_length=30, required=True, widget=TextInput())
    born_date = DateField(widget=DateInput())
    born_location = CharField(min_length=2, max_length=50, widget=TextInput())
    description = CharField(min_length=2, max_length=1500, widget=TextInput())

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class QuoteForm(ModelForm):

    quote = CharField(min_length=2, max_length=300, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ["quote"]
        exclude = ["author", "tags"]
