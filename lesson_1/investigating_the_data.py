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

print daily_engagement[0]['account_key']
print submission_num_rows