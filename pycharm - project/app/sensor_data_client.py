from influxdb_client import InfluxDBClient
import pytz

# Configuration for InfluxDB access
url = 'http://10.115.1.215:8086'
# use "localhost" only via ssh tunnel
#url = 'http://localhost:8086'
token = 'VTW0L1vStqUoDfKcHqTmMO6Cg31rw-CnMxrg2PqK1974Fj0_cXyt3olZjIqUtQEFou4fgLI-_7_puToDjoNGnA=='
org = 'htld'
bucket = 'monitoring'

# This class encapusaltes the InfluxDB query for retrieving
# sensor values with their timestamps
# All those values are stored within a "monitoring" bucket
# Note: The url works only internally @HTL Dornbirn
class SensorDataClient:
    def __init__(self, url=url, token=token, org=org, bucket=bucket):
        """Initialize the client with necessary parameters."""
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.bucket = bucket
    @staticmethod
    def getCESTDateTime(timestamp):
        # time zone settings
        utc_zone = pytz.utc
        cet_zone = pytz.timezone('Europe/Vienna')  # Vienna time zone represents CET when applicable

        utc_dt = timestamp.replace(tzinfo=utc_zone)  # Assume the original time is in UTC
        cest_dt = utc_dt.astimezone(cet_zone)  # Convert to CEST
        return cest_dt
    def get_latest_rssi(self):
        """Retrieve the latest RSSI value and its timestamp."""
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -1h)  
          |> filter(fn: (r) => r["_measurement"] == "wifi_status")
          |> filter(fn: (r) => r["SSID"] == "HTL-S")
          |> filter(fn: (r) => r["_field"] == "rssi")
          |> filter(fn: (r) => r["device"] == "ESP32")
          |> last() 
        '''

        result = self.client.query_api().query(query)
        for table in result:
            for record in table.records:
                return self.getCESTDateTime(record.get_time()), record.get_value()
        return None, None  # Return None if no data is available


    def get_latest_pv_yield_power(self):
        """Retrieve the latest RSSI value and its timestamp."""
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -1h)  
          |> filter(fn: (r) => r["_measurement"] == "Vrmapi")
          |> filter(fn: (r) => r["_field"] == "yield_power_f")
          |> last() 
        '''

        result = self.client.query_api().query(query)
        for table in result:
            for record in table.records:
                return self.getCESTDateTime(record.get_time()), record.get_value()
        return None, None  # Return None if no data is available

    def close(self):
        """Close the InfluxDB client connection."""
        self.client.close()

    def get_latest_temperature(self):
        """Retrieve the latest Temperature value and its timestamp."""
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -1h)  
          |> filter(fn: (r) => r["_measurement"] == "env_sensor1")
          |> filter(fn: (r) => r["_field"] == "temperature")
          |> filter(fn: (r) => r["environment"] == "env_sensor1")
          |> last() 
        '''

        result = self.client.query_api().query(query)
        for table in result:
            for record in table.records:
                return self.getCESTDateTime(record.get_time()), record.get_value()
        return None, None  # Return None if no data is available
