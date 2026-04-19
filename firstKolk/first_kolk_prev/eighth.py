from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    movies = {}

    n = int(input())
    for _ in range(n):
        film_info = input().split()
        film, genre, duration = film_info[0], film_info[1], float(film_info[2])
        movies[film] = (duration, genre)

    l_days = int(input())

    # -----------------------------------------------------
    # --- Variables and domains ---
    days = range(1, l_days + 1)
    hours = range(12, 24)  # films can start between 12:00 and 23:00
    cinemas = [1, 2]

    for film in movies:
        problem.addVariable(film, [(d, h, c) for d in days for h in hours for c in cinemas])

    # -----------------------------------------------------
    # --- Constraints ---

    # Horror films must start no earlier than 21:00
    for film, (duration, genre) in movies.items():
        if genre == "horror":
            problem.addConstraint(lambda x: x[1] >= 21, [film])

    # All films with duration < 2 hours must be shown on the same day
    short_films = [film for film, (duration, _) in movies.items() if duration < 2]
    if short_films:
        problem.addConstraint(lambda *args: len(set(x[0] for x in args)) == 1, short_films)

    # Films must not overlap or touch in same cinema/day
    def no_overlap(f1, f2, dur1, dur2):
        d1, h1, c1 = f1
        d2, h2, c2 = f2
        if d1 == d2 and c1 == c2:
            end1 = h1 + dur1
            end2 = h2 + dur2
            # require at least 1 hour gap
            if not (end1 + 1 <= h2 or end2 + 1 <= h1):
                return False
        return True

    for f1 in movies:
        for f2 in movies:
            if f1 != f2:
                problem.addConstraint(
                    lambda x, y, dur1=movies[f1][0], dur2=movies[f2][0]: no_overlap(x, y, dur1, dur2),
                    (f1, f2)
                )

    # -----------------------------------------------------
    # --- Solve ---
    result = problem.getSolution()

    # -----------------------------------------------------
    # --- Print result ---
    if result:
        for film in movies:
            day, hour, cinema = result[film]
            print(f"{film}: Day {day} {hour}:00 - Cinema {cinema}")
    else:
        print("No Solution!")
