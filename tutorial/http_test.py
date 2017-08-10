# -*- coding: utf-8 -*-

import requests


def get_users_info():
    # use 'get' to get data from users endpoint
    r = requests.get('http://localhost:8024/users/', auth=('admin', 'password123'))
    print(r.status_code)
    print(r.content)


def add_user():
    # add new user by 'post'
    new_user = {'username': 'xiaoming', 'email': 'xiaoming@126.com'}
    r = requests.post('http://localhost:8024/users/', auth=('admin', 'password123'), data=new_user)
    print(r.status_code)
    print(r.content)


def get_all_method():
    # check all of the method supported by this endpoint(url)
    verbs = requests.options('http://localhost:8024/users/')
    print(verbs.headers['allow'])

get_users_info()
get_all_method()

