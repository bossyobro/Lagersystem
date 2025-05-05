CREATE TABLE varer (
    id INT PRIMARY KEY AUTO_INCREMENT,
    navn VARCHAR(255) NOT NULL,
    varenummer INT NOT NULL,
    pris DECIMAL(10, 2) NOT NULL,
    antall INT NOT NULL,
    kategori ENUM('elektronikk', 'klaer', 'kontor') NOT NULL
);
