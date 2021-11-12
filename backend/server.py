from flask import Flask, jsonify
app= Flask(__name__)
@app.route('/api/v1.0/test')
def test():
	return jsonify("Probando a ver si devuelve")
if __name__ == '__main__':
	app.run(debug=True)