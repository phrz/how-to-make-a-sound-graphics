import sys
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
	# 'table_frames.txt'
	with open(sys.argv[2], 'wb') as f:
		f.write(request.data)
	print('terminating')
	proc.kill()
	shutdown_server()

if __name__ == '__main__':
	global proc
	chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
	# 'table.html'
	proc = subprocess.Popen([chrome, sys.argv[1]])

	print('running')
	app.run(debug=False, host='localhost', port='3333')