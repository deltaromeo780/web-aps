import os

current_directory = os.getcwd()


authors_file_path = os.path.join(
    current_directory, os.path.join("data_to_load", "authors.json")
)
quotes_file_path = os.path.join(
    current_directory, os.path.join("data_to_load", "quotes.json")
)
tags_file_path = os.path.join(
    current_directory, os.path.join("data_to_load", "tags.json")
)
