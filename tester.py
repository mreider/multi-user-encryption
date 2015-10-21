# -*- coding: utf-8 -*-
import requests


def test_get_data(url, user, password):
    payload = {'user': user, 'password': password}
    response = requests.get(url, params=payload)
    print response.text


def test_set_data(data_string, url, user, password):
    payload = {"user": user, "password": password, "content": data_string}
    response = requests.post(url, data=payload)
    print response.status_code

def test_rotate_data(url, user, password):
    payload = {"user": user, "password": password}
    response = requests.get(url, params=payload)
    print response.status_code
    print response.text


if __name__ == '__main__':
    data = "Some hello world String"
    url = "http://localhost:8000/api/v1.0/data"
    user = "Jim"
    password = "bunny"
    test_set_data(data, url, user, password)

    user = "Bill"
    password = "gopher"

    test_get_data(url, user, password)

    user = "Root"
    password = "password"
    test_get_data(url, user, password)

    url = "http://localhost:8000/api/v1.0/rotate"
    test_rotate_data(url,user,password)