-- Create and use the database
CREATE DATABASE IF NOT EXISTS my_database
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE my_database;

-- Drop table if exists (for idempotent re-runs)
DROP TABLE IF EXISTS titanic;

-- Create titanic table (12 columns)
CREATE TABLE titanic (
    PassengerId INT          NOT NULL,
    Survived    TINYINT      NOT NULL,
    Pclass      TINYINT      NOT NULL,
    Name        VARCHAR(255) NOT NULL,
    Sex         VARCHAR(10)  NOT NULL,
    Age         FLOAT            NULL,
    SibSp       SMALLINT     NOT NULL,
    Parch       SMALLINT     NOT NULL,
    Ticket      VARCHAR(50)  NOT NULL,
    Fare        FLOAT        NOT NULL,
    Cabin       VARCHAR(50)      NULL,
    Embarked    CHAR(1)          NULL
);

-- Load data from CSV mounted at /var/lib/mysql-files/
-- Empty strings in Age, Cabin, Embarked are converted to NULL via NULLIF
LOAD DATA INFILE '/var/lib/mysql-files/titanic.csv'
INTO TABLE titanic
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    PassengerId,
    Survived,
    Pclass,
    Name,
    Sex,
    @Age,
    SibSp,
    Parch,
    Ticket,
    @Fare,
    @Cabin,
    @Embarked
)
SET
    Age      = NULLIF(TRIM(@Age),      ''),
    Fare     = CAST(NULLIF(TRIM(@Fare), '') AS DECIMAL(10,4)),
    Cabin    = NULLIF(TRIM(@Cabin),    ''),
    Embarked = NULLIF(TRIM(@Embarked), '');