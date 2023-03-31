""" 
GPT-4 PROMPT:
can you refactor the schedule to a multi day event with similar timeslots?
"""
from ortools.sat.python import cp_model
import datetime

# Dummy talks with dummy speakers and dummy tracks
talks = [
    ('Talk 1', 'Speaker 1', 'Java', 100),
    ('Talk 2', 'Speaker 2', 'AI', 400),
    ('Talk 3', 'Speaker 3', 'Security', 600),
    ('Talk 4', 'Speaker 4', 'Culture', 10),
    ('Talk 5', 'Speaker 5', 'Server Side Java', 1000),
    ('Talk 6', 'Speaker 6', 'Java', 900),
    ('Talk 7', 'Speaker 7', 'AI', 666),
    ('Talk 8', 'Speaker 8', 'Security', 42),
    ('Talk 9', 'Speaker 9', 'Security', 142),
    ('Talk 10', 'Speaker 9', 'Server Side Java', 90),

    ('Talk 11', 'Speaker 12', 'Java', 0),
    ('Talk 12', 'Speaker 13', 'AI', 10),
    ('Talk 13', 'Speaker 14', 'Security', 20),
    ('Talk 14', 'Speaker 15', 'Culture', 30),
    ('Talk 15', 'Speaker 16', 'Server Side Java', 500),
    ('Talk 16', 'Speaker 17', 'Java', 900),
    ('Talk 17', 'Speaker 18', 'AI', 400),
    ('Talk 18', 'Speaker 19', 'Security', 20),
    ('Talk 19', 'Speaker 20', 'Culture', 30),
    ('Talk 20', 'Speaker 21', 'Server Side Java', 400),

    ('Talk 21', 'Speaker 22', 'Java', 200),
    ('Talk 22', 'Speaker 23', 'AI', 10),
    ('Talk 23', 'Speaker 24', 'Security', 20),
    ('Talk 24', 'Speaker 25', 'Culture', 30),
    ('Talk 25', 'Speaker 26', 'Server Side Java', 100),
    ('Talk 26', 'Speaker 27', 'Java', 500),
    ('Talk 27', 'Speaker 28', 'AI', 10),
    ('Talk 28', 'Speaker 1', 'Security', 10),
    ('Talk 29', 'Speaker 1', 'Culture', 1),
    ('Talk 30', 'Speaker 2', 'Culture', 100),
    
    ('Talk 31', 'Speaker 3', 'Java', 550),
    ('Talk 32', 'Speaker 3', 'Java', 777)
]

tracks = {'Java': 2, 'AI': 2, 'Security': 2, 'Culture': 1, 'Server Side Java': 1}

rooms = {
    'Room 1': 600,
    'Room 2': 400,
    'Room 3': 200,
    'Room 4': 100
}

# # Time slots
time_slots = [
    ('D1_09:00', 'D1_09:50'),
    ('D1_10:00', 'D1_10:50'),
    ('D1_11:00', 'D1_11:50'),
    ('D1_12:00', 'D1_12:50'),
    ('D1_14:00', 'D1_14:50'),
    ('D1_15:00', 'D1_15:50'),
    ('D1_16:00', 'D1_16:50'),
    ('D1_17:00', 'D1_17:50'),

    ('D2_09:00', 'D2_09:50'),
    ('D2_10:00', 'D2_10:50'),
    ('D2_11:00', 'D2_11:50'),
    ('D2_12:00', 'D2_12:50'),
    ('D2_14:00', 'D2_14:50'),
    ('D2_15:00', 'D2_15:50'),
    ('D2_16:00', 'D2_16:50'),
    ('D2_17:00', 'D2_17:50'),
]

model = cp_model.CpModel()

talk_vars = {}
for talk in talks:
    for room, capacity in rooms.items():
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

# Constraint: A speaker doesn't give two talks at the same time
# and ensure at least one time slot break between talks
for speaker in set(talk[1] for talk in talks):
    speaker_talks = [talk for talk in talks if talk[1] == speaker]
    for idx, time_slot in enumerate(time_slots[:-1]):
        next_time_slot = time_slots[idx + 1]
        model.Add(
            sum(
                talk_vars[(talk, room, time_slot)] + talk_vars[(talk, room, next_time_slot)]
                for talk in speaker_talks for room in rooms
            ) <= 1
        )

    # Ensure at least one time slot break between talks by the same speaker
    for idx, time_slot in enumerate(time_slots[:-2]):
        next_time_slot = time_slots[idx + 1]
        third_time_slot = time_slots[idx + 2]
        model.Add(
            sum(
                talk_vars[(talk, room, time_slot)] + talk_vars[(talk, room, third_time_slot)]
                for talk in speaker_talks for room in rooms
            ) <= 1
        )


# Constraint: Favs are respected and schedule in bigger rooms
# Define a cost function that penalizes less popular talks in bigger rooms
costs = []
for talk in talks:
    for room, capacity in rooms.items():
        for time_slot in time_slots:
            cost = (talk[3] / capacity) * talk_vars[(talk, room, time_slot)]
            costs.append(cost)

# Minimize the cost function
model.Minimize(sum(costs))

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print("Optimal schedule:")
    for time_slot in time_slots:
        print(f"{time_slot}")
        for room, capacity in rooms.items():
            for talk in talks:
                if solver.Value(talk_vars[(talk, room, time_slot)]) == 1:
                    print(f"{room} (Capacity: {capacity}): {talk[0]} by {talk[1]} ({talk[2]} track) - {talk[3]} favorites")
        print()
else:
    print("No optimal schedule found.")
