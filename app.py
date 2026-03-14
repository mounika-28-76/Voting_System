from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "voting_secret_key"

# ===============================
# ADMIN CREDENTIALS (TEMP)
# ===============================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ===============================
# CANDIDATES DATA
# ===============================
candidates = [
    {"id": 1, "name": "Candidate A", "party": "Party X"},
    {"id": 2, "name": "Candidate B", "party": "Party Y"},
    {"id": 3, "name": "Candidate C", "party": "Party Z"},
]

# Initialize votes dictionary
candidate_votes = {c["id"]: 0 for c in candidates}

# ===============================
# MAIN DASHBOARD
# ===============================
@app.route('/')
def index():
    return render_template('index.html')

# ===============================
# START VOTING PAGES
# ===============================
@app.route('/aadhaar')
def aadhaar():
    return render_template('aadhaar.html')

@app.route('/details', methods=['POST'])
def details():
    session['eligible'] = True
    return render_template('details.html')

@app.route('/face')
def face():
    return render_template('face.html')

@app.route('/fingerprint')
def fingerprint():
    return render_template('fingerprint.html')

@app.route('/vote')
def vote():
    if not session.get('eligible'):
        return redirect(url_for('index'))
    return render_template('vote.html', candidates=candidates)

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    cid = int(request.form['candidate_id'])
    candidate_votes[cid] += 1  # Increment vote
    session['last_vote'] = cid   # Save last voted candidate
    return redirect(url_for('success'))

# ===============================
# SUCCESS PAGE WITH VOTE RESULTS
# ===============================
@app.route('/success')
def success():
    if not session.get('eligible'):
        return redirect(url_for('index'))
    
    last_voted = session.get('last_vote')
    return render_template(
        'success.html',
        candidates=candidates,
        candidate_votes=candidate_votes,
        last_voted=last_voted
    )

# ===============================
# ADMIN LOGIN
# ===============================
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="❌ Invalid username or password")
    return render_template('admin_login.html')

# ===============================
# ADMIN DASHBOARD
# ===============================
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html', candidates=candidates, candidate_votes=candidate_votes)

# ===============================
# ADMIN LOGOUT
# ===============================
@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('index'))

# ===============================
# USER LOGOUT
# ===============================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ===============================
# RUN APP
# ===============================
if __name__ == '__main__':
    app.run(debug=True)
