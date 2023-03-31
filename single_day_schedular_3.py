"""
GPT-4 PROMPT:
Now make sure that no talks with the same track are schedule on the same time!
"""
from ortools.sat.python import cp_model
import datetime

# Dummy talks with dummy speakers and dummy tracks
talks = [
     ('Talk 1', 'Speaker 1', 'Java'),
    ('Talk 2', 'Speaker 2', 'AI'),
    ('Talk 3', 'Speaker 3', 'Security'),
    ('Talk 4', 'Speaker 4', 'Culture'),
    ('Talk 5', 'Speaker 5', 'Server Side Java'),
    ('Talk 6', 'Speaker 6', 'Java'),
    ('Talk 7', 'Speaker 7', 'AI'),
    ('Talk 8', 'Speaker 8', 'Security'),
    ('Talk 10', 'Speaker 11', 'Server Side Java'),

    ('Talk 11', 'Speaker 12', 'Java'),
    ('Talk 12', 'Speaker 13', 'AI'),
    ('Talk 13', 'Speaker 14', 'Security'),
    ('Talk 14', 'Speaker 15', 'Culture'),
    ('Talk 15', 'Speaker 16', 'Server Side Java'),
    ('Talk 16', 'Speaker 17', 'Java'),
    ('Talk 17', 'Speaker 18', 'AI'),
    ('Talk 18', 'Speaker 19', 'Security'),
    ('Talk 19', 'Speaker 20', 'Culture'),
    ('Talk 20', 'Speaker 21', 'Server Side Java'),

    ('Talk 21', 'Speaker 22', 'Java'),
    ('Talk 22', 'Speaker 23', 'AI'),
    ('Talk 23', 'Speaker 24', 'Security'),
    ('Talk 24', 'Speaker 25', 'Culture'),
    ('Talk 25', 'Speaker 26', 'Server Side Java'),
    ('Talk 26', 'Speaker 27', 'Java'),
    ('Talk 27', 'Speaker 28', 'AI'),
    ('Talk 28', 'Speaker 29', 'Security'),
    ('Talk 29', 'Speaker 30', 'Culture')
]

tracks = {'Java': 2, 'AI': 2, 'Security': 2, 'Culture': 1, 'Server Side Java': 1}

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

model = cp_model.CpModel()

talk_vars = {}
for talk in talks:
    for room in rooms:
        for idx, time_slot in enumerate(time_slots):
            var = model.NewBoolVar(f'{talk[0]}_{room}_{time_slot}')
            talk_vars[(talk, room, time_slot)] = var

for talk in talks:
    model.Add(sum(talk_vars[(talk, room, time_slot)] for room in rooms for time_slot in time_slots) == 1)

for room in rooms:
    for time_slot in time_slots:
        model.Add(sum(talk_vars[(talk, room, time_slot)] for talk in talks) <= 1)

# Constraint: No talks with the same track are scheduled at the same time
for track in set(talk[2] for talk in talks):
    track_talks = [talk for talk in talks if talk[2] == track]
    for time_slot in time_slots:
        model.Add(sum(talk_vars[(talk, room, time_slot)] for talk in track_talks for room in rooms) <= 1)

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print("Optimal schedule:")
    for time_slot in time_slots:
        print(f"{time_slot[0]} - {time_slot[1]}")
        for room in rooms:
            for talk in talks:
                if solver.Value(talk_vars[(talk, room, time_slot)]) == 1:
                    print(f"{room}: {talk[0]} by {talk[1]} ({talk[2]} track)")
        print()
else:
    print("No optimal schedule found.")