CREATE TABLE varer (
    id INT PRIMARY KEY AUTO_INCREMENT,
    navn VARCHAR(255) NOT NULL,
    varenummer INT NOT NULL,
    pris DECIMAL(10, 2) NOT NULL,
    antall INT NOT NULL,
    kategori ENUM('elektronikk', 'klaer', 'kontor') NOT NULL
);


CREATE TABLE brukere (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_type ENUM('Admin', 'Worker') NOT NULL
);


INSERT INTO brukere (username, password, user_type)
VALUES ('admin', 'admin', 'Admin');

INSERT INTO brukere (username, password, user_type)
VALUES ('worker', 'worker', 'Worker');