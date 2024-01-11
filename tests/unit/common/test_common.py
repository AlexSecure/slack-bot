"""
Unit tests for the Slack utility functions.

This test module contains unit tests for functions that extract user information
from Slack user data. It includes tests for both `get_slack_username` and
`get_slack_user_email` functions to ensure they handle various input scenarios correctly.
"""

import unittest
from common.parser import get_slack_username, get_slack_user_email


class TestSlackUtils(unittest.TestCase):
    """
    Test suite for Slack utility functions.
    """

    def test_get_slack_username_with_display_name(self):
        """
        Test if the `get_slack_username` function correctly extracts the display name
        when both display name and real name are present.
        """
        user = {
            "profile": {
                "display_name": "Display Name",
                "real_name": "Real Name"
            }
        }
        self.assertEqual(get_slack_username(user), "Display Name")

    def test_get_slack_username_with_real_name(self):
        """
        Test if the `get_slack_username` function correctly extracts the real name
        when only the real name is present.
        """
        user = {
            "profile": {
                "real_name": "Real Name"
            }
        }
        self.assertEqual(get_slack_username(user), "Real Name")

    def test_get_slack_username_with_no_name(self):
        """
        Test if the `get_slack_username` function returns 'Unknown'
        when neither display name nor real name is present.
        """
        user = {}
        self.assertEqual(get_slack_username(user), "Unknown")

    def test_get_slack_user_email_with_email(self):
        """
        Test if the `get_slack_user_email` function correctly extracts the email
        when an email is present in the user's profile.
        """
        user = {
            "profile": {
                "email": "user@example.com"
            }
        }
        self.assertEqual(get_slack_user_email(user), "user@example.com")

    def test_get_slack_user_email_with_no_email(self):
        """
        Test if the `get_slack_user_email` function returns an empty string
        when no email is present in the user's profile.
        """
        user = {"profile": {}}
        self.assertEqual(get_slack_user_email(user), "")


if __name__ == '__main__':
    unittest.main()
