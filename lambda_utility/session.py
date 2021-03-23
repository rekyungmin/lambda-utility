from __future__ import annotations

__all__ = (
    "DEFAULT_CONFIG",
    "create_client",
)

from typing import Optional, Union

import aiobotocore
import botocore.client

DEFAULT_CONFIG = botocore.client.Config(connect_timeout=300, read_timeout=300)


def create_client(
    service_name: str,
    region_name: Optional[str] = None,
    api_version: Optional[str] = None,
    use_ssl: bool = True,
    verify: Optional[Union[bool, str]] = None,
    endpoint_url: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
    config: Optional[botocore.client.Config] = None,
) -> aiobotocore.session.ClientCreatorContext:
    session = aiobotocore.get_session()
    if config:
        config = DEFAULT_CONFIG.merge(config)

    return session.create_client(
        service_name,
        region_name=region_name,
        api_version=api_version,
        use_ssl=use_ssl,
        verify=verify,
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        config=config,
    )
