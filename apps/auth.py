from ninja.errors import AuthenticationError


from datetime import datetime, timezone, timedelta

import secrets
from typing import Any

import jwt
from ninja.security import HttpBearer

from apps.user.models import User


class TokenUtil:

    def __init__(self, effective_time: int = 300, secret_key: str = None, algorithms: str = "HS256"):
        """
        token 🔧
        :param effective_time: 有效时间-当前时间 + 指定秒数
        :param secret_key: 密钥
        :param algorithms: 加密算法
        """
        if secret_key is None:
            self.secret_key = secrets.token_urlsafe(64)
        else:
            self.secret_key = secret_key
        self.effective_time = effective_time
        self.algorithms = algorithms

    def build(self, payload: Any) -> str:
        """
        生成token
        :param payload: 加密数据
        :return: token
        """
        data = {"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=self.effective_time)}
        data.update({"payload": payload})
        return jwt.encode(data, self.secret_key, self.algorithms)

    def parse(self, token: str) -> Any:
        """
        解析token
        :param token: token
        :return: 加密的数据
        """
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithms])
        return payload.get("payload")


token_util = TokenUtil()


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_id = token_util.parse(token)
            request.user = User.objects.get(id=user_id)
            return user_id
        except Exception as e:
            raise AuthenticationError


auth = dict(auth=AuthBearer())

