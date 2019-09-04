# Freshservice Ticket Update

Freshservice is a Python script that is used to update the due date of new-hire tickets to match the start date of the new hire and notate in the previous due date in the ticket.

## Description

Freshservice will run regularly to check all new-hire related tickets associated with the "Onboarding" group that have been updated in the last hour and it will update the due date of the ticket to be the start date of the new-hire as per the information provided by the HR team within the ticket. It will also add a public note containing the previous due date of the ticket.

## Installation

Install the dependencies in the requirements.txt.

```bash
pip install -r requirements.txt
```

## Usage

```python
python3 freshservice.py
```
