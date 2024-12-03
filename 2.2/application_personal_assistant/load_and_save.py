import pickle


def save_contacts(contacts):
    with open("data.bin", "wb") as f:
        pickle.dump(contacts, f)
    print("A record has been created in the file:", "data.bin")


def read_contacts():
    try:
        with open("data.bin", "rb") as f:
            contacts = pickle.load(f)
            print("contacts loaded")
            return contacts
    except FileNotFoundError:
        print("You don't have any contacts saved yet")
