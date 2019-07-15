import datetime
from dataclasses import dataclass

import aioboto3
import ujson
from boto3.dynamodb.conditions import Key

from odin.settings import AWS_REGION_NAME, DYNAMODB_TOKEN_TABLE, DYNAMODB_HOST
from odin.utils.crypto import AES256
from .user import User


@dataclass
class Token:
    value: str
    iv: str
    key: str

    @classmethod
    async def get(cls, value) -> 'Token':
        async with aioboto3.resource('dynamodb', region_name=AWS_REGION_NAME, endpoint_url=DYNAMODB_HOST) as dynamodb:
            table = dynamodb.Table(DYNAMODB_TOKEN_TABLE)
            result = await table.query(KeyConditionExpression=Key('value').eq(value), Limit=1)
            items = result.get('Items')
            if items:
                item = items[0]
                return cls(
                    value=value,
                    iv=item['iv'],
                    key=item['key']
                )

    @classmethod
    async def create_token(cls, user: User) -> 'Token':
        aes = AES256()
        data = ujson.dumps({
            'user_id': user.id,
            'created_at': datetime.datetime.now()
        })
        token = cls(
            value=aes.encrypt(data=data),
            iv=aes.iv,
            key=aes.key
        )
        await token.save()
        return token

    async def save(self):
        async with aioboto3.resource('dynamodb', region_name=AWS_REGION_NAME, endpoint_url=DYNAMODB_HOST) as dynamodb:
            table = dynamodb.Table(DYNAMODB_TOKEN_TABLE)
            await table.put_item(Item={
                'value': self.value,
                'iv': self.iv,
                'key': self.key,
            })
