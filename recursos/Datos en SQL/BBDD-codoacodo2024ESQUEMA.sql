-- Crear la base de datos
CREATE DATABASE codoacodo2024;

-- Usar la base de datos creada
USE codoacodo2024;

-- Crear la tabla countries
CREATE TABLE countries (
  id_country INT(11) NOT NULL,
  country VARCHAR(25) NOT NULL,
  PRIMARY KEY (id_country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear la tabla locations
CREATE TABLE locations (
  id_city INT(11) NOT NULL,
  id_country INT(11) DEFAULT NULL,
  city VARCHAR(50) DEFAULT NULL,
  longitude VARCHAR(50) DEFAULT NULL,
  latitude VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (id_city),
  FOREIGN KEY (id_country) REFERENCES countries(id_country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear la tabla distributors
CREATE TABLE distributors (
  distributor_id INT(11) NOT NULL,
  distributor VARCHAR(255) NOT NULL,
  location_id INT(11) NOT NULL,
  PRIMARY KEY (distributor_id),
  FOREIGN KEY (location_id) REFERENCES locations(id_city)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear la tabla transactions
CREATE TABLE transactions (
  id INT(11) NOT NULL,
  distributor_id INT(11) NOT NULL,
  country_id INT(11) NOT NULL,
  location_id INT(11) NOT NULL,
  transactions INT(11) NOT NULL,
  gross_margin DECIMAL(15,2) NOT NULL,
  date DATE NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (distributor_id) REFERENCES distributors(distributor_id),
  FOREIGN KEY (country_id) REFERENCES countries(id_country),
  FOREIGN KEY (location_id) REFERENCES locations(id_city)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear la tabla investments
CREATE TABLE investments (
  country_id INT(11) NOT NULL,
  investment DECIMAL(15,2) NOT NULL,
  FOREIGN KEY (country_id) REFERENCES countries(id_country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
