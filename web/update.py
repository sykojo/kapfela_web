from flask import Blueprint, render_template,flash,redirect,Response,request
import subprocess
import os
import paho.mqtt.client as mqtt
from.alive import InstrumentAlive
import json

bp_update = Blueprint('update', __name__)



def git_pull(url, branch, directory):
    os.chdir(directory)
    subprocess.run(['git', 'pull', url, branch])

@bp_update.route("/update")
def update():
    return render_template("settings/update.html")

@bp_update.route("/pull_gui",methods=['POST','GET'])
def pull_gui():
    git_pull("git@gitlab.fel.zcu.cz:projekty/kapfela/gui.git", 'main','/var/www/kapfela/gui')
    flash(f"Succesfully pulled from 'Gui' repository",category='success')
    return redirect('/update')
    
@bp_update.route("/pull_microcontroller",methods=['POST','GET'])
def pull_microcontroller():
    git_pull('git@gitlab.fel.zcu.cz:projekty/kapfela/microcontroller.git', 'main','/var/www/kapfela/microcontroller')
    flash(f"Succesfully pulled from 'Microcontroller' repository",category='success')
    return redirect('/update')

@bp_update.route("/update/download_file/<path:folder>/<path:file>", methods=["GET"])
def download_file(folder,file):
    dir_path = f"/var/www/kapfela/microcontroller/{folder}"
    os.chdir(dir_path) 
    file_path = dir_path + '/' + file
    with open(file_path, "r") as f:
        f_content = f.read()
        
    #Make response object and send
    response = Response(f_content)
    response.headers["Content-Disposition"] = f"attachment; filename={file}"
    response.headers["Content-Type"] = "text/plain"
    return response

@bp_update.route("/update/get_filenames/<path:instrument>",methods=['GET'])
def serve_filenames(instrument):
    instrument_folder = "control_" + instrument 
    filenames_list = []
    dir_path_list = ("/var/www/kapfela/microcontroller/common",
                f"/var/www/kapfela/microcontroller/{instrument_folder}")
    for dir in dir_path_list:
        dir_files_list = os.listdir(dir)
        filenames_list.append(dir_files_list)
    
    filenames_list = json.dumps(filenames_list)
        
    return filenames_list
'''----------------Doděalat pomocí upraveného Alive--------------------------    
@bp_update.route("/send_to_device", methods=['POST','GET'])
def send_to_device():
    """Sends a MQTT message to a device to activate update function on the device """

    client = mqtt.Client()
    alive = InstrumentAlive()
    client.on_publish = alive.mqtt_on_publish
    client.connect("192.168.10.1", 1883, keepalive=60)
    instruments = ["cajon","uku"]
#dodělat ošetření  neúspěšnosti poslání (callback)    
    for instrument in instruments:
        client.publish(f"kapfela/{instrument}/update","")
        flash("Zařízení dostalo zprávu o tom, že má dojít k updatu...","success") 

    client.disconnect()
    return redirect("/update")
'''

'''
@bp_update.route("/info/<instrument>")
def info_card(instrument_name):
    name = instrument_name
    status = getStatus()
    
    return(render_template("update-instrument-card.html",name,status))
    '''