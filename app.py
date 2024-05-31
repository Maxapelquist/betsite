import mysql.connector
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Sätt en säker nyckel för sessionshantering

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='pass',
        database='bet_database'
    )
    return conn

def get_events_with_details():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT DISTINCT
        e.EventID,
        e.EventName,
        e.EventDate,
        e.SportType,
        e.Status,
        LEAST(t1.TeamName, t2.TeamName) AS HostTeam,
        GREATEST(t1.TeamName, t2.TeamName) AS GuestTeam,
        eo1.OddsValue AS Odds_1,
        eo2.OddsValue AS Odds_X,
        eo3.OddsValue AS Odds_2,
        eo4.OddsValue AS Odds_OVER,
        eo5.OddsValue AS Odds_UNDER
    FROM Events e
    JOIN EventTeams et1 ON e.EventID = et1.EventID
    JOIN Teams t1 ON et1.TeamID = t1.TeamID
    JOIN EventTeams et2 ON e.EventID = et2.EventID
    JOIN Teams t2 ON et2.TeamID = t2.TeamID
    LEFT JOIN EventOdds eo1 ON e.EventID = eo1.EventID AND eo1.OddsType = '1'
    LEFT JOIN EventOdds eo2 ON e.EventID = eo2.EventID AND eo2.OddsType = 'X'
    LEFT JOIN EventOdds eo3 ON e.EventID = eo3.EventID AND eo3.OddsType = '2'
    LEFT JOIN EventOdds eo4 ON e.EventID = eo4.EventID AND eo4.OddsType = 'Over'
    LEFT JOIN EventOdds eo5 ON e.EventID = eo5.EventID AND eo5.OddsType = 'Under'
    WHERE e.Status = 'Open' AND t1.TeamID != t2.TeamID
    """
    cursor.execute(query)
    events = cursor.fetchall()

    conn.close()

    formatted_events = []
    for event in events:
        event_details = {
            "EventID": event["EventID"],
            "EventName": event["EventName"],
            "EventDate": event["EventDate"],
            "SportType": event["SportType"],
            "Status": event["Status"],
            "HostTeam": event["HostTeam"],
            "GuestTeam": event["GuestTeam"],
            "Odds_1": event["Odds_1"],
            "Odds_X": event["Odds_X"],
            "Odds_2": event["Odds_2"],
            "Odds_OVER": event["Odds_OVER"],
            "Odds_UNDER": event["Odds_UNDER"]
        }
        formatted_events.append(event_details)

    return formatted_events


@app.route('/')
def home():
    events_with_details = get_events_with_details()
    return render_template('index.html', events=events_with_details)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE Username = %s AND Password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['logged_in'] = True
            session['user_id'] = user['UserID']
            return redirect(url_for('profile'))
        else:
            flash("Incorrect username or password. Please try again.")
            return redirect(url_for('profile'))

    if 'logged_in' in session:
        user_id = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE UserID = %s", (user_id,))
        user = cursor.fetchone()
        cursor.execute("""
            SELECT e.EventName, b.BetAmount, b.BetOdds, b.BetResult
            FROM Bets b
            JOIN Events e ON b.EventID = e.EventID
            WHERE b.UserID = %s
        """, (user_id,))
        betting_history = cursor.fetchall()
        conn.close()
        return render_template('profile.html', user=user, betting_history=betting_history)

    return render_template('profile.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        legalname = request.form['legalname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        balance = 0.00  # Sätt ett startvärde för balance
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (LegalName, Username, Password, Email, Address, Balance) VALUES (%s, %s, %s, %s, %s, %s)",
                       (legalname, username, password, email, address, balance))
        conn.commit()
        conn.close()
        flash("Registration successful! Please log in.")
        return redirect(url_for('profile'))
    return render_template('register.html')

@app.route('/place_bet', methods=['POST'])
def place_bet():
    if 'logged_in' in session:
        user_id = session['user_id']
        bets = request.json.get('bets', [])
        conn = get_db_connection()
        cursor = conn.cursor()
        for bet in bets:
            print(bet['EventID'])
            cursor.execute(
                'INSERT INTO Bets (UserID, EventID, BetAmount, BetOdds, BetResult) VALUES (%s, %s, %s, %s, %s)',
                (user_id, bet['EventID'], bet['stake'], bet['odd'], 'Pending'))
        conn.commit()
        conn.close()
        return jsonify(success=True)
    else:
        return jsonify(success=False, message='User not logged in')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('profile'))


@app.route('/teams')
def teams():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT TeamName FROM Teams ORDER BY TeamName ASC")
    teams = cursor.fetchall()
    conn.close()
    return render_template('teams.html', teams=teams)

@app.route('/teams/<team_name>')
def team_details(team_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetching team details
    cursor.execute("SELECT TeamID, TeamName, TeamLogoURL FROM Teams WHERE TeamName = %s", (team_name,))
    team_details = cursor.fetchone()

    if not team_details:
        return "Team not found", 404  # Handling case where no team is found

    # Fetching players of the team
    cursor.execute("SELECT PlayerName FROM Players WHERE TeamID = %s", (team_details['TeamID'],))
    players = cursor.fetchall()

    # Fetching events for the team
    query = """
        SELECT DISTINCT
            e.EventID,
            e.EventName,
            e.EventDate,
            e.SportType,
            e.Status,
            t1.TeamName AS HostTeam,
            t2.TeamName AS GuestTeam,
            eo1.OddsValue AS Odds_1,
            eo2.OddsValue AS Odds_X,
            eo3.OddsValue AS Odds_2,
            eo4.OddsValue AS Odds_OVER,
            eo5.OddsValue AS Odds_UNDER
        FROM Events e
        JOIN EventTeams et1 ON e.EventID = et1.EventID
        JOIN Teams t1 ON et1.TeamID = t1.TeamID
        JOIN EventTeams et2 ON e.EventID = et2.EventID
        JOIN Teams t2 ON et2.TeamID = t2.TeamID
        LEFT JOIN EventOdds eo1 ON e.EventID = eo1.EventID AND eo1.OddsType = '1'
        LEFT JOIN EventOdds eo2 ON e.EventID = eo2.EventID AND eo2.OddsType = 'X'
        LEFT JOIN EventOdds eo3 ON e.EventID = eo3.EventID AND eo3.OddsType = '2'
        LEFT JOIN EventOdds eo4 ON e.EventID = eo4.EventID AND eo4.OddsType = 'Over'
        LEFT JOIN EventOdds eo5 ON e.EventID = eo5.EventID AND eo5.OddsType = 'Under'
        WHERE (t1.TeamID = %s OR t2.TeamID = %s) AND t1.TeamID != t2.TeamID
        ORDER BY e.EventDate ASC;
    """
    cursor.execute(query, (team_details['TeamID'], team_details['TeamID']))
    events = cursor.fetchall()

    # Filter events to ensure only one record per event and always in the format Host vs Guest
    unique_events = {}
    for event in events:
        event_key = tuple(sorted([event['HostTeam'], event['GuestTeam']]))
        if event_key not in unique_events:
            unique_events[event_key] = event
        elif event['EventDate'] < unique_events[event_key]['EventDate']:
            unique_events[event_key] = event

    events = list(unique_events.values())

    conn.close()
    return render_template('team_details.html', team=team_details, players=players, events=events)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
