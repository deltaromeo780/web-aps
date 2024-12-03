from contacts import Contacts  # klasa Contacts
from command_assistant import (command_assistant)  # prompter - check and give us the correct command
from load_and_save import save_contacts, read_contacts
from search import searcher


#
#
# Caller of function with 'name' argument
#
def check_and_call(fun, book: Contacts):
    while True:
        name = input("Enter the name or write 'exit' to resign\n")
        if name.lower() == "exit":
            break
        elif book.is_name_exist(name):
            fun(name)
            save_fun(book)
            break
        else:
            print("There is no such contact")


#
#
# Command handlers
#


def help_fun(book: Contacts):
    print(
        """List of keywords:
        save - saving list of contacts to file
        add - add new contacts to your contacts book
        show - display all information about contact/contacts    (value/values required in next step/steps)
        names - display all names with no more informations
        notes - menage notes of choosen contact     (value/values required in next step/steps)
        birthday - display contacts whoose birthday are cooming... 
        search - search contact by choosen field    (value/values required in next step/steps)
        edit - edit contact     (value/values required in next step/steps)
        delete - remove contact     (value/values required in next step/steps)
        exit
        if you write wrong command, assistant will help you
        """
    )


#
#
#


def save_fun(book: Contacts):
    save_contacts(book.get_list_contacts())


#
#
#


def add_fun(book: Contacts):
    if book.add_contact() == None:
        pass
    else:
        save_fun(book)


#
#
#


def show_fun(book: Contacts):
    while True:
        name = input(
            "Enter the name of contact OR input 'all' if you want to show all contacts OR input 'exit' to resign\n"
        )
        if name.lower() == "all":
            # print(book.__str__())
            book.show_all_contacts()
            break
        elif name in book.get_all_names():
            book.show_choosen_contact(name)
            break
        elif name == "exit":
            break
        else:
            print("There is no such contact")


#
#
#


def names_fun(book: Contacts):
    for name in book.get_all_names():
        print(name)


#
#
#


def notes_fun(book: Contacts):
    print("You need to enter the name of contact to manage notes of contact")
    check_and_call(book.manage_notes, book)
    save_fun(book)


#
#
#


def birthday_fun(book: Contacts):
    book.get_cooming_birthday()


#
#
#


def edit_fun(book: Contacts):
    print(
        "You need to enter the name of contact to edit: name, address, phone, email, birthday of contact"
    )
    check_and_call(book.edit, book)


#
#
#


def search_fun(book: Contacts):
    while True:
        keyword = input(
            "Write the name of field by that you want to search contacts (address/ phone/ email/ birthady/ notes) or input 'exit' to resign\n"
        )
        if keyword == "exit":
            break
        else:
            try:
                searcher(book.contacts, keyword)
            except:
                print("There is no such field.\n")


def delete_fun(book: Contacts):
    print("You need to enter the name of contact to remove it")
    check_and_call(book.remove_contact, book)


#
#
#

#
#
# Keywords
#
KEYWORDS = {
    "help": help_fun,
    "save": save_fun,
    "add": add_fun,
    "show": show_fun,
    "names": names_fun,
    "notes": notes_fun,
    "birthday": birthday_fun,
    "search": search_fun,
    "edit": edit_fun,
    "delete": delete_fun,
}


#
#
# Main function
# show


def main():
    print("\n\nHello User, I am your virtual assistant")
    my_contacts_book = Contacts()  # start class constuctor
    loaded_contacts = read_contacts()
    my_contacts_book.set_list_contacts(loaded_contacts)

    if isinstance(my_contacts_book.get_list_contacts(), list):
        pass
    else:
        pass

    while True:
        command = input(
            "\nWhat do you want to do? Input 'help' to get a list of keywords\n"
        )
        # print(command)

        if command in ["exit", "exit ", "quit", "quit ", "bye"]:
            break

        try:
            KEYWORDS[command](my_contacts_book)
        except:
            try:
                command = command_assistant(command)
                KEYWORDS[command](my_contacts_book)
            except:
                print(
                    "Sorry, I don't understand what do you want...\n***** *** \nWrite 'help' to display available commands"
                )

    save_contacts(my_contacts_book.get_list_contacts())
    print("See you soon!\n")


#
#
#
if __name__ == "__main__":
    main()
