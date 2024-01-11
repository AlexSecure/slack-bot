"""
This script defines functionality for creating and managing a modal view in a Slack application.
It defines a modal template (`VIEW_TEMPLATE`) for a questionnaire about security testing levels,
populates the modal with a list of predefined questions (`questions`), and provides utility
functions to generate the modal view (`get_view`), extract a number from a string (`extract_number`),
and parse selected answers from the modal (`get_selected_answers`). The focus is on creating a
user-interactive experience within Slack where users can respond to a series of questions
to determine the security testing requirements for their applications.
"""

import re
import typing

from common import parser

# A header for the questionnaire in the modal
SECURITY_TESTING_QUESTIONNAIRE = "Security Testing Level Determination Questionnaire:"


# Template for the Slack modal view
VIEW_TEMPLATE = {
    "type": "modal",
    "callback_id": parser.SLACK_MODAL_WINDOW_ID,  # Unique identifier for the modal
    "title": {
        "type": "plain_text",
        "text": "HB-Bot"  # Text for the modal window header
    },
    "submit": {
        "type": "plain_text",
        "text": "Submit"  # Text for the submit button
    },
    "blocks": [
        {
            "type": "section",
            "block_id": "section-identifier",  # Identifier for this block section
            "text": {
                "type": "mrkdwn",
                "text": SECURITY_TESTING_QUESTIONNAIRE
            },
            "accessory": {
                "type": "checkboxes",
                "action_id": "checkboxes-action",  # Identifier for the checkbox action
                "options": []  # Options for checkboxes will be added here
            }
        }
    ]
}

# Global variable to store the dynamically generated view.
VIEW = None


# List of questions to be included in the modal's checkboxes.
questions = [
    # Each question is a tuple of (Question Title, Question Description)
    (
        "Data Sensitivity",
        "Does your application process personally identifiable information or sensitive data? (GDPR relevant)",
    ),
    (
        "Internet Exposure",
        "Is your application accessible via the internet?"
    ),
    (
        "Business Criticality",
        "Is your application critical to your business operations?"
    ),
    (
        "Reputational Risk",
        "Would a security breach have a significant reputational impact on your business?"
    ),
    (
        "Compliance Requirements",
        "Does your application need to comply with specific regulatory requirements?"
    ),
    (
        "User Base",
        "Does your application serve a large number of users?"
    ),
    (
        "Transaction Handling",
        "Does your application handle financial transactions or sensitive user activities?"
    ),
    (
        "Data Volume",
        "Does your application process a large volume of data?"
    ),
    (
        "Third-Party Integrations",
        "Does your application integrate with third-party services or APIs?"
    ),
    (
        "Previous Security Incidents",
        "Has your application experienced security incidents in the past?"
    )
]


def get_view():
    """
    Generates and returns the view (modal) for the Slack app.
    The view is generated only once and stored in the global VIEW variable.
    """

    global VIEW

    # Check if the view is already generated
    if VIEW is None:

        # Start with the template
        VIEW = VIEW_TEMPLATE

        # Populate the options in the checkbox based on the questions
        for idx, question in enumerate(questions):
            name, description = question

            VIEW_TEMPLATE["blocks"][0]["accessory"]["options"].append({
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{idx + 1}. {name}*"  # Display name of the question
                },
                "description": {
                    "type": "mrkdwn",
                    "text": description  # Display description of the question
                },
                "value": f"value-{idx}"  # Value associated with the checkbox option
            })

    # Return the generated view
    return VIEW


def extract_number(input_string: str) -> int:
    """
    Extracts a number from a given string.

    Args:
        input_string (str): The string to extract the number from.

    Returns:
        int: The extracted number.

    Raises:
        ValueError: If no number is found in the input string.
    """

    match = re.search(r'\d+', input_string)

    if match:
        return int(match.group())
    else:
        raise ValueError("No number found in the input string.")


def get_selected_answers(selected_options: typing.List[typing.Dict]) -> typing.List[str]:
    """
    Parses a list of selected options and retrieves corresponding questions.

    This function takes a list of dictionaries representing selected options. Each option dictionary
    is expected to contain a 'value' key with a string value in the format "value-N", where N is an
    integer. It extracts these integer values, uses them to index into a globally defined list
    'questions', and formats the corresponding question title and description into a readable string.

    Parameters:
        selected_options (List[Dict]): A list of dictionaries, where each dictionary represents a
        selected option with a 'value' key.

    Returns:
        List[str]: A list of strings, each containing the formatted question title and description
        from the 'questions' list based on the selected options.

    Raises:
        Exception: If any 'value' key is missing, does not contain a hyphen, or its numeric part is
        out of range of the 'questions' list.
    """

    # Initialize an empty list to hold the results.
    results: typing.List[str] = list()

    # Iterate over each option in the selected_options list.
    for option in selected_options:
        # Extract the 'value' from the option dictionary.
        # This value is expected to be a string like "value-0".
        value = option.get("value")

        # Check if 'value' is valid and contains a hyphen.
        # If not, raise an exception as the format is not as expected.
        if not value or value.find("-") == -1:
            raise Exception("Fail to parse selected option value.")

        # Extract the numeric part from the 'value' string.
        value_int = extract_number(value)

        # Verify that the extracted number does not exceed the number of questions.
        # Raise an exception if the value is out of range.
        if value_int >= len(questions):
            raise Exception("Selected option value is higher than total questions number.")

        # Retrieve the question title and description using the extracted number as an index.
        title, description = questions[value_int]

        # Format and append the question information to the results list.
        results.append(f"\n{value_int + 1}. *{title}:* {description}")

    return results
