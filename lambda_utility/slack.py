from __future__ import annotations

__all__ = ("send_message",)

import slack_sdk


def send_message(token: str, channel: str, message: str) -> slack_sdk.web.SlackResponse:
    """send a slack message
    :exception: slack_sdk.errors.SlackApiError
    """
    client = slack_sdk.WebClient(token=token)
    response = client.chat_postMessage(channel=channel, text=message)
    return response
