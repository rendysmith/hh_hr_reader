from urllib.parse import urlparse, parse_qs
async def pars_resume_id(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    resume_id = path_parts[2]  # Берем часть после /resume/
    #print(resume_id)  # Вывод: 655e1d4b0009ee68a40016c12667647a48794b
    return resume_id