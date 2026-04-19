from constraint import *
if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    movies = dict()

    n = int(input())
    for _ in range(n):
        film_info = input()
        film, genre, time = film_info.split(' ')
        movies[film] = (float(time), genre)

    l_days = int(input())

    # Tuka definirajte gi promenlivite i domenite
    days = range(1, l_days + 1)
    hours = range(12, 24)
    cinemas = [1, 2]

    for film in movies:
        problem.addVariable(film, [(d, h, c) for d in days for h in hours for c in cinemas])
    # Tuka dodadete gi ogranichuvanjata
    for film, (duration, genre) in movies.items():
        if genre == "children's":
            problem.addConstraint(lambda x, dur=duration: x[1] <= 18, [film])


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

    genre_groups = {}
    for film, (duration, genre) in movies.items():
        if genre in ["sci-fi", "horror", "action"]:
            genre_groups.setdefault(genre, []).append(film)

    for genre, films in genre_groups.items():
        problem.addConstraint(lambda *args: len(set(x[2] for x in args)) == 1, films)

    result = problem.getSolution()

    # Tuka dodadete go kodot za pechatenje
    if result:
        # pick solution with latest possible start times
        #best = max(result, key=lambda sol: sum(sol[f][1] for f in movies))
        for film in movies:
            day, hour, cinema = result[film]
            print(f"{film}: Day {day} {hour}:00 - Cinema {cinema}")
    else:
        print("No Solution!")
