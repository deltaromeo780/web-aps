# Kamil

def add_note(notes: list) -> list:
    new_note = input("Write a new note\n")
    notes.append(new_note)
    print("Note added.")
    return notes

def delete_note(notes: list) -> list:

    show_notes(notes)
    try:
        choice = int(input("Enter the number of the note you want to delete: ")) - 1
        if 0 <= choice < len(notes):
            notes.remove(notes[choice])
            print("Note deleted.")
        else:
            print("Invalid note number.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    return notes  


def edit_note(notes: list) -> list:
    show_notes(notes)
    try:
        choice = int(input("Enter the number of the note you want to edit: ")) - 1
        if 0 <= choice < len(notes):
            new_note = input("Write a new note: ")
            notes[choice] = new_note
            print("Note edited.")
        else:
            print("Invalid note number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

    return notes

def show_notes(notes: list):
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note}")
    return notes

NOTES_KEYWORDS = {
    "add": add_note,
    "delete": delete_note,
    "edit": edit_note,
    "show": show_notes
}

def manage_notes(old_notes: list) -> list:
    while True:
        print("What do you want to do with notes? (add/delete/edit/show/exit)")
        notes_command = input()
        if notes_command == "exit":
            break
        try:
            old_notes = NOTES_KEYWORDS[notes_command](old_notes)
        except KeyError:
            print("I don't understand that command. Please try again.")
    return old_notes