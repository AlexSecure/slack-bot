"""
This script is designed to facilitate communication within a Slack application, specifically tailored
for conducting security testing level determination. It includes a detailed framework for assessing
security testing requirements based on a scoring system. The script defines constants and a namedtuple
for structured message formatting, along with a series of functions to create Slack message blocks,
calculate scores, and format messages for both Slack and JIRA integrations.
"""

import typing
from collections import namedtuple

from common import parser


# Constant header for the security testing levels
SECURITY_TESTING_LEVELS = "Security Testing Levels:"

# Information string providing context about the security testing approach
SECURITY_TESTING_INFO = "This structure provides a scalable approach to security testing based on the specific " \
                        "needs and risks associated with each application."

# Namedtuple 'Message' for structuring Slack messages with text and block elements
Message = namedtuple("Message", ["text", "blocks"], defaults=[str(), list()])


# Mapping of score ranges to results.
RESULTS = [
    # Each result is a tuple of (Minimum Score, Maximum Score, Result Description, Details List)
    (
        0, 2,
        "Level 1 - Automated Security Testing",
        [
            "Enroll the application in automated security testing tools.",
            "Ideal for low-sensitivity and low-criticality applications.",
            "Continuous scanning for basic vulnerabilities."
        ]
    ),
    (
        3, 4,
        "Level 2 - Freelance Security Assessment",
        [
            "Engagement of freelance security contractors for targeted assessments.",
            "Suitable for moderate sensitivity and criticality applications.",
            "Focus on more specific OWASP vulnerabilities."
        ]
    ),
    (
        5, 6,
        "Level 3 - Internal Security Team Review",
        [
            "Comprehensive review by the organization’s internal security team.",
            "For applications with higher business criticality.",
            "In-depth testing including manual code review."
        ]
    ),
    (
        7, 8,
        "Level 4 - Boutique Security Firm Engagement",
        [
            "Hiring specialized boutique security firms for advanced testing.",
            "For high-criticality applications with significant data sensitivity.",
            "Extensive testing, including advanced penetration testing and risk analysis."
        ]
    ),
    (
        9, 10,
        "Level 5 - Full Scope Penetration Test by NCC",
        [
            "A fully scoped penetration test conducted by NCC Group or similar.",
            "For the most critical applications with potential high reputational impact.",
            "The most comprehensive security testing, adhering strictly to OWASP Top 10."
        ]
    ),
]


def create_slack_block(message: str) -> typing.Dict:
    """
    Creates a Slack message block.

    Args:
        message (str): The message to be displayed in the block.

    Returns:
        dict: A dictionary representing a Slack message block.
    """

    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": message
        }
    }


def get_greeting(user: typing.Dict) -> str:
    """
    Generates a greeting message for a Slack user.

    Args:
        user (dict): A dictionary containing user information.

    Returns:
        str: A formatted greeting message.
    """

    username = parser.get_slack_username(user)
    return f"Hi *{username}*,"


def get_jira_heading(user: typing.Dict) -> str:
    """
    Generates a JIRA heading based on the Slack user's response.

    Args:
        user (dict): A dictionary containing user information.

    Returns:
        str: A formatted JIRA heading.
    """

    username = parser.get_slack_username(user)
    return f"*{username}* answered questions."


def get_selected_answers(selected_answers: typing.List[str]) -> str:
    """
    Compiles selected answers into a formatted string.

    Args:
        selected_answers (List[str]): A list of selected answers.

    Returns:
        str: A formatted string of selected answers.
    """

    result_str = "*Selected answers:*"

    for selected in selected_answers:
        result_str += f"\n{selected}"

    return result_str


def get_total_score(selected_answers: typing.List[str]) -> str:
    """
    Calculates and returns the total score based on selected answers.

    Args:
        selected_answers (List[str]): A list of selected answers.

    Returns:
        str: A formatted string displaying the total score.
    """

    return f"*Total score:* {len(selected_answers)}"


def get_result(selected_answers: typing.List[str]) -> str:
    """
    Determines and formats the security testing result based on the score.

    Args:
        selected_answers (List[str]): A list of selected answers.

    Returns:
        str: A formatted string of the result based on the score.
    """

    # Process the selected options to calculate a score
    score = len(selected_answers)
    result_str = "Result:"

    # Loop through predefined results and append the appropriate description
    for _, max_level, description, details in RESULTS:
        if score <= max_level:
            result_str = f"*{result_str} {description}*"

            for detail in details:
                result_str += f"\n- {detail}"
            break

    return result_str


def get_task(task_link: str) -> str:
    """
    Generates a task creation message.

    Args:
        task_link (str): The link to the created task.

    Returns:
        str: A formatted message indicating the task creation with a link.
    """

    return f"*Task created:* {task_link}"


def generate_response_slack(
        selected_answers: typing.List[str],
        user: typing.Dict,
        task_link: str
) -> Message:
    """
    Compiles a full response for Slack based on user answers and other data.

    Args:
        selected_answers (List[str]): A list of selected answers.
        user (dict): A dictionary containing user information.
        task_link (str): The link to the created task.

    Returns:
        Message: A namedtuple containing the response text and blocks for Slack.
    """

    # Retrieve and format the total score, stripping out markdown symbols for plain text
    text = get_total_score(selected_answers)
    text = text.replace("*", "")

    # Initialize an empty list to store message blocks
    blocks: typing.List = list()

    # Append various sections to the message blocks
    blocks.append(create_slack_block(get_greeting(user)))  # Greeting section
    blocks.append(create_slack_block(get_total_score(selected_answers)))  # Total score section
    blocks.append(create_slack_block(get_selected_answers(selected_answers)))  # Selected answers section
    blocks.append(create_slack_block(get_result(selected_answers)))  # Result based on the score
    blocks.append(create_slack_block(get_task(task_link)))  # Task link section

    # Return the compiled message as a namedtuple
    return Message(text=text, blocks=blocks)


def generate_response_jira(selected_answers: typing.List[str], user: typing.Dict) -> str:
    """
    Compiles a full response for JIRA based on user answers.

    Args:
        selected_answers (List[str]): A list of selected answers.
        user (dict): A dictionary containing user information.

    Returns:
        str: A formatted string suitable for JIRA.
    """

    # Start building the JIRA response as a formatted string
    # The string is assembled using formatted pieces to create a cohesive report
    result = \
        f"""
        {get_jira_heading(user)}  # Include a heading with the user's name indicating they answered questions

        {get_total_score(selected_answers)}  # Add the total score summary

        {get_selected_answers(selected_answers)}  # List all the selected answers

        {get_result(selected_answers)}  # Append the final result based on the answers
        """

    # Return the final compiled response
    return result
