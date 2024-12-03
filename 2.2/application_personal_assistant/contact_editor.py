# Ala
from command_assistant import command_assistant
from data_verification import (
    phone_verification,
    birthday_verification,
    email_verification,
)


def edit(old_data: dict) -> dict:
    # funkcja dostaje słownik: old_data = {"address": contact["address"], "phone": contact["phone"], "email" :contact["email"], "birthday": contact["birthday"],} i zwraca słownik new_data = {"address": contact["address"], "phone": contact["phone"], "email" :contact["email"], "birthday": contact["birthday"],} ze zmienionymi odpowiednimi danymi
    # nazwa argumentu może się zmienić, nie ma to znaczenia na zewnątrz funkcji
    while True:
        command = input(
            "What do you want to edit?\nphone\naddress\nemail\nbirthday\nnotes\nTo end edition and return to main menu type: close.\n"
        )
        if command not in [
            "phone",
            "address",
            "email",
            "birthday",
            "close",
            "notes",
        ]:
            proper = command_assistant(command)
            answer = input(f"I didn't understand you. Did you mean <{proper}>? yes/no")
            if answer == "no":
                continue
            else:
                command = command_assistant(command)

        if command == "close":
            break
        elif command in ["phone", "address", "email", "birthday"]:
            searched_dict = old_data
            if command == "address":
                new_address = input("Enter new address. ")
                print("Address has been changed successfully.")
                return {
                    "address": new_address,
                    "phone": searched_dict["phone"],
                    "email": searched_dict["email"],
                    "birthday": searched_dict["birthday"],
                }

            elif command == "phone":
                while True:
                    new_phone = input("Enter new phone number. To exit type: close.")
                    if new_phone == "close":
                        break
                    elif phone_verification(new_phone) == True:
                        print("Phone number has been changed successfully.")
                        return {
                            "address": searched_dict["address"],
                            "phone": new_phone,
                            "email": searched_dict["email"],
                            "birthday": searched_dict["birthday"],
                        }

                    else:
                        print("Format of given number is wrong. Try again")

            elif command == "email":
                while True:
                    new_email = input("Enter new email. To exit type: close.")
                    if new_email == "close":
                        break
                    elif email_verification(new_email) == True:
                        print("Email has been changed successfully.")
                        return {
                            "address": searched_dict["address"],
                            "phone": searched_dict["phone"],
                            "email": new_email,
                            "birthday": searched_dict["birthday"],
                        }

                    else:
                        print("Format of given email is wrong. Try again")

            elif command == "birthday":
                while True:
                    new_birthday = input("Enter new birthday. To exit type: close.")
                    if new_birthday == "close":
                        break
                    elif birthday_verification(new_birthday) == True:
                        print("Birthday date has been changed successfully.")
                        return {
                            "address": searched_dict["address"],
                            "phone": searched_dict["phone"],
                            "email": searched_dict["email"],
                            "birthday": new_birthday,
                        }

                    else:
                        print("Format of given birthday date is wrong. Try again")
