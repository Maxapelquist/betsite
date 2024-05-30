from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from faker import Faker
import hashlib
from models import Base, User, Event, Team, EventTeam, Bet, EventOdds, TransactionHistory, Player, CreditCard, FootballEvent

faker = Faker()

def generate_data(session):
    for _ in range(10):
        user = User(
            LegalName=faker.name(),
            Username=faker.user_name(),
            Password=hashlib.sha256(faker.password().encode()).hexdigest(),
            Email=faker.email(),
            Address=faker.address(),
            Balance=random.uniform(10.0, 5000.0)
        )
        session.add(user)

    session.commit()  # Ensure users are committed to generate UserIDs

    for _ in range(5):
        team = Team(
            TeamName=faker.company(),
            SportType=random.choice(['Football', 'Basketball', 'Tennis']),
            TeamLogoURL=faker.image_url()
        )
        session.add(team)

    session.commit()  # Ensure teams are committed to generate TeamIDs

    for _ in range(10):
        event = Event(
            EventName=f"{faker.company()} vs {faker.company()}",
            EventDate=faker.date_between(start_date='-30d', end_date='today'),
            SportType=random.choice(['Football', 'Basketball', 'Tennis']),
            Status=random.choice(['Open', 'Closed'])
        )
        session.add(event)

    session.commit()  # Ensure events are committed to generate EventIDs

    users = session.query(User).all()
    events = session.query(Event).all()
    teams = session.query(Team).all()

    for event in events:
        team_ids = random.sample([team.TeamID for team in teams], 2)  # Select two random teams
        for team_id in team_ids:
            event_team = EventTeam(
                EventID=event.EventID,
                TeamID=team_id
            )
            session.add(event_team)

    for event in events:
        for odds_type in ['1', 'X', '2', 'Over', 'Under']:
            event_odd = EventOdds(
                EventID=event.EventID,
                OddsType=odds_type,
                OddsValue=random.uniform(1.0, 5.0)
            )
            session.add(event_odd)

    for _ in range(20):
        bet = Bet(
            UserID=random.choice(users).UserID,
            EventID=random.choice(events).EventID,
            BetAmount=random.uniform(50.0, 500.0),
            BetType=random.choice(['1x2', 'Over/Under']),
            BetOdds=random.uniform(1.0, 5.0),
            BetResult=random.choice(['Win', 'Loss', 'Pending'])
        )
        session.add(bet)

        transaction = TransactionHistory(
            UserID=random.choice(users).UserID,
            TransactionDate=faker.date_between(start_date='-30d', end_date='today'),
            TransactionType=random.choice(['Deposit', 'Withdrawal', 'Bet']),
            Amount=bet.BetAmount
        )
        session.add(transaction)

        player = Player(
            TeamID=random.choice(teams).TeamID,
            PlayerName=faker.name()
        )
        session.add(player)

        credit_card = CreditCard(
            UserID=random.choice(users).UserID,
            CardNumber=faker.credit_card_number(),
            ExpiryDate=faker.future_date(end_date="+10y"),
            CVV=faker.random_number(digits=3)
        )
        session.add(credit_card)

    session.commit()
    print("All data has been successfully inserted.")

def main():
    engine = create_engine('mysql+mysqlconnector://root:Rust=cohle26@localhost/bet_database')
    Base.metadata.drop_all(engine)  # Caution: This will drop all tables!
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    generate_data(session)

if __name__ == "__main__":
    main()
