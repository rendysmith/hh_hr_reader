import asyncio
import os

from utils.ai_module import get_answer_ai, get_answer_gemini
from requests.auth import HTTPBasicAuth

from utils.hh_module import get_resume_data

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
2 - Проведи максимально тщательный анализ резюме соискателя.
3 - Дай точную оценку, подходит ли нам данный соискатель. 
- Учти нужные нам навыки - мы ищем человека у которого есть практический навыки обучения и дообучения моделей. 
- Также обрати внимание сколько месте сменил соискатель и как часто он их менял.
- Оцени примерна на какую зарплату будет рассчитывать данный специалист (место работы Москва или remote)
- Выведи процент на сколько нам подходит данный соискатель.
4 - Дай очень краткий вывод своего анализа. Опиши свой результат 3-4 предложениями.
"""

async def main():
    resume_text = await get_resume_data('1d208fab000e60d5490016c126304e4469704a')
    #print(resume_text)

    prompt = prompt_text.format(resume_text=resume_text)


    result = await get_answer_gemini(prompt)
    #result = await get_answer_ai(auth, prompt)
    print(result)

if "__main__" in __name__:
    asyncio.run(main())