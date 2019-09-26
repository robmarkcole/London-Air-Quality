"""
Test london_tube_stats with pytest.
"""
import requests_mock
import json
import sys
import os

this_directory = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(this_directory))
import london_air_quality as laq

def test_request_data():
    """
    Test that the request returns the AI data.
    """
    with open(this_directory + '/hourly.json') as json_file:
        api_hourly_json = json.load(json_file)

    with requests_mock.Mocker() as mock_req:
        url = laq.LAQ_HOURLY_URL
        mock_req.get(url, json=api_hourly_json)
        hourly_data_raw = laq.request_data(url)
        assert len(hourly_data_raw['HourlyAirQualityIndex']['LocalAuthority']) == 33
