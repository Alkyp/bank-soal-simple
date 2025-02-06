from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__, static_url_path="/static")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
app.config["SECRET_KEY"] = "R4h45la"

mysqlApp = MySQL(app)


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    return redirect(url_for('bank_soal'))


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        cursor = mysqlApp.connection.cursor()
        cursor.execute("select * from data_siswa where username = %s", (username,))
        acount = cursor.fetchone()
        print(acount)

        if check_password_hash(acount[2], password):
            session["username"] = username
            return redirect(url_for('bank_soal'))

        else:
            return "Gagal"
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        nisn = request.form.get('nisn')
        nama = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))

        cursor = mysqlApp.connection.cursor()
        cursor.execute('insert into data_siswa(nisn, username, password) VALUES (%s, %s, %s)', (nisn, nama, password))
        cursor.connection.commit()
        cursor.close()
        return redirect(url_for('login'))

    return render_template("register.html")


@app.route('/tambah-soal', methods=["GET", "POST"])
def inputSoal():
    opsi = ['a', 'b', 'c', 'd', 'e']
    if request.method == "POST":
        soal = request.form["soal"]
        a = request.form.get('a')
        b = request.form.get('b')
        c = request.form.get('c')
        d = request.form.get('d')
        e = request.form.get('e')
        benar = request.form.get('benar')

        cursor = mysqlApp.connection.cursor()
        cursor.execute('''insert into bank_soal(soal, a, b, c, d, e, jawaban_benar) 
        values (%s, %s, %s, %s, %s, %s, %s)''', (soal, a, b, c, d, e, benar))
        cursor.connection.commit()
        cursor.close()
        return redirect(url_for('bank_soal'))
    return render_template("input-soal.html", opsi=opsi)


@app.route('/soal', methods=["POST", "GET"])
def bank_soal():
    cursor = mysqlApp.connection.cursor()
    cursor.execute('select * from bank_soal')
    data = cursor.fetchall()
    cursor.close()
    return render_template("soal.html", data=data)


@app.route('/edit-soal', methods=["POST", "GET"])
def editSoal():
    cursor = mysqlApp.connection.cursor()
    edit = request.form.get('edit')

    cursor.execute('select * from bank_soal where soal=%s', (edit,))
    data = cursor.fetchone()
    cursor.execute('SHOW COLUMNS FROM bank_soal')
    col = cursor.fetchall()
    print(edit)

    if 'simpan' in request.form and request.method == "POST":
        simpan = request.form.get('simpan')
        soal = request.form.get('soal')
        a = request.form.get('a')
        b = request.form.get('b')
        c = request.form.get('c')
        d = request.form.get('d')
        e = request.form.get('e')
        benar = request.form.get('benar')

        cursor.execute('''update bank_soal set soal=%s, a=%s, b=%s, c=%s, d=%s, e=%s, jawaban_benar=%s where soal=%s''',
                       (soal, a, b, c, d, e, benar, simpan,))
        cursor.connection.commit()
        cursor.close()
        return redirect(url_for('bank_soal'))
    return render_template("edit-soal.html", data=data, col=col)


@app.route('/hapus-soal', methods=["POST", "GET"])
def hapusSoal():
    if request.method == "POST":
        hapus = request.form.get('hapus')

        cursor = mysqlApp.connection.cursor()
        cursor.execute('delete from bank_soal where soal = %s', (hapus,))
        cursor.connection.commit()
        cursor.close()

    return redirect(url_for('bank_soal'))


if __name__ == '__main__':
    app.run(debug=True)
