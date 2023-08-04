import csv
import random
import requests
import datetime
from pprint import pprint

# Survey question options with weights
question1_options = [
    "Action/Adventure",
    "Role-Playing Games (RPGs)",
    "First-Person Shooter (FPS)",
    "Sports/Simulation",
    "Strategy",
    "Puzzle",
    "Racing",
    "Fighting",
    "Other"
]
question1_weights = [8, 6, 4, 5, 3, 2, 2, 2, 1]

question2_options = [
    "Daily",
    "3-6 times a week",
    "1-2 times a week",
    "Occasionally",
    "Rarely",
    "Never"
]
question2_weights = [6, 5, 4, 3, 2, 1]

question3_options = [
    "PC (Personal Computer)",
    "PlayStation",
    "Xbox",
    "Nintendo Switch",
    "Mobile Devices",
    "Other"
]
question3_weights = [7, 5, 4, 3, 5, 1]

# Function to calculate age from date of birth


def calculate_age(birth_date):
    birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
    today = datetime.date.today()
    age = today.year - birth_date.year - \
        ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


# Function to generate random salary data


def generate_salary_data():
    salaries = [
        {
            "salary": 30000,
            "probability": 10,
        },
        {
            "salary": 40000,
            "probability": 15,
        },
        {
            "salary": 50000,
            "probability": 10,
        },
        {
            "salary": 60000,
            "probability": 7,
        },
        {
            "salary": 70000,
            "probability": 5,
        },
        {
            "salary": 80000,
            "probability": 3,
        },
        {
            "salary": 90000,
            "probability": 1,
        },
        {
            "salary": 100000,
            "probability": 1,
        }
    ]

    return random.choices([salary["salary"] for salary in salaries], weights=[salary["probability"] for salary in salaries], k=1)[0]


# Function to generate random survey data
def generate_survey_data(num_entries):
    survey_data = []
    persons_res = requests.get(
        f"https://fakerapi.it/api/v1/persons?_quantity={num_entries}").json()["data"]

    for i in range(num_entries):
        person = persons_res[i]
        entry = {
            "Name": person["firstname"] + " " + person["lastname"],
            "Age": calculate_age(person["birthday"]),
            "Gender": person["gender"],
            "Salary": generate_salary_data(),
            "Favorite Genre": random.choices(question1_options, weights=question1_weights)[0],
            "Play Frequency": random.choices(question2_options, weights=question2_weights)[0],
            "Preferred Platform": random.choices(question3_options, weights=question3_weights)[0]
        }
        survey_data.append(entry)
    return survey_data


# Generate 10 random survey entries
num_entries = 1000
random_survey_data = generate_survey_data(num_entries)

# Write generated data to CSV file
with open("data.csv", "w", newline="\n") as file:
    writer = csv.DictWriter(
        file, fieldnames=random_survey_data[0].keys())
    writer.writeheader()
    writer.writerows(random_survey_data)
