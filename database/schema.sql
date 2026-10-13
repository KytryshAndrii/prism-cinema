-- Prism.Cinema database schema: tables, views, functions, triggers and indexes.
-- Loaded automatically by the db container on first start (see docker-compose.yml).

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
-- Name: check_movie_has_director(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.check_movie_has_director() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM "MOVIE_DIRECTORS" 
        WHERE movie_id = NEW.movie_id
    ) THEN
        RAISE EXCEPTION '[Error]: Movie "%" must have director!', NEW.movie_name;
    END IF;
    RETURN NULL;
END;
$$;

--
-- Name: check_movie_release_year(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.check_movie_release_year() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.movie_release_date > CURRENT_DATE THEN
        RAISE EXCEPTION '[Error]: Date is back to future. Not valid!';
    END IF;

    RETURN NEW;
END;
$$;

--
-- Name: cleanup_movie_dependencies(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.cleanup_movie_dependencies() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Usuwanie powiązanych ulubionych filmów
    DELETE FROM "FAVOURITE_MOVIES" WHERE movie_id = OLD.movie_id;
    -- Usuwanie powiązanych licencji filmu
    DELETE FROM "MOVIE_LICENSES" WHERE movie_id = OLD.movie_id;
    -- Usuwanie powiązań z aktorami, reżyserami i gatunkami
    DELETE FROM "MOVIE_ACTORS"   WHERE movie_id = OLD.movie_id;
    DELETE FROM "MOVIE_DIRECTORS" WHERE movie_id = OLD.movie_id;
    DELETE FROM "MOVIE_GENRES"   WHERE movie_id = OLD.movie_id;
    -- Usuwanie dodatkowych danych i lokalizacji (np. plakatu, języka, napisów)
    DELETE FROM "ADDITIONAL_MOVIE_DATA" WHERE movie_id = OLD.movie_id;
    DELETE FROM "MOVIE_LOCALIZATIONS"   WHERE movie_id = OLD.movie_id;
    RETURN OLD;
END;
$$;

--
-- Name: cleanup_user_dependencies(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.cleanup_user_dependencies() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  DELETE FROM "FAVOURITE_MOVIES" WHERE user_id = OLD.user_id;
    RETURN NULL;
END;
$$;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ACTORS; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ACTORS" (
    actor_id uuid NOT NULL,
    first_name character varying(35) NOT NULL,
    middle_name character varying(35),
    last_name character varying(35) NOT NULL,
    birthplace character varying(100)
);

--
-- Name: TABLE "ACTORS"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."ACTORS" IS 'Table consist id of each actor and their name, middle name and surname';

--
-- Name: ADDITIONAL_MOVIE_DATA; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ADDITIONAL_MOVIE_DATA" (
    movie_id uuid NOT NULL,
    movie_poster bytea NOT NULL,
    movie_trailer text NOT NULL,
    movie_language character varying(3),
    movie_preview_poster bytea
);

--
-- Name: TABLE "ADDITIONAL_MOVIE_DATA"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."ADDITIONAL_MOVIE_DATA" IS 'Table with trailer link and movie poster';

--
-- Name: DIRECTORS; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."DIRECTORS" (
    director_id uuid NOT NULL,
    first_name character varying(35) NOT NULL,
    middle_name character varying(35),
    last_name character varying(35) NOT NULL,
    birthplace character varying(100)
);

--
-- Name: TABLE "DIRECTORS"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."DIRECTORS" IS 'Table consist id of each director and their name';

--
-- Name: FAVOURITE_MOVIES; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."FAVOURITE_MOVIES" (
    user_id uuid NOT NULL,
    movie_id uuid
);

--
-- Name: TABLE "FAVOURITE_MOVIES"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."FAVOURITE_MOVIES" IS 'The joint table that joins movies and users using MANY-to-MANY connection';

--
-- Name: GENRES; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."GENRES" (
    genre_id uuid NOT NULL,
    genre_name character varying(255) NOT NULL,
    genre_description character varying(255)
);

--
-- Name: TABLE "GENRES"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."GENRES" IS 'Table of movie GENRES descriptions and ect....';

--
-- Name: LICENSES; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."LICENSES" (
    license_id uuid NOT NULL,
    license_region character varying(3) NOT NULL,
    license_expiration_date date NOT NULL
);

--
-- Name: TABLE "LICENSES"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."LICENSES" IS 'Table that include licenses for exact film';

--
-- Name: MOVIES; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."MOVIES" (
    movie_id uuid NOT NULL,
    movie_name character varying(255) NOT NULL,
    movie_rating double precision DEFAULT 0.0,
    movie_release_date date NOT NULL,
    movie_pg character varying(10) NOT NULL,
    movie_description character varying(255) NOT NULL
);

--
-- Name: TABLE "MOVIES"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."MOVIES" IS 'Table of movies with their meta data and id';

--
-- Name: MOVIE_ACTORS; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."MOVIE_ACTORS" (
    movie_id uuid NOT NULL,
    actor_id uuid NOT NULL
);

--
-- Name: TABLE "MOVIE_ACTORS"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."MOVIE_ACTORS" IS 'Table that join actors and movies together. MANY-to-MANY';

--
-- Name: MOVIE_DIRECTORS; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."MOVIE_DIRECTORS" (
    movie_id uuid NOT NULL,
    director_id uuid NOT NULL
);

--
-- Name: TABLE "MOVIE_DIRECTORS"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."MOVIE_DIRECTORS" IS 'Table that join directors and movies together. MANY-to-MANY';

--
-- Name: MOVIE_GENRES; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."MOVIE_GENRES" (
    movie_id uuid NOT NULL,
    genre_id uuid NOT NULL
);

--
-- Name: TABLE "MOVIE_GENRES"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."MOVIE_GENRES" IS 'Table that join movies genres and movies and are related to them in MANY-to-MANY';

--
-- Name: MOVIE_LICENSES; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."MOVIE_LICENSES" (
    movie_id uuid NOT NULL,
    license_id uuid NOT NULL
);

--
-- Name: TABLE "MOVIE_LICENSES"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."MOVIE_LICENSES" IS 'Join table MANY-to-MANY';

--
-- Name: MOVIE_LOCALIZATIONS; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."MOVIE_LOCALIZATIONS" (
    movie_id uuid NOT NULL,
    subtitles_language character varying(3),
    subtitles json
);

--
-- Name: SERVICE_SUBSCRIPTION_PLANS; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."SERVICE_SUBSCRIPTION_PLANS" (
    subscription_plan_id uuid NOT NULL,
    subscription_plan_type character varying(50) NOT NULL,
    subscription_plan_cost integer NOT NULL,
    subscription_plan_description character varying(255)
);

--
-- Name: TABLE "SERVICE_SUBSCRIPTION_PLANS"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."SERVICE_SUBSCRIPTION_PLANS" IS 'Table that consist of plans that are able for user to choose from';

--
-- Name: USERS; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."USERS" (
    user_id uuid NOT NULL,
    user_login character varying(16) NOT NULL,
    user_password character varying(255) NOT NULL,
    user_mail character varying(255) NOT NULL,
    user_is_subscribed boolean NOT NULL,
    user_subscription_plan_id uuid,
    user_subscription_period daterange,
    user_is_admin boolean NOT NULL,
    user_location_region character varying(3) NOT NULL,
    user_date_of_birth date NOT NULL
);

--
-- Name: TABLE "USERS"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public."USERS" IS 'Table which will consist users';

--
-- Name: highest_rate_movies; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.highest_rate_movies AS
 SELECT movie_id,
    movie_name,
    movie_rating
   FROM public."MOVIES"
  WHERE (movie_rating > (8.5)::double precision);

--
-- Name: movies_language_info; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.movies_language_info AS
 SELECT m.movie_name AS movie_title,
    amd.movie_language AS original_language,
    ml.subtitles_language
   FROM ((public."MOVIES" m
     JOIN public."ADDITIONAL_MOVIE_DATA" amd ON ((amd.movie_id = m.movie_id)))
     JOIN public."MOVIE_LOCALIZATIONS" ml ON ((ml.movie_id = amd.movie_id)));

--
-- Name: movies_with_actors; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.movies_with_actors AS
 SELECT m.movie_name AS movie_title,
    (((a.first_name)::text || ' '::text) || (a.last_name)::text) AS actor
   FROM ((public."MOVIES" m
     JOIN public."MOVIE_ACTORS" ma ON ((ma.movie_id = m.movie_id)))
     JOIN public."ACTORS" a ON ((a.actor_id = ma.actor_id)));

--
-- Name: movies_with_directors; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.movies_with_directors AS
 SELECT m.movie_name AS movie_title,
    string_agg((((d.first_name)::text || ' '::text) || (d.last_name)::text), ', '::text) AS directors
   FROM ((public."MOVIES" m
     JOIN public."MOVIE_DIRECTORS" md ON ((md.movie_id = m.movie_id)))
     JOIN public."DIRECTORS" d ON ((d.director_id = md.director_id)))
  GROUP BY m.movie_name;

--
-- Name: user_favourites_movies; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.user_favourites_movies AS
 SELECT u.user_login AS user_,
    m.movie_name AS favourite_movie
   FROM ((public."FAVOURITE_MOVIES" f
     JOIN public."USERS" u ON ((u.user_id = f.user_id)))
     JOIN public."MOVIES" m ON ((m.movie_id = f.movie_id)));

--
-- Name: ACTORS ACTORS_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ACTORS"
    ADD CONSTRAINT "ACTORS_pkey" PRIMARY KEY (actor_id);

--
-- Name: DIRECTORS DIRECTORS_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."DIRECTORS"
    ADD CONSTRAINT "DIRECTORS_pkey" PRIMARY KEY (director_id);

--
-- Name: GENRES GENRES_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GENRES"
    ADD CONSTRAINT "GENRES_pkey" PRIMARY KEY (genre_id);

--
-- Name: LICENSES LICENSES_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."LICENSES"
    ADD CONSTRAINT "LICENSES_pkey" PRIMARY KEY (license_id);

--
-- Name: MOVIES MOVIES_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MOVIES"
    ADD CONSTRAINT "MOVIES_pkey" PRIMARY KEY (movie_id);

--
-- Name: SERVICE_SUBSCRIPTION_PLANS SERVICE_SUBSCRIPTION_PLANS_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."SERVICE_SUBSCRIPTION_PLANS"
    ADD CONSTRAINT "SERVICE_SUBSCRIPTION_PLANS_pkey" PRIMARY KEY (subscription_plan_id);

--
-- Name: USERS USERS_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."USERS"
    ADD CONSTRAINT "USERS_pkey" PRIMARY KEY (user_id);

--
-- Name: USERS login_not_email; Type: CHECK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE public."USERS"
    ADD CONSTRAINT login_not_email CHECK (((user_login)::text !~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::text)) NOT VALID;

--
-- Name: MOVIES movie_release_date; Type: CHECK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE public."MOVIES"
    ADD CONSTRAINT movie_release_date CHECK ((movie_release_date <= CURRENT_DATE)) NOT VALID;

--
-- Name: USERS user_birth_date_check; Type: CHECK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE public."USERS"
    ADD CONSTRAINT user_birth_date_check CHECK ((user_date_of_birth <= CURRENT_DATE)) NOT VALID;

--
-- Name: actor_birth_place_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX actor_birth_place_index ON public."ACTORS" USING btree (birthplace) WITH (deduplicate_items='true');

--
-- Name: actor_first_last_name_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX actor_first_last_name_index ON public."ACTORS" USING btree (first_name, last_name) WITH (deduplicate_items='true');

--
-- Name: actors_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX actors_index ON public."ACTORS" USING btree (actor_id) WITH (deduplicate_items='true');

--
-- Name: actors_movie_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX actors_movie_index ON public."MOVIE_ACTORS" USING btree (actor_id, movie_id) WITH (deduplicate_items='true');

--
-- Name: additional_movie_data_language_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX additional_movie_data_language_index ON public."ADDITIONAL_MOVIE_DATA" USING btree (movie_language) WITH (deduplicate_items='true');

--
-- Name: additional_movie_data_movie_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX additional_movie_data_movie_id_index ON public."ADDITIONAL_MOVIE_DATA" USING btree (movie_id) WITH (deduplicate_items='true');

--
-- Name: director_birth_place_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX director_birth_place_index ON public."DIRECTORS" USING btree (birthplace) WITH (deduplicate_items='true');

--
-- Name: director_first_last_name_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX director_first_last_name_index ON public."DIRECTORS" USING btree (first_name, last_name) WITH (deduplicate_items='true');

--
-- Name: director_movie_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX director_movie_index ON public."MOVIE_DIRECTORS" USING btree (director_id, movie_id) WITH (deduplicate_items='true');

--
-- Name: directors_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX directors_index ON public."DIRECTORS" USING btree (director_id) WITH (deduplicate_items='true');

--
-- Name: fav_movies_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fav_movies_index ON public."FAVOURITE_MOVIES" USING btree (user_id, movie_id) WITH (deduplicate_items='true');

--
-- Name: genre_movie_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX genre_movie_index ON public."MOVIE_GENRES" USING btree (genre_id, movie_id) WITH (deduplicate_items='true');

--
-- Name: genres_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX genres_index ON public."GENRES" USING btree (genre_id) WITH (deduplicate_items='true');

--
-- Name: genres_name_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX genres_name_index ON public."GENRES" USING btree (genre_name) WITH (deduplicate_items='true');

--
-- Name: movie_actors_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX movie_actors_index ON public."MOVIE_ACTORS" USING btree (movie_id, actor_id) WITH (deduplicate_items='true');

--
-- Name: movie_directors_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX movie_directors_index ON public."MOVIE_DIRECTORS" USING btree (movie_id, director_id) WITH (deduplicate_items='true');

--
-- Name: movie_genres_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX movie_genres_index ON public."MOVIE_GENRES" USING btree (movie_id, genre_id) WITH (deduplicate_items='true');

--
-- Name: movie_licence_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX movie_licence_index ON public."MOVIE_LICENSES" USING btree (license_id) WITH (deduplicate_items='true');

--
-- Name: movie_localization_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX movie_localization_id_index ON public."MOVIE_LOCALIZATIONS" USING btree (movie_id) INCLUDE (subtitles) WITH (deduplicate_items='true');

--
-- Name: movie_localization_langiage_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX movie_localization_langiage_index ON public."MOVIE_LOCALIZATIONS" USING btree (subtitles_language) WITH (deduplicate_items='true');

--
-- Name: movie_pg_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX movie_pg_index ON public."MOVIES" USING btree (movie_pg) WITH (deduplicate_items='true');

--
-- Name: movie_rating_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX movie_rating_index ON public."MOVIES" USING btree (movie_rating) WITH (deduplicate_items='true');

--
-- Name: movies_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX movies_index ON public."MOVIES" USING btree (movie_id) WITH (deduplicate_items='true');

--
-- Name: user_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX user_index ON public."USERS" USING btree (user_id) INCLUDE (user_is_subscribed, user_subscription_plan_id, user_is_admin) WITH (deduplicate_items='true');

--
-- Name: user_password_mail_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX user_password_mail_index ON public."USERS" USING btree (user_password, user_mail) WITH (deduplicate_items='true');

--
-- Name: MOVIES trg_check_movie_release_year; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_check_movie_release_year BEFORE INSERT ON public."MOVIES" FOR EACH ROW EXECUTE FUNCTION public.check_movie_release_year();

--
-- Name: MOVIES trg_cleanup_movie_delete; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_cleanup_movie_delete BEFORE DELETE ON public."MOVIES" FOR EACH ROW EXECUTE FUNCTION public.cleanup_movie_dependencies();

--
-- Name: USERS trg_cleanup_user_delete; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_cleanup_user_delete BEFORE DELETE ON public."USERS" FOR EACH ROW EXECUTE FUNCTION public.cleanup_user_dependencies();

--
-- Name: MOVIES trg_movie_has_director; Type: TRIGGER; Schema: public; Owner: -
--

CREATE CONSTRAINT TRIGGER trg_movie_has_director AFTER INSERT ON public."MOVIES" DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION public.check_movie_has_director();

ALTER TABLE public."MOVIES" DISABLE TRIGGER trg_movie_has_director;

--
-- Name: MOVIE_ACTORS Actor key; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MOVIE_ACTORS"
    ADD CONSTRAINT "Actor key" FOREIGN KEY (actor_id) REFERENCES public."ACTORS"(actor_id) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: CONSTRAINT "Actor key" ON "MOVIE_ACTORS"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT "Actor key" ON public."MOVIE_ACTORS" IS 'FK for actors table ids. MANY-to_MANY';

--
-- Name: MOVIE_DIRECTORS Director key; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MOVIE_DIRECTORS"
    ADD CONSTRAINT "Director key" FOREIGN KEY (director_id) REFERENCES public."DIRECTORS"(director_id) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: CONSTRAINT "Director key" ON "MOVIE_DIRECTORS"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT "Director key" ON public."MOVIE_DIRECTORS" IS 'FK for directors table and their ids, MANY-to-MANY';

--
-- Name: MOVIE_GENRES Genre id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MOVIE_GENRES"
    ADD CONSTRAINT "Genre id" FOREIGN KEY (genre_id) REFERENCES public."GENRES"(genre_id) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: CONSTRAINT "Genre id" ON "MOVIE_GENRES"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT "Genre id" ON public."MOVIE_GENRES" IS 'FK for genres table';

--
-- Name: MOVIE_LICENSES LICENSE_ID FK; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MOVIE_LICENSES"
    ADD CONSTRAINT "LICENSE_ID FK" FOREIGN KEY (license_id) REFERENCES public."LICENSES"(license_id);

--
-- Name: MOVIE_LICENSES MOVIE_ID FK; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MOVIE_LICENSES"
    ADD CONSTRAINT "MOVIE_ID FK" FOREIGN KEY (movie_id) REFERENCES public."MOVIES"(movie_id) MATCH FULL;

--
-- Name: MOVIE_LOCALIZATIONS MOVIE_LOCALIZATIONS_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MOVIE_LOCALIZATIONS"
    ADD CONSTRAINT "MOVIE_LOCALIZATIONS_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES public."MOVIES"(movie_id);

--
-- Name: FAVOURITE_MOVIES Movie Id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."FAVOURITE_MOVIES"
    ADD CONSTRAINT "Movie Id" FOREIGN KEY (movie_id) REFERENCES public."MOVIES"(movie_id);

--
-- Name: CONSTRAINT "Movie Id" ON "FAVOURITE_MOVIES"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT "Movie Id" ON public."FAVOURITE_MOVIES" IS 'FK to movies table';

--
-- Name: ADDITIONAL_MOVIE_DATA Movie id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ADDITIONAL_MOVIE_DATA"
    ADD CONSTRAINT "Movie id" FOREIGN KEY (movie_id) REFERENCES public."MOVIES"(movie_id) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: CONSTRAINT "Movie id" ON "ADDITIONAL_MOVIE_DATA"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT "Movie id" ON public."ADDITIONAL_MOVIE_DATA" IS 'FK to PK of movies table';

--
-- Name: MOVIE_GENRES Movie id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MOVIE_GENRES"
    ADD CONSTRAINT "Movie id" FOREIGN KEY (movie_id) REFERENCES public."MOVIES"(movie_id) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: CONSTRAINT "Movie id" ON "MOVIE_GENRES"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT "Movie id" ON public."MOVIE_GENRES" IS 'FK for movie table';

--
-- Name: MOVIE_ACTORS Movie key; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MOVIE_ACTORS"
    ADD CONSTRAINT "Movie key" FOREIGN KEY (movie_id) REFERENCES public."MOVIES"(movie_id) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: CONSTRAINT "Movie key" ON "MOVIE_ACTORS"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT "Movie key" ON public."MOVIE_ACTORS" IS 'FK for movies table';

--
-- Name: MOVIE_DIRECTORS Movie key; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MOVIE_DIRECTORS"
    ADD CONSTRAINT "Movie key" FOREIGN KEY (movie_id) REFERENCES public."MOVIES"(movie_id);

--
-- Name: CONSTRAINT "Movie key" ON "MOVIE_DIRECTORS"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT "Movie key" ON public."MOVIE_DIRECTORS" IS 'KF for movies table and its id. MANY-to-MANY';

--
-- Name: USERS USERS_user_subscription_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."USERS"
    ADD CONSTRAINT "USERS_user_subscription_plan_id_fkey" FOREIGN KEY (user_subscription_plan_id) REFERENCES public."SERVICE_SUBSCRIPTION_PLANS"(subscription_plan_id) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: FAVOURITE_MOVIES User id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."FAVOURITE_MOVIES"
    ADD CONSTRAINT "User id" FOREIGN KEY (user_id) REFERENCES public."USERS"(user_id);

--
-- Name: CONSTRAINT "User id" ON "FAVOURITE_MOVIES"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT "User id" ON public."FAVOURITE_MOVIES" IS 'FK for user in users table ';

--
--
