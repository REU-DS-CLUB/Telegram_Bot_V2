from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import datetime

SCOPES = "https://www.googleapis.com/auth/drive"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage('token.json')
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)

form_service = discovery.build('forms', 'v1', http=creds.authorize(
    Http()), discoveryServiceUrl=DISCOVERY_DOC)

form_id = '1J6Z5vL9xk6sJ9tEz31G_XEY7mBPLsodXpZnjwsYVrUA'
result = form_service.forms().responses().list(
    formId=form_id).execute()


# переводит время из формата YYYY-MM-DDTH:M:S.MS в unix
def string_to_time(time: str) -> float:
    time = time[:-4]
    unix_time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.").timestamp()
    return unix_time


# проверяет актульаность ответа на форму
def check_actual(tmptime: float):
    if tmptime >= (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp():
        return True
    if tmptime < (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp():
        return False


# создает список дат ответов на форму
def get_response_time(self):
    create_times = []
    for i in range(len(result['responses'])):
        create_time = result['responses'][i]['createTime']
        create_times.append(create_time)
    return create_times


# создает список, состоящий из нужной информации о каждом кандидате
def get_candidate_info(self):
    info = []
    for i in range(len(result['responses'])):
        info_str = ""
        name = result['responses'][i]['answers']['4488b80d']['textAnswers']['answers'][0]['value']
        profession = result['responses'][i]['answers']['5a6a0108']['textAnswers']['answers'][0]['value']
        contact = result['responses'][i]['answers']['2cb8c2bc']['textAnswers']['answers'][0]['value']
        info_str = "ФИО: " + str(name) + "\n" + "Cпециальность: " + str(profession) + "\n" + "Контакт: " + str(contact)
        info.append(info_str)
        info_str = ""
    return info


# создает список информации об актуальных кандидатах
def get_relevant_info_list(self):
    create_times = get_response_time(result)
    info_list = []
    for i in range(len(create_times)):
        if check_actual(string_to_time(create_times[i])):
            info_list.append(get_candidate_info(result)[i])
    return info_list


# возвращает отформатированную ифнормацию об актуальных кандидатах
def get_relevant_forms(self):
    info_list = get_relevant_info_list(result)
    if info_list:
        str_info = "Пам-пам новые заявочки" + "\n"
        for i in range(len(info_list)):
            if len(info_list) != 1:
                str_info = str_info + str(info_list[i]) + "\n" + "==========================" + "\n"
            else:
                return str(info_list[i])
        return str_info
    else:
        return "Пам-пам никто не заполнил форму"










