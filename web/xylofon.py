from flask import Blueprint, render_template
import paho.mqtt.client as mqtt



# index
bp_xylofon = Blueprint('xylofon', __name__)

def send(txt):
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

@bp_xylofon.route('/xylofon')
def xylofon():
    message = 'Ahoj'
    return render_template('xylofon.html', message=message)


@bp_xylofon.route('/xylofon_button_1', methods=["POST"])
def xylofon_button_1():
    print("tl.1")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "C1"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 1"
@bp_xylofon.route('/xylofon_button_2', methods=["POST"])
def xylofon_button_2():
    print("tl.2")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "D"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 2"
@bp_xylofon.route('/xylofon_button_3', methods=["POST"])
def xylofon_button_3():
    print("tl.3")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "E"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 3"
@bp_xylofon.route('/xylofon_button_4', methods=["POST"])
def xylofon_button_4():
    print("tl.4")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "F"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 4"
@bp_xylofon.route('/xylofon_button_5', methods=["POST"])
def xylofon_button_5():
    print("tl.5")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "G"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 5"
@bp_xylofon.route('/xylofon_button_6', methods=["POST"])
def xylofon_button_6():
    print("tl.6")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "A"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 6"
@bp_xylofon.route('/xylofon_button_7', methods=["POST"])
def xylofon_button_7():
    print("tl.7")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "H"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 7"
@bp_xylofon.route('/xylofon_button_8', methods=["POST"])
def xylofon_button_8():
    print("tl.8")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "C2"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 8"
@bp_xylofon.route('/xylofon_button_9', methods=["POST"])
def xylofon_button_9():
    print("tl.9")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "120,G,G,E,X,G,G,E,X,G,G,A,G,G,X,F,X,F,F,D,X,F,F,D,X,F,F,G,F,F,X,E,X,G,G,E,X,G,G,E,X,G,G,A,G,G,X,F,X,F,F,D,X,F,F,D,X,F,F,G,F,F,X,E,X"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 9"
@bp_xylofon.route('/xylofon_button_10', methods=["POST"])
def xylofon_button_10():
    print("tl.10")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "120,G,E,X,G,E,X,F,E,D,G,E,X,F,E,D,C1,D,E,F,E,D,D,C1,X,G,E,X,G,E,X,F,E,D,G,E,X,F,E,D,C1,D,E,F,E,D,D,C1,X"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 10"
@bp_xylofon.route('/xylofon_button_11', methods=["POST"])
def xylofon_button_11():
    print("tl.11")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "140,G,X,A,X,G,X,E,X,G,X,A,X,G,X,E,X,G,X,A,X,G,X,E,X,G,X,A,X,G,X,E,X,G,X,G,X,G,X,G,E,G,X,G,X,G,G,G,G,G,E,G,X,G,E,G,G,E,E,E,X"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 11"
@bp_xylofon.route('/xylofon_button_12', methods=["POST"])
def xylofon_button_12():
    print("tl.12")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "120,C1,X,E,X,G,X,C1,X,E,X,G,X,E,E,D,E,F,X,D,X,E,E,D,E,F,X,D,X,E,X,D,X,C1,X,C1,X,E,X,G,X,C1,X,E,X,G,X,E,E,D,E,F,X,D,X,E,E,D,E,F,X,D,X,E,X,D,X,C1,X"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 12"
@bp_xylofon.route('/xylofon_button_13', methods=["POST"])
def xylofon_button_13():
    print("tl.13")
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    txt = "120,G,G,A,G,G,G,A,G,G,G,A,G,G,G,A,G,F,F,F,F,E,E,E,X,D,D,G,G,C,C,C,X,G,G,A,G,G,G,A,G,G,G,A,G,G,G,A,G,F,F,F,F,E,E,E,X,D,D,G,G,C,C,C,X"
    client.publish(f'kapfela/xylofon/button', txt)
    client.disconnect()

    return "Vse OK - Button 13"


