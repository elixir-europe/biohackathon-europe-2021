import os
import csv
import yaml

PROJECTS_FILE = "projects2020.csv"
PROJECTS_FOLDER = "projects"
PROJECT_YAML = "projects.yml"
PROJECTS_REPOSITORY = "https://github.com/elixir-europe/BioHackathon-projects-2020/tree/master/projects/{number}"

# ACEPTED PROJECTS COLUMN NAMES
ACPT_PROJECT_NUMBER = "number"
ACPT_PROJECT_MERGED = "merged_from"
ACPT_PROJECT_TITLE = "title"
ACPT_PROJECT_SUBMITTER = "submitter"

# EASY CHAIR DUMP PROJECT COLUMNS
PROJECT_NUMBER = "#"
PROJECT_EVENBRITE = "EventBrite"
PROJECT_AUTHORS = "Authors"
PROJECT_TITLE = "Title"
PROJECT_ABSTRACT = "Abstract"

PROJECT_LEADS = "Leads for Project"
PROJECT_NOMINATED_PARTICIPANT = "Nominated participant"
PROJECT_EXPECTED_OUTCOMES = "Expected outcomes"
PROJECT_EXPECTED_AUDIENCE = "Expected participants"
PROJECT_NUMBER_OF_EXPECTED_HACKING_DAYS = "Number of days for project"
PROJECT_HACKING_TOPIC = "Topics"
PROJECT_DECISION = "Decision"

PROJECT_PAPER = "paper"


def load_all_projects():
    projects = []

    with open(PROJECTS_FILE) as pro_file:
        reader = csv.DictReader(pro_file, delimiter=',')
        line_count = 0
        accepted_count = 0
        for index, row in enumerate(reader):
            if line_count == 0:
                print(f'Projects column names are {", ".join(row)}')

            if row.get(PROJECT_DECISION) == "Accepted":
                accepted_count += 1
                project_link = PROJECTS_REPOSITORY.format(
                    number=row.get(PROJECT_EVENBRITE))             
                project = dict(
                    number=row.get(PROJECT_NUMBER),
                    authors=row.get(PROJECT_AUTHORS),                
                    title=row.get(PROJECT_TITLE),
                    leads=row.get(PROJECT_LEADS),
                    expected_outcomes=row.get(PROJECT_EXPECTED_OUTCOMES),
                    expected_audience=row.get(PROJECT_EXPECTED_AUDIENCE),        
                    nominated_participant=row.get(PROJECT_NOMINATED_PARTICIPANT),
                    number_of_expected_hacking_days=row.get(
                        PROJECT_NUMBER_OF_EXPECTED_HACKING_DAYS),                
                    hacking_topic=row.get(PROJECT_HACKING_TOPIC),
                    decision=row.get(PROJECT_DECISION),
                    abstract=row.get(PROJECT_ABSTRACT),
                    link=project_link,
                    project_number=row.get(PROJECT_EVENBRITE),
                )                
                projects.append(project)
            
            line_count += 1
    projects.sort(key = lambda project: int(project.get("project_number")))
    return projects


def to_file(project):

    path = "{}/{}".format(PROJECTS_FOLDER, project.get("project_number"))
    os.makedirs(path)

    file_name = "{}/{}/README.md".format(PROJECTS_FOLDER,
                                         project.get("project_number"))
    print("Creating file {}".format(file_name))

    with open(file_name, "w+") as output_file:
        output_file.write("# Project {}: {}\n\n".format(project.get("project_number"), project.get("title")))

        output_file.write("## Abstract\n\n")
        output_file.write(project.get("abstract"))

        output_file.write("\n\n## Topics\n\n")
        output_file.write(project.get("hacking_topic"))

        output_file.write(
            "\n\n**Project Number:** {}\n\n".format(project.get("project_number")))
        
        output_file.write(
            "\n\n**EasyChair Number:** {}\n\n".format(project.get("number")))

        output_file.write("## Team\n\n")

        output_file.write("### Lead(s)\n\n")
        output_file.write(project.get("leads"))

        output_file.write("\n\n### Nominated participant(s)\n\n")
        output_file.write(project.get("nominated_participant"))

        output_file.write("\n\n## Expected outcomes\n\n")
        output_file.write(project.get("expected_outcomes"))

        output_file.write("\n\n## Expected audience\n\n")
        output_file.write(project.get("expected_audience"))

        output_file.write(
            "\n\n**Number of expected hacking days**: {}\n\n".format(project.get("number_of_expected_hacking_days")))


def main():
    projects = load_all_projects()

    projects_yaml = []

    for xls_project in projects:
        to_file(xls_project)
        
    yaml_projects = dict(
        project_list=projects
    )
    with open(PROJECTS_FILE) as pro_file, open(PROJECT_YAML, "w+") as yaml_output_file:
        yaml_output_file.write(
            yaml.dump(yaml_projects, default_flow_style=False))
    
    for xls_project in projects:
        print("* [Project {}](projects/{}) {}".format(xls_project.get("project_number"), xls_project.get("project_number"), xls_project.get("title")))

if __name__ == '__main__':
    main()
