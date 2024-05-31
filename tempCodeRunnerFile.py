@app.route('/betting_history', methods=['GET', 'POST'])
def betting_history():
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
        return render_template('betting_history.html', user=user, betting_history=betting_history)

    return render_template('betting_history.html')
