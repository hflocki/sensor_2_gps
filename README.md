# sensor_to_gps


´´´´ýaml
device_tracker:
  - platform: sensor_2_gps
    name: "Camper GPS"
    latitude_sensor: sensor.rut505_latitude
    longitude_sensor: sensor.rut505_longitude
    altitude_sensor: sensor.rut505_altitude   # Optional
    speed_sensor: sensor.rut505_speed         # Optional
´´´´
