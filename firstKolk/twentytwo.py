from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    lecture_slots_AI = int(input())
    lecture_slots_ML = int(input())
    lecture_slots_R = int(input())
    lecture_slots_BI = int(input())

    AI_lectures_domain = ["Mon_11", "Mon_12", "Wed_11", "Wed_12", "Fri_11", "Fri_12"]
    ML_lectures_domain = ["Mon_12", "Mon_13", "Mon_15", "Wed_12", "Wed_13", "Wed_15", "Fri_12", "Fri_13", "Fri_15"]
    R_lectures_domain = ["Mon_10", "Mon_11", "Mon_12", "Mon_13", "Mon_14", "Mon_15", "Wed_10", "Wed_11", "Wed_12",
                         "Wed_13", "Wed_14", "Wed_15", "Fri_10", "Fri_11", "Fri_12", "Fri_13", "Fri_14", "Fri_15"]
    BI_lectures_domain = ["Mon_10", "Mon_11", "Wed_10", "Wed_11", "Fri_10", "Fri_11"]

    AI_exercises_domain = ["Tue_10", "Tue_11", "Tue_12", "Tue_13", "Thu_10", "Thu_11", "Thu_12", "Thu_13"]
    ML_exercises_domain = ["Tue_11", "Tue_13", "Tue_14", "Thu_11", "Thu_13", "Thu_14"]
    BI_exercises_domain = ["Tue_10", "Tue_11", "Thu_10", "Thu_11"]

    # ---Add the variables here--------------------

    # Add lecture variables for each subject
    for i in range(lecture_slots_AI):
        problem.addVariable(f"AI_lecture_{i + 1}", AI_lectures_domain)

    for i in range(lecture_slots_ML):
        problem.addVariable(f"ML_lecture_{i + 1}", ML_lectures_domain)

    for i in range(lecture_slots_R):
        problem.addVariable(f"R_lecture_{i + 1}", R_lectures_domain)

    for i in range(lecture_slots_BI):
        problem.addVariable(f"BI_lecture_{i + 1}", BI_lectures_domain)

    # Add exercise variables (always 1 slot if the subject has exercises)
    # AI, ML, and BI have exercises; Robotics has none
    problem.addVariable("AI_exercises", AI_exercises_domain)
    problem.addVariable("ML_exercises", ML_exercises_domain)
    problem.addVariable("BI_exercises", BI_exercises_domain)

    # ---Add the constraints here----------------

    # Collect all variables for overlap checking
    all_variables = []

    # Collect AI lecture variables
    ai_lectures = [f"AI_lecture_{i + 1}" for i in range(lecture_slots_AI)]
    all_variables.extend(ai_lectures)

    # Collect ML lecture variables
    ml_lectures = [f"ML_lecture_{i + 1}" for i in range(lecture_slots_ML)]
    all_variables.extend(ml_lectures)

    # Collect R lecture variables
    r_lectures = [f"R_lecture_{i + 1}" for i in range(lecture_slots_R)]
    all_variables.extend(r_lectures)

    # Collect BI lecture variables
    bi_lectures = [f"BI_lecture_{i + 1}" for i in range(lecture_slots_BI)]
    all_variables.extend(bi_lectures)

    # Add exercises
    all_variables.extend(["AI_exercises", "ML_exercises", "BI_exercises"])

    # Constraint 1: No time slots may overlap - all classes must be at different times
    problem.addConstraint(AllDifferentConstraint(), all_variables)

    # Constraint 2: Lectures and exercises for Machine Learning must start at different times
    # This means all ML lecture slots must be different from the ML exercise slot
    ml_all = ml_lectures + ["ML_exercises"]
    if len(ml_all) > 1:
        # Extract just the time part (remove day prefix) and ensure they're different
        def ml_different_times(*slots):
            # Get unique time parts (the hour portion after the underscore)
            times = [slot.split('_')[1] for slot in slots]
            # All times must be different
            return len(times) == len(set(times))


        problem.addConstraint(ml_different_times, ml_all)

    # ----------------------------------------------------
    solution = problem.getSolution()

    print(solution)