from data_verification import (
    phone_verification,
    email_verification,
    birthday_verification,
)
from notes import manage_notes
from contact_editor import edit
from birthday import cooming_birthday


class Contacts:
    #
    #
    #
    #
    #
    def __init__(self):
        self.contacts = []

    #   constructor; sets list of contacts as empty list;
    #
    #
    #
    #
    #
    def get_list_contacts(self):
        return self.contacts

    #   returns list of contacts
    #
    #
    #
    #
    #
    def set_list_contacts(self, list_of_contacts):
        if isinstance(list_of_contacts, list):
            # print(f"{list_of_contacts} is list")
            pass
        else:
            # print(f"Error, {list_of_contacts} is not a list...")
            return None
        for contact in list_of_contacts:
            if isinstance(contact, dict):
                # print(f"{contact} is dict")
                if list(contact.keys()) == [
                    "name",
                    "address",
                    "phone",
                    "email",
                    "birthday",
                    "notes",
                ]:
                    # print(f"Inputed keys = {contact.keys()}")
                    pass
                else:
                    # print(f"Error, inputed keys = {contact.keys()} are wrong")
                    return None

            else:
                # print(f"Error, {contact} is not dict")
                return None
        self.contacts = list_of_contacts

    #   sets list of contacts
    #
    #
    #
    #
    #

    def is_name_exist(self, name: str, print_if_not = True) -> bool:
        # print(f"is_name_exist(self, {name})")
        if name in self.get_all_names():
            return True
        else:
            if print_if_not:
                print("There is no such name")
            return False

    #   checks if given name exist in contacts list
    #
    #
    #
    #
    #
    def add_contact(self):
        # print(f"add_contacts(self)")
        while True:
            name = input(
                "Input name of contact to continue adding new contact or write 'exit' to resign: \n"
            )
            if name == "exit":
                print(f"New contact hasn't been added...")
                return None

            elif self.is_name_exist(name, print_if_not=False):
                print(
                    f"Such name exist in your contacts. List of names in your contacts: {list(self.get_all_names())}. You have to choose different name."
                )
                continue
            else:
                break

        address = input(
            "Input address of contact to continue adding new contact or write 'exit' to resign: \n"
        )
        if address == "exit":
            print(f"New contact hasn't been added...")
            return None

        while True:
            phone = input(
                "Input phone number of contact to continue adding new contact or write 'exit' to resign: \n"
            )
            if phone == "exit":
                print(f"New contact hasn't been added")
                return None
            elif phone_verification(phone) == True:
                break
            else:
                print("Format of given number is wrong. Try again\n")

        while True:
            email = input(
                "Input email of contact to continue adding new contact or write 'exit' to resign: \n"
            )
            if email == "exit":
                print(f"New contact hasn't been added")
                return None
            elif email_verification(email) == True:
                break
            else:
                print("Format of given email is wrong. Try again\n")

        while True:
            birthday = input(
                "Input birthday (yyyy-mm-dd) of contact to continue adding new contact or write 'exit' to resign: \n"
            )
            if birthday == "exit":
                print(f"New contact hasn't been added")
                return None
            elif birthday_verification(birthday) == True:
                break
            else:
                print("Format of given birthday is wrong. Try again\n")

        new_contact = {
            # "id": Contacts.current_id,  # id kontaktu się nie zmienia
            "name": name,
            "address": address,
            "phone": phone,
            "email": email,
            "birthday": birthday,
            "notes": [],
        }
        

        while True:
            decision = input(
                f"Do you want to add contact {new_contact} to your contacts list? \nEnter 'y' or 'yes' to accept\nEnter 'n' or 'no' to not accept\n"
            ).lower()
            if decision in ["yes", "y"]:
                self.contacts.append(new_contact)
                # Contacts.current_id += 1
                print(f"Contact '{name}' has been succesfully added")
                break
            elif decision in ["n", "no"]:
                print(f"Contact '{name}' hasn't been added")
                return None
            else:
                print(
                    f"Contact '{name}' hasn't been added, enter 'y' or 'yes'/'n' or 'no' to accept or not accept the contact."
                )
                continue

            # print(f"You have {self.count_contacts()} contacts")
        self.count_contacts()
        return "Contact added"


    #   adds new contact with all fields except notes; ask user for name, address, phone, email, birthday
    #
    #
    #
    #
    #
    def show_choosen_contact(self, name):
        # print(f"show_choosen_contact(self, {name})")
        for contact in self.contacts:
            if contact["name"] == name:
                print(contact)

    #   prints all informations about contact with given name
    #
    #
    #
    #
    #
    def show_all_contacts(self):
        # print(f"show_all_contact(self)")
        if self.contacts == []:
            print("You don't have any contact in your contact list")
        else:
            for contact in self.contacts:
                print(contact)
        self.count_contacts()

    #   prints all informations about every contact in contacts list
    #
    #
    #
    #
    #
    def remove_contact(self, name):
        # print(f"remove_contact(self, {name})")
        for contact in self.contacts:
            if contact["name"] == name:
                self.contacts.remove(contact)
                print(f"Contact {name} has been succesfully deleted")

        self.count_contacts()

    #   deletes contact with given name
    #
    #
    #
    #
    def manage_notes(self, name):
        # print(f"manage_notes(self, {name})")
        number_of_contact = -1
        for contact in self.contacts:
            number_of_contact += 1
            if contact["name"] == name:
                old_notes = contact["notes"]
                new_notes = manage_notes(old_notes)
                try:
                    self.contacts[number_of_contact]["notes"] = new_notes
                except:
                    print("Edition of notes failed")
                # print(f"notes of {name} has been changed") - to lepiej niech manager notatek robi

    #   starts outer function; gives existing list of notes (value of field "notes") to outer manager of notes and rewrites field "notes"
    #
    #
    #
    #
    #
    def get_all_names(self):
        # print(f"get_all_names(self)")
        for contact in self.contacts:
            name = contact["name"]
            yield name

    # names of contacts generator, usefull in for loop
    #
    #
    #
    #
    #

    def get_cooming_birthday(self):
        birthday_list = []
        for contact in self.contacts:
            birthday = {"name": contact["name"], "birthday": contact["birthday"]}
            birthday_list.append(birthday)
        cooming_birthday(birthday_list)

    #   calls outer function witch (która :D, nigdy nie pamiętam jak to się pisze) prints names and birthdays of contacts whose birthday is close to current date; user decides how close
    #
    #
    #
    #
    #

    def edit(self, name):
        number_of_contact = -1
        for contact in self.contacts:
            number_of_contact += 1
            if contact["name"] == name:
                old_data = {
                    "address": contact["address"],
                    "phone": contact["phone"],
                    "email": contact["email"],
                    "birthday": contact["birthday"],
                }
                new_data = edit(old_data)
                try:
                    self.contacts[number_of_contact]["address"] = new_data["address"]
                    self.contacts[number_of_contact]["phone"] = new_data["phone"]
                    self.contacts[number_of_contact]["email"] = new_data["email"]
                    self.contacts[number_of_contact]["birthday"] = new_data["birthday"]
                except:
                    print("Edition of contacts failed")

        print(f"contact <{name}> has been edited.")

  
    #
    #
    #
    #

    def count_contacts(self) -> int:
        number_of_contacts = len(self.contacts)
        print(f"You have {number_of_contacts} contact(s) on your list of contacts")
        return number_of_contacts

    # counts a number of contacts and returns it

    ##
