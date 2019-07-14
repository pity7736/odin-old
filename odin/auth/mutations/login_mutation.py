import graphene

from odin.auth.models import User
from odin.auth.models.user_credential import UserCredential
from odin.auth.utils import make_password


class LoginMutation(graphene.Mutation):
    token = graphene.String()
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    @staticmethod
    async def mutate(root, info, email, password):
        user = await User.get(email=email)
        if user is None:
            return LoginMutation(token=None, message=f'Does not exists an user with email: {email}')

        user_credential = await UserCredential.get(email=email)
        encrypted_password = make_password(raw_password=password, salt=user_credential.salt)[0]
        token = None
        message = 'email or password are wrong'
        if encrypted_password == user.password:
            token = 'hola'
            message = 'login successfully'

        return LoginMutation(token=token, message=message)
