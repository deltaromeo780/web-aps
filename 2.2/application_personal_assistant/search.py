def search_by_notes(contacts): #funkcja Kamila przeklejona
    note = input("Input note you want to find.\n")
    i = 0
    for contact in contacts:
        if note in contact["notes"]:
            i += 1
            print(contact)
    if i == 0:
        print("No contact found with such a note.")
    else:
        print(f"You found {i} contacts with that note.")


def searcher(contacts, keyword):  # funkcja dopisana przez Olkę
    print(list(contacts[0].keys()))
    if keyword == "notes":
        search_by_notes(contacts)
    elif keyword not in list(contacts[0].keys()):
        raise Exception
    else:
        phrase_to_find = input(f"Input {keyword} to find\n")
        list_of_expected_contacts = []
        for contact in contacts:
            if phrase_to_find in contact[keyword]:
                list_of_expected_contacts.append(contact)

        if bool(list_of_expected_contacts):
            print(
                f"{len(list_of_expected_contacts)} contacts with {keyword}: {phrase_to_find} have been found."
            )
            print(f"List of contact:")
            for contact in list_of_expected_contacts:
                print(contact)

        else:
            print(f"No contacts with {keyword}: {phrase_to_find} have been found.")
