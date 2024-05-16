import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from datetime import datetime
import random
import numpy as np
import hashlib

# Set seed for random module and Faker library
random.seed(42)
Faker.seed(42)

class SQLDataGenerator:
    def __init__(self, engine):
        self.engine = engine
        self.fake = Faker()

    def generate_username(self, first_name, last_name):
        patterns = [
            lambda fn, ln: fn.lower()[:3] + ln.lower()[:3] + str(random.randint(0, 99)),
            lambda fn, ln: fn.lower() + ln.lower(),
            lambda fn, ln: ln.lower() + str(random.randint(100, 999))
        ]
        return random.choice(patterns)(first_name, last_name)

    def generate_users(self, num_users):
        users = []
        domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']
        for i in range(num_users):
            first_name, last_name = self.fake.first_name(), self.fake.last_name()
            users.append({
                "Username": self.generate_username(first_name, last_name),
                "LegalName": f"{first_name} {last_name}",
                "Address": self.fake.address(),
                "Password": hashlib.sha256(self.fake.password().encode()).hexdigest(),
                "Email": f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}",
                "Balance": round(random.uniform(100, 10000), 2),
                "UserID": i + 1
            })
        return pd.DataFrame(users)

    def generate_teams(self, num_teams):
        sports = ['Football', 'Volleyball', 'Ice hockey']
        teams = []
        for i in range(num_teams):
            teams.append({
                "TeamID": i + 1,
                "TeamName": self.fake.company(),
                "SportType": random.choice(sports)
            })
        return pd.DataFrame(teams)

    def generate_events(self, num_events, teams_df):
        events = []
        for i in range(num_events):
            sport_type = random.choice(teams_df['SportType'].unique())
            possible_teams = teams_df[teams_df['SportType'] == sport_type]
            if len(possible_teams) >= 2:
                team1, team2 = random.sample(list(possible_teams['TeamName']), 2)
                events.append({
                    "EventName": f"{team1} vs {team2}",
                    "EventDate": self.fake.date_between(start_date='-30d', end_date='+30d'),
                    "Status": 'Open',
                    "SportType": sport_type,
                    "EventID": i
                })
        return pd.DataFrame(events)

    def populate_event_teams(self, events_df, teams_df):
        event_teams_data = []
        for event in events_df.itertuples():
            team_names = event.EventName.split(' vs ')
            for team_name in team_names:
                team_id = teams_df[teams_df['TeamName'] == team_name]['TeamID'].iloc[0]
                event_teams_data.append({"EventID": event.EventID, "TeamID": team_id})
        return pd.DataFrame(event_teams_data)

    def execute_sql(self, df, table_name):
        """Execute SQL statements to insert data into the database."""
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            for index, row in df.iterrows():
                columns = ', '.join(row.index)
                values = ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in row.values])
                session.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
            session.commit()
        except Exception as e:
            session.rollback()
            print("Error inserting data:", e)
        finally:
            session.close()

if __name__ == "__main__":
    engine = create_engine('mysql+mysqlconnector://root:12345678@localhost/bet_database')
    generator = SQLDataGenerator(engine)

    users_df = generator.generate_users(200)
    teams_df = generator.generate_teams(10)
    events_df = generator.generate_events(20, teams_df)
    event_teams_df = generator.populate_event_teams(events_df, teams_df)

    generator.execute_sql(users_df, 'Users')
    generator.execute_sql(teams_df, 'Teams')
    generator.execute_sql(events_df, 'Events')
    generator.execute_sql(event_teams_df, 'EventTeams')
    print("Data inserted successfully.")
