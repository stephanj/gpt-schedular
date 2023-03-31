from ortools.sat.python import cp_model

class ConferenceScheduling:
    def __init__(self, talks):
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

        self.talks = talks

    def create_speakers(self, num_speakers, speaker_availability):
        self.speakers = range(num_speakers)
        self.speaker_availability = speaker_availability

    def create_talks(self, talks):
        self.talks = talks

    def create_rooms(self, room_capacities):
        self.room_capacities = room_capacities
        self.rooms = range(len(room_capacities))

    def create_schedule(self, days, start_time, end_time, lunch_break_duration):
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.lunch_break_duration = lunch_break_duration

    def optimize_schedule(self):
        # Create variables
        self.schedule_vars = {}
        
        for talk in self.talks:
            for day in self.days:
                for room in self.rooms:
                    for time in range(self.start_time, self.end_time - talk['duration'] + 1):
                        var_name = f'talk_{talk["id"]}_day_{day}_room_{room}_time_{time}'
                        var = self.model.NewBoolVar(var_name)
                        self.schedule_vars[(talk['id'], day, room, time)] = var

        # Constraint 1: Speaker availability
        # for talk in self.talks:
        #     speaker_availability = self.speaker_availability[talk['speaker_id']]
        #     self.model.Add(sum(self.schedule_vars[(talk['id'], day, room, time)] for day, available in enumerate(speaker_availability) if available for room in self.rooms for time in range(self.start_time, self.end_time - talk['duration'] + 1)) == 1)

        # # Constraint 2: Track constraints
        # for i, talk1 in enumerate(self.talks):
        #     for j, talk2 in enumerate(self.talks):
        #         if i < j and talk1['track'] == talk2['track']:
        #             for day in self.days:
        #                 for room in self.rooms:
        #                     for time in range(self.start_time, self.end_time - max(talk1['duration'], talk2['duration']) + 1):
        #                         self.model.AddBoolOr([
        #                             self.schedule_vars[(talk1['id'], day, room, time)] == 0,
        #                             self.schedule_vars[(talk2['id'], day, room, time)] == 0
        #                         ])


    def solve(self):
        self.status = self.solver.Solve(self.model)
        return self.status

    def print_schedule(self):
        if self.status == cp_model.OPTIMAL:
            for day in self.days:
                print(f"Day {day + 1}:")
                for room in self.rooms:
                    print(f"  Room {room + 1}:")
                    for talk in self.talks:
                        for time in range(self.start_time, self.end_time - talk['duration'] + 1):
                            if self.solver.Value(self.schedule_vars[(talk['id'], day, room, time)]) == 1:
                                print(f"    {time:02d}:00 - {time + talk['duration']:02d}:00: Talk {talk['id']} (Speaker {talk['speaker_id']}, Track {talk['track']}, Favorites {talk['favorites']})")
        else:
            print("No solution found.")

if __name__ == "__main__":

    # Example: Define the conference parameters (talks, speakers, rooms, etc.)
    # speaker_availability = [
    #     [True, True, True, True, True] for _ in range(220)
    # ]

    speaker_availability = [
        [True, True, True, False, False],  # Speaker 0 is available on Monday, Tuesday, and Wednesday
        [False, True, True, True, False],  # Speaker 1 is available on Tuesday, Wednesday, and Thursday
        [False, True, True, True, False],  # Speaker 2 is available on Tuesday, Wednesday, and Thursday
        [False, True, True, True, False],  # Speaker 3 is available on Tuesday, Wednesday, and Thursday
        [False, True, True, True, False],  # Speaker 4 is available on Tuesday, Wednesday, and Thursday
        [False, True, True, True, False],  # Speaker 5 is available on Tuesday, Wednesday, and Thursday
        [False, True, True, True, False],  # Speaker 6 is available on Tuesday, Wednesday, and Thursday
        [False, True, True, True, False],  # Speaker 7 is available on Tuesday, Wednesday, and Thursday
        [True, True, True, True, True],  # Speaker 8 is available on all days
        [True, True, True, True, True],  # Speaker 9 is available on all days
        [True, True, True, True, True],  # Speaker 10 is available on all days
        [True, True, True, True, True],  # Speaker 11 is available on all days
        [True, True, True, True, True],  # Speaker 12 is available on all days
        [True, True, True, True, True],  # Speaker 13 is available on all days
        [True, True, True, True, True],  # Speaker 14 is available on all days
        [True, True, True, True, True],  # Speaker 15 is available on all days
        [True, True, True, True, True],  # Speaker 16 is available on all days
        [True, True, True, True, True],  # Speaker 17 is available on all days
        [True, True, True, True, True],  # Speaker 18 is available on all days
        [True, True, True, True, True]   # Speaker 19 is available on all days
    ]


    # talks = [
    #     {'id': i, 'speaker_id': i % 220, 'duration': 50 if i % 10 == 0 else 180, 'track': i % 5, 'favorites': i % 10}
    #     for i in range(226)
    # ]

    talks = [
        {"title": "Talk 1", "speaker_id": 0, "duration": 180, "track": 0, "favorites": 120},
        {"title": "Talk 2", "speaker_id": 1, "duration": 180, "track": 1, "favorites": 80},
        {"title": "Talk 3", "speaker_id": 2, "duration": 180, "track": 2, "favorites": 200},
        {"title": "Talk 4", "speaker_id": 3, "duration": 180, "track": 0, "favorites": 50},
        {"title": "Talk 5", "speaker_id": 4, "duration": 180, "track": 1, "favorites": 30},
        {"title": "Talk 6", "speaker_id": 5, "duration": 50, "track": 0, "favorites": 100},
        {"title": "Talk 7", "speaker_id": 6, "duration": 50, "track": 2, "favorites": 400},
        {"title": "Talk 8", "speaker_id": 7, "duration": 50, "track": 1, "favorites": 300},
        {"title": "Talk 9", "speaker_id": 8, "duration": 50, "track": 0, "favorites": 10},
        {"title": "Talk 10", "speaker_id": 9, "duration": 50, "track": 2, "favorites": 20},
        {"title": "Talk 11", "speaker_id": 10, "duration": 50, "track": 3, "favorites": 20},
        {"title": "Talk 12", "speaker_id": 11, "duration": 50, "track": 3, "favorites": 2},
        {"title": "Talk 13", "speaker_id": 12, "duration": 50, "track": 3, "favorites": 20},
        {"title": "Talk 14", "speaker_id": 13, "duration": 50, "track": 3, "favorites": 320},
        {"title": "Talk 15", "speaker_id": 14, "duration": 50, "track": 4, "favorites": 120},
        {"title": "Talk 16", "speaker_id": 15, "duration": 50, "track": 4, "favorites": 520},
        {"title": "Talk 17", "speaker_id": 16, "duration": 50, "track": 4, "favorites": 20},
        {"title": "Talk 18", "speaker_id": 17, "duration": 50, "track": 5, "favorites": 90},
        {"title": "Talk 19", "speaker_id": 18, "duration": 50, "track": 5, "favorites": 20},
        {"title": "Talk 20", "speaker_id": 19, "duration": 50, "track": 5, "favorites": 220}
    ]

    room_capacities = [200, 200, 400, 400, 400, 400, 800, 800]

    days = range(5)
    start_time = 9
    end_time = 20
    lunch_break_duration = 1

    conference = ConferenceScheduling(talks=talks)

    conference.create_speakers(20, speaker_availability)
    conference.create_rooms(room_capacities)
    conference.create_schedule(days, start_time, end_time, lunch_break_duration)
    conference.optimize_schedule()

    if conference.solve() == cp_model.OPTIMAL:
        conference.print_schedule()
    else:
        print("No solution found.")
