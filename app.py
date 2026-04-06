from flask import Flask, render_template, request, redirect, session
import MySQLdb

app = Flask(__name__)
app.secret_key = "secret"

def db():
    return MySQLdb.connect(host="localhost", user="root", passwd="licet@123", db="tree_portal")

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        con = db(); cur = con.cursor()
        cur.execute("INSERT INTO users (username, name, mobile, address, password) VALUES (%s,%s,%s,%s,%s)",
            (request.form['username'], request.form['name'], request.form['mobile'],
             request.form['address'], request.form['password']))
        con.commit(); con.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        con = db(); cur = con.cursor()
        cur.execute("SELECT user_id, name FROM users WHERE username=%s AND password=%s",
            (request.form['username'], request.form['password']))
        user = cur.fetchone(); con.close()
        if user:
            session['user_id'] = user[0]
            session['name'] = user[1]
            return redirect('/dashboard')
        error = 'Wrong username or password'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    con = db(); cur = con.cursor()
    cur.execute("SELECT tree_id, tree_name, planted_date FROM trees WHERE user_id=%s", (session['user_id'],))
    trees = cur.fetchall(); con.close()
    return render_template('dashboard.html', trees=trees, name=session['name'])

@app.route('/add_tree', methods=['GET', 'POST'])
def add_tree():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        con = db(); cur = con.cursor()
        cur.execute("INSERT INTO trees (user_id, tree_name, planted_date) VALUES (%s,%s,%s)",
            (session['user_id'], request.form['tree_name'], request.form['planted_date']))
        con.commit(); con.close()
        return redirect('/dashboard')
    return render_template('add_tree.html')

@app.route('/add_growth/<int:tree_id>', methods=['GET', 'POST'])
def add_growth(tree_id):
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        con = db(); cur = con.cursor()
        cur.execute("INSERT INTO growth (tree_id, height, temperature, humidity, area_size) VALUES (%s,%s,%s,%s,%s)",
            (tree_id, request.form['height'], request.form['temperature'],
             request.form['humidity'], request.form['area_size']))
        con.commit(); con.close()
        return redirect('/dashboard')
    return render_template('growth.html', tree_id=tree_id)

@app.route('/view_growth/<int:tree_id>')
def view_growth(tree_id):
    if 'user_id' not in session:
        return redirect('/login')
    con = db(); cur = con.cursor()
    cur.execute("SELECT tree_name FROM trees WHERE tree_id=%s", (tree_id,))
    tree = cur.fetchone()
    cur.execute("SELECT height, temperature, humidity, area_size, recorded_at FROM growth WHERE tree_id=%s", (tree_id,))
    records = cur.fetchall(); con.close()
    return render_template('view_growth.html', tree=tree, records=records, tree_id=tree_id)

if __name__ == '__main__':
    app.run(debug=True)
