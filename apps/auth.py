from ninja.errors import AuthenticationError

from apps.user.models import User


def session_auth(request):
    try:
        user_id = request.session['user']
        user = User.objects.get(id=user_id)
        return user
    except Exception as e:
        print(e)
        raise AuthenticationError

