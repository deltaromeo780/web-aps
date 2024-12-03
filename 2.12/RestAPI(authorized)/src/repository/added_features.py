from datetime import datetime, timedelta

from fastapi import status, HTTPException


def get_id_birthday_upcoming(dates_id_list: list[tuple[datetime, int]]) -> list[int]:

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

    if bool(contacts) == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No contact found"
        )
