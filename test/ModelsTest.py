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


if __name__ == '__main__':
    unittest.main()
