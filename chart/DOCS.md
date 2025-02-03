# Bitmap Chart Server Add-on Documentation

## Configuration

### Add-on Configuration

The add-on can be configured through the Home Assistant UI under Add-ons > Bitmap Chart Server > Configuration.

#### Option: `default_entity_id`
- Required: yes
- Type: string
- Default: `sensor.garten_wetterstation_actual_temperature`

The entity ID of the sensor you want to display by default. This should be a valid Home Assistant sensor entity ID.

#### Option: `picture_size_x`
- Required: yes
- Type: integer (1-4096)
- Default: `1024`

The width of the generated chart image in pixels.

#### Option: `picture_size_y`
- Required: yes
- Type: integer (1-4096)
- Default: `768`

The height of the generated chart image in pixels.

#### Option: `background_color`
- Required: yes
- Type: string (hex color code)
- Default: `"#FFFFFF"`

The background color of the image in hexadecimal format.

#### Option: `chart_background_color`
- Required: yes
- Type: string (hex color code)
- Default: `"#FFFFFF"`

The background color of the chart area in hexadecimal format.

#### Option: `chart_line_color`
- Required: yes
- Type: string (hex color code)
- Default: `"#00FF00"`

The color of the chart line and fill area in hexadecimal format.

## How to use

1. Install the add-on
2. Configure the options in the add-on configuration
3. Start the add-on
4. Access the chart through:
   - The Ingress interface in Home Assistant
   - Direct access via `http://your-home-assistant:5000/chart`
   - Using the entity_id parameter: `http://your-home-assistant:5000/chart?entity_id=sensor.your_sensor`

## Features

- Generates bitmap charts of sensor data for the last 24 hours
- Customizable chart dimensions and colors
- Shows min/max values with arrows
- Displays current value and sensor name
- 4-hour interval time grid
- Supports any numeric sensor entity

## Network

The add-on exposes the following ports:

| Port | Description |
|------|-------------|
| 5000 | Web interface |

## Security

The add-on uses Home Assistant's authentication system to ensure secure access to your data. All connections are protected by Home Assistant's authentication layer.

## Known issues and limitations

- Currently supports single sensor visualization at a time
- Shows only the last 24 hours of data
- Requires a valid Home Assistant sensor entity with numeric values
- Entity must have `unit_of_measurement` and `friendly_name` attributes

## Support

If you have any questions or need help, please open an issue on our GitHub repository.

## Authors & contributors

- Wolfgang Schneiderhan wolfgang@schneiderhan.com

## License

MIT License - see the LICENSE file for details