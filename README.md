# Sensor 2 GPS Tracker for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/default)

A custom Home Assistant integration that combines separate sensors for latitude, longitude, altitude, and speed into a native `device_tracker` entity.

This is especially useful for hardware like LTE/GPS routers (e.g., Teltonika RUT series), Modbus devices, MQTT entities, or custom ESPHome setups that expose GPS coordinates as individual sensors instead of a unified tracker entity.

## Features

- 🛰️ **Native Device Tracker:** Generates a real `device_tracker` entity compatible with integrations requiring location trackers (e.g., DWD Weather, Home Assistant Zones).
- ⚙️ **Config Flow (UI Setup):** Easily configure and select your sensors directly via the Home Assistant user interface.
- 📐 **Flexible Sensor Mapping:**
  - Latitude (Required)
  - Longitude (Required)
  - Altitude (Optional)
  - Speed (Optional)
- 🚀 **HACS Compatible:** Easy installation and updates through HACS.

## Installation

### Method 1: HACS (Recommended)

1. Open **HACS** in your Home Assistant instance.
2. Click on the three dots in the top right corner and select **Custom repositories**.
3. Add the URL of this repository: `https://github.com/YOUR_USERNAME/YOUR_REPOSITORY`
4. Select **Integration** as the Category and click **Add**.
5. Search for **Sensor 2 GPS Tracker** in HACS and click **Download**.
6. Restart Home Assistant.

### Method 2: Manual Installation

1. Copy the `custom_components/sensor_2_gps` folder from this repository into your Home Assistant `/config/custom_components/` directory.
2. Restart Home Assistant.

## Setup & Configuration

1. Go to **Settings** -> **Devices & Services** in Home Assistant.
2. Click **Add Integration** in the bottom right corner.
3. Search for **Sensor 2 GPS Tracker**.
4. Configure your tracker:
   - **Name:** Enter a name for the device tracker (e.g., `Camper GPS`).
   - **Latitude Sensor:** Select your latitude sensor entity.
   - **Longitude Sensor:** Select your longitude sensor entity.
   - **Altitude Sensor:** (Optional) Select your altitude sensor entity.
   - **Speed Sensor:** (Optional) Select your speed sensor entity.
5. Submit the form. A new `device_tracker` entity will be created.

## How It Works

The integration listens to state changes of the selected source sensors and dynamically updates the `latitude`, `longitude`, and `altitude` attributes of the target `device_tracker` entity. Additional details like speed are stored as extra state attributes.

## License

This project is licensed under the MIT License.


<a href="https://www.buymeacoffee.com/hflocki" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me a Coffee" height="60" width="217">
</a>
