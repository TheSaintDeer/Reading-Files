from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class RequestTests(APITestCase):

    def setUp(self):
        self.uuidfile_ok = "0514091c-8ea2-43f5-8c21-cddc722f703b"
        self.uuidfile_error = "0514091c-8ea2-43f5-8c21-cddc722f703c"
        self.statfile = {
            "name": "0514091c-8ea2-43f5-8c21-cddc722f703b.txt",
            "size": 5,
            "mimetype": "text/plain",
            "create_datetime": "2024-10-17T16:53:59.987253"
        }
        self.contentfile = "Hello"
    
    def test_filestat_ok(self):
        '''Test for reading metadata of an existing file'''

        response = self.client.get(f"/file/{self.uuidfile_ok}/stat/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.statfile)

    def test_filestat_error(self):
        '''Test for reading metadata of a non-existent file'''

        response = self.client.get(f"/file/{self.uuidfile_error}/stat/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fileread_ok(self):
        '''Test for reading an existing file'''

        response = self.client.get(f"/file/{self.uuidfile_ok}/read/")
        content = list(response.streaming_content)[0].decode("utf-8")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content, self.contentfile)

    def test_fileread_error(self):
        '''Test for reading a non-existent file'''
        
        response = self.client.get(f"/file/{self.uuidfile_error}/read/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)