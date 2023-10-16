from jose import jwt
import config
import time

# app = Flask(__name__)


# 生成token
def generate_token(user, operation, **kwargs):
    key = config.SECRET_KEY
    data = {"id": user, "operation": operation}
    data["exp"] = int(time.time()) + config.JWT_TIME
    data.update(**kwargs)
    return jwt.encode(claims=data, key=key, algorithm="HS256")

# 验证token
def validate_token(token, *operation):
    key = config.SECRET_KEY
    try:
        data = jwt.decode(token, key, algorithms='HS256')
    except:
        return False
    return True
