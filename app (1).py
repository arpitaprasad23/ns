from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# ---------------------------
# Initialize Database
# ---------------------------
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("DELETE FROM users")
    c.execute("INSERT INTO users VALUES ('admin', 'password123')")
    c.execute("INSERT INTO users VALUES ('guest', 'guest123')")

    c.execute("CREATE TABLE IF NOT EXISTS secrets (id INTEGER, secret TEXT)")
    c.execute("DELETE FROM secrets")
    c.execute("INSERT INTO secrets VALUES (1, 'This data is confidential...Admin:P@ssw0rd!$strong')")

    conn.commit()
    conn.close()

init_db()

# ---------------------------
# 🎨 COMMON STYLE
# ---------------------------
base_style = """
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.container {
    background: rgba(255,255,255,0.95);
    padding: 30px;
    border-radius: 18px;
    width: 95%;
    max-width: 550px;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

h2 {
    margin-bottom: 20px;
    font-size: 1.8em;
    background: linear-gradient(45deg,#667eea,#764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

p {
    color: #fff;
}

input {
    width: 90%;
    padding: 12px;
    margin: 10px 0;
    border-radius: 10px;
    border: 1px solid #ccc;
    outline: none;
}

button {
    background: linear-gradient(45deg, #4CAF50, #45a049);
    color: white;
    padding: 12px 25px;
    border-radius: 25px;
    border: none;
    cursor: pointer;
    margin-top: 10px;
    transition: 0.3s;
}

button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(76,175,80,0.3);
}

.result {
    margin-top: 20px;
}

a {
    text-decoration: none;
}

.task-grid {
    display: grid;
    gap: 20px;
}

.task-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 20px;
    border-radius: 15px;
    color: white;
    transition: 0.3s;
}

.task-card:hover {
    transform: translateY(-5px);
}
</style>
"""

# ---------------------------
# 🏠 HOME PAGE
# ---------------------------
@app.route('/')
def home():
    return render_template_string(f"""
    <html>
    <head>{base_style}</head>
    <body>
        <div class="container">
            <h2>Network Security - Experiment 1</h2>
            

            <div class="task-grid">

                <a href="/task1">
                    <div class="task-card">
                        <h3>🔐 Task 1</h3>
                        <p>Login Bypass (SQL Injection)</p>
                    </div>
                </a>

                <a href="/task2">
                    <div class="task-card">
                        <h3>🔍 Task 2</h3>
                        <p>Data Extraction</p>
                    </div>
                </a>

                <a href="/task3">
                    <div class="task-card">
                        <h3>💻 Task 3</h3>
                        <p>XSS Challenge</p>
                    </div>
                </a>

            </div>
        </div>
    </body>
    </html>
    """)

# ---------------------------
# 🔐 TASK 1
# ---------------------------
@app.route('/task1', methods=['GET', 'POST'])
def task1():
    message = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        try:
            result = c.execute(query).fetchone()
        except:
            result = None

        conn.close()

        if result:
            return f"""
            <html><head>{base_style}</head><body>
            <div class="container">
                <h2>🎉 Access Granted</h2>
                <h4>Flag 1: THM{{SQLI_LOGIN_BYPASS}}</h4>
                <a href="/"><button>Back Home</button></a>
            </div>
            </body></html>
            """
        else:
            message = "Invalid credentials"

    return render_template_string(f"""
    <html><head>{base_style}</head><body>
        <div class="container">
            <h2>🔐 Login Portal</h2>

            <form method="POST">
                <input name="username" placeholder="Username">
                <input name="password" type="password" placeholder="Password">
                <button type="submit">Login</button>
            </form>

            <p style="color:red;">{message}</p>
            <a href="/"><button>Back</button></a>
        </div>
    </body></html>
    """)

# ---------------------------
# 🔍 TASK 2
# ---------------------------
@app.route('/task2', methods=['GET', 'POST'])
def task2():
    results = ""

    if request.method == 'POST':
        username = request.form['username']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        query = f"SELECT username FROM users WHERE username = '{username}'"

        try:
            data = c.execute(query).fetchall()
            results = "<br>".join([row[0] for row in data])
        except:
            results = "Error"

        conn.close()

        if "Admin:P@ssw0rd!$strong" in results:
            results += "<h4>Flag 2: THM{SQLI_UNION_SUCCESS}</h4>"

    return render_template_string(f"""
    <html><head>{base_style}</head><body>
        <div class="container">
            <h2>🔍 User Search</h2>

            <form method="POST">
                <input name="username" placeholder="Enter username">
                <button type="submit">Search</button>
            </form>

            <div class="result">{results}</div>
            <a href="/"><button>Back</button></a>
        </div>
    </body></html>
    """)

# ---------------------------
# 💻 TASK 3
# ---------------------------
@app.route('/task3', methods=['GET', 'POST'])
def task3():
    output = ""

    if request.method == 'POST':
        comment = request.form['comment']
        output = f"You said: {comment}"

        if "<script>alert(1)</script>" in comment:
            output += "<h4>Flag 3: THM{XSS_SUCCESS}</h4>"

    return render_template_string(f"""
    <html><head>{base_style}</head><body>
        <div class="container">
            <h2>💻 Feedback Page</h2>

            <form method="POST">
                <input name="comment" placeholder="Enter comment">
                <button type="submit">Submit</button>
            </form>

            <div class="result">{output}</div>
            <a href="/"><button>Back</button></a>
        </div>
    </body></html>
    """)

# ---------------------------
# RUN APP
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)