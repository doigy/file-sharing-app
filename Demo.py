'''
user names
encryption
compression
'''
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from threading import Timer
import os, threading, time, socket, webbrowser

app = Flask(__name__)

hostname = socket.gethostname()    
iph = socket.gethostbyname(hostname)

'''
@app.route('/'):
def sign_up():
	try:
		return render_template('user_name.html')
	except FileExistsError:
		return redirect('http://192.168.100.8:8000/', code = 302)
	except PermissionError:
		return redirect('http://192.168.100.8:8000/', code = 302)

@app.route('/', methods = ['GET', 'POST']):
def sign_up():
	global ip
	global ipv
	ip = request.environ['REMOTE_ADDR'] #Device ip
	ipv = request.remote_addr #Visitor ip

	try:
		usr_nme = request.form['user_name']
		usrnmefile = open(f'users/{ipv}/usr_nme.txt', 'w+')
		usrnmefile.write(usr_nme)
		return redirect('http://192.168.100.8:8000/home', code = 302)
	except FileExistsError:
		return redirect('http://192.168.100.8:8000/home', code = 302)
	except PermissionError:
		return redirect('http://192.168.100.8:8000/home', code = 302)
'''

@app.route('/')
def home():
	global filesdisplay
	global usersdisplay
	global process
	global ipv
	ipv = request.remote_addr #Visitor ip
	
	try:
		os.makedirs(f'users/{ipv}')
	except FileExistsError:
		pass

	'''
	0 - error
	1 - successful
	2 - default
	'''
	filesdisplay = os.listdir(f'users/{ipv}')
	usersdisplay = os.listdir('users')
	process = 2

	#Display list of users
	try:
		return render_template('home.html', process = process, filesdisplay = filesdisplay, usersdisplay = usersdisplay)
	except FileNotFoundError:
		return render_template('home.html', process = process, filesdisplay = filesdisplay, usersdisplay = usersdisplay)
	except PermissionError:
		return render_template('home.html', process = process, filesdisplay = filesdisplay, usersdisplay = usersdisplay)

@app.route('/', methods = ['GET', 'POST'])
def home_post():
	choice = request.form['option']

	if choice == 'existing':
		try:
			user = str(request.form['users_choice'])
			UPLOAD_FOLDER = f'users/{user}'
			app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
			file = request.files['file']
			#<compression - encryption>
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
			process = 1
			return render_template('home.html', process = process, filesdisplay = filesdisplay, usersdisplay = usersdisplay)
		except FileNotFoundError:
			process = 0
			return render_template('home.html', process = process, filesdisplay = filesdisplay, usersdisplay = usersdisplay)
		except PermissionError:
			process = 0
			return render_template('home.html', process = process, filesdisplay = filesdisplay, usersdisplay = usersdisplay)

	#Upload file for a new user
	elif choice == 'new':
		try:
			user_new = request.form['new_user']
			os.makedirs(f'users/{user_new}')
			UPLOAD_FOLDER = f'users/{user_new}'
			app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
			file = request.files['file']
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
			process = 1
			return render_template('home.html', process = process, filesdisplay = filesdisplay, usersdisplay = usersdisplay)
		except FileNotFoundError:
			process = 0
			return render_template('home.html', process = process, filesdisplay = filesdisplay, usersdisplay = usersdisplay)
		except PermissionError:
			process = 0
			return render_template('home.html', process = process, filesdisplay = filesdisplay, usersdisplay = usersdisplay)			

@app.route('/download', methods = ['GET', 'POST'])
def download():
	filedownload = request.form['files_choice']
	
	#Delete file after downloading
	'''
	def file_del():
		time.sleep(1)
		os.remove(f'users/{ipv}/{filedownload}')
	thread = threading.Thread(target = file_del)
	thread.start()
	'''

	return send_file(f'users/{ipv}/{filedownload}', as_attachment = True, attachment_filename = filedownload)

def Open_browser():
	#Set debug = False to prevent it from opening two tabs
	#Open browser tab
	webbrowser.open(f'http://{iph}:8000/')

if __name__ == '__main__':
	Timer(0.1, Open_browser).start()
	app.run(debug = True, host = '0.0.0.0', port = 8000)