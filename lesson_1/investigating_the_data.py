import unicodecsv


def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)


enrollments = read_csv('../datasets/enrollments.csv')
daily_engagement = read_csv('../datasets/daily_engagement.csv')
project_submissions = read_csv('../datasets/project_submissions.csv')

### For each of these three tables, find the number of rows in the table and
### the number of unique students in the table. To find the number of unique
### students, you might want to create a set of the account keys in each table.

enrollment_num_rows = len(enrollments)  # Replace this with your code
enrollment_num_unique_students = len(set([x['account_key'] for x in enrollments]))

for engagement_record in daily_engagement:
    engagement_record['account_key'] = engagement_record.pop('acct')

engagement_num_rows = len(daily_engagement)  # Replace this with your code
engagement_num_unique_students = len(set([x['account_key'] for x in daily_engagement]))  # Replace this with your code

submission_num_rows = len(project_submissions)  # Replace this with your code
submission_num_unique_students = len(set([x['account_key'] for x in project_submissions]))

def get_unique_students(data):
    return set([x['account_key'] for x in data])

def get_test_accounts(enrollments): return set([x['account_key'] for x in enrollments if x['is_udacity']])


from datetime import datetime as dt


# Takes a date as a string, and returns a Python datetime object.
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')


# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)


# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])

# Clean up the data types in the engagement table
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])

# Clean up the data types in the submissions table
for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])


len(enrollments)
unique_enrolled_students = get_unique_students(enrollments)
len(unique_enrolled_students)
len(daily_engagement)
unique_engagement_students = get_unique_students(daily_engagement)
len(unique_engagement_students)
len(project_submissions)
unique_project_submitters = get_unique_students(project_submissions)
len(unique_project_submitters)
udacity_test_accounts = get_test_accounts(enrollments)

def is_problem_student(enrollment, unique_engagement_students):
    return enrollment['account_key'] not in unique_engagement_students and enrollment['join_date'] != enrollment['cancel_date']

students_in_need = filter(lambda enrollment: is_problem_student(enrollment, unique_engagement_students), enrollments)

def remove_udacity_accounts(data):
    return [x for x in data if x['account_key'] not in udacity_test_accounts]

non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

print(len(non_udacity_enrollments))
print(len(non_udacity_engagement))
print(len(non_udacity_submissions))

paid_students = {}
for enrollment in non_udacity_enrollments:
    if (not enrollment['is_canceled'] or
            enrollment['days_to_cancel'] > 7):
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date']
        if (account_key not in paid_students or
                enrollment_date > paid_students[account_key]):
            paid_students[account_key] = enrollment_date
len(paid_students)
print(len(paid_students))

# Takes a student's join date and the date of a specific engagement record,
# and returns True if that engagement record happened within one week
# of the student joining.
def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7

def remove_free_trial(data):
    return [x for x in data if x['account_key'] in paid_students]

paid_enrollments = remove_free_trial(non_udacity_enrollments)
paid_engagement = remove_free_trial(non_udacity_engagement)
paid_submissions = remove_free_trial(non_udacity_submissions)

print(len(paid_enrollments))
print(len(paid_engagement))
print(len(paid_submissions))

paid_engagement_in_first_week = []
for engage in paid_engagement:
    account_key = engage['account_key']
    join_date = paid_students[account_key]
    engagement_date = engage['utc_date']
    if within_one_week(join_date, engagement_date):
        paid_engagement_in_first_week.append(engage)

print(len(paid_engagement_in_first_week))

from collections import defaultdict

engagement_by_account = defaultdict(list)
for engagement_record in paid_engagement_in_first_week:
    account_key = engagement_record['account_key']
    engagement_by_account[account_key].append(engagement_record)

# Create a dictionary with the total minutes each student spent in the classroom during the first week.
# The keys are account keys, and the values are numbers (total minutes)
total_minutes_by_account = {}
for account_key, engagement_for_student in engagement_by_account.items():
    total_minutes = 0
    for engagement_record in engagement_for_student:
        total_minutes += engagement_record['total_minutes_visited']
    total_minutes_by_account[account_key] = total_minutes

total_minutes = total_minutes_by_account.values()

import numpy as np

print 'Mean:', np.mean(total_minutes)
print 'Standard deviation:', np.std(total_minutes)
print 'Minimum:', np.min(total_minutes)
print 'Maximum:', np.max(total_minutes)

