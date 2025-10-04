CREATE TABLE funny_table (
    id SERIAL PRIMARY KEY,
    number_value INT NOT NULL,
    text_value TEXT NOT NULL
);

INSERT INTO funny_table (number_value, text_value)
VALUES
  (1, 'Lorem ipsum dolor sit amet'),
  (2, 'Consectetur adipiscing elit'),
  (3, 'Sed do eiusmod tempor incididunt'),
  (4, 'Ut labore et dolore magna aliqua');
