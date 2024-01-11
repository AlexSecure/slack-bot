import typing
from collections import namedtuple

from common import parser

SECURITY_TESTING_LEVELS = "Security Testing Levels:"

SECURITY_TESTING_INFO = "This structure provides a scalable approach to security testing based on the specific " \
                        "needs and risks associated with each application."

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

Message = namedtuple("Message", ["text", "blocks"], defaults=[str(), list()])


def create_slack_block(message: str) -> typing.Dict:
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": message
        }
    }


def get_greeting(user: typing.Dict) -> str:
    username = parser.get_slack_username(user)
    return f"Hi *{username}*,"


def get_jira_heading(user: typing.Dict) -> str:
    username = parser.get_slack_username(user)
    return f"*{username}* answered questions."


def get_selected_answers(selected_answers: typing.List[str]) -> str:
    result_str = "*Selected answers:*"

    for selected in selected_answers:
        result_str += f"\n{selected}"

    return result_str


def get_total_score(selected_answers: typing.List[str]) -> str:
    return f"*Total score:* {len(selected_answers)}"


def get_result(selected_answers: typing.List[str]) -> str:
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
    return f"*Task created:* {task_link}"


def generate_response_slack(
        selected_answers: typing.List[str],
        user: typing.Dict,
        task_link: str
) -> Message:

    text = get_total_score(selected_answers)
    text = text.replace("*", "")

    blocks: typing.List = list()

    blocks.append(create_slack_block(get_greeting(user)))
    blocks.append(create_slack_block(get_total_score(selected_answers)))
    blocks.append(create_slack_block(get_selected_answers(selected_answers)))
    blocks.append(create_slack_block(get_result(selected_answers)))
    blocks.append(create_slack_block(get_task(task_link)))

    return Message(text=text, blocks=blocks)


def generate_response_jira(selected_answers: typing.List[str], user: typing.Dict) -> str:

    result = \
        f"""
        {get_jira_heading(user)}

        {get_total_score(selected_answers)}

        {get_selected_answers(selected_answers)}

        {get_result(selected_answers)}
        """

    return result
