# homeassistant-mi-water-purifier
XiaoMi Water Purifier component for Home Assistant.
model：yunmi.waterpuri.lx11

![Screenshot1](https://raw.githubusercontent.com/bit3725/homeassistant-mi-water-purifier/master/images/screenshot1.png)
![Screenshot2](https://raw.githubusercontent.com/bit3725/homeassistant-mi-water-purifier/master/images/screenshot2.png)
![Screenshot3](https://raw.githubusercontent.com/bit3725/homeassistant-mi-water-purifier/master/images/screenshot3.png)

## Installation
1. Install HACS in HA.
2. Install the integration in HACS by adding custom repo: `ptbsare/homeassistant-mi-water-purifier`
3. Follow [Retrieving the Access Token](https://home-assistant.io/components/vacuum.xiaomi_miio/#retrieving-the-access-token) guide to get the token of your sensor

## Configuration
```yaml
sensor:
  - platform: mi_water_purifier
    host: YOUR_SENSOR_IP
    token: YOUR_SENSOR_TOKEN
    name: YOUT_SENSOR_NAME
```

```yaml
xiaomi_water_purifier:
  name: 厨房净水器
  icon: mdi:water
  entities:
    - sensor.zi_lai_shui
    - sensor.guo_lu_zhi_yin_shui
    - sensor.jin_shui_wen_du
    - sensor.qian_zhi_ppmian_lu_xin
    - sensor.chun_shui_rolu_xin
    - sensor.hou_zhi_fu_he_tan_lu_xin
```
