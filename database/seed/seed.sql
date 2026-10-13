-- Prism.Cinema demo data: 10 movies with cast, genres, licenses, subtitles, posters and 3 demo users.
-- Loaded automatically after schema.sql on the db container's first start.

--
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: ACTORS; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."ACTORS" VALUES
	('88f1ab30-b17d-4d01-9978-ee6ef34d56dd', 'Tim', NULL, 'Robbins', 'West Covina, California, USA'),
	('8bef0b65-c095-4349-b4e0-0ee266fbfe9d', 'Morgan', NULL, 'Freeman', 'Memphis, Tennessee, USA'),
	('5780bedd-2f20-4f06-b15d-62935949f083', 'Marlon', NULL, 'Brando', 'Omaha, Nebraska, USA'),
	('f7758d85-48c0-4d97-9ddb-3c49f012dee8', 'Al', NULL, 'Pacino', 'New York City, New York, USA'),
	('c241520b-aded-4a17-8b7f-f7df2aebd045', 'Christian', NULL, 'Bale', 'Haverfordwest, Wales'),
	('ebcc9ee5-c5ec-45ae-a4ef-e75a126eeba2', 'Heath', NULL, 'Ledger', 'Perth, Australia'),
	('bc04396f-4105-4c8d-a285-f162a7db54db', 'Henry', NULL, 'Fonda', 'Grand Island, Nebraska, USA'),
	('4b6439ff-fb4f-49f5-a402-7150966262d5', 'Lee', 'J.', 'Cobb', 'New York City, New York, USA'),
	('5d487084-d46b-4f15-97e1-25d4669f3e47', 'Liam', NULL, 'Neeson', 'Ballymena, Northern Ireland'),
	('b5d1c852-d60d-42f8-b764-d15d0d0979f4', 'Ralph', NULL, 'Fiennes', 'Ipswich, Suffolk, England'),
	('67af546d-50eb-4254-a46e-3b1c27341971', 'Elijah', NULL, 'Wood', 'Cedar Rapids, Iowa, USA'),
	('b13edc03-ec91-4fd8-a560-c0ed74bd9759', 'Viggo', NULL, 'Mortensen', 'New York City, New York, USA'),
	('0c798182-c87b-408e-966c-ba4389ffd7d9', 'John', NULL, 'Travolta', 'Englewood, New Jersey, USA'),
	('7ee6783d-c329-413e-8ac6-5c56701214b2', 'Samuel', 'L.', 'Jackson', 'Washington, D.C., USA'),
	('507c036d-bd1a-483c-9ef5-478598bb9bc6', 'Tom', NULL, 'Hanks', 'Concord, California, USA'),
	('fad73d9b-d078-47d5-ab5e-994c50bcfb1a', 'Robin', NULL, 'Wright', 'Dallas, Texas, USA'),
	('8477d1f9-9763-40e9-adbc-3324503c2f8a', 'Leonardo', NULL, 'DiCaprio', 'Los Angeles, California, USA'),
	('af709f5a-f1d1-4cd3-aa3f-6e15a217fa79', 'Joseph', 'Gordon', 'Levitt', 'Los Angeles, California, USA'),
	('59eda81d-2fac-4fa3-962e-04051cef681a', 'Edward', NULL, 'Norton', 'Boston, Massachusetts, USA'),
	('962a4717-fe8e-43b8-b22a-542f76facae2', 'Brad', NULL, 'Pitt', 'Shawnee, Oklahoma, USA');

--
-- Data for Name: DIRECTORS; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."DIRECTORS" VALUES
	('66f1e938-4351-4df5-a6f3-77450c13e3fb', 'Frank', NULL, 'Darabont', 'Montbéliard, France'),
	('5f25afc8-74b3-41a2-a368-3d06b18714d2', 'Francis', 'Ford', 'Coppola', 'Detroit, Michigan, USA'),
	('a103ec14-9036-4e81-b5b7-f57f67a88f60', 'Christopher', NULL, 'Nolan', 'London, England'),
	('a95bffd4-28ce-4fec-9878-c2625dccefee', 'Sidney', NULL, 'Lumet', 'Philadelphia, Pennsylvania, USA'),
	('80dd8081-ca03-4351-aea1-134916f98ed3', 'Steven', NULL, 'Spielberg', 'Cincinnati, Ohio, USA'),
	('1c48400f-344a-46c3-9f0d-71a580dbfc70', 'Peter', NULL, 'Jackson', 'Pukerua Bay, New Zealand'),
	('1315e2fd-f090-480e-8b9b-54cc4ff117dc', 'Quentin', NULL, 'Tarantino', 'Knoxville, Tennessee, USA'),
	('b8542c80-1d43-4442-a7c8-40366499b0f1', 'Robert', NULL, 'Zemeckis', 'Chicago, Illinois, USA'),
	('bca7b6b5-08c3-481e-85fb-c54ea84e956b', 'Christopher', NULL, 'Nolan', 'London, England'),
	('69c89287-5937-4231-82d2-7af29324c45b', 'David', NULL, 'Fincher', 'Denver, Colorado, USA');

--
-- Data for Name: GENRES; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."GENRES" VALUES
	('b4658226-4460-4601-9575-2cc7e96a0514', 'Drama', 'Serious stories focusing on realistic characters and emotional themes.'),
	('63991ad8-404a-4caa-a3fa-674dac413312', 'Crime', 'Stories centered around criminals, criminal acts, and their consequences.'),
	('f9b9f45e-b104-4a24-b2bb-33b9c9af6006', 'Action', 'High energy, big-budget physical stunts and chases.'),
	('6698abed-54e4-4e86-9ef6-a79718c37f26', 'Biography', 'Based on the life of a real person.'),
	('199bd07c-531b-401a-a371-47b74955049b', 'History', 'Depicts historical events or settings.'),
	('a8bfaec9-a352-4d51-a863-382319d49a6a', 'Adventure', 'Exciting stories involving journeys or exploration.'),
	('3b2d9ec1-d534-40e6-af8f-80307964c577', 'Fantasy', 'Includes magical, mythical, or supernatural elements.'),
	('ad29a40a-f9ef-4cf7-858f-fa8ffd49be39', 'Romance', 'Focuses on love and romantic relationships.'),
	('e5d2c8df-b1b9-4580-9414-9ced6688cd0b', 'Sci-Fi', 'Speculative science, futuristic technology or space exploration.');

--
-- Data for Name: LICENSES; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."LICENSES" VALUES
	('a2e4370e-946d-4b73-8585-0b9db3418262', 'USA', '2026-12-31'),
	('1a6eedc5-6715-4e16-8405-36d725d0f91d', 'CAN', '2025-09-30'),
	('fc84bc24-4120-43e7-bc4e-44b0dd38b29a', 'GBR', '2027-05-15'),
	('fc19df30-d43d-4cba-9735-13f6faefc787', 'POL', '2025-12-01'),
	('821c9354-7523-486e-99dc-d9ad2b02c8c8', 'DEU', '2026-06-20'),
	('a9623bac-c5a2-4d13-8383-a4f1bd6d29ea', 'FRA', '2026-07-01'),
	('18f64358-1522-4bf3-88b5-d54ee0968be3', 'ESP', '2025-11-10'),
	('8394e86f-bdc4-417c-931d-5fc4bcb1d6af', 'ITA', '2026-03-25'),
	('cd75b768-2976-4910-8aa4-990d4a642dc7', 'JPN', '2027-01-01'),
	('640bda7d-f88a-48c6-a94c-9fc66666bbd4', 'AUS', '2026-09-09');

--
-- Data for Name: MOVIES; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."MOVIES" VALUES
	('5976adbc-5e7f-40a9-8fea-d4dbc54748f1', 'The Shawshank Redemption', 9.3, '1994-09-23', 'R', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption.'),
	('04f47120-edf1-4101-984a-14137747ca9b', 'The Godfather', 9.2, '1972-03-24', 'R', 'The aging patriarch of an organized crime dynasty transfers control of his empire to his reluctant son.'),
	('05cae0bb-461b-48e7-939f-d02bb0ab187d', 'The Dark Knight', 9, '2008-07-18', 'PG-13', 'Batman faces the Joker, a criminal mastermind who plunges Gotham into anarchy.'),
	('724d15d6-96f2-4ada-9137-0a5918843cba', '12 Angry Men', 9, '1957-04-10', 'PG', 'A jury holdout attempts to prevent a miscarriage of justice.'),
	('33d2499d-6637-41f9-ac62-3f6bbf9907a9', 'Schindler''s List', 9, '1993-12-15', 'R', 'A businessman saves hundreds of Jews during the Holocaust.'),
	('20f31eac-2b5a-40ba-9b70-57a942496082', 'The Lord of the Rings: The Return of the King', 8.9, '2003-12-17', 'PG-13', 'The final confrontation between the forces of good and evil for the control of Middle-earth.'),
	('d7ef8bc9-e170-4905-bf68-cd664ed1bab5', 'Pulp Fiction', 8.9, '1994-10-14', 'R', 'The lives of two mob hitmen, a boxer, and others intertwine in four tales of violence and redemption.'),
	('88e10ed8-6697-4aae-942c-b1851d278e0d', 'Forrest Gump', 8.8, '1994-07-06', 'PG-13', 'The story of Forrest Gump, a man with a low IQ but good intentions.'),
	('a17f96fb-0931-4015-b2f1-cf6694b044c2', 'Inception', 8.8, '2010-07-16', 'PG-13', 'A thief steals corporate secrets through the use of dream-sharing technology.'),
	('936cfef3-775a-45d2-9712-2bf51732e7dc', 'Fight Club', 8.8, '1999-10-15', 'R', 'An insomniac office worker forms an underground fight club.');

--
-- Data for Name: MOVIE_ACTORS; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."MOVIE_ACTORS" VALUES
	('5976adbc-5e7f-40a9-8fea-d4dbc54748f1', '88f1ab30-b17d-4d01-9978-ee6ef34d56dd'),
	('5976adbc-5e7f-40a9-8fea-d4dbc54748f1', '8bef0b65-c095-4349-b4e0-0ee266fbfe9d'),
	('04f47120-edf1-4101-984a-14137747ca9b', '5780bedd-2f20-4f06-b15d-62935949f083'),
	('04f47120-edf1-4101-984a-14137747ca9b', 'f7758d85-48c0-4d97-9ddb-3c49f012dee8'),
	('05cae0bb-461b-48e7-939f-d02bb0ab187d', 'c241520b-aded-4a17-8b7f-f7df2aebd045'),
	('05cae0bb-461b-48e7-939f-d02bb0ab187d', 'ebcc9ee5-c5ec-45ae-a4ef-e75a126eeba2'),
	('724d15d6-96f2-4ada-9137-0a5918843cba', 'bc04396f-4105-4c8d-a285-f162a7db54db'),
	('724d15d6-96f2-4ada-9137-0a5918843cba', '4b6439ff-fb4f-49f5-a402-7150966262d5'),
	('33d2499d-6637-41f9-ac62-3f6bbf9907a9', '5d487084-d46b-4f15-97e1-25d4669f3e47'),
	('33d2499d-6637-41f9-ac62-3f6bbf9907a9', 'b5d1c852-d60d-42f8-b764-d15d0d0979f4'),
	('20f31eac-2b5a-40ba-9b70-57a942496082', '67af546d-50eb-4254-a46e-3b1c27341971'),
	('20f31eac-2b5a-40ba-9b70-57a942496082', 'b13edc03-ec91-4fd8-a560-c0ed74bd9759'),
	('d7ef8bc9-e170-4905-bf68-cd664ed1bab5', '0c798182-c87b-408e-966c-ba4389ffd7d9'),
	('d7ef8bc9-e170-4905-bf68-cd664ed1bab5', '7ee6783d-c329-413e-8ac6-5c56701214b2'),
	('88e10ed8-6697-4aae-942c-b1851d278e0d', '507c036d-bd1a-483c-9ef5-478598bb9bc6'),
	('88e10ed8-6697-4aae-942c-b1851d278e0d', 'fad73d9b-d078-47d5-ab5e-994c50bcfb1a'),
	('a17f96fb-0931-4015-b2f1-cf6694b044c2', '8477d1f9-9763-40e9-adbc-3324503c2f8a'),
	('a17f96fb-0931-4015-b2f1-cf6694b044c2', 'af709f5a-f1d1-4cd3-aa3f-6e15a217fa79'),
	('936cfef3-775a-45d2-9712-2bf51732e7dc', '59eda81d-2fac-4fa3-962e-04051cef681a'),
	('936cfef3-775a-45d2-9712-2bf51732e7dc', '962a4717-fe8e-43b8-b22a-542f76facae2');

--
-- Data for Name: MOVIE_DIRECTORS; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."MOVIE_DIRECTORS" VALUES
	('5976adbc-5e7f-40a9-8fea-d4dbc54748f1', '66f1e938-4351-4df5-a6f3-77450c13e3fb'),
	('04f47120-edf1-4101-984a-14137747ca9b', '5f25afc8-74b3-41a2-a368-3d06b18714d2'),
	('05cae0bb-461b-48e7-939f-d02bb0ab187d', 'a103ec14-9036-4e81-b5b7-f57f67a88f60'),
	('724d15d6-96f2-4ada-9137-0a5918843cba', 'a95bffd4-28ce-4fec-9878-c2625dccefee'),
	('33d2499d-6637-41f9-ac62-3f6bbf9907a9', '80dd8081-ca03-4351-aea1-134916f98ed3'),
	('20f31eac-2b5a-40ba-9b70-57a942496082', '1c48400f-344a-46c3-9f0d-71a580dbfc70'),
	('d7ef8bc9-e170-4905-bf68-cd664ed1bab5', '1315e2fd-f090-480e-8b9b-54cc4ff117dc'),
	('88e10ed8-6697-4aae-942c-b1851d278e0d', 'b8542c80-1d43-4442-a7c8-40366499b0f1'),
	('a17f96fb-0931-4015-b2f1-cf6694b044c2', 'a103ec14-9036-4e81-b5b7-f57f67a88f60'),
	('936cfef3-775a-45d2-9712-2bf51732e7dc', '69c89287-5937-4231-82d2-7af29324c45b');

--
-- Data for Name: MOVIE_GENRES; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."MOVIE_GENRES" VALUES
	('5976adbc-5e7f-40a9-8fea-d4dbc54748f1', 'b4658226-4460-4601-9575-2cc7e96a0514'),
	('5976adbc-5e7f-40a9-8fea-d4dbc54748f1', '63991ad8-404a-4caa-a3fa-674dac413312'),
	('04f47120-edf1-4101-984a-14137747ca9b', 'b4658226-4460-4601-9575-2cc7e96a0514'),
	('04f47120-edf1-4101-984a-14137747ca9b', '63991ad8-404a-4caa-a3fa-674dac413312'),
	('05cae0bb-461b-48e7-939f-d02bb0ab187d', 'f9b9f45e-b104-4a24-b2bb-33b9c9af6006'),
	('05cae0bb-461b-48e7-939f-d02bb0ab187d', '63991ad8-404a-4caa-a3fa-674dac413312'),
	('05cae0bb-461b-48e7-939f-d02bb0ab187d', 'b4658226-4460-4601-9575-2cc7e96a0514'),
	('724d15d6-96f2-4ada-9137-0a5918843cba', 'b4658226-4460-4601-9575-2cc7e96a0514'),
	('33d2499d-6637-41f9-ac62-3f6bbf9907a9', 'b4658226-4460-4601-9575-2cc7e96a0514'),
	('33d2499d-6637-41f9-ac62-3f6bbf9907a9', '6698abed-54e4-4e86-9ef6-a79718c37f26'),
	('33d2499d-6637-41f9-ac62-3f6bbf9907a9', '199bd07c-531b-401a-a371-47b74955049b'),
	('20f31eac-2b5a-40ba-9b70-57a942496082', 'f9b9f45e-b104-4a24-b2bb-33b9c9af6006'),
	('20f31eac-2b5a-40ba-9b70-57a942496082', 'a8bfaec9-a352-4d51-a863-382319d49a6a'),
	('20f31eac-2b5a-40ba-9b70-57a942496082', '3b2d9ec1-d534-40e6-af8f-80307964c577'),
	('d7ef8bc9-e170-4905-bf68-cd664ed1bab5', '63991ad8-404a-4caa-a3fa-674dac413312'),
	('d7ef8bc9-e170-4905-bf68-cd664ed1bab5', 'b4658226-4460-4601-9575-2cc7e96a0514'),
	('88e10ed8-6697-4aae-942c-b1851d278e0d', 'b4658226-4460-4601-9575-2cc7e96a0514'),
	('88e10ed8-6697-4aae-942c-b1851d278e0d', 'ad29a40a-f9ef-4cf7-858f-fa8ffd49be39'),
	('a17f96fb-0931-4015-b2f1-cf6694b044c2', 'f9b9f45e-b104-4a24-b2bb-33b9c9af6006'),
	('a17f96fb-0931-4015-b2f1-cf6694b044c2', 'e5d2c8df-b1b9-4580-9414-9ced6688cd0b'),
	('936cfef3-775a-45d2-9712-2bf51732e7dc', 'b4658226-4460-4601-9575-2cc7e96a0514');

--
-- Data for Name: MOVIE_LICENSES; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."MOVIE_LICENSES" VALUES
	('5976adbc-5e7f-40a9-8fea-d4dbc54748f1', '1a6eedc5-6715-4e16-8405-36d725d0f91d'),
	('5976adbc-5e7f-40a9-8fea-d4dbc54748f1', 'fc84bc24-4120-43e7-bc4e-44b0dd38b29a'),
	('04f47120-edf1-4101-984a-14137747ca9b', '8394e86f-bdc4-417c-931d-5fc4bcb1d6af'),
	('04f47120-edf1-4101-984a-14137747ca9b', '1a6eedc5-6715-4e16-8405-36d725d0f91d'),
	('04f47120-edf1-4101-984a-14137747ca9b', 'cd75b768-2976-4910-8aa4-990d4a642dc7'),
	('05cae0bb-461b-48e7-939f-d02bb0ab187d', 'a9623bac-c5a2-4d13-8383-a4f1bd6d29ea'),
	('05cae0bb-461b-48e7-939f-d02bb0ab187d', '640bda7d-f88a-48c6-a94c-9fc66666bbd4'),
	('724d15d6-96f2-4ada-9137-0a5918843cba', 'fc84bc24-4120-43e7-bc4e-44b0dd38b29a'),
	('724d15d6-96f2-4ada-9137-0a5918843cba', '1a6eedc5-6715-4e16-8405-36d725d0f91d'),
	('724d15d6-96f2-4ada-9137-0a5918843cba', 'cd75b768-2976-4910-8aa4-990d4a642dc7'),
	('33d2499d-6637-41f9-ac62-3f6bbf9907a9', '821c9354-7523-486e-99dc-d9ad2b02c8c8'),
	('33d2499d-6637-41f9-ac62-3f6bbf9907a9', 'fc84bc24-4120-43e7-bc4e-44b0dd38b29a'),
	('20f31eac-2b5a-40ba-9b70-57a942496082', '821c9354-7523-486e-99dc-d9ad2b02c8c8'),
	('20f31eac-2b5a-40ba-9b70-57a942496082', 'a2e4370e-946d-4b73-8585-0b9db3418262'),
	('d7ef8bc9-e170-4905-bf68-cd664ed1bab5', '18f64358-1522-4bf3-88b5-d54ee0968be3'),
	('88e10ed8-6697-4aae-942c-b1851d278e0d', '18f64358-1522-4bf3-88b5-d54ee0968be3'),
	('88e10ed8-6697-4aae-942c-b1851d278e0d', 'a2e4370e-946d-4b73-8585-0b9db3418262'),
	('88e10ed8-6697-4aae-942c-b1851d278e0d', 'cd75b768-2976-4910-8aa4-990d4a642dc7'),
	('a17f96fb-0931-4015-b2f1-cf6694b044c2', 'cd75b768-2976-4910-8aa4-990d4a642dc7'),
	('936cfef3-775a-45d2-9712-2bf51732e7dc', '640bda7d-f88a-48c6-a94c-9fc66666bbd4'),
	('936cfef3-775a-45d2-9712-2bf51732e7dc', '8394e86f-bdc4-417c-931d-5fc4bcb1d6af'),
	('936cfef3-775a-45d2-9712-2bf51732e7dc', 'cd75b768-2976-4910-8aa4-990d4a642dc7');

--
-- Data for Name: MOVIE_LOCALIZATIONS; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."MOVIE_LOCALIZATIONS" VALUES
	('5976adbc-5e7f-40a9-8fea-d4dbc54748f1', 'eng', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "This is an English subtitle sample."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Another example line."}]'),
	('5976adbc-5e7f-40a9-8fea-d4dbc54748f1', 'pol', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "To jest przyk\u0142adowy polski napis."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Kolejna linia napis\u00f3w."}]'),
	('5976adbc-5e7f-40a9-8fea-d4dbc54748f1', 'esp', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "Esto es un subt\u00edtulo en espa\u00f1ol."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Otra l\u00ednea de ejemplo."}]'),
	('04f47120-edf1-4101-984a-14137747ca9b', 'eng', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "This is an English subtitle sample."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Another example line."}]'),
	('04f47120-edf1-4101-984a-14137747ca9b', 'pol', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "To jest przyk\u0142adowy polski napis."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Kolejna linia napis\u00f3w."}]'),
	('04f47120-edf1-4101-984a-14137747ca9b', 'esp', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "Esto es un subt\u00edtulo en espa\u00f1ol."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Otra l\u00ednea de ejemplo."}]'),
	('05cae0bb-461b-48e7-939f-d02bb0ab187d', 'eng', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "This is an English subtitle sample."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Another example line."}]'),
	('05cae0bb-461b-48e7-939f-d02bb0ab187d', 'pol', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "To jest przyk\u0142adowy polski napis."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Kolejna linia napis\u00f3w."}]'),
	('05cae0bb-461b-48e7-939f-d02bb0ab187d', 'esp', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "Esto es un subt\u00edtulo en espa\u00f1ol."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Otra l\u00ednea de ejemplo."}]'),
	('724d15d6-96f2-4ada-9137-0a5918843cba', 'eng', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "This is an English subtitle sample."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Another example line."}]'),
	('724d15d6-96f2-4ada-9137-0a5918843cba', 'pol', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "To jest przyk\u0142adowy polski napis."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Kolejna linia napis\u00f3w."}]'),
	('724d15d6-96f2-4ada-9137-0a5918843cba', 'esp', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "Esto es un subt\u00edtulo en espa\u00f1ol."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Otra l\u00ednea de ejemplo."}]'),
	('33d2499d-6637-41f9-ac62-3f6bbf9907a9', 'eng', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "This is an English subtitle sample."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Another example line."}]'),
	('33d2499d-6637-41f9-ac62-3f6bbf9907a9', 'pol', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "To jest przyk\u0142adowy polski napis."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Kolejna linia napis\u00f3w."}]'),
	('33d2499d-6637-41f9-ac62-3f6bbf9907a9', 'esp', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "Esto es un subt\u00edtulo en espa\u00f1ol."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Otra l\u00ednea de ejemplo."}]'),
	('20f31eac-2b5a-40ba-9b70-57a942496082', 'eng', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "This is an English subtitle sample."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Another example line."}]'),
	('20f31eac-2b5a-40ba-9b70-57a942496082', 'pol', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "To jest przyk\u0142adowy polski napis."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Kolejna linia napis\u00f3w."}]'),
	('20f31eac-2b5a-40ba-9b70-57a942496082', 'esp', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "Esto es un subt\u00edtulo en espa\u00f1ol."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Otra l\u00ednea de ejemplo."}]'),
	('d7ef8bc9-e170-4905-bf68-cd664ed1bab5', 'eng', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "This is an English subtitle sample."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Another example line."}]'),
	('d7ef8bc9-e170-4905-bf68-cd664ed1bab5', 'pol', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "To jest przyk\u0142adowy polski napis."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Kolejna linia napis\u00f3w."}]'),
	('d7ef8bc9-e170-4905-bf68-cd664ed1bab5', 'esp', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "Esto es un subt\u00edtulo en espa\u00f1ol."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Otra l\u00ednea de ejemplo."}]'),
	('88e10ed8-6697-4aae-942c-b1851d278e0d', 'eng', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "This is an English subtitle sample."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Another example line."}]'),
	('88e10ed8-6697-4aae-942c-b1851d278e0d', 'pol', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "To jest przyk\u0142adowy polski napis."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Kolejna linia napis\u00f3w."}]'),
	('88e10ed8-6697-4aae-942c-b1851d278e0d', 'esp', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "Esto es un subt\u00edtulo en espa\u00f1ol."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Otra l\u00ednea de ejemplo."}]'),
	('a17f96fb-0931-4015-b2f1-cf6694b044c2', 'eng', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "This is an English subtitle sample."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Another example line."}]'),
	('a17f96fb-0931-4015-b2f1-cf6694b044c2', 'pol', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "To jest przyk\u0142adowy polski napis."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Kolejna linia napis\u00f3w."}]'),
	('a17f96fb-0931-4015-b2f1-cf6694b044c2', 'esp', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "Esto es un subt\u00edtulo en espa\u00f1ol."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Otra l\u00ednea de ejemplo."}]'),
	('936cfef3-775a-45d2-9712-2bf51732e7dc', 'eng', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "This is an English subtitle sample."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Another example line."}]'),
	('936cfef3-775a-45d2-9712-2bf51732e7dc', 'pol', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "To jest przyk\u0142adowy polski napis."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Kolejna linia napis\u00f3w."}]'),
	('936cfef3-775a-45d2-9712-2bf51732e7dc', 'esp', '[{"start": "00:00:01,000", "end": "00:00:04,000", "text": "Esto es un subt\u00edtulo en espa\u00f1ol."}, {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Otra l\u00ednea de ejemplo."}]');

--
-- Data for Name: SERVICE_SUBSCRIPTION_PLANS; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."SERVICE_SUBSCRIPTION_PLANS" VALUES
	('208ba2df-df25-4786-81ef-40d0d8d4289f', 'Free', 0, 'You have unlimited access to the full list of movies and their detailed information. However, you are not allowed to watch the movies.'),
	('8430b074-7509-4516-9ff8-5b81b563de02', 'Monthly', 97, 'Enjoy full access to all movies – you can stream them without any limitations and create your own lists of favorite titles. The subscription renews every month.'),
	('8573e95b-506c-49b4-9e3f-b706ef7ea488', 'Semiannual', 244, 'Includes all the features of the Monthly Plan. A one-time payment gives you access to the platform for 6 months – a convenient option for regular users.');

--
--

-- Posters are read from database/seed/assets, mounted into the db container at /seed-assets.
INSERT INTO public."ADDITIONAL_MOVIE_DATA" (movie_id, movie_poster, movie_trailer, movie_language, movie_preview_poster)
SELECT m.movie_id,
       pg_read_binary_file('/seed-assets/posters/' || v.file_no || '.jpg'),
       v.trailer,
       v.lang,
       pg_read_binary_file('/seed-assets/previews/' || v.file_no || '.jpg')
FROM (VALUES
	('The Shawshank Redemption', 0, 'https://www.youtube.com/watch?v=6hB3S9bIaco', 'eng'),
	('The Godfather', 1, 'https://www.youtube.com/watch?v=sY1S34973zA', 'eng'),
	('The Dark Knight', 2, 'https://www.youtube.com/watch?v=EXeTwQWrcwY', 'eng'),
	('12 Angry Men', 3, 'https://www.youtube.com/watch?v=fSG38tk6TpI', 'eng'),
	('Schindler''s List', 4, 'https://www.youtube.com/watch?v=gG22XNhtnoY', 'eng'),
	('The Lord of the Rings: The Return of the King', 5, 'https://www.youtube.com/watch?v=r5X-hFf6Bwo', 'eng'),
	('Pulp Fiction', 6, 'https://www.youtube.com/watch?v=s7EdQ4FqbhY', 'eng'),
	('Forrest Gump', 7, 'https://www.youtube.com/watch?v=bLvqoHBptjg', 'eng'),
	('Inception', 8, 'https://www.youtube.com/watch?v=YoHD9XEInc0', 'eng'),
	('Fight Club', 9, 'https://www.youtube.com/watch?v=SUXWAEX2jlg', 'eng')
) AS v(movie_name, file_no, trailer, lang)
JOIN public."MOVIES" m ON m.movie_name = v.movie_name;

-- Demo accounts (passwords are listed in the README):
--   admin      / admin123       administrator, Monthly plan
--   subscriber / subscriber123  Semiannual plan, can watch and like movies
--   viewer     / viewer123      Free plan, can only browse
INSERT INTO public."USERS" (user_id, user_login, user_password, user_mail, user_is_subscribed,
                            user_subscription_plan_id, user_subscription_period, user_is_admin,
                            user_location_region, user_date_of_birth)
SELECT v.user_id::uuid, v.login, v.password_hash, v.mail, v.is_subscribed, p.subscription_plan_id,
       CASE WHEN v.is_subscribed THEN daterange(CURRENT_DATE, CURRENT_DATE + v.days) END,
       v.is_admin, 'PL', v.birth::date
FROM (VALUES
	('00000000-0000-4000-8000-000000000001', 'admin', '$2b$12$DlCgHl9Y/H4EOEKMHFVGHeyX80nr1kYZl7L22g.4kK4/p8z8TPO3C', 'admin@prism.cinema', true, 'Monthly', 30, true, '1990-01-01'),
	('00000000-0000-4000-8000-000000000002', 'subscriber', '$2b$12$J.ivHUIVJ4zBXeBsaV/JKO7n7Fdazb1Gnk7uBi5yiO5j4d6.hX9b2', 'subscriber@prism.cinema', true, 'Semiannual', 180, false, '1995-05-05'),
	('00000000-0000-4000-8000-000000000003', 'viewer', '$2b$12$5I9cCnbamYFUPoAAgFvKEO3F/HBJsHAP9/UHX8p6AiZRm8uBaE5la', 'viewer@prism.cinema', false, 'Free', 0, false, '2000-10-10')
) AS v(user_id, login, password_hash, mail, is_subscribed, plan, days, is_admin, birth)
JOIN public."SERVICE_SUBSCRIPTION_PLANS" p ON p.subscription_plan_type = v.plan;

INSERT INTO public."FAVOURITE_MOVIES" (user_id, movie_id)
SELECT '00000000-0000-4000-8000-000000000002', movie_id
FROM public."MOVIES"
WHERE movie_name IN ('The Shawshank Redemption', 'The Godfather', 'Inception', 'Fight Club');
