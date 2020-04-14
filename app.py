import requests
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
app.config['DEBUG'] = True
ACCESS_TOKEN = '6576252f0198cbfd67c388ed9d33d4ab'
DEFAULT_CITY = 'Нижний Новгород'

def return_weather(access_key, city):
    params = {
            'access_key': access_key,
            'query': city
        }

    error_flag = False
    weather = {
            'city' : " - ",
            'temperature' : "0",
            'precip' : " - ",
            'pressure' : " - ",
            'weather_descriptions' : " - ",
            'icon' : " - ",
            'clothes' : "else"
            }

    api_result = requests.get('http://api.weatherstack.com/current', params)
    api_response = api_result.json()
    try:
        temperature = int(api_response['current']['temperature'])
        clothes = "else"

        def get_temp_description(temp):
            return {
                temp < -15: 'minus15',
                -15 <= temp < 0:   'minus0',
                  0 <= temp < 10:  'plus10',
                 10 <= temp < 20:  'plus20',
                 20 <= temp:       'plus50'
            }[True]
        
        try:
            clothes = get_temp_description(temperature)
        except TypeError:
            clothes = "else"
        
        weather = {
            'city' : api_response['location']['name'],
            'temperature' : api_response['current']['temperature'],
            'precip' : api_response['current']['precip'],
            'pressure' : api_response['current']['pressure'],
            'weather_descriptions' : api_response['current']['weather_descriptions'][0],
            'icon' : api_response['current']['weather_icons'][0],
            'clothes' : clothes,
            }
    except KeyError:
        error_flag = True
    return weather, error_flag

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_default, error_flag_default = return_weather(ACCESS_TOKEN, DEFAULT_CITY)
    if request.method == 'POST':
        city = request.form.get('city')
        print(city)
        weather, error_flag = return_weather(ACCESS_TOKEN, city)
        print(weather)
        if error_flag == True:
            return render_template('error.html')
        else:
            return render_template('other_city.html', weather=weather)
    if error_flag_default == True:
            return render_template('error_on_default.html')
    return render_template('index.html', weather=weather_default)

@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def error_403(e):
    return render_template('403.html'), 403

@app.errorhandler(500)
def error_500(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)