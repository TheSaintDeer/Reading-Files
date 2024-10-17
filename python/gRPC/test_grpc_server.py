import unittest
from unittest.mock import patch, MagicMock
import grpc
import service_file_pb2
import service_file_pb2_grpc
from FileServicer import FileServicer
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

class TestFileService(unittest.TestCase):
    def setUp(self):
        self.service = FileServicer()

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.getctime')
    @patch('os.stat')
    @patch('mimetypes.guess_type')
    def test_stat_success(self, mock_guess_type, mock_stat, mock_getctime, mock_listdir, mock_exists):
        '''Test for reading metadata of an existing file'''

        mock_exists.return_value = True
        mock_listdir.return_value = ['0514091c-8ea2-43f5-8c21-cddc722f703b'] # name
        mock_getctime.return_value = datetime.datetime(2024, 10, 17, 16, 53, 59, 987253).timestamp() # create_datetime
        mock_stat.return_value.st_size = 5  # file size in bytes 
        mock_guess_type.return_value = ('text/plain', None)  # mimetype

        request = service_file_pb2.StatRequest(uuid=service_file_pb2.Uuid(value='0514091c-8ea2-43f5-8c21-cddc722f703b'))
        context = MagicMock()
        response = self.service.stat(request, context)

        self.assertEqual(response.data.name, '0514091c-8ea2-43f5-8c21-cddc722f703b')
        self.assertEqual(response.data.size, 5)
        self.assertEqual(response.data.create_datetime.ToDatetime(), datetime.datetime(2024, 10, 17, 16, 53, 59, 987253))
        self.assertEqual(response.data.mimetype, 'text/plain')

    @patch('os.listdir')
    @patch('os.path.exists')
    def test_stat_file_not_found(self, mock_exists, mock_listdir):
        '''Test for reading metadata of a non-existent file'''

        mock_exists.return_value = False
        mock_listdir.return_value = []

        request = service_file_pb2.StatRequest(uuid=service_file_pb2.Uuid(value='0514091c-8ea2-43f5-8c21-cddc722f703c'))
        context = MagicMock()
        response = self.service.stat(request, context)

        context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
        context.set_details.assert_called_once_with('File not found')
        self.assertIsNone(response)

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=b'Test')
    def test_read_success(self, mock_open, mock_listdir, mock_exists):
        '''Test for reading an existing file'''

        mock_exists.return_value = True
        mock_listdir.return_value = ['0514091c-8ea2-43f5-8c21-cddc722f703b'] # name 

        request = service_file_pb2.ReadRequest(uuid=service_file_pb2.Uuid(value='0514091c-8ea2-43f5-8c21-cddc722f703b'), size=1024)
        context = MagicMock()

        responses = list(self.service.read(request, context))

        self.assertEqual(responses[0].data.data, b'Test')

    @patch('os.listdir')
    @patch('os.path.exists')
    def test_read_file_not_found(self, mock_exists, mock_listdir):
        '''Test for reading a non-existent file'''
        
        mock_exists.return_value = False
        mock_listdir.return_value = []

        request = service_file_pb2.StatRequest(uuid=service_file_pb2.Uuid(value='0514091c-8ea2-43f5-8c21-cddc722f703c'))
        context = MagicMock()
        response = self.service.stat(request, context)

        context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
        context.set_details.assert_called_once_with('File not found')
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()
