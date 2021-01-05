'''
Objective:  Generate csv files containing fake data

Using Python, create CSV files for the roster, homework grades and exam, quiz and other
class assignment grades. Dictionary keys and values will be headers and values, respectively,
in CSV files.
'''

import numpy as np
import string
import csv


# Global variables for the number of students and chapters covered in the mock data
num_students = 8
num_chaps = 6


def roster():
    '''Create a CSV file resembling a class roster.

    8 student names are randomly generated along with their ids, academic program of interest
    and email addresses.
    '''
    # Create a list of random names, "Last Name, First Name, Middle Initial (where applicable)"
    # and academic program preferences by randomly selecting from the lists below.

    first = ['Noah', 'Sophia', 'Jacob', 'Mia', 'Ethan', 'Emma', 'Daniel', 'Olivia',
             'Matthew', 'Isabella', 'Camila', 'Michael', 'Charlotte', 'Nathan', 'Samantha',
             'Benjamin', 'Evelyn', 'Anthony', 'Scarlett', 'Isaac', 'Madison', 'Mason',
             'Zoey', 'Isaiah', 'Lily', 'Gabriel', 'Aubrey', 'Ryan', 'Delilah', 'Samuel',
             'Leah', 'Jose', 'Maya', 'Luke', 'Ximena', 'Christian', 'Aaliyah', 'Damian',
             'Layla', 'Jackson', 'Harper', 'Kevin', 'Hannah', 'Dominic', 'Violet', 'Leonardo',
             'Brooklyn', 'Brandon', 'Valentina', 'Caleb', 'Bella', 'Adam', 'Natalia',
             'Diego', 'Naomi', 'Austin', 'Aurora', 'Jeremiah', 'Nicole', 'Roman', 'Katherine',
             'Leo', 'Alice', 'Carter', 'Amy', 'Nathaniel', 'Ariel', 'Xavier', 'Eliana',
             'Vincent', 'Gianna', 'Giovanni', 'Alina', 'Ezra', 'Jocelyn', 'Thomas',
             'Alexandra', 'Hudson', 'Anna', 'Miguel', 'Melody', 'Jaxon', 'Madelyn', 'Ayden',
             'Leilani', 'Nolan', 'Jade', 'Emiliano', 'Liliana', 'Alejandro', 'Lillian',
             'Ryder', 'Angelina', 'Abraham', 'Sophie', 'Melanie', 'Allison', 'Herman']

    middle = list(string.ascii_uppercase)

    last = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Wong', 'Saechao', 'Ng', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzales',
            'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White', 'Harris',
            'Sanchez', 'Clark', 'Dinh', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young',
            'Allen', 'King', 'Wright', 'Chan', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
            'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
            'Carter', 'Roberts', 'Gomez,''Phillips', 'Tsang', 'Evans', 'Turner', 'Diaz', 'Parker',
            'Cruz', 'Cooper', 'Peterson', 'Bailey', 'Ly', 'Reed', 'Kelly', 'Howard', 'Ramos',
            'Kim', 'Cox', 'Ward', 'Richardson', 'Watson', 'Moon', 'Brooks', 'Chavez', 'Wood',
            'Mendoza', 'Ruiz', 'Hughes', 'Price', 'Alvarez', 'Pham', 'Castillo', 'Sanders', 'Saephan'
            'Patel', 'Myers', 'Long', 'Ross', 'Foster', 'Jimenez', 'Singh', 'Castillo', 'Teoh']

    certs = ["NURPRP", "AS.NURS", "AS.MATH", "AST.BUSAD", "AS.BIOSC",
             "AS.COMP", "AA.SPAN", "AS.MEDIC", "AA.LIBST"]

    # Keys for dictionaries for the roster. These will be headers in the csv
    roster_header = ["Student Name", "Student ID",
                     "Academic Program", "Preferred Email"]

    # Initialize lists to populate and zip in key, value pairs
    names, sids, programs, emails, roster_lst = [], [], [], [], []

    # Loop to create lists of some number of students, num_student, and their student id
    # numbers, academic program preferences and email addresses.
    for i in range(num_students):

        # Not all generated students will have a middle initial.
        if (i + 1) % 2 == 0:
            name = f"{np.random.choice(last)}, {np.random.choice(first)}, {np.random.choice(middle)}."

        else:
            name = f"{np.random.choice(last)}, {np.random.choice(first)}"

        names.append(name)

        # Generate SIDs
        sids.append(np.random.randint(100000, 4999999))

        # Randomly select an academic program
        programs.append(np.random.choice(certs))

        # E-mail addresses are derived from student last name and first initial. In all cases,
        # a 3-digit number is added to the end for uniqueness.
        three_digit = np.random.randint(100, 999)
        emails.append(
            f"{name.split(', ')[0]}{name.split()[1][0]}{three_digit}@university.edu".lower())

    # Sort according to last name of the student to create an alphabetized roster. This means
    # that e-mail addresses must also be sorted accordingly.
    sorted_names = sorted(names)
    sorted_emails = sorted(emails)

    # Zip each element in the lists into a dictionary. Each row in the csv file is a dictionary.
    for idx in range(len(sids)):
        row = dict(zip(roster_header, [
                   sorted_names[idx], sids[idx], programs[idx], sorted_emails[idx]]))
        roster_lst.append(row)

    # Save the roster to a csv file
    with open('../data/generated_roster.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=roster_header)
        writer.writeheader()
        for data in roster_lst:
            writer.writerow(data)

    # Return the sorted_names and sids for use in creating homework and overall class grades csvs
    return sorted_names, sids


def assign_score(max_pts, mu, sigma):
    '''Generates an assignment score(random floats > 0).

    This function can be used to create homework, quiz, discussion, laboratory assignments,
    extra credit and exam scores of varying points.

    Keyword arguments:
    max_pts - - int. assignment maximum score
    mu - - float. assignment mean score
    sigma - - float. assignment standard deviation
    '''

    # Randomly generate an assignment score between 0.0 and max_pts
    # Initialize the points
    score = 0.00

    # Assign score of 0 to all reading assignments
    if max_pts == 0.00:
        score = score

    # Assign a score to all non-reading assignments
    else:
        point = round(np.random.normal(mu, sigma), 2)

        # Limit the range of the score to a non-negative value that is less than the max points
        if point > max_pts:
            score = max_pts
        elif point < 0:
            score = score
        else:
            score = point

    return score


def hmwks_xcs():
    '''Create a dictionary of assignment scores.

    This function uses the assign_score function to create a dictionary of scores for
    the reading, homework and extra credit assignments for a single student.
    '''

    # Dictionary storing the max_points, average points and standard deviation for the
    # reading, homework and extra credit assignments
    hmwk_params = {'reading': [0.00, 0.00, 0.00], 'hmwk': [5.00, 4.416, 0.731],
                   'xc': [2.00, 1.647, 0.770]}

    # Initialize lists
    assignments, scores = [], []

    # Create headers for reading, homework and extra credit assignments according to some
    # number of chapters (a global variable)
    for num in range(1, num_chaps + 1):
        assignments.append((f'Chapter {num}: E-BOOK (Not Graded) (10)',
                            f'Chapter {num}: Required (5.0)',
                            f'Chapter {num}: Extra Credit (2.0)'))

    # Function call to create scores for each assignment type for each student
        for v in hmwk_params.values():
            scores.append(assign_score(list(v)[0],
                                       list(v)[1], list(v)[2]))

    # Flatten the list of headers
    headers = [title for sublist in assignments for title in sublist]

    # Create k, v for student name at the beginning of the dict. Third-party program only
    # lists student names along with their scores; the assignment maximum score is not listed
    headers.insert(0, 'Name')
    scores.insert(0, 'temp_name')  # Using 'temp_name' as a placeholder

    return dict(zip(headers, scores))


def hmwk_to_csv():
    '''Creates a list of dictionaries where keys are headers and values are names, scores.

    This function calls the hmwks_xcs function to create a list of dictionaries where keys
    are column headers consisting of student and assignment names and values are the student
    names and scores for each assignment. This function also calls the roster() function to
    maintain a consistent set of student names and ids. Students do not typically report the
    middle initial in this file and are thus omitted.
    '''

    # Calls the roster function to maintain a consistent set of student names and student IDs
    roster_tup = roster()
    full_names, sids = roster_tup[0], roster_tup[1]

    # Remove middle initials to mimic names appearing in homework
    names = [name[:-4] if name[-1] == "." else name for name in full_names]

    # Initialize list. Will be list of dictionaries
    hmwk_lst = []

    # Create a list of scores for len(name) number of students; this is consistent with the
    # global variable, num_students.
    # Add rows of scores for each student
    for _ in range(len(names)):
        hmwk_lst.append(hmwks_xcs())

    # Add student names to placeholder from hmwks_xcs function
    for idx in range(len(hmwk_lst)):
        hmwk_lst[idx]['Name'] = names[idx]

    # Save the homework scores to a csv file, but first pull the headers from the dictionary
    header = list(hmwk_lst[0].keys())

    with open('../data/generated_hmwk_scores.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for data in hmwk_lst:
            writer.writerow(data)

    # Return the sorted_names and sids for use in homework and overall class grades csvs
    return names, sids


def other_scores():
    '''Create a dictionary of other assignment scores.

    This function uses the assign_score function to create a dictionary of scores for
    quizzes, discussions, laboratory assignments, midterms and a cumulative exam for a
    single student. These assignment scores were created separate from the homework
    scores to mimic assignments are administered through an LMS.
    '''

    # Dictionary storing the max_points, average points and standard deviation for the
    # quiz, lab and discussion assignments as well as the midterm and cumulative exams
    assign_params = {'quiz': [5.0, 4.00, 1.092], 'labs': [5.0, 4.354, 0.946],
                     'discussions': [2.0, 1.833, 0.280]}

    midt_params = {'midt mc': [90.0, 70.25, 20.58],
                   'midt sa': [60.0, 39.87, 20.03]}

    cumulative_params = {"cumulative": [100.0, 76.64, 24.78]}

    # Initialize lists
    assignments, scores = [], []

    # Create a list of headers for quiz, lab and discussion assignments according to some
    # number of chapters, num_chaps, a global variable.
    for num in range(1, num_chaps + 1):
        assignments.append((f'Canvas Quiz {num}: Chapter {num}',
                            f'Laboratory #{num}',
                            f'Discussion Week {num}'))

        # Function call to create scores for each assignment type for each student
        for val in assign_params.values():
            scores.append(assign_score(list(val)[0],
                                       list(val)[1], list(val)[2]))

    # Create a list of headers for the midterms. The way the LMS is set up, the grading for
    # the midterms is separated according to multiple choice and essay question scores. Also,
    # there are only 2 midterms.
    for midt in range(1, 3):
        assignments.append((f'Midterm #{midt}: Multiple Choice',
                            f'Midterm #{midt}: Short Answer'))

        # Function call to create midterm scores for each student
        for v in midt_params.values():
            scores.append(assign_score(list(v)[0],
                                       list(v)[1], list(v)[2]))

    # Create header for cumulative exanm and function call to create scores for each student
    assignments.append(('Cumulative Exam',))
    scores.append(assign_score(cumulative_params['cumulative'][0],
                               cumulative_params['cumulative'][1],
                               cumulative_params['cumulative'][2]))

    # Flatten the list of headers
    headers = [title for sublist in assignments for title in sublist]

    # Create k, v (headers, scores, respectively) for student name and student id at the
    # beginning of the dict
    headers.insert(0, 'Name')
    headers.insert(1, 'Student ID Number')
    headers.insert(2, 'Course Section')
    scores.insert(0, 'temp_name')  # Using 'temp_name' as a placeholder
    scores.insert(1, 'temp_id')  # Using 'temp_id' as a placeholder
    scores.insert(2, 'temp_section')  # Using 'temp_section' as a placeholder

    return dict(zip(headers, scores))


def other_to_csv():
    '''Creates a list of dictionaries where keys are headers and values are names, scores.

    This function calls the other_scores function to create a list of dictionaries where keys
    are column headers consisting of student and assignment names and values are the student
    names and scores for each assignment. This function also calls the hmwk_to_csv function to
    maintain a consistent set of student names and ids.
    '''

    # Calls the roster function to maintain a consistent set of student names and student IDs
    tups = hmwk_to_csv()
    names, sids = tups[0], tups[1]

    # Initialize list. Will be list of dictionaries
    other_lst = []

    # Create a list of scores for len(name) number of students; this is consistent with the
    # global variable, num_students.
    # Add rows of scores for each student
    for _ in range(len(names)):
        other_lst.append(other_scores())

    # Add student names and student ids to placeholder from other_scores function
    for idx in range(len(other_lst)):
        other_lst[idx]['Name'] = names[idx]
        other_lst[idx]['Student ID Number'] = sids[idx]
        other_lst[idx]['Course Section'] = 'CHEM100 - 1234'

    # Save the homework scores to a csv file, but first pull the headers from the dictionary
    header = list(other_lst[0].keys())

    with open('../data/generated_other_scores.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for data in other_lst:
            writer.writerow(data)


if __name__ == "__main__":

    print(other_to_csv())
    print
