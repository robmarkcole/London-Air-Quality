from datetime import timedelta
import requests
from typing import List, Dict

AUTHORITIES = [
    "Barking and Dagenham",
    "Barnet",
    "Bexley",
    "Brent",
    "Bromley",
    "Camden",
    "City of London",
    "Croydon",
    "Ealing",
    "Enfield",
    "Greenwich",
    "Hackney",
    "Hammersmith and Fulham",
    "Haringey",
    "Harrow",
    "Havering",
    "Hillingdon",
    "Hounslow",
    "Islington",
    "Kensington and Chelsea",
    "Kingston",
    "Lambeth",
    "Lewisham",
    "Merton",
    "Newham",
    "Redbridge",
    "Richmond",
    "Southwark",
    "Sutton",
    "Tower Hamlets",
    "Waltham Forest",
    "Wandsworth",
    "Westminster",
]

LAQ_HOURLY_URL = (
    "http://api.erg.kcl.ac.uk/AirQuality/Hourly/MonitoringIndex/GroupName=London/Json"
)

TIMEOUT = 10


class LondonAirQualityException(Exception):
    pass


def request_data(url: str, timeout: int = TIMEOUT) -> Dict:
    """
    Request data from a URL and return valid data as dictionary.
    """
    try:
        response = requests.get(url, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            raise LondonAirQualityException(
                f"Status code {response.status_code} returned from {url}"
            )

    except requests.exceptions.Timeout:
        raise LondonAirQualityException(
            f"Request timeout, current timeout is {timeout} seconds"
        )

    except requests.exceptions.ConnectionError as exc:
        raise LondonAirQualityException(f"Internet connection error: {exc}")


def parse_hourly_response(hourly_response: Dict) -> Dict:
    """
    Return hourly response data to index by Borough.
    Allows filtering authorities with no data, and cleans up some data structure.
    """
    data = dict.fromkeys(AUTHORITIES)
    for authority in AUTHORITIES:
        try:
            for entry in hourly_response["HourlyAirQualityIndex"]["LocalAuthority"]:
                if entry["@LocalAuthorityName"] == authority:

                    if isinstance(entry["Site"], dict):
                        entry_sites_data = [entry["Site"]]
                    else:
                        entry_sites_data = entry["Site"]

                    data[authority] = parse_site(entry_sites_data)
        except Exception:
            data[authority] = {}
    return data


def parse_species(species_data: List[Dict]) -> List[Dict]:
    """Iterate over list of species at each site."""
    parsed_species_data = []
    quality_list = []
    for species in species_data:
        if species["@AirQualityBand"] != "No data":
            species_dict = {}
            species_dict["description"] = species["@SpeciesDescription"]
            species_dict["code"] = species["@SpeciesCode"]
            species_dict["quality"] = species["@AirQualityBand"]
            species_dict["index"] = species["@AirQualityIndex"]
            species_dict["summary"] = (
                species_dict["code"] + " is " + species_dict["quality"]
            )
            parsed_species_data.append(species_dict)
            quality_list.append(species_dict["quality"])
    return parsed_species_data, quality_list


def parse_site(entry_sites_data: List[Dict]) -> List[Dict]:
    """Iterate over all sites at an local authority and tidy the data."""
    authority_data = []
    for site in entry_sites_data:
        site_data = {}
        species_data = []

        site_data["updated"] = site["@BulletinDate"]
        site_data["latitude"] = site["@Latitude"]
        site_data["longitude"] = site["@Longitude"]
        site_data["site_code"] = site["@SiteCode"]
        site_data["site_name"] = site["@SiteName"].split("-")[-1].lstrip()
        site_data["site_type"] = site["@SiteType"]

        if isinstance(site["Species"], dict):
            species_data = [site["Species"]]
        else:
            species_data = site["Species"]

        parsed_species_data, quality_list = parse_species(species_data)

        if not parsed_species_data:
            parsed_species_data.append("no_species_data")
        site_data["pollutants"] = parsed_species_data

        if quality_list:
            site_data["pollutants_status"] = max(
                set(quality_list), key=quality_list.count
            )
            site_data["number_of_pollutants"] = len(quality_list)
        else:
            site_data["pollutants_status"] = "no_species_data"
            site_data["number_of_pollutants"] = 0

        authority_data.append(site_data)
    return authority_data


def get_hourly_data_flat(hourly_data: Dict) -> List[Dict]:
    all_data = []
    for authority in hourly_data.keys():
        for site in hourly_data[authority]:
            for pollutant in site["pollutants"]:
                try:
                    pollutant["borough"] = authority
                    pollutant["site_code"] = site["site_code"]
                    pollutant["site_name"] = site["site_name"]
                    pollutant["latitude"] = site["latitude"]
                    pollutant["longitude"] = site["longitude"]
                    pollutant["updated"] = site["updated"]
                    all_data.append(pollutant)
                except:
                    pass
    return all_data
