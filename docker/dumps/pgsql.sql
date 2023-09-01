--
-- PostgreSQL database dump
--

-- Dumped from database version 15.0
-- Dumped by pg_dump version 15.0

-- Started on 2023-08-31 20:49:23

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
-- TOC entry 220 (class 1255 OID 51229)
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
-- TOC entry 221 (class 1255 OID 51169)
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
-- TOC entry 234 (class 1255 OID 51239)
-- Name: sign_in(character varying, character varying, character varying, character varying, inet, bigint); Type: FUNCTION; Schema: public; Owner: mypass
--

CREATE FUNCTION public.sign_in(email character varying, secret_string character varying, token character varying, device character varying, ip inet, expiration bigint) RETURNS boolean
    LANGUAGE plpgsql
    AS $_$DECLARE
user_id UUID;
timestmp BIGINT;
BEGIN
timestmp := EXTRACT(EPOCH FROM current_timestamp)::bigint;
SELECT u_id INTO user_id FROM u_users WHERE u_email = $1 AND u_secret_string=$2;
IF user_id IS NULL THEN
	RETURN FALSE;
END IF;
INSERT INTO t_tokens VALUES(gen_random_uuid (),user_id,$3,timestmp,timestmp,$4,$5,timestmp+$6);
RETURN TRUE;
END$_$;


ALTER FUNCTION public.sign_in(email character varying, secret_string character varying, token character varying, device character varying, ip inet, expiration bigint) OWNER TO mypass;

--
-- TOC entry 237 (class 1255 OID 51228)
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
-- TOC entry 235 (class 1255 OID 51240)
-- Name: sign_up(character varying, character varying, character varying, inet, character varying, boolean); Type: PROCEDURE; Schema: public; Owner: mypass
--

CREATE PROCEDURE public.sign_up(IN email character varying, IN secret_string character varying, IN login character varying, IN reg_ip inet, IN avatar character varying, IN confirm boolean)
    LANGUAGE plpgsql
    AS $_$BEGIN
INSERT INTO u_users VALUES (gen_random_uuid(),$1,$3,$4,$5,$6,EXTRACT(EPOCH FROM current_timestamp)::bigint,$2);
END$_$;


ALTER PROCEDURE public.sign_up(IN email character varying, IN secret_string character varying, IN login character varying, IN reg_ip inet, IN avatar character varying, IN confirm boolean) OWNER TO mypass;

--
-- TOC entry 236 (class 1255 OID 51241)
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
-- TOC entry 233 (class 1255 OID 51212)
-- Name: update_token_info(character varying, character varying, inet); Type: FUNCTION; Schema: public; Owner: mypass
--

CREATE FUNCTION public.update_token_info(token character varying, device character varying, ip inet) RETURNS boolean
    LANGUAGE plpgsql
    AS $_$BEGIN
    UPDATE t_tokens
    SET t_last_login = EXTRACT(EPOCH FROM current_timestamp)::BIGINT,
        t_device = $2,
		t_last_ip = $3
    WHERE active_token($1) = TRUE;
    RETURN FOUND;
END;$_$;


ALTER FUNCTION public.update_token_info(token character varying, device character varying, ip inet) OWNER TO mypass;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 51040)
-- Name: a_accesses; Type: TABLE; Schema: public; Owner: mypass
--

CREATE TABLE public.a_accesses (
    a_id uuid NOT NULL,
    a_u_id uuid NOT NULL,
    a_s_id uuid NOT NULL
);


ALTER TABLE public.a_accesses OWNER TO mypass;

--
-- TOC entry 218 (class 1259 OID 51083)
-- Name: e_ecodes; Type: TABLE; Schema: public; Owner: mypass
--

CREATE TABLE public.e_ecodes (
    e_id uuid NOT NULL,
    e_u_id uuid NOT NULL,
    e_code integer NOT NULL,
    e_expiration bigint NOT NULL
);


ALTER TABLE public.e_ecodes OWNER TO mypass;

--
-- TOC entry 216 (class 1259 OID 51028)
-- Name: r_records; Type: TABLE; Schema: public; Owner: mypass
--

CREATE TABLE public.r_records (
    r_id uuid NOT NULL,
    r_s_id uuid NOT NULL,
    r_title character varying(512),
    r_partition jsonb,
    r_notes character varying(512),
    r_tags character varying(512),
    r_last_change bigint NOT NULL,
    r_created bigint NOT NULL,
    r_icon character varying(512) NOT NULL,
    r_category character varying(64) NOT NULL,
    r_favourite boolean NOT NULL
);


ALTER TABLE public.r_records OWNER TO mypass;

--
-- TOC entry 215 (class 1259 OID 51016)
-- Name: s_safes; Type: TABLE; Schema: public; Owner: mypass
--

CREATE TABLE public.s_safes (
    s_id uuid NOT NULL,
    s_u_id uuid NOT NULL,
    s_name character varying(256) NOT NULL,
    s_description character varying(256) NOT NULL,
    s_icon character varying(512) NOT NULL
);


ALTER TABLE public.s_safes OWNER TO mypass;

--
-- TOC entry 214 (class 1259 OID 51002)
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
-- TOC entry 219 (class 1259 OID 51193)
-- Name: u_users; Type: TABLE; Schema: public; Owner: mypass
--

CREATE TABLE public.u_users (
    u_id uuid NOT NULL,
    u_email character varying(320) NOT NULL,
    u_login character varying(50) NOT NULL,
    u_reg_ip inet NOT NULL,
    u_icon character varying(512) NOT NULL,
    u_confirm boolean NOT NULL,
    u_reg_time bigint NOT NULL,
    u_secret_string character varying(512) NOT NULL
);


ALTER TABLE public.u_users OWNER TO mypass;

--
-- TOC entry 3364 (class 0 OID 51040)
-- Dependencies: 217
-- Data for Name: a_accesses; Type: TABLE DATA; Schema: public; Owner: mypass
--

COPY public.a_accesses (a_id, a_u_id, a_s_id) FROM stdin;
\.


--
-- TOC entry 3365 (class 0 OID 51083)
-- Dependencies: 218
-- Data for Name: e_ecodes; Type: TABLE DATA; Schema: public; Owner: mypass
--

COPY public.e_ecodes (e_id, e_u_id, e_code, e_expiration) FROM stdin;
\.


--
-- TOC entry 3363 (class 0 OID 51028)
-- Dependencies: 216
-- Data for Name: r_records; Type: TABLE DATA; Schema: public; Owner: mypass
--

COPY public.r_records (r_id, r_s_id, r_title, r_partition, r_notes, r_tags, r_last_change, r_created, r_icon, r_category, r_favourite) FROM stdin;
\.


--
-- TOC entry 3362 (class 0 OID 51016)
-- Dependencies: 215
-- Data for Name: s_safes; Type: TABLE DATA; Schema: public; Owner: mypass
--

COPY public.s_safes (s_id, s_u_id, s_name, s_description, s_icon) FROM stdin;
\.


--
-- TOC entry 3361 (class 0 OID 51002)
-- Dependencies: 214
-- Data for Name: t_tokens; Type: TABLE DATA; Schema: public; Owner: mypass
--

COPY public.t_tokens (t_id, t_u_id, t_token, t_first_login, t_last_login, t_device, t_last_ip, t_expiration) FROM stdin;
d26407f4-2237-4a67-ba59-82e31105833d	658ed9f5-84bc-463b-a2b9-075413ff51bc	5dca31539d3c09934fe8e2587ae0c2fc30e6c95cb087d9114ebfe98cef9f3cab	1692803824	1692803824	Windows	192.168.1.1	1692805624
\.


--
-- TOC entry 3366 (class 0 OID 51193)
-- Dependencies: 219
-- Data for Name: u_users; Type: TABLE DATA; Schema: public; Owner: mypass
--

COPY public.u_users (u_id, u_email, u_login, u_reg_ip, u_icon, u_confirm, u_reg_time, u_secret_string) FROM stdin;
658ed9f5-84bc-463b-a2b9-075413ff51bc	rfe@efmail.com	FirstUser	192.168.1.1	None	f	1692803210	Hello=
\.


--
-- TOC entry 3208 (class 2606 OID 51044)
-- Name: a_accesses a_access_pkey; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.a_accesses
    ADD CONSTRAINT a_access_pkey PRIMARY KEY (a_id);


--
-- TOC entry 3210 (class 2606 OID 51087)
-- Name: e_ecodes e_ecodes_pkey; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.e_ecodes
    ADD CONSTRAINT e_ecodes_pkey PRIMARY KEY (e_id);


--
-- TOC entry 3206 (class 2606 OID 51034)
-- Name: r_records r_login_pkey; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.r_records
    ADD CONSTRAINT r_login_pkey PRIMARY KEY (r_id);


--
-- TOC entry 3204 (class 2606 OID 51022)
-- Name: s_safes s_safes_pkey; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.s_safes
    ADD CONSTRAINT s_safes_pkey PRIMARY KEY (s_id);


--
-- TOC entry 3200 (class 2606 OID 51008)
-- Name: t_tokens t_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.t_tokens
    ADD CONSTRAINT t_tokens_pkey PRIMARY KEY (t_id);


--
-- TOC entry 3202 (class 2606 OID 51172)
-- Name: t_tokens t_tokens_t_token_key; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.t_tokens
    ADD CONSTRAINT t_tokens_t_token_key UNIQUE (t_token);


--
-- TOC entry 3212 (class 2606 OID 51199)
-- Name: u_users u_users_pkey; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.u_users
    ADD CONSTRAINT u_users_pkey PRIMARY KEY (u_id);


--
-- TOC entry 3214 (class 2606 OID 51201)
-- Name: u_users u_users_u_email_key; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.u_users
    ADD CONSTRAINT u_users_u_email_key UNIQUE (u_email);


--
-- TOC entry 3216 (class 2606 OID 51238)
-- Name: u_users u_users_u_secret_string_key; Type: CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.u_users
    ADD CONSTRAINT u_users_u_secret_string_key UNIQUE (u_secret_string);


--
-- TOC entry 3218 (class 2606 OID 51050)
-- Name: a_accesses a_access_a_s_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.a_accesses
    ADD CONSTRAINT a_access_a_s_id_fkey FOREIGN KEY (a_s_id) REFERENCES public.s_safes(s_id);


--
-- TOC entry 3217 (class 2606 OID 51035)
-- Name: r_records r_login_r_s_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mypass
--

ALTER TABLE ONLY public.r_records
    ADD CONSTRAINT r_login_r_s_id_fkey FOREIGN KEY (r_s_id) REFERENCES public.s_safes(s_id);


-- Completed on 2023-08-31 20:49:24

--
-- PostgreSQL database dump complete
--

