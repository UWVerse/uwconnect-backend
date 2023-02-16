"""
import unittest
import requests

class TestApp(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Setup the Base url link
        self.BASE_URL = "http://localhost:5000" 
        
    def test_get_all_requests(self):
        response = requests.get('%s/request' % (self.BASE_URL))
        self.assertIsTrue(response.ok)
"""
