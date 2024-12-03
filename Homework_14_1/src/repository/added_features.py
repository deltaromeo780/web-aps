from datetime import datetime, timedelta

from fastapi import status, HTTPException


def get_id_birthday_upcoming(dates_id_list: list[tuple[datetime, int]]) -> list[int]:
    """
       Function to retrieve the IDs of contacts with upcoming birthdays.

       This function takes a list of tuples containing birth dates and contact IDs,
       and returns a list of contact IDs for contacts whose birthdays are upcoming within the next 7 days.

       Args:
           dates_id_list (List[Tuple[datetime, int]]): A list of tuples where each tuple contains
               a birth date (datetime object) and a contact ID (int).

       Returns:
           List[int]: A list containing the IDs of contacts with upcoming birthdays within the next 7 days.

       Example:
           Given the input dates_id_list:
           [(datetime(2024, 2, 20), 1), (datetime(2024, 2, 26), 2), (datetime(2024, 3, 2), 3)]

           If today's date is 2024-02-24, the function would return [2, 3] because contacts with IDs 2 and 3
           have birthdays within the next 7 days.
       """
    print("We are in get_id_birthady_upcoming")
    
    id_list = []

    today = datetime.now().date()
    this_year = today.year
    days = timedelta(days=7)

    for date_tuple in dates_id_list:
        born_date = date_tuple[0].date()
        contact_id = date_tuple[1]
        born_day = born_date.day
        born_month = born_date.month

        closest_birthday = datetime(
            year=this_year, month=born_month, day=born_day
        ).date()

        if closest_birthday < today:
            closest_birthday = datetime(
                year=this_year + 1, month=born_month, day=born_day
            ).date()

        if closest_birthday - today <= days:
            id_list.append(contact_id)

    return id_list


def get_no_contacts_exception(contacts):
    """
       Function to raise an HTTP exception if no contacts are found.

       This function checks if the provided contacts list is empty, and if so, raises
       an HTTP 404 Not Found exception with the detail message "No contact found".

       Args:
           contacts: The list of contacts to check for emptiness.

       Raises:
           HTTPException: An HTTP 404 Not Found exception is raised if the contacts list is empty.

       Example:
           If the provided contacts list is empty, calling this function will raise an HTTPException
           with status code 404 and detail message "No contact found".
       """
    print("We are in get_no_contact_exeption")

    if not bool(contacts):  # bool(contacts) == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No contact found"
        )
