"""
GPT-4 PROMPT:
Can you create an example python app which creates an optimal schedule for a one day event?
The event has 4 rooms and the talks are 50 minutes with 10 minutes breaks in between.
Event starts at 9h00 until 18h00 and has a one hour lunch break and two coffee breaks of 30 minutes. 
Create dummy talks with dummy speakers.  Each talk must be scheduled once.
"""
from ortools.sat.python import cp_model
import datetime

# Dummy talks with dummy speakers
talks = [
    ('Talk 1', 'Speaker 1'),
    ('Talk 2', 'Speaker 2'),
    ('Talk 3', 'Speaker 3'),
    ('Talk 4', 'Speaker 4'),
    ('Talk 5', 'Speaker 5'),
    ('Talk 6', 'Speaker 6'),
    ('Talk 7', 'Speaker 7'),
    ('Talk 8', 'Speaker 8'),
    ('Talk 9', 'Speaker 9'),
    ('Talk 10', 'Speaker 11'),

    ('Talk 11', 'Speaker 12'),
    ('Talk 12', 'Speaker 13'),
    ('Talk 13', 'Speaker 14'),
    ('Talk 14', 'Speaker 15'),
    ('Talk 15', 'Speaker 16'),
    ('Talk 16', 'Speaker 17'),
    ('Talk 17', 'Speaker 18'),
    ('Talk 18', 'Speaker 19'),
    ('Talk 19', 'Speaker 20'),
    ('Talk 20', 'Speaker 21'),

    ('Talk 21', 'Speaker 22'),
    ('Talk 22', 'Speaker 23'),
    ('Talk 23', 'Speaker 24'),
    ('Talk 24', 'Speaker 25'),
    ('Talk 25', 'Speaker 26'),
    ('Talk 26', 'Speaker 27'),
    ('Talk 27', 'Speaker 28'),
    ('Talk 28', 'Speaker 29'),
    ('Talk 29', 'Speaker 30'),
]

rooms = ['Room 1', 'Room 2', 'Room 3', 'Room 4']

# Time slots
time_slots = [
    ('09:00', '09:50'),
    ('10:00', '10:50'),
    ('11:00', '11:50'),
    ('12:00', '12:50'),
    ('14:00', '14:50'),
    ('15:00', '15:50'),
    ('16:00', '16:50'),
    ('17:00', '17:50'),
]

# Create the model
model = cp_model.CpModel()

# Create variables
talk_vars = {}
for talk in talks:
    for room in rooms:
        for idx, time_slot in enumerate(time_slots):
            var = model.NewBoolVar(f'{talk[0]}_{room}_{time_slot}')
            talk_vars[(talk, room, time_slot)] = var

# Each talk must be scheduled once
for talk in talks:
    model.Add(sum(talk_vars[(talk, room, time_slot)] for room in rooms for time_slot in time_slots) == 1)

# No overlapping talks in the same room
for room in rooms:
    for time_slot in time_slots:
        model.Add(sum(talk_vars[(talk, room, time_slot)] for talk in talks) <= 1)

# Solve the model
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Print the result
if status == cp_model.OPTIMAL:
    print("Optimal schedule:")
    for time_slot in time_slots:
        print(f"{time_slot[0]} - {time_slot[1]}")
        for room in rooms:
            for talk in talks:
                if solver.Value(talk_vars[(talk, room, time_slot)]) == 1:
                    print(f"{room}: {talk[0]} by {talk[1]}")
        print()
else:
    print("No optimal schedule found.")
