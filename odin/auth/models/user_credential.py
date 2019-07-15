from dataclasses import dataclass

import aioboto3
from boto3.dynamodb.conditions import Key

from odin.settings import DYNAMODB_USER_CREDENTIALS_TABLE, DYNAMODB_HOST, AWS_REGION_NAME


@dataclass
class UserCredentials:
    email: str
    salt: str

    @classmethod
    async def get(cls, email) -> 'UserCredentials':
        async with aioboto3.resource('dynamodb', region_name=AWS_REGION_NAME, endpoint_url=DYNAMODB_HOST) as dynamodb:
            table = dynamodb.Table(DYNAMODB_USER_CREDENTIALS_TABLE)
            result = await table.query(KeyConditionExpression=Key('email').eq(email), Limit=1)
            items = result.get('Items')
            if items:
                item = items[0]
                return cls(
                    email=email,
                    salt=item['salt'],
                )

    async def save(self):
        async with aioboto3.resource('dynamodb', region_name=AWS_REGION_NAME, endpoint_url=DYNAMODB_HOST) as dynamodb:
            table = dynamodb.Table(DYNAMODB_USER_CREDENTIALS_TABLE)
            await table.put_item(Item={
                'email': self.email,
                'salt': self.salt,
            })
