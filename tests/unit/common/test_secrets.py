import unittest
from unittest.mock import patch
import enum
from common.secrets import BotSecrets


# Mocking external function get_secrets
def mocked_get_secrets():
    return {
        BotSecrets.SLACK_BOT_TOKEN.name: "slack_bot_token_value",
        BotSecrets.SLACK_SIGNING_SECRET.name: "slack_signing_secret_value",
        BotSecrets.SLACK_SLASH_COMMAND.name: "slack_slash_command_value",
        BotSecrets.JIRA_API_TOKEN.name: "jira_api_token_value",
        BotSecrets.JIRA_URL.name: "jira_url_value",
        BotSecrets.JIRA_USER.name: "jira_user_value",
        BotSecrets.JIRA_PROJECT_KEY.name: "jira_project_key_value",
        # Add other secrets here as needed
    }


class TestBotSecrets(unittest.TestCase):
    """
    Unit tests for the BotSecrets class.
    """

    @patch('common.secrets.get_secrets', side_effect=mocked_get_secrets)
    def test_get_all_secrets(self, mock_get_secrets):
        """
        Test retrieving all secrets using BotSecrets.get.
        """
        for secret in BotSecrets:
            with self.subTest(secret=secret):
                secret_value = BotSecrets.get(secret)
                self.assertEqual(secret_value, mocked_get_secrets()[secret.name])

    @patch('common.secrets.get_secrets', side_effect=mocked_get_secrets)
    def test_get_non_existing_secret(self, mock_get_secrets):
        """
        Test retrieving a non-existing secret using BotSecrets.get and expecting an exception.
        """
        class OtherEnum(enum.Enum):
            NON_EXISTING_SECRET = enum.auto()

        with self.assertRaises(Exception) as context:
            _ = BotSecrets.get(OtherEnum.NON_EXISTING_SECRET)

        self.assertTrue("Fail to find secret key" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
