from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/test')
def test():
	return render_template('test.html')

# For system_1.
@app.route('/system_1/get_unique_words', methods=['POST'])
def get_unique_words():
	voice = request.form.get("voice")
	all_texts = request.form.get("voice")
	return str(voice)


if __name__ == '__main__':
	app.run(debug=True, port=8000)