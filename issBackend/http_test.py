# -*- coding: utf-8 -*-

import requests
BASE_URL = 'http://localhost:8024/'


def get_users_info():
    # use 'get' to get data from users endpoint
    r = requests.get(BASE_URL + 'images/', auth=('belter', 'password123'))
    print(r.status_code)
    print(r.content)


def add_user():
    # add new user by 'post'
    new_user = {'username': 'xiaoming', 'email': 'xiaoming@126.com'}
    r = requests.post(BASE_URL + 'users/', auth=('admin', 'password123'), data=new_user)
    print(r.status_code)
    print(r.content)


def get_all_method():
    # check all of the method supported by this endpoint(url)
    verbs = requests.options(BASE_URL + 'images/')
    print(verbs.headers['allow'])


def test_post_permission():
    # add new user by 'post'
    file = {'file': ('slogan-and-logo.png',
                     open(r"E:\test\slogan-and-logo.png", 'rb'),
                     'image/png', {'Expires': '0'})}
    new_snippets = {'title': 'xiaoming',
                    'code': 'print("Hurry up")',
                    'language': 'python',
                    'style': 'friendly'}
    r = requests.post('http://localhost:8024/snippets/', auth=('belter', ''), data=new_snippets)
    r2 = requests.post('http://localhost:8024/snippets/', auth=('belter', 'password123'), data=new_snippets)
    print(r.status_code)
    print(r.content)
    print(r2.status_code)
    print(r2.content)

get_users_info()
get_all_method()
# test_post_permission()
