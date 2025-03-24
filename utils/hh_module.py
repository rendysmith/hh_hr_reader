import asyncio
from distutils.command.build_scripts import first_line_re
from pprint import pprint

import aiohttp
import requests
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

Client_ID = os.environ.get("Client_ID")
Client_Secret = os.environ.get("Client_Secret")
Redirect_URI = os.environ.get("Redirect_URI")

#Используется только один раз для получения токена
authorization_code = 'KPD639TU5QIHCOPEJHETRH2IPKGQCTV13S1BKS6T5CJDACRPUDNS0LUQTNVNJKMO'

access_token = os.environ.get("access_token")

async def get_code():
    #ССылка для получения authorization_code - код нужно ловить в потоке
    url_code = f'https://hh.kz/oauth/authorize?response_type=code&client_id={Client_ID}'
    print('CODE', url_code)

async def get_limits():
    """
    employer_id: = Идентификатор работодателя, который можно узнать в информации о текущем пользователе https://api.hh.ru/openapi/redoc#tag/Informaciya-o-menedzhere/operation/get-current-user-info
    manager_id: = Идентификатор менеджера, который можно узнать в информации о текущем пользователе https://api.hh.ru/openapi/redoc#tag/Informaciya-o-menedzhere/operation/get-current-user-info
    :return:
    """
    url = "https://api.hh.ru/employers/{employer_id}/managers/{manager_id}/limits/resume"


async def get_access_token():
    url = 'https://api.hh.ru/token'
    headers = {
        'User-Agent': 'api-test-agent'
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': Client_ID,
        'client_secret': Client_Secret,
        'code': authorization_code
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    r_json = response.json()
    print(r_json)

    if response.status_code == 400:
        if r_json['error_description'] == 'code has already been used':
            print('code - уже был использован (его можно использовать только один раз)')

        elif r_json['error_description'] == 'error_description':
            print('code - истек')

    return response.json()

async def get_me():
    """
        Получает информацию о пользователе
    """

    # Заголовки запроса
    headers = {
        "User-Agent": "YourApp/1.0 (anku@sidorinlab.ru)"  # Замените на ваш User-Agent
    }

    # Если предоставлен токен доступа, добавляем его в заголовки
    headers["Authorization"] = f"Bearer {access_token}"

    url = f'https://api.hh.ru/me'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            r_json = await response.json()
            print(r_json)
            return r_json

async def get_mine():
    """
        Получает информацию о пользователе
    """

    # Заголовки запроса
    headers = {
        "User-Agent": "YourApp/1.0 (anku@sidorinlab.ru)"  # Замените на ваш User-Agent
    }

    # Если предоставлен токен доступа, добавляем его в заголовки
    headers["Authorization"] = f"Bearer {access_token}"

    url = f'https://api.hh.ru/manager_accounts/mine'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            r_json = await response.json()
            print(r_json)
            return r_json


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
        async with session.get(url, headers=headers) as response:
            r_status = response.status
            r_json = await response.json()
            if r_status == 200:
                print(f'Statsu: {r_status}')
                #pprint(r_json)

            elif r_status == 403:
                pass

            elif r_status == 404:
                error_text = "Резюме не существует или недоступно для текущего пользователя"
                print(r_status, error_text)
                print(r_json['errors'])
                return error_text

    #pprint(r_json)

    last_name = r_json.get("last_name") or 'No last name'
    first_name = r_json.get("first_name") or 'No name'

    fio = last_name + " " + first_name
    age = r_json["age"]
    gender = r_json["gender"]["name"]
    area = r_json["area"]["name"]
    experience = 'experience:\n'
    for exp in r_json["experience"]:
        experience += (f'Position: {exp["position"]}\n'
                       f'Period: {exp["start"]} - {exp["end"]}\n'
                       f'Company name: {exp["company"]}\n'
                       f'Description: {exp["description"]}\n\n')

    skill_set = r_json["skill_set"]
    skills = r_json["skills"]

    resume_description = f"""
    {fio}
    {age}
    {gender}
    {area}
    {experience}
    {skill_set}
    {skills}
    """
    return resume_description





async def get_negotiations():
    """
        Получает информацию о пользователе
    """

    # Заголовки запроса
    headers = {
        "User-Agent": "YourApp/1.0 (anku@sidorinlab.ru)"  # Замените на ваш User-Agent
    }

    # Если предоставлен токен доступа, добавляем его в заголовки
    headers["Authorization"] = f"Bearer {access_token}"

    url = f'https://api.hh.ru/negotiations'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            r_json = await response.json()
            print(r_json)
            return r_json



if "__main__" in __name__:
    a = asyncio.run(get_resume_data('ba185b570007f6ad4a0016c1266a7542366a44'))
    print(a)