--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4 (Debian 15.4-1.pgdg120+1)
-- Dumped by pg_dump version 15.4 (Debian 15.4-1.pgdg120+1)

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
-- Name: active_token(character varying); Type: FUNCTION; Schema: public; Owner: mypass
--

CREATE FUNCTION public.active_token(token character varying) RETURNS boolean
    LANGUAGE plpgsql
    AS $_$DECLARE
    record_exists BOOLEAN;
BEGIN
SELECT EXISTS (SELECT t_id FROM t_tokens WHERE t_token = $1 AND EXTRACT(EPOCH FROM current_timestamp)::BIGINT <= t_expiration) INTO record_exists;
RETURN record_exists;
END;$_$;


ALTER FUNCTION public.active_token(token character varying) OWNER TO mypass;

--
-- Name: create_safe(character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: mypass
--

CREATE FUNCTION public.create_safe(token character varying, name character varying, description character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $_$
declare
    user_id UUID;
    safe_id UUID;
    timestmp BIGINT;
begin
timestmp := EXTRACT(EPOCH FROM current_timestamp)::bigint;
SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;
IF user_id IS NULL THEN
    RETURN -1;
END IF;
INSERT INTO s_safes VALUES (gen_random_uuid(),user_id,$2,$3,timestmp,timestmp) RETURNING s_id INTO safe_id;
IF safe_id IS NULL THEN
    RETURN -2;
END IF;
RETURN 0;
end;
$_$;


ALTER FUNCTION public.create_safe(token character varying, name character varying, description character varying) OWNER TO mypass;

--
-- Name: send_code(character varying, integer, bigint); Type: PROCEDURE; Schema: public; Owner: mypass
--

CREATE PROCEDURE public.send_code(IN email character varying, IN code integer, IN expiration bigint)
    LANGUAGE plpgsql
    AS $_$DECLARE
user_id UUID;
BEGIN
SELECT u_id INTO user_id FROM u_users WHERE u_email = $1;
INSERT INTO e_ecodes VALUES (gen_random_uuid(),user_id,$2,$3);
END$_$;


ALTER PROCEDURE public.send_code(IN email character varying, IN code integer, IN expiration bigint) OWNER TO mypass;

--
-- Name: sign_in(character varying, character varying, character varying, character varying, inet, bigint); Type: FUNCTION; Schema: public; Owner: mypass
--

CREATE FUNCTION public.sign_in(login character varying, secret_string character varying, token character varying, device character varying, ip inet, expiration bigint) RETURNS boolean
    LANGUAGE plpgsql
    AS $_$DECLARE
user_id UUID;
timestmp BIGINT;
BEGIN
timestmp := EXTRACT(EPOCH FROM current_timestamp)::bigint;
SELECT u_id INTO user_id FROM u_users WHERE u_login = $1 AND u_secret_string=$2 AND u_confirm = TRUE;
IF user_id IS NULL THEN
	RETURN FALSE;
END IF;
INSERT INTO t_tokens VALUES(gen_random_uuid (),user_id,$3,timestmp,timestmp,$4,$5,timestmp+$6);
RETURN TRUE;
END$_$;


ALTER FUNCTION public.sign_in(login character varying, secret_string character varying, token character varying, device character varying, ip inet, expiration bigint) OWNER TO mypass;

--
-- Name: sign_out(character varying, uuid); Type: FUNCTION; Schema: public; Owner: mypass
--

CREATE FUNCTION public.sign_out(token character varying, token_id uuid) RETURNS boolean
    LANGUAGE plpgsql
    AS $_$DECLARE
    user_id UUID;
    deletion_successful BOOLEAN;
BEGIN
    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1;
    
    IF user_id IS NULL THEN
        deletion_successful := FALSE;
    ELSE
        DELETE FROM t_tokens WHERE t_u_id = user_id AND t_id = $2;
        IF FOUND THEN
            deletion_successful := TRUE;
        ELSE
            deletion_successful := FALSE;
        END IF;
    END IF;
    
    RETURN deletion_successful;
END;
$_$;


ALTER FUNCTION public.sign_out(token character varying, token_id uuid) OWNER TO mypass;

--
-- Name: sign_up(character varying, character varying, inet, boolean, character varying, integer[]); Type: FUNCTION; Schema: public; Owner: mypass
--

CREATE FUNCTION public.sign_up(login character varying, secret_string character varying, reg_ip inet, confirm boolean, secret_code character varying, reserves integer[]) RETURNS integer
    LANGUAGE plpgsql
    AS $_$
declare
    user_id UUID;
    code_id UUID;

    user_id_insert UUID;
    code_id_insert UUID;
    current_timeu BIGINT;
BEGIN
current_timeu := EXTRACT(EPOCH FROM current_timestamp)::bigint;

SELECT u_id INTO user_id FROM u_users WHERE u_login = $1 AND u_secret_string = $2 AND u_confirm = FALSE;

IF user_id IS NULL THEN
    INSERT INTO u_users VALUES (gen_random_uuid (),$1,$3,$4,current_timeu,$2) RETURNING u_id INTO user_id_insert;
    IF user_id_insert IS NULL THEN
        RETURN -1;
    END IF;
    INSERT INTO c_codes VALUES (gen_random_uuid(),user_id_insert,$5,$6,current_timeu) RETURNING c_id INTO code_id_insert;
    IF code_id_insert IS NULL THEN
        RETURN -2;
    END IF;
    RETURN 0;
END IF;

SELECT c_id INTO code_id FROM c_codes WHERE c_u_id = user_id;
IF code_id IS NULL THEN
    INSERT INTO c_codes VALUES (gen_random_uuid(),user_id,$5,$6,current_timeu) RETURNING c_id INTO code_id_insert;
    IF code_id_insert IS NULL THEN
        RETURN -3;
    END IF;
    RETURN 1;
END IF;

UPDATE c_codes SET c_secret_code = $5,c_reserves = $6,c_created_at = current_timeu WHERE c_u_id = user_id RETURNING c_codes.c_id INTO code_id;
IF code_id IS NULL THEN
    RETURN -4;
END IF;
RETURN 2;

END
$_$;


ALTER FUNCTION public.sign_up(login character varying, secret_string character varying, reg_ip inet, confirm boolean, secret_code character varying, reserves integer[]) OWNER TO mypass;

--
-- Name: update_secret_string(character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: mypass
--

CREATE FUNCTION public.update_secret_string(old_secret_string character varying, new_secret_string character varying, token character varying) RETURNS boolean
    LANGUAGE plpgsql
    AS $_$BEGIN
UPDATE u_users AS u_us
SET u_secret_string = $2
FROM t_tokens AS t_ts
WHERE t_ts.t_u_id = u_us.u_id AND u_secret_string = $1 AND active_token($3) = TRUE;
RETURN FOUND;
END;$_$;


ALTER FUNCTION public.update_secret_string(old_secret_string character varying, new_secret_string character varying, token character varying) OWNER TO mypass;

--
-- Name: update_token_info(character varying, character varying, inet); Type: FUNCTION; Schema: public; Owner: mypass
--

CREATE FUNCTION public.update_token_info(token character varying, device character varying, ip inet) RETURNS boolean
    LANGUAGE plpgsql
    AS $_$BEGIN

    UPDATE t_tokens

    SET t_last_login = EXTRACT(EPOCH FROM current_timestamp)::BIGINT,

        t_device = $2,

		t_last_ip = $3

    WHERE active_token($1) = TRUE AND t_token = $1;

    RETURN FOUND;

END;$_$;


ALTER FUNCTION public.update_token_info(token character varying, device character varying, ip inet) OWNER TO mypass;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: a_accesses; Type: TABLE; Schema: public; Owner: mypass
--

CREATE TABLE public.a_accesses (
    a_id uuid NOT NULL,
    a_u_id uuid NOT NULL,
    a_s_id uuid NOT NULL
);


ALTER TABLE public.a_accesses OWNER TO mypass;

--
-- Name: c_codes; Type: TABLE; Schema: public; Owner: mypass
--

CREATE TABLE public.c_codes (
    c_id uuid NOT NULL,
    c_u_id uuid NOT NULL,
    c_secret_code character varying(32) NOT NULL,
    c_reserves integer[] NOT NULL,
    c_created_at bigint NOT NULL
);


ALTER TABLE public.c_codes OWNER TO mypass;

--
-- Name: r_records; Type: TABLE; Schema: public; Owner: mypass
--

CREATE TABLE public.r_records (
    r_id uuid NOT NULL,
    r_s_id uuid NOT NULL,
    r_title character varying(512),
    r_partition character varying(1024),
    r_notes character varying(512),
    r_tags character varying(512),
    r_last_change bigint NOT NULL,
    r_created bigint NOT NULL,
    r_category character varying(64) NOT NULL,
    r_favourite boolean NOT NULL
);


ALTER TABLE public.r_records OWNER TO mypass;

--
-- Name: s_safes; Type: TABLE; Schema: public; Owner: mypass
--

CREATE TABLE public.s_safes (
    s_id uuid NOT NULL,
    s_u_id uuid NOT NULL,
    s_name character varying(256) NOT NULL,
    s_description character varying(500) NOT NULL,
    s_created_at bigint NOT NULL,
    s_updated_at bigint NOT NULL
);


ALTER TABLE public.s_safes OWNER TO mypass;

--
-- Name: t_tokens; Type: TABLE; Schema: public; Owner: mypass
--

CREATE TABLE public.t_tokens (
    t_id uuid NOT NULL,
    t_u_id uuid NOT NULL,
    t_token character varying(128) NOT NULL,
    t_first_login bigint NOT NULL,
    t_last_login bigint NOT NULL,
    t_device character varying(50) NOT NULL,
    t_last_ip inet NOT NULL,
    t_expiration bigint NOT NULL
);


ALTER TABLE public.t_tokens OWNER TO mypass;

--
-- Name: u_users; Type: TABLE; Schema: public; Owner: mypass
--

CREATE TABLE public.u_users (
    u_id uuid NOT NULL,
    u_login character varying(64) NOT NULL,
    u_reg_ip inet NOT NULL,
    u_confirm boolean NOT NULL,
    u_reg_time bigint NOT NULL,
    u_secret_string character varying(512) NOT NULL
);


ALTER TABLE public.u_users OWNER TO mypass;

--
-- Data for Name: a_accesses; Type: TABLE DATA; Schema: public; Owner: mypass
--

COPY public.a_accesses (a_id, a_u_id, a_s_id) FROM stdin;
\.


--
-- Data for Name: c_codes; Type: TABLE DATA; Schema: public; Owner: mypass
--

COPY public.c_codes (c_id, c_u_id, c_secret_code, c_reserves, c_created_at) FROM stdin;
\.


--
-- Data for Name: r_records; Type: TABLE DATA; Schema: public; Owner: mypass
--

COPY public.r_records (r_id, r_s_id, r_title, r_partition, r_notes, r_tags, r_last_change, r_created, r_category, r_favourite) FROM stdin;
\.


--
-- Data for Name: s_safes; Type: TABLE DATA; Schema: public; Owner: mypass
--

COPY public.s_safes (s_id, s_u_id, s_name, s_description, s_created_at, s_updated_at) FROM stdin;
1a5206a9-566b-46ff-aed6-552b0a6a8ee7	d66228e1-62b3-42e7-8011-3f55065e9bdf	safe1	63ef04244a72f021557e8b6df3c54e973747c53bf8e6ec1f16ccfd2b51dd51caa5f802fd7262a54dbd3930f05c107cd607c48b4fa04c5b0cec2e84d911f5fa0ef98550e0500874460502383ba5	1694626830	1694626830
\.


--
-- Data for Name: t_tokens; Type: TABLE DATA; Schema: public; Owner: mypass
--

COPY public.t_tokens (t_id, t_u_id, t_token, t_first_login, t_last_login, t_device, t_last_ip, t_expiration) FROM stdin;
a55dca73-b199-4324-9049-9d6abf309d87	d66228e1-62b3-42e7-8011-3f55065e9bdf	c3dca6323b4dc8ccae9d3d997cd849ce08b0b239900aabd9ee96dd4c45c21c07	1694626829	1694626829	python/win	192.168.1.1	1694630429
643d4acd-62aa-4b05-9f45-52746a44b067	d66228e1-62b3-42e7-8011-3f55065e9bdf	2b80b37c0da8efe298e70f68c0f68662487fc057260e34d02d3d68a9f538ff00	1694626830	1694626830	python/win	192.168.1.1	1694630430
d77f19c5-c025-4fcb-a37e-1fca95cff5a0	d66228e1-62b3-42e7-8011-3f55065e9bdf	1af34bdfde746082680756c3c3d6bfd2a3b082e29979eb388a271fedf61666a0	1694626830	1694626830	python/win	192.168.1.1	1694630430
101f88cc-2b9f-44c8-a62b-34df2d5541aa	d66228e1-62b3-42e7-8011-3f55065e9bdf	f98011afcc37e944bcdfdd6ce3df2d90dba487185c25c19fede5a9c50002869a	1694626830	1694626830	python/win	192.168.1.1	1694630430
\.


--
-- Data for Name: u_users; Type: TABLE DATA; Schema: public; Owner: mypass
--

COPY public.u_users (u_id, u_login, u_reg_ip, u_confirm, u_reg_time, u_secret_string) FROM stdin;
\.


--
-- Name: a_accesses a_access_pkey; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.a_accesses
    ADD CONSTRAINT a_access_pkey PRIMARY KEY (a_id);


--
-- Name: c_codes c_codes_pk; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.c_codes
    ADD CONSTRAINT c_codes_pk UNIQUE (c_u_id);


--
-- Name: c_codes e_ecodes_pkey; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.c_codes
    ADD CONSTRAINT e_ecodes_pkey PRIMARY KEY (c_id);


--
-- Name: r_records r_login_pkey; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.r_records
    ADD CONSTRAINT r_login_pkey PRIMARY KEY (r_id);


--
-- Name: s_safes s_safes_pkey; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.s_safes
    ADD CONSTRAINT s_safes_pkey PRIMARY KEY (s_id);


--
-- Name: t_tokens t_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.t_tokens
    ADD CONSTRAINT t_tokens_pkey PRIMARY KEY (t_id);


--
-- Name: t_tokens t_tokens_t_token_key; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.t_tokens
    ADD CONSTRAINT t_tokens_t_token_key UNIQUE (t_token);


--
-- Name: u_users u_users_pk; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.u_users
    ADD CONSTRAINT u_users_pk UNIQUE (u_login);


--
-- Name: u_users u_users_pkey; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.u_users
    ADD CONSTRAINT u_users_pkey PRIMARY KEY (u_id);


--
-- Name: u_users u_users_u_secret_string_key; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.u_users
    ADD CONSTRAINT u_users_u_secret_string_key UNIQUE (u_secret_string);


--
-- Name: a_accesses a_access_a_s_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.a_accesses
    ADD CONSTRAINT a_access_a_s_id_fkey FOREIGN KEY (a_s_id) REFERENCES public.s_safes(s_id);


--
-- Name: r_records r_login_r_s_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.r_records
    ADD CONSTRAINT r_login_r_s_id_fkey FOREIGN KEY (r_s_id) REFERENCES public.s_safes(s_id);


--
-- PostgreSQL database dump complete
--

