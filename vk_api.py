import vk_api
import datetime
import time
import re

tok = 'vk1.a.xeg0gC7s2aColB_UDSG99WdOPzi3Hj1LO8m8l4S98NlQy-AaWEuCnipdJidrjyVLeaadc555_7HEWRZp-XHljB7frTeL9NkP4FmgpTUr1B1tgOk_bHa1Mnzc1l5u1FhDNdApg2iM8ltVOsQde6JhI1v0-bKLS2boDJUGnMygensAGOv-hKGSCUVadyaK-QSCKKmtC7KOuHM42-Fc8qzTRA'
# тут пока мой токен, но попозже можно поменять на левый
session = vk_api.VkApi(token=tok)
vk = session.get_api()
id = -200843593  # id группы
n = vk.wall.get(owner_id=id, count=10)  # единожды запускаем, чтобы получить время 10 сверху поста(можно и более нового)
last_time = datetime.datetime.utcfromtimestamp(n['items'][-1]['date'])


def GET_RELEVANT_POST(id):
    global last_time
    posts = []
    wall_posts = vk.wall.get(owner_id=id, count=5)  # получаем список постов(последние пять)
    for post in wall_posts['items'][::-1]:  # проходимся по списку постов, начиная с тех, что были пораньше выложены
        post_time = datetime.datetime.utcfromtimestamp(post['date'])
        if post_time > last_time and re.search(r'DSC_events', post['text']) is not None:  # смотрим, есть ли пост, который выложен после последнего, который мы рассмотрели
            last_time = post_time  # присваиваем нашей переменной время последнего выложенного поста
            if "attachments" in post.keys() and 'photo' in post['attachments'][0].keys():  # проверяем на наличие фотки
                    posts.append({'text': post['text'], 'photo': post['attachments'][0]['photo']['sizes'][4]['url']})
            else:
                posts.append({'text': post['text']})
    return posts


l = GET_RELEVANT_POST(id)
