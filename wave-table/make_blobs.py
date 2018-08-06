import subprocess
from flask import Flask, request
app = Flask("blob-helper")

def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()

@app.route("/", methods=['POST'])
def listen():
	global proc
	print('got data:')
	with open('table_frames.txt', 'wb') as f:
		f.write(request.data)
	print('terminating')
	proc.kill()
	shutdown_server()

if __name__ == '__main__':
	global proc
	chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
	proc = subprocess.Popen([chrome, 'table.html'])

	print('running')
	app.run(debug=False, host='localhost', port='3333')