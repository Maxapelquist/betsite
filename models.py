from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Date, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
from faker import Faker

Base = declarative_base()
faker = Faker()

class User(Base):
    __tablename__ = 'Users'
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    LegalName = Column(String(255), nullable=False)
    Username = Column(String(255), nullable=False)
    Password = Column(String(255), nullable=False)
    Email = Column(String(255), nullable=False)
    Address = Column(String(255), nullable=False)
    Balance = Column(DECIMAL(10, 2), nullable=False, default=0.00)

class Event(Base):
    __tablename__ = 'Events'
    EventID = Column(Integer, primary_key=True, autoincrement=True)
    EventName = Column(String(255), nullable=False)
    EventDate = Column(Date, nullable=False)
    SportType = Column(String(255), nullable=False)
    Status = Column(Enum('Open', 'Closed'), nullable=False)



Base = declarative_base()
faker = Faker()

class User(Base):
    __tablename__ = 'Users'
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    LegalName = Column(String(255), nullable=False)
    Username = Column(String(255), nullable=False)
    Password = Column(String(255), nullable=False)
    Email = Column(String(255), nullable=False)
    Address = Column(String(255), nullable=False)
    Balance = Column(DECIMAL(10, 2), nullable=False, default=0.00)

class Event(Base):
    __tablename__ = 'Events'
    EventID = Column(Integer, primary_key=True, autoincrement=True)
    EventName = Column(String(255), nullable=False)
    EventDate = Column(Date, nullable=False)
    SportType = Column(String(255), nullable=False)
    Status = Column(Enum('Open', 'Closed'), nullable=False)
    WinningTeamID = Column(Integer, ForeignKey('Teams.TeamID'), nullable=True)

class Team(Base):
    __tablename__ = 'Teams'
    TeamID = Column(Integer, primary_key=True, autoincrement=True)
    TeamName = Column(String(255), nullable=False)
    SportType = Column(String(255), nullable=False)
    TeamLogoURL = Column(String(255))


class EventTeam(Base):
    __tablename__ = 'EventTeams'
    EventID = Column(Integer, ForeignKey('Events.EventID'), primary_key=True)
    TeamID = Column(Integer, ForeignKey('Teams.TeamID'), primary_key=True)

class Bet(Base):
    __tablename__ = 'Bets'
    BetID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    EventID = Column(Integer, ForeignKey('Events.EventID'), nullable=False)
    BetAmount = Column(DECIMAL(10, 2), nullable=False)
    BetType = Column(Enum('1x2', 'Over/Under'), nullable=False)
    BetOdds = Column(DECIMAL(5, 2), nullable=False)
    BetResult = Column(Enum('Win', 'Loss', 'Pending'), nullable=False)


class EventOdds(Base):
    __tablename__ = 'EventOdds'
    OddsID = Column(Integer, primary_key=True, autoincrement=True)
    EventID = Column(Integer, ForeignKey('Events.EventID'), nullable=False)
    OddsType = Column(Enum('1', 'X', '2', 'Over', 'Under'), nullable=False)
    OddsValue = Column(DECIMAL(5, 2), nullable=False)

class TransactionHistory(Base):
    __tablename__ = 'TransactionHistory'
    TransactionID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    TransactionDate = Column(Date, nullable=False)
    TransactionType = Column(Enum('Deposit', 'Withdrawal', 'Bet'), nullable=False)
    Amount = Column(DECIMAL(10, 2), nullable=False)

class Player(Base):
    __tablename__ = 'Players'
    PlayerID = Column(Integer, primary_key=True, autoincrement=True)
    TeamID = Column(Integer, ForeignKey('Teams.TeamID'), nullable=False)
    PlayerName = Column(String(255), nullable=False)

class CreditCard(Base):
    __tablename__ = 'CreditCards'
    CardID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    CardNumber = Column(String(19), nullable=False)
    ExpiryDate = Column(Date, nullable=False)
    CVV = Column(String(3), nullable=False)
