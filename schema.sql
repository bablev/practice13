DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Invoice;
DROP TABLE IF EXISTS Nomenclature;
CREATE TABLE Invoice
(
    id        INTEGER PRIMARY KEY,
    created   TIMESTAMP   NOT NULL,
    status    VARCHAR(20) NOT NULL DEFAULT 'Not issued',
    consignee TEXT        NOT NULL
);
CREATE TABLE Item
(
    id         INTEGER PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title      TEXT      NOT NULL,
    amount     INTEGER   NOT NULL,
    unit       INTEGER   NOT NULL,
    invoiceId  INTEGER   NOT NULL,
    FOREIGN KEY (invoiceId) REFERENCES Invoice (id)
);
CREATE TABLE Nomenclature
(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    unit VARCHAR(20) NOT NULL
)