from constraint import *

if __name__ == '__main__':

    bands = dict()

    band_info = input()
    while band_info != 'end':
        band, genre, duration = band_info.split(' ')
        bands[band] = (genre, duration)
        band_info = input()

    # Add the variables here
    variables = list(bands.keys())

    domain = [f'S{i + 1}' for i in range(3)]

    problem = Problem(BacktrackingSolver())

    # Change this section if necessary
    problem.addVariables(variables, domain)

    # Add the constraints here

    # Constraint 1: Each stage may have at most one performance of 120 minutes
    for stage in domain:
        def max_one_120(*assignments, s=stage):
            count_120 = sum(1 for i, band in enumerate(variables)
                            if assignments[i] == s and bands[band][1] == '120')
            return count_120 <= 1


        problem.addConstraint(max_one_120, variables)

    # Constraint 2: Each stage may have at most 5 bands whose duration is less than 80 minutes
    for stage in domain:
        def max_five_under_80(*assignments, s=stage):
            count_under_80 = sum(1 for i, band in enumerate(variables)
                                 if assignments[i] == s and int(bands[band][1]) < 80)
            return count_under_80 <= 5


        problem.addConstraint(max_five_under_80, variables)

    # Constraint 3: If total performance time of bands from same genre <= 300 minutes,
    # then those bands must perform on the same stage
    genre_groups = {}
    for band, (genre, duration) in bands.items():
        if genre not in genre_groups:
            genre_groups[genre] = []
        genre_groups[genre].append(band)

    for genre, genre_bands in genre_groups.items():
        total_duration = sum(int(bands[band][1]) for band in genre_bands)
        if total_duration <= 300:
            # All bands from this genre must be on the same stage
            if len(genre_bands) > 1:
                problem.addConstraint(AllEqualConstraint(), genre_bands)

    result = problem.getSolution()

    # Add the printing section here
    if result:
        for band in variables:
            print(f"{band} (('{bands[band][0]}', '{bands[band][1]}')): {result[band]}")