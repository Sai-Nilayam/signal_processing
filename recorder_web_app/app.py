from flask import Flask, render_template, request
import json
import librosa
import numpy as np
import soundfile as sf
import os
import shutil
import datetime
import traceback
import audio2numpy as a2n
from pydub import AudioSegment
import getpass
import sys
import magic
import time
# import tensorflow as tf
from formatter import formatter

app = Flask(__name__)

# For testing only.
@app.route('/test')
def test():
	html_content = '<h1>This is test</h1>'
	return html_content

@app.route('/')
def index():
	# html_content = open('static/htmls/index.html', 'r').read()
	return "Try out the URL 'https://prefix.domain_name.extension/signal_processing'"

# For testing only.
@app.route('/signal_processing')
def signal_processing():
	html_content = open('static/htmls/signal_processing.html', 'r').read()
	return html_content

# For system_1.
# Getting all the text codes from the python file.
f = open('apis/system_1.py', 'r')
text_code = f.read()
exec(text_code)
f.close()

# For system_2.
# Getting all the text codes from the python file.
f = open('apis/system_2.py', 'r')
text_code = f.read()
exec(text_code)
f.close()

# For system_2_a.
# Getting all the text codes from the python file.
f = open('apis/system_2_a.py', 'r')
text_code = f.read()
exec(text_code)
f.close()

# For system_3.
# Getting all the text codes from the python file.
f = open('apis/system_3.py', 'r')
text_code = f.read()
exec(text_code)
f.close()

# For TTS public service.
f = open('apis/system_5.py', 'r')
text_code = f.read()
exec(text_code)
f.close()

if __name__ == '__main__':
	# app.run(debug=True, port=8000)
	app.run(debug=True, host='0.0.0.0')
	# app.run(debug=True, host='127.0.0.1')