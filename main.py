import asyncio
import os

from requests.auth import HTTPBasicAuth

from utils.gs_editor import get_service, read_table_id, append_data_to_sheet_cell
from utils.central_module import pars_resume_id
from utils.hh_module import get_resume_data
from utils.ai_module import get_answer_ai

auth_username = os.environ.get("HOST_USERNAME")
auth_password = os.environ.get("HOST_PASSWORD")
auth = HTTPBasicAuth(auth_username, auth_password)

SS_ID = '1Qznst9tRjeFaODj0PLsq7i-cl6AA5zF4dpmhtSVUiUU'
TAB_NAME = 'NLP'

prompt_text = """
Ты рекрутёр нашей компании, ты должен найти NLP инженера для обучения и дообучения языковых моделей под наши задачи, 
такие как BERT

Ты должен: 
-------------------НАЧАЛО РЕЗЮМЕ--------------------
{resume_text}
-------------------КОНЕЦ РЕЗЮМЕ---------------------

1 - Внимательно прочитать резюме соискателя выше
2 - Проведи максимально тщательный анализ резюме соискателя.
3 - Дай точную оценку, подходит ли нам данный соискатель. Учти нужные нам навыки и как часто меняла работу.
4 - Дай очень краткий вывод своего анализа. Опиши свой результат 3-4 предложениями.
"""

async def main():
    service = await get_service()
    df = await read_table_id(service, SS_ID, TAB_NAME)

    for idx, row in df.iterrows():
        print('\n-----------------------------------')
        interview = row['Собеседование']
        if interview:
            continue

        name = row['ФИО']
        print(name)
        salary = row['ЗП']
        print(salary)
        print('-----------------------------------')

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

        await append_data_to_sheet_cell(service, SS_ID, TAB_NAME, 'Андрей', idx + 2, result)








if __name__ == '__main__':
    asyncio.run(main())
