import csv
import os
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

# Create the bronze folder if it doesn't exist
output_folder = 'data/bronze'
os.makedirs(output_folder, exist_ok=True)

# Set the number of data points and the maximum number of commit messages
num_data_points = 300
max_commit_messages = 30

# Generate developer data
developers = [{'DeveloperKey': i + 1,
               'DeveloperName': fake.name(),
               'DeveloperRole': fake.job()} for i in range(20)]


# Generate project data
projects = [{'ProjectKey': i + 1,
             'ProjectName': fake.bs(),
             'ProjectStart': fake.date_between(start_date='-365d', end_date='today'),
             'ProjectEnd': fake.date_between(start_date='today', end_date='+365d'),
             'RevenueGenerated': fake.random_int(min=100000, max=500000)} for i in range(10)]

projects_name_key_map = {ele["ProjectName"]: ele["ProjectKey"] for ele in projects}

# Generate JiraGitDimension data
jira_git_data = []
jira_ticket_commit_messages = []
for i in range(num_data_points):
    project = random.choice(projects)
    developer = random.choice(developers)

    jira_ticket_key = fake.uuid4()
    story_point = fake.random_int(min=1, max=20)
    commit_time = fake.date_time_between_dates(datetime.combine(project['ProjectStart'], datetime.min.time()),
                                               datetime.combine(project['ProjectEnd'], datetime.max.time()))
    
    # Ensure one-to-one relationship between JiraTicketKey and StoryPoint
    jira_git_data.append({
        'JiraGitKey': i + 1,
        'ProjectKey': projects_name_key_map[project['ProjectName']],
        'DeveloperKey': developer['DeveloperKey'],
        'StoryPoints': story_point,
        'JiraTicket': jira_ticket_key,
        'GitHubRepo': project['ProjectName'],
        'CommitMessage': f"Initial commit for project {project['ProjectName']} by {developer['DeveloperName']}",
        'CommitTime': commit_time,
    })

    # Ensure one-to-many relationship between JiraTicketKey and CommitMessage
    num_commit_messages = fake.random_int(min=1, max=max_commit_messages)
    commit_messages = [
        {
            'JiraGitKey': i + 1,
            'ProjectKey': projects_name_key_map[project['ProjectName']],
            'DeveloperKey': developer['DeveloperKey'],
            'StoryPoints': story_point,
            'JiraTicket': jira_ticket_key,
            'GitHubRepo': project['ProjectName'],
            'CommitMessage': f"Commit {j+1} by {developer['DeveloperName']} on project {project['ProjectName']}",
            'CommitTime': fake.date_time_between_dates(commit_time, datetime.combine(project['ProjectEnd'], datetime.max.time())),
        } for j in range(num_commit_messages)
    ]
    jira_ticket_commit_messages.extend(commit_messages)

# Write data to CSV in the bronze folder
with open(os.path.join(output_folder, 'developer_dimension.csv'), 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=developers[0].keys())
    writer.writeheader()
    writer.writerows(developers)

with open(os.path.join(output_folder, 'project_dimension.csv'), 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=projects[0].keys())
    writer.writeheader()
    writer.writerows(projects)

with open(os.path.join(output_folder, 'jira_git_dimension.csv'), 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=jira_git_data[0].keys())
    writer.writeheader()
    writer.writerows(jira_git_data)

# Write JiraGitCommit data to CSV in the bronze folder
with open(os.path.join(output_folder, 'jira_git_fact.csv'), 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=jira_ticket_commit_messages[0].keys())
    writer.writeheader()
    writer.writerows(jira_ticket_commit_messages)
