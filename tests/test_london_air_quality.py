"""
Test london_tube_stats with pytest.
"""
import requests_mock
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
import london_air_quality as laq

def test_request_data():
    with requests_mock.Mocker() as mock_req:
        url = laq.LAQ_HOURLY_URL
        mock_req.get(url, text=json.loads("tests/hourly.json"))
        hourly_data_raw = laq.request_data(url)
        assert len(hourly_data_raw.keys()) == 33
