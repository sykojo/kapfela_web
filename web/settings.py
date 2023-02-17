from flask import Blueprint, render_template, request, flash
import json
import paho.mqtt.client as mqtt

from .modules.instrument import get_song
from .alive import InstrumentAlive

# index
bp_settings = Blueprint('settings', __name__)


@bp_settings.route('/settings_visualization', methods=['POST', 'GET'])
def settings_visualization():
    '''
        Gets color data from form http request
        and publishes them on topics for changing color
    '''
    on_press_color = '#FF0000'
    background_color = '#0000FF'
    client = mqtt.Client()
    alive = InstrumentAlive()
    client.on_publish = alive.mqtt_on_publish
    client.connect("localhost", 1883, 60)

    if request.method == 'POST':
        on_press_color = request.form.get('on-press-color', '')
        background_color = request.form.get('background-color', '')
        print(f"On press color HEX: {on_press_color}")
        print(f"Background color HEX: {background_color}")
        '''
        on_press_color = hex_to_rgb(on_press_color)
        background_color = hex_to_rgb(background_color)
        on_press_color = str(on_press_color)
        background_color = str(background_color)
        print(f"On press color RGB: {on_press_color}")
        print(f"Background color RGB: {background_color}")
        '''

        client.publish("kapfela/vizualizace/set_color_on_fret_press", on_press_color)
        client.publish('kapfela/vizualizace/set_background_color', background_color)

        '''If message was sent to broker successfully, flashes a message to the user. Else displays an error '''
        if client.on_publish:
            flash(
                f"Background color was successfully changed to: {background_color} \n Fret color was successfully changed to : {on_press_color}",
                category='success')
        else:
            flash(f"Error!", category='error')

    client.disconnect()

    return render_template('settings/visualization.html', on_press_color=on_press_color, background_color=background_color)


@bp_settings.route('/settings_ukulele', methods=['POST', 'GET'])
def settings_ukulele():
    '''
        Gets ukulele pics range from form http request
        and publishes them on topics for set pics range
    '''
    angle_pics_low = [75, 75, 75, 75]
    angle_pics_high = [105, 105, 105, 105]
    low_keys_str = ('angle_low_1', 'angle_low_2', 'angle_low_3', 'angle_low_4')
    high_keys_str = ('angle_high_1', 'angle_high_2', 'angle_high_3', 'angle_high_4')

    client = mqtt.Client()
    alive = InstrumentAlive()
    client.on_publish = alive.mqtt_on_publish
    client.connect("localhost", 1883, 60)

    if request.method == 'POST':
        for i in range(4):
            angle_pics_low[i] = request.form.get(low_keys_str[i], '')
            print(
                f'vychozi uhel {i}. trsatka vycten z fomrulare {low_keys_str[i]}, byl nastaven na {angle_pics_low[i]}')
            angle_pics_high[i] = request.form.get(high_keys_str[i], '')

        angle_pics_low_json = json.dumps(angle_pics_low)
        angle_pics_high_json = json.dumps(angle_pics_high)

        client.publish("kapfela/uku/set_angle_pics_low", angle_pics_low_json)
        client.publish('kapfela/uku/set_angle_pics_high', angle_pics_high_json)

        '''If message was sent to broker successfully, flashes a message to the user. Else displays an error '''
        if client.on_publish:
            flash(
                f"Low angles is successfully changed to: {angle_pics_low} \n High angle is successfully changed to: {angle_pics_high}",
                category='success')
        else:
            flash(f"Error!", category='error')

    client.disconnect()

    return render_template('settings/ukulele.html', angle_pics_low=angle_pics_low, angle_pics_high=angle_pics_high)
