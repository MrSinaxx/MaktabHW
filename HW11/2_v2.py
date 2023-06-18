import argparse

def calculate_gpa(grades):
    total_grades = sum(grades)
    num_grades = len(grades)
    gpa = total_grades / num_grades
    return gpa

def main():
    parser = argparse.ArgumentParser(description='Calculate GPA')
    parser.add_argument('-g', '--grades', nargs='+', type=float, help='list of grades')
    parser.add_argument('-f', '--float', type=int, default=2, help='number of decimal places')
    args = parser.parse_args()

    grades = args.grades
    gpa = calculate_gpa(grades)

    float_format = '{:.' + str(args.float) + 'f}'
    formatted_gpa = float_format.format(gpa)
    print(formatted_gpa)

if __name__ == '__main__':
    main()