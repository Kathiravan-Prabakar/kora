import random
import string
import sqlite3
from flask import Flask, render_template, jsonify, request, redirect, url_for, make_response

app = Flask(__name__)
db = sqlite3.connect("bot.db", check_same_thread=False)
cur = db.cursor()

@app.route("/")
def home():
	logged = request.cookies.get('uname')
	if logged:
		return render_template("logged.html", name=logged)
	else:
		return render_template("index.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():
	logged = request.cookies.get('uname')
	if logged:
		return redirect(url_for('home'))
	else:
		if request.method == 'POST':
			logged = request.cookies.get('uname')
			if logged:
				return redirect(url_for('home'))
			else:
				cur.execute("SELECT username FROM userData")
				names = []
				data = cur.fetchall()
				for each in data:
					names.append(each[0])
				uname = request.form.get('unameinp')
				pwd = request.form.get('pwdinp')
				if uname in names:
					return """<html><head><title>Error</title></head><body><script>alert('Username exists, try again with different username')</script></body>"""
				else:
					cur.execute("INSERT INTO userData(username, pwd) VALUES(?,?)", (uname, pwd))
					db.commit()
					resp = make_response(redirect(url_for('home')))
					resp.set_cookie('uname', uname)
					resp.set_cookie('pwd', pwd)
					return resp
		else:
			return render_template('signup.html')

@app.route("/signin", methods=['POST', 'GET'])
def signin():
	logged = request.cookies.get('uname')
	if logged:
		return redirect(url_for('home'))
	else:
		if request.method == 'POST':
			logged = request.cookies.get('uname')
			if logged:
				return redirect(url_for('home'))
			else:
				uname = request.form.get('unameinp')
				pwd = request.form.get('pwdinp')
				cur.execute('SELECT * FROM userData WHERE username = ?', (uname,))
				data = cur.fetchone()
				print(uname)
				print(data)
				if data is not None:
					if data[0] != uname and data[1] != pwd:
						return """<html><head><title>Error</title></head><body><script>alert('Username/Password is wrong.')</script></body>"""
					else:
						resp = make_response(redirect(url_for('home')))
						resp.set_cookie('uname', uname)
						resp.set_cookie('pwd', pwd)
						return resp
				else:
					return """<html><head><title>Error</title></head><body><script>alert('Given username is not in the database')</script></body>"""
		else:
			return render_template('signin.html')

@app.route("/signout")
def signout():
	logged = request.cookies.get('uname')
	if not logged:
		return redirect(url_for('signin'))
	else:
		resp = make_response(redirect(url_for('home')))
		resp.delete_cookie('uname')
		resp.delete_cookie('pwd')
		return resp

@app.route("/shorturl", methods=['POST', 'GET'])
def shorturl():
	if request.method == 'GET':
		logged = request.cookies.get('uname')
		if logged:
			return redirect(url_for('home'))
		else:
			return redirect(url_for('home'))
	else:
		name = request.cookies.get('uname')
		url = request.form.get('iurl')
		print(url)
		key = ''.join(random.choice(string.ascii_letters) for _ in range(4))
		cur.execute('INSERT INTO urlData(key, url) VALUES(?,?)', (key, url))
		db.commit()
		return render_template('key.html', name=name, url=f"http://127.0.0.1:5000/{key}")

@app.route("/<key>")
def redkey(key):
	if request.method == 'GET':
		logged = request.cookies.get('uname')
		if logged:
			cur.execute("SELECT url FROM urlData WHERE key = ?", (key,))
			data = cur.fetchone()
			if data is not None:
				return f"""<html><head></head><body><script>window.location.href = "{data[0]}"</script></body>"""
			else:
				return f"""<html><head><title>Error</title></head><body><script>alert('Given key({key}) is not in the database')</script></body>"""


if __name__ == '__main__':
	app.run()