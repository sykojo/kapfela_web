from flask import Blueprint, redirect, render_template, request, flash
import os
from flask import jsonify
import json
import datetime

import time
import paho.mqtt.client as mqtt

from .modules.instrument import get_song
from .db import DB
from .alive import InstrumentAlive
import threading

# index
bp_index = Blueprint('index', __name__)


@bp_index.route('/')
def main():
    '''Main function, which renders index.html'''
    
    '''Alive initialization'''
    alive_ = InstrumentAlive()
    alive_.start()
    mqtt_thread = threading.Thread(target=alive_.start)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    
    '''Table of songs initialization'''
    db = DB()
    selection = db.selection()
    # split to artist and song
    try:
        [artist, song] = selection.split(" - ")
    except:
        [artist, song] = [selection, ""]

    songs = []
    dir = 'static/music/uku'
    for filename in os.listdir(dir):
        if os.path.isfile("{}/{}".format(dir, filename)):
            # fn
            fn, extension = os.path.splitext(filename)

            # counter
            db = DB()
            counter = db.counter(fn)

            # dict
            songs.append({"name": fn, "counter": counter})

    return render_template('index.html', selection=selection, artist=artist, songs=songs)


@bp_index.route('/counter_increase', methods=["GET"])
def counter_increase():
    if "song" in request.values:
        fn = request.values["song"]

        db = DB()
        db.counter_increase(fn)

    return redirect("/")


@bp_index.route('/song')
def song():
    db = DB()
    selection = db.selection()

    data = get_song("static/music/uku/{}.gp5".format(selection))

    # with open('data.txt', 'w') as outfile:
    #     json.dump(data, outfile)

    return jsonify(data)


@bp_index.route('/send_song', methods=["POST"])
def send_song():
    if "song" in request.values:
        song_fn = request.values["song"]
        client = mqtt.Client()
        client.connect("localhost", 1883, 60)
        instruments = {'uku','cajon','vizualizace'}
        start = time.time_ns()
        for instrument in instruments:
            try:
                notes = get_song(f'static/music/{instrument}/{song_fn}.gp5',start)
                print(f'static/music/{instrument}/{song_fn}.gp5 --------Passsed-------')
                json_notes = json.dumps(notes)
                print(f"{instrument} playing")
                client.publish(f'kapfela/{instrument}/play',json_notes)
            except:
                flash(f'Notes for {instrument} are not available')
                print(f'static/music/{instrument}/{song_fn}.gp5 --------Failed-------')
                
        client.disconnect()
        
        return f"JSON '{song_fn}' SENT"

    return "FAILED"


@bp_index.route('/stop_song', methods=["POST"])
def stop_song():
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.publish("kapfela/stop", "")
    client.disconnect()

    return "Song stopped."


@bp_index.route('/alphatab')
def alphatab():
    db = DB()
    selection = db.selection()

    return render_template('alphatab.html', filename="music/uku/{}.gp5".format(selection))


@bp_index.route("/alive", methods=['POST', 'GET'])
def alive():
    alive_ = InstrumentAlive()
    out = '<div class="text-center"><table class="table table-lm text-center display" id="songs">'
    out += '<thead class="thead-dark"s><tr><th class="text-left">Instrument</th><th>State</th><th>Time</th></tr></thead>'
    out += '<tbody>' 

    for instrument in alive_.instruments:
        state = instrument["state"]
        ts = int(instrument["time"])
        
        elapsed_time_last_message = alive_.current_time - ts - alive_.NTP_EPOCH_OFFSET
        formated_time = datetime.datetime.utcfromtimestamp(ts/1000000000).strftime("%H:%M:%S")
        
        if elapsed_time_last_message > alive_.MAX_TIME_DIFFERENCE or elapsed_time_last_message < -alive_.NTP_EPOCH_OFFSET:
            state = "Disconnected"
            
        print(instrument["name"])
        print(elapsed_time_last_message)
        out += f'<tr><td class="text-left">{instrument["name"]}</td><td>{state}</td><td>{formated_time}</td></tr>'

    return out




