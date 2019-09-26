# London-Air-Quality
Queries the London air quality data feed provided by Kings College London via [Londonair.org](https://www.londonair.org.uk/LondonAir/Default.aspx). 

28 London Boroughs have monitoring sites at different geographical positions within the borough, and each of those sites can monitor up to six different kinds of pollutant. The pollutants are Carbon Monoxide (CO2), Nitrogen Dioxide (NO2), Ozone (O3), Sulfur Dioxide (SO2), PM2.5 & PM10 particulates. Nominally data is published hourly, but in my experience this can vary. 

## Development
* Use `venv` -> `python3 -m venv venv` then `source venv/bin/activate`
* `pip install -r requirements.txt`
* `pip install -r requirements-dev.txt`
* Run tests with `venv/bin/pytest tests/*`
* Black format with `venv/bin/black london_air_quality/*`
