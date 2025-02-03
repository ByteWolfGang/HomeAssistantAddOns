from flask import Flask, request, send_file, Response
import requests
import matplotlib
import matplotlib.pyplot as plt
import io
import datetime
import os

from matplotlib.dates import AutoDateLocator

app = Flask(__name__)

HA_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
HA_URL = "http://supervisor/core/api/history/period"

@app.route('/')
def root():
    return Response(status=302, headers={'Location': './chart'})

@app.route('/chart')
def doTheJob():
    entity_id = request.args.get('entity_id', os.getenv("default_entity_id"))
    if entity_id == None:
        return "No sensor entity_id provided.", 400
    
    picture_size_x = int(os.getenv("picture_size_x", 800))
    picture_size_y = int(os.getenv("picture_size_y", 600))
    background_color = os.getenv("background_color", "#FFFFFF")
    chart_background_color = os.getenv("chart_background_color", "#FFFFFF")
    chart_line_color = os.getenv("chart_line_color", "#0000FF")
    
    headers = {"Authorization": f"Bearer {HA_TOKEN}"}
    url = f"{HA_URL}"
    response = requests.get(url, headers=headers, params={"filter_entity_id": entity_id})
    if response.status_code != 200:
        return f"Error fetching data: {response.text}", 500

    data = response.json()
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No data found for the sensor", 404

    timestamps = []
    values = []
    einheit = "?"
    bezeichnung = "?"

    for entry in data[0]:
        try:
            ts = datetime.datetime.fromisoformat(entry['last_changed'])
            value = float(entry['state'])
            
            if not (isinstance(value, (int, float)) and value != float('inf') and value != float('-inf')):
                continue
                
            timestamps.append(ts)
            values.append(value)
        except (ValueError, AttributeError, TypeError):
            continue

    if not timestamps or not values:
        return "No valid data found.", 404

    einheit = data[0][0]['attributes']['unit_of_measurement']
    bezeichnung = data[0][0]['attributes']['friendly_name']

    last_value = str(data[0][-1]['state']).replace(".", ",")
    bezeichnung2 = f"{last_value} {einheit}"
    
    max_value = max(values)
    min_value = min(values)

    matplotlib.rcParams['timezone'] = 'Europe/Berlin'

    dpi = 100
    
    plt.figure(figsize=(picture_size_x/dpi, picture_size_y/dpi), dpi=dpi, facecolor=chart_background_color)
    plt.plot(timestamps, values, label=entity_id, color=chart_line_color, drawstyle='steps-post')

    ax = plt.gca()
    ax.set_facecolor(chart_background_color)
    ax.margins(x=0, y=0)

    y_range = max_value - min_value
    y_padding = y_range * 0.3
    ax.set_ylim(min_value - y_padding, max_value + y_padding)

    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Hh'))
    ax.xaxis.set_major_locator(plt.matplotlib.dates.HourLocator(interval=4))

    plt.fill_between(timestamps, min_value- y_padding, values, alpha=.15, color=chart_line_color, step='post')

    plt.grid(True, linestyle='--', alpha=0.15, color='gray')

    plt.text(0.5, 0.56, bezeichnung,
             color="gray",
             alpha=0.9,
             fontsize=12,
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)  
    plt.text(0.5, 0.51, bezeichnung2,
             color="gray",
             alpha=0.9,
             fontsize=12,
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes)  

    maximalwertbez = str(max_value)
    maximalwertbez = maximalwertbez.replace(".", ",")
    minimalwertbez = str(min_value)
    minimalwertbez = minimalwertbez.replace(".", ",")

    plt.annotate(f'{maximalwertbez} {einheit}', xy=(timestamps[values.index(max_value)], max_value), color='gray',
             xytext=(picture_size_x/2, picture_size_y-picture_size_y*.2),
                 textcoords='figure pixels', ha="center",
             arrowprops=dict(color='gray', arrowstyle='->'))

    plt.annotate(f'{minimalwertbez} {einheit}', xy=(timestamps[values.index(min_value)], min_value), color='gray',
             xytext=(picture_size_x/2, picture_size_y-picture_size_y*.8),
                 textcoords='figure pixels', ha="center",
             arrowprops=dict(color='gray', arrowstyle='->'))

    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=100, facecolor=background_color)  
    img.seek(0)
    plt.close()

    response = send_file(img, mimetype='image/png')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)