# Freshservice Ticket Update

freshservice.py is a Python script that is used to update the due date of new-hire tickets to match the start date of the new hire and notate in the previous due date in the ticket within the Freshservice ticketing system.

### Description

freshservice.py will run regularly to check all new-hire related tickets associated with the "Onboarding" group that have been updated in the last hour and it will update the due date of the ticket to be the start date of the new-hire as per the information provided by the HR team within the ticket. It will also add a public note containing the previous due date of the ticket. If the ticket has already been updated it will not update the ticket and report that the ticket has already been updated.

### Installation

Install the dependencies in the requirements.txt.

```bash
pip install -r requirements.txt
```

### Usage

```python
python3 freshservice.py
```

### Usage Example

```
python3 freshservice.py
INFO:root:Script run on: 2019-09-04 11:58:56.983343
Got list of all new hire tickets.
Added note on ticket - Ticket ID: 6
Added note on ticket - Ticket ID: 5
Ticket 4 already updated
Update due date for new hire ticket - Ticket ID: 5
Update due date for new hire ticket - Ticket ID: 6

python3 freshservice.py
INFO:root:Script run on: 2019-09-04 11:58:43.476274
Got list of all new hire tickets.
Ticket 6 already updated.
Ticket 5 already updated.
Ticket 4 already updated.
```
