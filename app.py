from flask import Flask, send_from_directory
from logging import FileHandler, WARNING


from web.pages import bp_index
from web.settings import bp_settings
from web.xylofon import bp_xylofon
from web.update import bp_update

app = Flask(__name__)

file_handler = FileHandler('errorlog.txt')
file_handler. setLevel(WARNING)


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

app.register_blueprint(bp_index)
app.register_blueprint(bp_settings)
app.register_blueprint(bp_xylofon)
app.register_blueprint(bp_update)
app.config['SECRET_KEY'] = 'secret!'

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, host="0.0.0.0")