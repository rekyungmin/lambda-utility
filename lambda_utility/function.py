from __future__ import annotations

__all__ = ("invoke",)

from typing import Optional, Literal, Union, BinaryIO

import aiobotocore
import botocore.client

from lambda_utility.session import create_client
from lambda_utility.schema import LambdaInvocationResponse

InvocationType = Literal["Event", "RequestResponse", "DryRun"]
LogType = Literal["None", "Tail"]


async def invoke(
    function_name: str,
    invocation_type: InvocationType,
    payload: Union[bytes, BinaryIO],
    log_type: LogType = "None",
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
) -> LambdaInvocationResponse:
    if client is None:
        client = create_client("lambda", config=config)

    async with client as client_obj:
        resp = await client_obj.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            LogType=log_type,
            Payload=payload,
        )
        try:
            received_payload_stream = resp.pop("Payload")
            received_payload = await received_payload_stream.read()
        except KeyError:
            received_payload = None

        return LambdaInvocationResponse(**resp, payload=received_payload)
