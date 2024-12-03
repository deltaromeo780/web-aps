# models.py
from mongoengine import Document, StringField, ReferenceField

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    text = StringField(required=True)
    author = ReferenceField(Author)


# from mongoengine import Document, StringField, ReferenceField, ListField
#
#
# class Author(Document):
#     author = StringField(required=True)
#
#
# class Quote(Document):
#     quote = StringField(required=True)
#     author = ReferenceField(Author)
