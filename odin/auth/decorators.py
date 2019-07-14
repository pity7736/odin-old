from starlette.authentication import AuthenticationError, UnauthenticatedUser


def login_required(f):
    async def wrapper(root, info, *args, **kwargs):
        user = info.context['request'].user
        if isinstance(user, UnauthenticatedUser):
            raise AuthenticationError('login required!')
        return await f(root, info, *args, **kwargs)
    return wrapper


def permissions_required(permissions):
    def decorator(f):
        async def wrapper(root, info, *args, **kwargs):
            for permission in permissions:
                if permission not in info.context['request'].auth.scopes:
                    raise ValueError(f'Permission required: {permission}')
            return await f(root, info, *args, **kwargs)
        return wrapper
    return decorator
