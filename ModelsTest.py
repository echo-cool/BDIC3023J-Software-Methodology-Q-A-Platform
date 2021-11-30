import os
import unittest
from app import models


class TestModels(unittest.TestCase):

    def testExist(self):
        self.assertIsNotNone(models.db)
        self.assertIsNotNone(models.User)
        self.assertIsNotNone(models.Role)
        self.assertIsNotNone(models.Permission)
        self.assertIsNotNone(models.Post)
        self.assertIsNotNone(models.AnonymousUser)
        self.assertIsNotNone(models.Collect)
        self.assertIsNotNone(models.Comment)
        self.assertIsNotNone(models.Follow)
        self.assertIsNotNone(models.Like)
        self.assertIsNotNone(models.Activity)
        self.assertIsNotNone(models.Notification)
        self.assertIsNotNone(models.Want)

    def testApp(self):
        from app import create_app
        self.assertIsNotNone(create_app(os.getenv('FLASK_CONFIG') or 'default'))

    def testWeb(self):
        from app import create_app
        app = create_app(os.getenv('FLASK_CONFIG') or 'default')
        app.testing = True
        self.client = app.test_client()
        self.assertIsNotNone(self.client)
        response = app.test_client().get('/', data={})
        self.assertEqual(response.status_code, 200)
        response = app.test_client().get('/trans', data={})
        self.assertEqual(response.status_code, 308)

        response = app.test_client().get('/trans', data={})
        self.assertEqual(response.status_code, 308)

        response = app.test_client().get('/act', data={})
        self.assertEqual(response.status_code, 308)

        response = app.test_client().get('/foll', data={})
        self.assertEqual(response.status_code, 308)

        response = app.test_client().get('/query/s', data={})
        self.assertEqual(response.status_code, 200)

        response = app.test_client().post('/query/s', data={
            "inf": "hi"
        })
        self.assertIsNotNone(response.data)

        response = app.test_client().get('/query-user', data={})
        self.assertEqual(response.status_code, 200)

        response = app.test_client().get('/query-transaction', data={})
        self.assertEqual(response.status_code, 200)

        response = app.test_client().post('/query-transaction', data={
            "transaction": 1
        })
        self.assertIsNotNone(response.data)

        response = app.test_client().get('/user/bross', data={})
        self.assertEqual(response.status_code, 200)

        response = app.test_client().get('/auth/logintest', data={})
        response = app.test_client().post('/auth/logintest', data={})
        response = app.test_client().get('/auth/login', data={})
        response = app.test_client().post('/auth/login', data={})
        response = app.test_client().get('/auth/album', data={})

        response = app.test_client().get('/auth/guidance', data={})
        response = app.test_client().get('/auth/music', data={})
        response = app.test_client().get('/auth/logout', data={})
        response = app.test_client().get('/auth/register', data={})
        response = app.test_client().post('/auth/register', data={})
        response = app.test_client().get('/auth/unconfirmed', data={})
        response = app.test_client().get('/auth/confirm/0s33h2432hjk432h4kj3', data={})
        response = app.test_client().get('/auth/confirm', data={})
        response = app.test_client().get('/auth/reset', data={})
        response = app.test_client().post('/auth/reset', data={})
        response = app.test_client().get('/auth/reset/dfsfsdff3f3eef', data={})
        response = app.test_client().post('/auth/reset/dfsfsdff3f3eef', data={})
        response = app.test_client().get('/auth/change-password', data={})
        response = app.test_client().post('/auth/change-password', data={})

        response = app.test_client().get('/auth/change_email', data={})
        response = app.test_client().post('/change_email', data={})

        response = app.test_client().get('/auth/change_email/32hgj32ghg4jh2g34hjg23jg4jh23', data={})
        response = app.test_client().post('/auth/change_email/32hgj32ghg4jh2g34hjg23jg4jh23', data={})

        response = app.test_client().post('/', data={})
        response = app.test_client().post('/query/s', data={})
        response = app.test_client().post('/query/s', data={
            "inf": "hi"
        })
        response = app.test_client().post('/query-user', data={})
        response = app.test_client().post('/query-transaction', data={})
        response = app.test_client().post('/query-transaction', data={
            "transaction": 1
        })
        response = app.test_client().post('/user/bross', data={})


if __name__ == '__main__':
    unittest.main()
