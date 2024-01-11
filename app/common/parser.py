"""
This module provides utility functions to extract user information from Slack user data.

The module contains two functions:
- `get_slack_user_name` which extracts and returns the display name or the real name of a Slack user.
- `get_slack_user_email` which extracts and returns the email address of a Slack user.

Both functions expect a dictionary containing user data as obtained from Slack's API. These functions are helpful when working with Slack user information, especially in applications that need to display user names or contact them via email.

Functions:
    get_slack_user_name(user: typing.Dict) -> str
    get_slack_user_email(user: typing.Dict) -> str
"""

import typing


SLACK_MODAL_WINDOW_ID = "id-modal-window"


def get_slack_username(slack_user: typing.Dict) -> str:
    """
    Extracts the display name or real name of a Slack user from the user info dictionary.

    Args:
        slack_user (typing.Dict): A dictionary containing Slack user information.

    Returns:
        str: The user's display name or real name. Returns "Unknown" if neither is available.
    """

    # Initialize an empty string for the username
    username = str()

    # If the 'profile' key exists in the user dictionary, try to get the display name.
    # If the display name is not available, get the real name from the profile.
    if "profile" in slack_user:
        username = slack_user["profile"].get("display_name") or slack_user["profile"].get("real_name")

    # If the username is still not set, try to get the real name or name directly from the user dictionary.
    if not username:
        user_name = slack_user.get("real_name") or slack_user.get("name")

    # If no name is found, return "Unknown"
    if not username:
        return "Unknown"

    # Return the found username
    return username


def get_slack_user_email(slack_user: typing.Dict) -> str:
    """
    Extracts the email of a Slack user from the user info dictionary.

    Args:
        slack_user (typing.Dict): A dictionary containing Slack user information.

    Returns:
        str: The user's email address. Returns an empty string if the email is not available.
    """

    # Return the email from the user's profile, defaulting to an empty string if not found.
    return slack_user.get("profile", {}).get("email", str())
