import asyncio
import os

from requests.auth import HTTPBasicAuth

from utils.gs_editor import get_service, read_table_id
from utils.central_module import pars_resume_id
from utils.hh_module import get_resume_data
from utils.ai_module import get_answer_ai

auth_username = os.environ.get("HOST_USERNAME")
auth_password = os.environ.get("HOST_PASSWORD")
auth = HTTPBasicAuth(auth_username, auth_password)

prompt_text = """
Ты рекрутёр нашей компании, ты должен найти NLP инженера для обучения и дообучения языковых моделей под наши задачи, 
такие как BERT

Ты должен: 
-------------------НАЧАЛО РЕЗЮМЕ--------------------
{resume_text}
-------------------КОНЕЦ РЕЗЮМЕ---------------------

1 - Внимательно прочитать резюме соискателя выше
2 - Дать предварительную оценку, подходит ли нам данный соискатель
3 - Дать краткий вывод своего анализа
"""

async def main():
    service = await get_service()
    df = await read_table_id(service, '1Qznst9tRjeFaODj0PLsq7i-cl6AA5zF4dpmhtSVUiUU', 'NLP')

    for idx, row in df.iterrows():
        print('-----------------------------------')
        interview = row['Собеседование']
        if interview:
            continue

        salary = row['ЗП']
        print(salary)

        status = input('Введите 1 для анализа вакансии или пробел для пропуска: ')
        print(type(status))
        if status == "":
            continue

        resume_url = row['Резюме']
        resume_id = await pars_resume_id(resume_url)

        resume_description = await get_resume_data(resume_id)
        prompt = prompt_text.format(resume_text=resume_description)

        result = await get_answer_ai(auth, prompt)
        print(result)








if __name__ == '__main__':
    asyncio.run(main())
