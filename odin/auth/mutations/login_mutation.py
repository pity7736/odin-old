import graphene

from odin.auth.controllers.login_controller import LoginController


class LoginMutation(graphene.Mutation):
    token = graphene.String()
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    @staticmethod
    async def mutate(root, info, email, password):
        controller = LoginController(email=email, password=password)
        token, message = await controller.login()
        return LoginMutation(token=token, message=message)
