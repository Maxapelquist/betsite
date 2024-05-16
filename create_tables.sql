-- Users Table
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    LegalName VARCHAR(255) NOT NULL,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    Balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00
);

-- Teams Table
CREATE TABLE Teams (
    TeamID INT PRIMARY KEY,
    TeamName VARCHAR(255) NOT NULL,
    SportType VARCHAR(255) NOT NULL,
    TeamLogoURL VARCHAR(255)
);

-- Events Table
CREATE TABLE Events (
    EventID INT PRIMARY KEY,
    EventName VARCHAR(255) NOT NULL,
    EventDate DATE NOT NULL,
    SportType VARCHAR(255) NOT NULL,
    Status ENUM('Open', 'Closed') NOT NULL
);

-- EventTeams Linking Table (Many-to-Many relationship between Events and Teams)
CREATE TABLE EventTeams (
    EventID INT NOT NULL,
    TeamID INT NOT NULL,
    PRIMARY KEY (EventID, TeamID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
);

-- Bets Table
CREATE TABLE api_bet (
    BetID INT PRIMARY KEY,
    UserID INT NOT NULL,
    EventID INT NOT NULL,
    BetAmount DECIMAL(10, 2) NOT NULL,
    BetType ENUM('Win', 'Draw', 'Over/Under') NOT NULL,
    BetOdds DECIMAL(5, 2) NOT NULL,
    BetResult ENUM('Win', 'Loss', 'Pending') NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

-- Transaction History Table
CREATE TABLE TransactionHistory (
    TransactionID INT PRIMARY KEY,
    UserID INT NOT NULL,
    TransactionDate DATETIME NOT NULL,
    TransactionType ENUM('Deposit', 'Withdrawal', 'Bet') NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Players Table
CREATE TABLE Players (
    PlayerID INT PRIMARY KEY,
    TeamID INT NOT NULL,
    PlayerName VARCHAR(255) NOT NULL,
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
);

-- CreditCards Table
CREATE TABLE CreditCards (
    CardID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    CardNumber VARCHAR(16) NOT NULL,
    ExpiryDate DATE NOT NULL,
    CVV VARCHAR(3) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
CREATE TABLE FootballEvent (
    EventID INT PRIMARY KEY,
    NoYellowCards INT NOT NULL DEFAULT 0,
    RedCards INT NOT NULL DEFAULT 0,
    Corners INT NOT NULL DEFAULT 0,
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
    ON DELETE CASCADE
);
