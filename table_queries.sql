CREATE TABLE IF NOT EXISTS Category (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    cat_name VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY(id))
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Product (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    generic_name VARCHAR(300) NOT NULL,
    cat_id SMALLINT UNSIGNED NOT NULL,
    code_prod VARCHAR(13) NOT NULL UNIQUE,
    brand_name VARCHAR(100) NOT NULL,
    url VARCHAR(150) NOT NULL,
    nova_gps SMALLINT UNSIGNED NOT NULL,
    nutri_grades CHAR(1) NOT NULL,
    pnns_gps_1 VARCHAR(100) NOT NULL,
    pnns_gps_2 VARCHAR(100) NOT NULL,
    store_name VARCHAR(100) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT fk_prod_cat FOREIGN KEY(cat_id)
    REFERENCES Category(id)
    ON UPDATE CASCADE
    ) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Favorite_product (
    prod_id SMALLINT UNSIGNED NOT NULL,
    substitute_id SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY(prod_id, substitute_id),
    CONSTRAINT fk_favprod_prod FOREIGN KEY(prod_id)
    REFERENCES Product(id)
    ON UPDATE CASCADE,
    CONSTRAINT fk_favprod_prodsubst FOREIGN KEY(substitute_id)
    REFERENCES Product(id)
    ON UPDATE CASCADE
    ) ENGINE = InnoDB;