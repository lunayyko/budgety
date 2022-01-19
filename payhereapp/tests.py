# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest, json, bcrypt, jwt, datetime
from unittest          import mock

from django.test       import Client, TestCase
from django.conf       import settings
from my_settings       import SECRET_KEY, ALGORITHM

from .models           import User, Book



class BookViewTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.test_user = User.objects.create(
            id       = 1,
            email    = 'wecode@wecode.com',
            password = 'wecode12#',
        )
        
        self.mocked_date_time = datetime.datetime(2021,1,1,0,0,0)

        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=self.mocked_date_time)):
            Book.objects.create(
                user_id    = 1,
                memo       = '극락조',
                amount     = '-50000',
            )
            Book.objects.create(
                user_id    = 1,
                memo       = '월급',
                amount     = '2500000',
            )

    def tearDown(self):
        User.objects.all().delete(),
        Book.objects.all().delete()

    def test_book_get_success(self):
        access_token = jwt.encode(
            {"user_id": self.test_user.id}, SECRET_KEY, ALGORITHM
        )

        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}

        response = client.get("/book", **header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), 
            {
                "results": [
                    {
                        "book_id"    : 1,
                        "created_at" : self.mocked_date_time.strftime('%Y-%m-%d'),
                        "updated_at" : self.mocked_date_time.strftime('%Y-%m-%d'),
                        "amount"     : -50000,
                        "memo"       : '극락조',
                    },
                    {
                        "book_id"    : 2,
                        "created_at" : self.mocked_date_time.strftime('%Y-%m-%d'),
                        "updated_at" : self.mocked_date_time.strftime('%Y-%m-%d'),
                        "amount"     : 2500000,
                        "memo"       : '월급',
                    }
                ],
                "total": {
                    "amount__sum": 2450000
                }
            }
        )