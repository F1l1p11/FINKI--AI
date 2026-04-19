from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    # Add the domains
    # Attendance variables: 1 if person attends, 0 if not
    problem.addVariable("Marija_attendance", [0, 1])
    problem.addVariable("Simona_attendance", [0, 1])
    problem.addVariable("Petar_attendance", [0, 1])

    # Time slots: 12, 13, 14, 15, 16, 17, 18, 19 (start times for 1-hour meetings)
    problem.addVariable("time_meeting", [12, 13, 14, 15, 16, 17, 18, 19])

    # Constraint 1: Simona must attend (she's the manager)
    problem.addConstraint(lambda s: s == 1, ["Simona_attendance"])

    # Constraint 2: At least one other person must attend with Simona
    problem.addConstraint(
        lambda m, p: m + p >= 1,
        ["Marija_attendance", "Petar_attendance"]
    )

    # Constraint 3: Simona's availability
    # Simona available: 13:00-15:00 (13, 14), 16:00-17:00 (16), 19:00-20:00 (19)
    problem.addConstraint(
        lambda t, s: s == 0 or t in [13, 14, 16, 19],
        ["time_meeting", "Simona_attendance"]
    )

    # Constraint 4: Maria's availability
    # Maria available: 14:00-16:00 (14, 15), 18:00-19:00 (18)
    problem.addConstraint(
        lambda t, m: m == 0 or t in [14, 15, 18],
        ["time_meeting", "Marija_attendance"]
    )

    # Constraint 5: Petar's availability
    # Petar available: 12:00-14:00 (12, 13), 16:00-20:00 (16, 17, 18, 19)
    problem.addConstraint(
        lambda t, p: p == 0 or t in [12, 13, 16, 17, 18, 19],
        ["time_meeting", "Petar_attendance"]
    )

    # [print(solution) for solution in problem.getSolutions()]
    for i in [14,19,16,13]:
        for solution in problem.getSolutions():
            if solution["time_meeting"] == i:
                ordered = {
                    "Simona_attendance": solution["Simona_attendance"],
                    "Marija_attendance": solution["Marija_attendance"],
                    "Petar_attendance": solution["Petar_attendance"],
                    "time_meeting": solution["time_meeting"]
                }
                print(ordered)