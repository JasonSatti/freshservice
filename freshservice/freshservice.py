#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
freshservice - Used to update the due date of new-hire tickets to match
the start date of the new hire and notate the previous due date in the ticket.
"""
import requests
import json
from datetime import datetime, timedelta
import logging
from config import BASE_URL, AUTH


def setup_logger():
    """Sets up a logger for error reporting."""
    now = datetime.now()
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.info(f"Scrip run on: {now}")


def get_group_id():
    """This function would be used to return the group ID of the group with
    the name onboarding. I do not have the privileges to use that API call.

    For my purposes case I queried all the tickets and I can see the new hire
    tickets use the group_id: 15000022833

    API Docs: https://api.freshservice.com/v2/#view_all_group
    Note: Only users with "Play God with Super Admin controls" privilege can
    access the following APIs.
    """
    url = f"{BASE_URL}/api/v2/tickets/api/v2/groups"
    headers = {"AUTHorization": f"Basic {AUTH}"}
    r = requests.get(url, headers=headers)
    if r.ok:
        print('Got group ID for "Onboarding" Group')
    else:
        logging.debug(f"Error - {r.status_code} - {r.content}")
    groups = r.json()
    for group in groups:
        if group["name"] == "Onboarding":
            group_id = group["id"]

    return group_id


def add_ticket_note(ticket_id, due_date):
    """Add a public note containing the due date before updating.

    :param ticket_id: provided via get_newhire_tickets()
    :param due_date: provided via get_newhire_tickets()
    """
    url = f"{BASE_URL}/api/v2/tickets/{ticket_id}/notes"
    headers = {"AUTHorization": f"Basic {AUTH}", "Content-Type": "application/json"}
    data = {"body": f"Past due date: {due_date}", "private": False}

    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.ok:
        print(f"Added note on ticket - Ticket ID: {ticket_id}")
    else:
        logging.debug(f"Error - {r.status_code} - {r.content}")


def get_newhire_tickets(group_id):
    """Get a list of all new hire related tickets that have been updated in
    the last hour and add a note stating the current due date.

    :param group_id: group id for agent group
    :return: Set of all new hire ticket ids
    """
    url = f"{BASE_URL}/api/v2/tickets"
    headers = {"AUTHorization": f"Basic {AUTH}"}
    r = requests.get(url, headers=headers)
    if r.ok:
        print(f"Got list of all new hire tickets.")
    else:
        logging.debug(f"Error - {r.status_code} - {r.content}")
    tickets = r.json()["tickets"]
    ticket_ids = set()
    last_hour = datetime.now() - timedelta(hours=1)

    for ticket in tickets:
        update_time = datetime.strptime(ticket["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
        # Check for tickets modified in the last hour
        if update_time > last_hour:
            # Verify the subject and group are related to New Hire Onboarding
            if "New Hire" in ticket["subject"] and ticket["group_id"] == group_id:
                start_date = get_start_date(ticket["id"])
                # Check to see if ticket due date was already updated
                if start_date == ticket["due_by"][0:10]:
                    print(f'Ticket {ticket["id"]} already updated')
                else:
                    ticket_ids.add(ticket["id"])
                    add_ticket_note(ticket["id"], ticket["due_by"][0:10])

    return ticket_ids


def get_start_date(ticket_id):
    """Get start date of new employee from ticket.

    :param ticket_id: provided via get_newhire_tickets()
    :return: Str of new hire start date
    """
    url = f"{BASE_URL}/api/v2/tickets/{ticket_id}/requested_items.json"
    headers = {"AUTHorization": f"Basic {AUTH}"}
    ticket_info = requests.get(url, headers=headers)
    if not ticket_info.ok:
        logging.debug(f"Error - {ticket_info.status_code} - {ticket_info.content}")
    else:
        # print(f"Got start date for new hire - Ticket ID: {ticket_id}")
        # Disabled in prod; leave this for debugging purposes
        custom_fields = ticket_info.json()[0]["custom_fields"]

    for field in custom_fields:
        if field["label"] == "Start Date":
            start_date = field["value"]
            start_date = start_date[0:10]  # Keep only date values

    return start_date


def update_ticket_info(ticket_id):
    """Update new hire ticket due date to be the start date of the new hire.

    :param ticket_id: provided via get_newhire_tickets()
    """
    start_date = get_start_date(ticket_id)
    url = f"{BASE_URL}/helpdesk/tickets/{ticket_id}.json"
    headers = {"AUTHorization": f"Basic {AUTH}", "Content-Type": "application/json"}
    data = '{ "helpdesk_ticket":{ "due_by":"{%s}","frDueBy":"%s"}}' % (
        start_date,
        start_date,
    )

    r = requests.put(url, headers=headers, data=data)
    if r.ok:
        print(f"Update due date for new hire ticket - Ticket ID: {ticket_id}")
    else:
        logging.debug(f"Error - {r.status_code} - {r.content}")


def main():
    """Retrieve all new-hire tickets modified in the last hour.
    Add a note to the ticket containing the current due date.
    Modify the due date to be the start date of the new-hire.
    """
    # group_id = get_group_id() This would be used if I had
    # the appropriate privileges
    group_id = 15000022833
    setup_logger()
    ticket_ids = get_newhire_tickets(group_id)
    for ticket_id in ticket_ids:
        update_ticket_info(ticket_id)


if __name__ == "__main__":
    main()
