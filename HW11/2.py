import sys

def calculate_gpa(grades):
    total_grades = sum(grades)
    num_grades = len(grades)
    gpa = total_grades / num_grades
    return gpa

