from DarkSky import DarkSky

# initialize variables
jax_latitude = 30.183475
jax_longitude = -81.80263339999999
data_file_csv = 'weather_data.csv'
data_file_json = 'weather_data_json'

# get data
darksky1 = DarkSky(jax_latitude, jax_longitude, data_file_csv, data_file_json)
darksky_response = darksky1.get_weather_data()

# write data
darksky1.write_data_to_file(darksky_response)
