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

VALID_BARKING = [
    {
        "updated": "2019-09-26 11:00:00",
        "latitude": "51.563752",
        "longitude": "0.177891",
        "site_code": "BG1",
        "site_name": "Rush Green",
        "site_type": "Suburban",
        "pollutants": ["no_species_data"],
        "pollutants_status": "no_species_data",
        "number_of_pollutants": 0,
    },
    {
        "updated": "2019-09-26 11:00:00",
        "latitude": "51.529389",
        "longitude": "0.132857",
        "site_code": "BG2",
        "site_name": "Scrattons Farm",
        "site_type": "Suburban",
        "pollutants": [
            {
                "description": "Nitrogen Dioxide",
                "code": "NO2",
                "quality": "Low",
                "index": "1",
                "summary": "NO2 is Low",
            },
            {
                "description": "PM10 Particulate",
                "code": "PM10",
                "quality": "Low",
                "index": "1",
                "summary": "PM10 is Low",
            },
        ],
        "pollutants_status": "Low",
        "number_of_pollutants": 2,
    },
]


def test_all():
    """
    Very lasy test of all.
    """
    with open(this_directory + "/hourly.json") as json_file:
        api_hourly_json = json.load(json_file)

    with requests_mock.Mocker() as mock_req:
        url = laq.LAQ_HOURLY_URL
        mock_req.get(url, json=api_hourly_json)
        hourly_data_raw = laq.request_data(url)

    hourly_data = laq.parse_hourly_response(hourly_data_raw)
    assert len(hourly_data) == 33
    assert hourly_data["Barking and Dagenham"] == VALID_BARKING
