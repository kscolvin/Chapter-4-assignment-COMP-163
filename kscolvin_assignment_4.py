# Assignment 4: College Life Adventure Game !

"""
COMP 163 - Introduction to Programming
Assignment: Chapter 4 - College Life Adventure Game
Name: Kennedi Colvin
GitHub Username: Kscolvin
Date: 02.09.2026
Description: This is a simple adventure game where the player navigates through college life. The player will make choices that affect the outcome of the game, including their GPA, stress levels, and social points. The game has multiple endings based on the player's decisions throughout the semester.
AI Usage: I used AI to help debug and improve the code after testing it, as well as improving my answer replies. (I added my own charm still!)
"""


# ========================================

# Part 1 : Introduction and Character Stats
# This is a simple adventure game where the player navigates through college life. The player will make choices that affect the outcome of the game.

student_name = "Kennedi Colvin" # Characters name.
current_gpa = 3.0 # Staring GPA. It will affect the ending of the game.
study_hours = 0 # Starting study hours available to the player.
social_points = 50 # Starting social points. It will affect the player's ability to manage stress.
stress_level = 40 # Starting stress level. It will affect the player's ability to make certain choices and will also affect the ending of the game.

print(f"Welcome to College Life, {student_name}!")
print("You are a college student trying to balance your academics and social life. These are your current stats:")
print("Your current GPA is:", current_gpa)
print("You have", study_hours, "hours of study time available.")
print("Your social points are:", social_points)
print("Your stress level is:", stress_level)


# ========================================
# ========================================

# Part 2 : Course Planning Decision
# The player will be presented with choices to manage their time and stress levels. The choices will affect study hours and stress levels.

print("Course Load Decision: Light / Standard / Heavy")
course_load = input("Choose your workload!: ") 

if course_load == "Light":
    study_hours = study_hours + 5
    stress_level = stress_level + 10
    print("You chose a light course load. You don't study as much and have less stress!") # Choosing a light load improves study time and increases stress level slightly because you might feel like you're not doing enough.
elif course_load == "Standard":
    study_hours = study_hours + 10
    stress_level = stress_level + 20
    print("You chose a standard course load. Your study hours and stress level increase. It's getting serious!") # Choosing a standard load improves study time and increases stress level moderately.
elif course_load == "Heavy":
    study_hours = study_hours + 20
    stress_level = stress_level + 30
    print("You chose a heavy course load. You have to study longer and your stress increases!") # Choosing a heavy load improves study time significantly but also increases stress level significantly because it's a lot of work.
elif course_load != "Light" and course_load != "Standard" and course_load != "Heavy":
    print("Invalid choice. Please choose 'Light', 'Standard', or 'Heavy'.")
else:
    print("Invalid GPA. Please choose 'Light', 'Standard', or 'Heavy'.")

# Show Stats !
print()
print("Your current GPA is:", current_gpa)
print("Your current study hours are:", study_hours)
print("Your current stress level is:", stress_level)


# ========================================
# ========================================

# Part 3 : Study Strategy Decision
# The player will choose a study strategy that affects their GPA and stress levels.

study_options = ["Group Study", "Solo Study", "Tutoring", "Not Study"]
print("Study Strategy Decision: Group Study / Solo Study / Tutoring / Not Study")
study_strategy = input("Choose your study strategy!: ")

# The following code will determine the effects of the chosen study strategy on GPA and stress levels.
if study_strategy not in study_options:
    print("Invalid choice. Please choose 'Group Study', 'Solo Study', 'Tutoring', or 'Not Study'.")

else: 
    if study_strategy == "Group Study" and stress_level > 30 and social_points >= 10:
        current_gpa = current_gpa + 0.2
        stress_level = stress_level + 10
        study_hours = study_hours + 5
        social_points = social_points - 10
        print("You chose Group Study. Your GPA increases and your stress level increases because your socially anxious!") # Group study is productive. Improves stats but as an introvert, adds stress lol!
    elif study_strategy == "Solo Study" and stress_level >= 50:
        current_gpa = current_gpa + 0.1
        stress_level = stress_level + 5
        study_hours = study_hours + 5
        social_points = social_points +5 
        print("You chose Solo Study. Your GPA increases slightly but your stress level increases due to isolation.") # Solo study is productive but can be isolating, you don't always trust yourself to teach, which adds stress.
    elif study_strategy == "Tutoring" and (current_gpa < 3.0 or stress_level > 60):
        current_gpa = current_gpa + 0.3
        stress_level = stress_level - 15
        study_hours = study_hours + 3
        social_points = social_points - 5
        print("You chose Tutoring. Your GPA increases significantly and your stress level decreases. You had a good tutor!") # Tutoring is very productive, it improves GPA significantly and reduces stress because you have someone to help you.
    elif study_strategy == "Not Study":
        current_gpa = current_gpa - 1.0
        stress_level = stress_level + 20
        study_hours = study_hours + 0
        social_points = social_points + 0
        print("You chose Not Study. Your GPA decreases and your stress level increases.") # Not studying is detrimental, it decreases GPA and increases stress level significantly because you're not preparing for the exam.
    else:
        print("This study strategy had no effect.")

# Show stats !
print()
print("Your current GPA is:", current_gpa)
print("Your current stress level is:", stress_level)
print("Your current social points are:", social_points)
print("Your current study hours are:", study_hours)


# ========================================
# ========================================

# Part 4 : Multiple Endings Setup
print("\nBased on your final stats...")

if type(current_gpa) is not float or type(stress_level) is not int or type(study_hours) is not int:
    print("Error: Invalid data types for GPA, stress level, or study hours. Please check your inputs and try again.")

# Determine Ending
if current_gpa >= 3.5:
    if stress_level <= 60 and study_hours >= 25:
            print("Congratulations! You got the STUDIOUS ending! You've successfully completed the semester with a high GPA and low stress.") # Best ending because you pass the semester and you have low stress. No burnout!
    else:
            print("You got the SUCCESSFUL ending! You've completed the semester with a high GPA, but your stress levels were a bit high. Try to manage your stress better next time!") # You pass the semester but you're burnt out.
elif current_gpa >= 3.0:
    if stress_level < 50 and study_hours >= 20:
            print("Congratulations! You got the BALANCED ending! You've completed the semester with a decent GPA and manageable stress levels. Keep up the good work!") # A good outcome. Very balanced all levels are normal but not extraordinary.
    else:
            print("You got the AVERAGE ending! You've completed the semester with an average GPA and stress levels. Try to improve next time!") # You pass the semester but your stress levels are high or your study hours are low, which is not ideal.
elif current_gpa < 2.5: 
    if stress_level >= 70:
        print("Unfortunately, You got the WORST ending! Your GPA is too low to pass the semester and you're stressed out. Better luck next time!") # You failed the semester and you're very stressed out, which is the worst outcome.
    else:
        print("You got the STRUGGLING ending. Your GPA is low, but your stress levels are manageable. Try to improve your GPA next time!") # You failed the semester but at least you're not stressed out, which is better ig.
else:
    print("You got the FAILURE ending. Your GPA and stress levels are in a gray area. Try to improve both next time!") # You are in a gray area, you didn't fail but you didn't do well either.

# ========================================

