from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

access_token = os.environ.get("access_token")
print(access_token)

async def get_resume_data(resume_id):
    """
        Получает информацию о резюме по его ID через API hh.ru

        Args:
            resume_id (str): ID резюме
            access_token (str, optional): Токен доступа для авторизации

        Returns:
            dict: Данные резюме в формате JSON или None в случае ошибки
        """
    # Заголовки запроса
    headers = {
        "User-Agent": "YourApp/1.0 (anku@sidorinlab.ru)"  # Замените на ваш User-Agent
    }

    # Если предоставлен токен доступа, добавляем его в заголовки
    headers["Authorization"] = f"Bearer {access_token}"

    url = f'https://api.hh.ru/resumes/{resume_id}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            r_json = await response.json()
            return r_json


