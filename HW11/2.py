import sys

def calculate_gpa(grades):
    total_grades = sum(grades)
    num_grades = len(grades)
    gpa = total_grades / num_grades
    return gpa

def main():
    grades = [int(grade) for grade in sys.argv[1:]]
    gpa = calculate_gpa(grades)
    print(gpa)

if __name__ == '__main__':
    main()