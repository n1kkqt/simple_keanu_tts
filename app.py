import os	
import gc
import json
import base64
from io import BytesIO
from tts import TextToSpeech
from scipy.io.wavfile import write
from flask import Flask, request, render_template, redirect, jsonify, send_from_directory

tts = TextToSpeech()
app = Flask(__name__)

'''@app.route('/', methods=['GET'])
def send_index():
	return send_from_directory('./www', "index.html")

@app.route('/<path:path>', methods=['GET'])
def send_root(path):
	return send_from_directory('./www', path)

@app.route('/play/text', methods=['POST'])
def play_play():

	content = request.form.get('text')#request.get_json(silent=True)
	text = json.loads(content)
	
	audio_out = tts.get_pronunciation(text)
	byte_file = BytesIO()
	write(byte_file, 48000, audio_out)
	byte_file = base64.b64encode(byte_file.getvalue())

	answer = {'wav':str(byte_file)[2:-1], 'len':str(len(audio_out) / 48000.0)}

	del byte_file
	gc.collect()
	return jsonify(answer)'''

@app.route('/play/text', methods=['POST'])
def play_play():
	answer = {"response": 'playtext'}
    
    return jsonify(answer)

@app.route('/', methods=['POST'])
def c():
	answer = {"response": 'c'}
    
    return jsonify(answer)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
	#app.run(debug=True, host='127.0.0.1', #0.0.0.0
	#	port=int(os.environ.get('PORT', 8080)))