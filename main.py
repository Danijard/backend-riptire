from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import tokenlib

# Модели запросов
class LoginRequest(BaseModel):
    login: str

class AuthRequest(BaseModel):
    login: str
    password: str

class TokenRequest(BaseModel):
    token: str

# Создание приложения FastAPI
app = FastAPI()
secret="YOAKIM_BRAND"


# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешение всех источников или можно указать конкретные
    allow_credentials=True,
    allow_methods=["*"],  # Разрешение всех методов
    allow_headers=["*"],  # Разрешение всех заголовков
)

user_id_list = {'+71': 1, '1@riptire.org': 1,
                '+72': 2, '2@riptire.org': 2,
                '+73': 3, '3@riptire.org': 3,
                '+74': 4, '4@riptire.org': 4}

id_password_list = {1: '111', 2: '222', 3: '333', 4: None}

id_name_relation = {1: 'Иван', 2: 'Петр', 3: 'Сергей', 4: 'Алексей'}

id_role_relation = {1: 'Администратор', 2: 'Мастер', 3: 'Менеджер', 4: 'Аналитик'}

# Маршрут для проверки существования пользователя и пароля
@app.post("/api/login-info")
def check_login(login_request: LoginRequest):
    user_id = user_id_list.get(login_request.login)
    password = id_password_list.get(user_id)

    return {
        "isExist": user_id is not None,
        "hasPassword": password is not None
    }

@app.post("/api/user-info")
def user_info(token: TokenRequest):
    user_id = tokenlib.parse_token(token.token, secret=secret).get('user_id')
    if user_id is not None:
        return {
            "name": id_name_relation.get(user_id),
            "role": id_role_relation.get(user_id)
        }

    return {
        "name": None,
        "role": None
    }

# Маршрут для авторизации
@app.post("/api/auth")
def authenticate(auth_request: AuthRequest):
    user_id = user_id_list.get(auth_request.login)
    s_password = auth_request.password
    r_password = id_password_list.get(user_id)

    if r_password is None and s_password is not None:
        token = tokenlib.make_token({"user_id": user_id}, secret=secret)
        return {
            "isAuth": True,
            "token": token
        }
    if r_password is not None and s_password == r_password:
        token = tokenlib.make_token({"user_id": user_id}, secret=secret)
        return {
            "isAuth": True,
            "token": token
        }
    return {
        "isAuth": False,
        "token": None
    }

@app.post("/api/update-token")
def update_token(token: TokenRequest):
    user_id = tokenlib.parse_token(token.token, secret=secret).get('user_id')
    if user_id is not None:
        return {
            "token": tokenlib.make_token({"user_id": user_id}, secret=secret)
        }


# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)