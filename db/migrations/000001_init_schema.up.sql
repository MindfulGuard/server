CREATE TYPE public.object_ AS ENUM (
    'user',
    'safe',
    'item',
    'file'
);

CREATE TYPE public.action_status AS ENUM (
    'create',
    'update',
    'delete',
    'download',
    'upload',
    'sign_up',
    'sign_in',
    'sign_out'
);

CREATE TABLE public.u_users (
    u_id uuid NOT NULL PRIMARY KEY,
    u_login character varying(64) NOT NULL,
    u_reg_ip inet NOT NULL,
    u_confirm boolean NOT NULL,
    u_created_at bigint NOT NULL,
    u_secret_string character varying(512) NOT NULL,
    u_admin boolean NOT NULL
);

CREATE TABLE public.t_tokens (
    t_id uuid NOT NULL PRIMARY KEY,
    t_u_id uuid NOT NULL,
    t_token character varying(128) NOT NULL,
    t_created_at bigint NOT NULL,
    t_updated_at bigint NOT NULL,
    t_device character varying(512) NOT NULL,
    t_last_ip inet NOT NULL,
    t_expiration bigint NOT NULL,
    FOREIGN KEY (t_u_id) REFERENCES public.u_users (u_id)
);

CREATE TABLE public.c_codes (
    c_id uuid NOT NULL PRIMARY KEY,
    c_u_id uuid NOT NULL,
    c_secret_code character varying(32) NOT NULL,
    c_backup_codes integer [] NOT NULL,
    c_created_at bigint NOT NULL,
    c_updated_at bigint NOT NULL,
    FOREIGN KEY (c_u_id) REFERENCES public.u_users (u_id)
);

CREATE TABLE public.s_safes (
    s_id uuid NOT NULL PRIMARY KEY,
    s_u_id uuid NOT NULL,
    s_name character varying(64) NOT NULL,
    s_description character varying(580) NOT NULL,
    s_created_at bigint NOT NULL,
    s_updated_at bigint NOT NULL,
    FOREIGN KEY (s_u_id) REFERENCES public.u_users (u_id)
);

CREATE TABLE public.r_records (
    r_id uuid NOT NULL PRIMARY KEY,
    r_s_id uuid NOT NULL,
    r_u_id uuid NOT NULL,
    r_title character varying(512) NOT NULL,
    r_item json NOT NULL,
    r_notes character varying(1024) NOT NULL,
    r_tags character varying [] NOT NULL,
    r_created_at bigint NOT NULL,
    r_updated_at bigint NOT NULL,
    r_category character varying(64) NOT NULL,
    r_favorite boolean NOT NULL,
    FOREIGN KEY (r_u_id) REFERENCES public.u_users (u_id),
    FOREIGN KEY (r_s_id) REFERENCES public.s_safes (s_id)
);

CREATE TABLE public.a_audit (
    a_id character varying NOT NULL PRIMARY KEY,
    a_u_id uuid NOT NULL,
    a_created_at bigint NOT NULL,
    a_ip inet NOT NULL,
    a_object public.object_ NOT NULL,
    a_action public.action_status NOT NULL,
    a_device character varying(512) NOT NULL,
    FOREIGN KEY (a_u_id) REFERENCES public.u_users (u_id)
);

CREATE TABLE public.st_settings (
    st_id uuid NOT NULL PRIMARY KEY,
    st_key character varying NOT NULL,
    st_value character varying NOT NULL
);

CREATE UNIQUE INDEX u_login_idx ON public.u_users (u_login);

CREATE UNIQUE INDEX t_token_idx ON public.t_tokens (t_token);

CREATE UNIQUE INDEX st_key_idx ON public.st_settings (st_key);

INSERT INTO public.st_settings (st_id, st_key, st_value) VALUES (
    '25bf1152-0507-4ebc-8c46-f297c07e5f37',
    'item_types',
    '["STRING","PASSWORD","EMAIL","CONCEALED","URL","OTP","DATE","MONTH_YEAR","MENU","FILE"]'
);
INSERT INTO public.st_settings (st_id, st_key, st_value) VALUES (
    '1e187a16-4e75-42f2-93a4-caf003cec774',
    'password_rule',
    '^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W]).{8,64}$'
);
INSERT INTO public.st_settings (st_id, st_key, st_value) VALUES (
    '3f2385ba-e3c3-4d80-bbe1-3d3746de8d9f', 'scan_time_routines_tokens', '60'
);
INSERT INTO public.st_settings (st_id, st_key, st_value) VALUES (
    'c82d4aeb-b250-4032-a989-15256de626de', 'scan_time_routines_users', '60'
);
INSERT INTO public.st_settings (st_id, st_key, st_value) VALUES (
    '24775562-22d7-4f71-873b-2503ff1135fd', 'confirmation_period', '604800'
);
INSERT INTO public.st_settings (st_id, st_key, st_value) VALUES (
    '057327e8-1f62-4d70-af07-623a62d6f2fe',
    'item_categories',
    '["LOGIN","PASSWORD","API_CREDENTIAL","SERVER","DATABASE","CREDIT_CARD","MEMBERSHIP","PASSPORT","SOFTWARE_LICENSE","OUTDOOR_LICENSE","SECURE_NOTE","WIRELESS_ROUTER","BANK_ACCOUNT","DRIVER_LICENSE","IDENTITY","REWARD_PROGRAM","DOCUMENT","EMAIL_ACCOUNT","SOCIAL_SECURITY_NUMBER","MEDICAL_RECORD","SSH_KEY","OTHER"]'
);
INSERT INTO public.st_settings (st_id, st_key, st_value) VALUES (
    '5c55e596-5b88-40e6-869b-4cb6fb3a931e', 'disk_space_per_user', '1073741824'
);
INSERT INTO public.st_settings (st_id, st_key, st_value) VALUES (
    '498e9042-1492-44d8-8697-76b9a73967ec', 'registration', 'true'
);

CREATE FUNCTION public.sign_up(
    login character varying,
    secret_string character varying,
    reg_ip inet,
    confirm boolean,
    secret_code character varying,
    backup_codes integer []
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
    code_id UUID;
    user_id_insert UUID;
    uuid_user_id UUID;
    code_id_insert UUID;
    current_timeu BIGINT;
    is_registration BOOLEAN;
BEGIN
    current_timeu := EXTRACT(EPOCH FROM current_timestamp)::bigint;
    uuid_user_id := gen_random_uuid ();

    SELECT st_value::BOOLEAN INTO is_registration FROM st_settings WHERE st_id = '498e9042-1492-44d8-8697-76b9a73967ec';

    IF is_registration IS FALSE OR is_registration IS NULL THEN
        RETURN -5;
    END IF;

    SELECT u_id INTO user_id FROM u_users WHERE u_login = $1 AND u_secret_string = $2 AND u_confirm = FALSE;

    IF user_id IS NULL THEN
        INSERT INTO u_users VALUES (uuid_user_id,$1,$3,$4,current_timeu,$2,False) RETURNING u_id INTO user_id_insert;

        IF user_id_insert IS NULL THEN
            RETURN -1;
        END IF;

        INSERT INTO c_codes VALUES (gen_random_uuid(),user_id_insert,$5,$6,current_timeu,current_timeu) RETURNING c_id INTO code_id_insert;

        IF code_id_insert IS NULL THEN
            RETURN -2;
        END IF;
        RETURN 0;
    END IF;

    SELECT c_id INTO code_id FROM c_codes WHERE c_u_id = user_id;

    IF code_id IS NULL THEN
        INSERT INTO c_codes VALUES (gen_random_uuid(),user_id,$5,$6,current_timeu,current_timeu) RETURNING c_id INTO code_id_insert;

        IF code_id_insert IS NULL THEN
            RETURN -3;
        END IF;
        RETURN 1;
    END IF;

    UPDATE c_codes SET c_secret_code = $5,c_backup_codes = $6,c_created_at = current_timeu WHERE c_u_id = user_id RETURNING c_codes.c_id INTO code_id;

    IF code_id IS NULL THEN
        RETURN -4;
    END IF;

    RETURN 2;
END;
$_$;

CREATE FUNCTION public.sign_in(
    login character varying,
    secret_string character varying,
    token character varying,
    device character varying,
    ip inet,
    expiration bigint,
    is_verified_code boolean
) RETURNS boolean
LANGUAGE plpgsql
AS $_$DECLARE
    user_id UUID;
    user_confirm BOOLEAN;
    timestmp BIGINT;
    token_id uuid;
BEGIN
    token_id := gen_random_uuid();
    timestmp := EXTRACT(EPOCH FROM current_timestamp)::bigint;

    SELECT u_id,u_confirm INTO user_id, user_confirm FROM u_users WHERE u_login = $1 AND u_secret_string=$2;

    IF $7 IS TRUE THEN
        IF user_id IS NULL THEN
            RETURN FALSE;
        END IF;

        IF user_confirm IS FALSE THEN
            UPDATE u_users SET u_confirm = $7 WHERE u_id = user_id;
        END IF;

        INSERT INTO t_tokens VALUES(token_id,user_id,$3,timestmp,timestmp,$4,$5,timestmp+$6);

        call create_audit_item($3, $5, 'user', 'sign_in', $4);

        RETURN TRUE;
    END IF;

    RETURN FALSE;
END;
$_$;

CREATE FUNCTION public.sign_out(
    token character varying, token_id uuid
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
    deletion_successful INTEGER;
    token_device character varying;
    token_last_ip inet;

BEGIN
    SELECT t_u_id, t_device, t_last_ip
    INTO user_id, token_device, token_last_ip
    FROM t_tokens WHERE t_token = $1 and active_token($1) = TRUE;

    IF user_id IS NULL THEN
        deletion_successful := -1;
    ELSE
        CALL create_audit_item($1, token_last_ip, 'user', 'sign_out', token_device);

        DELETE FROM t_tokens WHERE t_u_id = user_id AND t_id = $2;
        IF FOUND THEN
            deletion_successful := 0;
        ELSE
            deletion_successful := -2;
        END IF;
    END IF;

    RETURN deletion_successful;
END;
$_$;

CREATE FUNCTION public.active_token(token character varying) RETURNS boolean
LANGUAGE plpgsql
AS $_$DECLARE
    record_exists BOOLEAN;
BEGIN
    SELECT EXISTS (SELECT t_id FROM t_tokens WHERE t_token = $1 AND EXTRACT(EPOCH FROM current_timestamp)::BIGINT <= t_expiration) INTO record_exists;

    RETURN record_exists;
END;
$_$;

CREATE FUNCTION public.active_token_admin(
    token character varying
) RETURNS integer
LANGUAGE plpgsql
AS $_$DECLARE
    user_id UUID;
    is_admin BOOLEAN;
BEGIN
    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND EXTRACT(EPOCH FROM current_timestamp)::BIGINT <= t_expiration;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    SELECT u_admin INTO is_admin FROM u_users
    WHERE u_id = user_id;

    IF is_admin IS FALSE THEN
        RETURN -2;
    END IF;

    RETURN 0;
END;
$_$;

CREATE FUNCTION public.update_token_info(
    token character varying, device character varying, ip inet
) RETURNS boolean
LANGUAGE plpgsql
AS $_$
BEGIN
    UPDATE t_tokens
    SET t_updated_at = EXTRACT(EPOCH FROM current_timestamp)::BIGINT,
    t_device = $2,
    t_last_ip = $3
    WHERE active_token($1) = TRUE AND t_token = $1;

    RETURN FOUND;
END;
$_$;

CREATE FUNCTION public.create_safe(
    token character varying,
    name character varying,
    description character varying
) RETURNS integer
LANGUAGE plpgsql
AS $_$

DECLARE
    user_id UUID;
    safe_id UUID;
    timestmp BIGINT;

BEGIN
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
END;
$_$;

CREATE FUNCTION public.update_safe(
    token character varying,
    safe_id uuid,
    name character varying,
    description character varying
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    safe_id UUID;
    user_id UUID;
BEGIN
    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    UPDATE s_safes SET s_name = $3, s_description = $4,s_updated_at = EXTRACT(EPOCH FROM current_timestamp)::bigint
    WHERE s_u_id = user_id AND s_id = $2
    RETURNING s_id INTO safe_id;

    IF safe_id IS NULL THEN
        RETURN -2;
    END IF;

    RETURN 0;
END;
$_$;

CREATE FUNCTION public.delete_safe(
    token character varying, id uuid
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
    safe_id UUID;
BEGIN
    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    DELETE FROM r_records WHERE r_s_id = $2 AND r_u_id = user_id;

    DELETE FROM s_safes WHERE s_u_id = user_id AND s_id = $2 RETURNING s_id INTO safe_id;

    IF safe_id IS NULL THEN
        RETURN -2;
    END IF;

    RETURN 0;
END;
$_$;

CREATE FUNCTION public.safe_and_element_exists(
    token character varying, safe_id uuid
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
    _safe_id UUID;
    timestmp BIGINT;
BEGIN
    timestmp := EXTRACT(EPOCH FROM current_timestamp)::bigint;

    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    SELECT s_id INTO _safe_id FROM s_safes
    WHERE s_id = $2 AND s_u_id = user_id;

    IF _safe_id IS NULL THEN
        RETURN -2;
    END IF;

    CALL update_safe_info($1,$2);
RETURN 0;

END;
$_$;

CREATE FUNCTION public.create_item(
    token character varying,
    safe_id uuid,
    title character varying,
    item json,
    notes character varying,
    tags character varying [],
    category character varying,
    favorite boolean
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
    _safe_id UUID;
    record_id UUID;
    timestmp BIGINT;
BEGIN
    timestmp := EXTRACT(EPOCH FROM current_timestamp)::bigint;

    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    SELECT s_id INTO _safe_id FROM s_safes WHERE s_u_id = user_id AND s_id = $2;

    IF _safe_id IS NULL THEN
        RETURN -2;
    END IF;

    INSERT INTO r_records VALUES (gen_random_uuid(),_safe_id,user_id,$3,$4,$5,$6,timestmp,timestmp,$7,$8) RETURNING r_id INTO record_id;

    IF record_id IS NULL THEN
        RETURN -2;
    END IF;

    CALL update_safe_info($1,$2);

    RETURN 0;
END;
$_$;

CREATE FUNCTION public.update_item(
    token character varying,
    safe_id uuid,
    item_id uuid,
    title character varying,
    item json,
    notes character varying,
    tags character varying [],
    category character varying
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
    record_id UUID;
BEGIN
    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    UPDATE r_records
    SET r_title = $4,
    r_category = $8,
    r_item = $5,
    r_notes = $6,
    r_tags = $7,
    r_updated_at = EXTRACT(EPOCH FROM current_timestamp)::BIGINT
    WHERE r_s_id = $2 AND r_u_id = user_id AND r_id = $3
    RETURNING r_id INTO record_id;

    IF record_id IS NULL THEN
        RETURN -2;
    END IF;

    CALL update_safe_info($1,$2);

    RETURN 0;
END;
$_$;

CREATE PROCEDURE public.update_safe_info(
    IN token character varying, IN safe_id uuid
)
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
BEGIN
    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN;
    END IF;

    UPDATE s_safes
    SET s_updated_at = EXTRACT(EPOCH FROM current_timestamp)::BIGINT
    WHERE s_id = $2 AND s_u_id=user_id;
END;
$_$;

CREATE FUNCTION public.move_item_to_new_safe(
    token character varying, old_safe_id uuid, new_safe_id uuid, item_id uuid
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
    _old_safe_id UUID;
    _new_safe_id UUID;
    record_id UUID;
BEGIN
    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    --looking for a old safe, checks if it belongs to the owner

    SELECT s_id INTO _old_safe_id
    FROM s_safes
    WHERE s_id = $2
    AND s_u_id = user_id;

    --looking for a new safe, checks if it belongs to the owner

    SELECT s_id INTO _new_safe_id
    FROM s_safes
    WHERE s_id = $3
    AND s_u_id = user_id;

    IF _old_safe_id IS NULL OR _new_safe_id IS NULL THEN
        RETURN -2;
    END IF;

    UPDATE r_records
    SET r_s_id = $3,
    r_updated_at = EXTRACT(EPOCH FROM current_timestamp)::BIGINT
    WHERE r_id = $4
    AND r_s_id = $2
    AND r_u_id = user_id
    RETURNING r_id INTO record_id;

    IF record_id IS NULL THEN
        RETURN -2;
    END IF;

    CALL update_safe_info($1,$2);

    RETURN 0;
END;
$_$;

CREATE FUNCTION public.item_favorite(
    token character varying, safe_id uuid, item_id uuid
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
    record_id UUID;
BEGIN
    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    UPDATE r_records
    SET r_favorite = NOT r_favorite,
    r_updated_at = EXTRACT(EPOCH FROM current_timestamp)::BIGINT
    WHERE r_s_id = $2 AND r_u_id = user_id AND r_id = $3
    RETURNING r_id INTO record_id;

    IF record_id IS NULL THEN
        RETURN -2;
    END IF;

    CALL update_safe_info($1,$2);

    RETURN 0;
END;
$_$;

CREATE FUNCTION public.delete_item(
    token character varying, safe_id uuid, item_id uuid
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
    record_id UUID;
BEGIN

    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    DELETE FROM r_records
    WHERE r_id = $3
    AND r_s_id = $2
    AND r_u_id = user_id
    RETURNING r_id INTO record_id;

    IF record_id IS NULL THEN
        RETURN -2;
    END IF;

    CALL update_safe_info($1,$2);

    RETURN 0;
END;
$_$;

CREATE PROCEDURE public.create_audit_item(
    IN token character varying,
    IN ip inet,
    IN _object public.object_,
    IN action_ public.action_status,
    IN device character varying
)
LANGUAGE plpgsql
AS $_$
DECLARE 
    user_id UUID;
    timestmp BIGINT;
	BEGIN
	timestmp := EXTRACT(EPOCH FROM current_timestamp)::bigint;

	SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

	IF user_id IS NULL THEN
	    RETURN;
	END IF;

	INSERT INTO a_audit VALUES (
	gen_random_uuid(),
	user_id,
	timestmp,
	$2,
	$3,
	$4,
	$5
	);
END;
$_$;

CREATE FUNCTION public.insert_audit_data_limit() RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    num_to_delete INT;
BEGIN
    -- Check the number of records for the given a_u_u_id
    SELECT COUNT(*) INTO num_to_delete FROM a_audit WHERE a_u_id = NEW.a_u_id;

    IF num_to_delete > 256 THEN
        -- Calculate the number of unnecessary records to be deleted

        num_to_delete := num_to_delete - 256;

        DELETE FROM a_audit 
        WHERE a_id IN (
            SELECT a_id
            FROM a_audit
            WHERE a_u_id = NEW.a_u_id
            ORDER BY a_created_at ASC
            LIMIT num_to_delete + 1
        );
    END IF;

    RETURN NEW;
END;
$$;

CREATE FUNCTION public.update_c_codes_code(
    token character varying, secret_string character varying, data integer []
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
    code_id UUID;
BEGIN
    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    UPDATE c_codes
    SET c_backup_codes = $3,
    c_updated_at = EXTRACT(EPOCH FROM current_timestamp)::bigint
    FROM u_users ur
    WHERE c_u_id = user_id AND ur.u_secret_string = $2 AND ur.u_id = user_id

    RETURNING c_id INTO code_id;

    IF code_id IS NULL THEN
        RETURN -2;
    END IF;

    RETURN 0;
END;
$_$;

CREATE FUNCTION public.update_c_codes_code(
    token character varying,
    secret_string character varying,
    data character varying
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
    code_id UUID;
BEGIN
    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    UPDATE c_codes
    SET c_secret_code = $3,
    c_updated_at = EXTRACT(EPOCH FROM current_timestamp)::bigint
    FROM u_users ur
    WHERE c_u_id = user_id AND ur.u_secret_string = $2 AND ur.u_id = user_id
    RETURNING c_id INTO code_id;

    IF code_id IS NULL THEN
        RETURN -2;
    END IF;

    RETURN 0;
END
$_$;

CREATE FUNCTION public.update_secret_string(
    token character varying,
    old_secret_string character varying,
    new_secret_string character varying
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    uid UUID;
    user_id UUID;
BEGIN
    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    UPDATE u_users SET
    u_secret_string = $3
    WHERE u_secret_string=$2 AND u_id = user_id
    RETURNING u_id INTO uid;

    IF uid IS NULL THEN
        RETURN -2;
    END IF;

   	DELETE FROM t_tokens WHERE t_u_id = user_id;

    RETURN 0;
END;
$_$;

CREATE FUNCTION public.delete_user(user_id uuid) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    verification_secret_string UUID;
    code_u_id UUID;
    delete_id UUID;
BEGIN
    SELECT u_id INTO verification_secret_string FROM u_users
    WHERE u_id = $1 AND u_admin = FALSE;

    IF verification_secret_string IS NULL THEN
        RETURN -2;
    END IF;

    DELETE FROM r_records
    WHERE r_u_id = $1;

    DELETE FROM s_safes
    WHERE s_u_id = $1;

    DELETE FROM t_tokens
    WHERE t_u_id = $1;
    delete from a_audit
    where a_u_id = $1;

    DELETE FROM c_codes
    WHERE c_u_id = $1
    RETURNING c_id INTO code_u_id;

    IF code_u_id IS NULL THEN
        RETURN -2;
    END IF;

    DELETE FROM u_users
    WHERE u_id = $1
    RETURNING u_id INTO delete_id;

    IF delete_id IS NULL THEN
        RETURN -2;
    END IF;

    RETURN 0;
END;
$_$;

CREATE FUNCTION public.delete_user(
    token character varying,
    secret_string character varying,
    one_time_code_confirm boolean
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    verification_secret_string UUID;
    user_id UUID;
    code_u_id UUID;
    delete_id UUID;
BEGIN
    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND active_token($1) = TRUE;

    IF user_id IS NULL THEN
        RETURN -1;
    END IF;

    SELECT u_id INTO verification_secret_string FROM u_users
    WHERE u_id = user_id
    AND u_secret_string = $2
    AND $3 = TRUE;

    IF verification_secret_string IS NULL THEN
        RETURN -2;
    END IF;

    DELETE FROM r_records
    WHERE r_u_id = user_id;

    DELETE FROM s_safes
    WHERE s_u_id = user_id;

    DELETE FROM t_tokens
    WHERE t_u_id = user_id;

    delete from a_audit
    where a_u_id = user_id;

    DELETE FROM c_codes
    WHERE c_u_id = user_id
    RETURNING c_id INTO code_u_id;

    IF code_u_id IS NULL THEN
        RETURN -2;
    END IF;

    DELETE FROM u_users
    WHERE u_id = user_id
    RETURNING u_id INTO delete_id;

    IF delete_id IS NULL THEN
        RETURN -2;
    END IF;

    RETURN 0;
END;
$_$;

CREATE FUNCTION public.update_settings_admin(
    token character varying, key character varying, value character varying
) RETURNS integer
LANGUAGE plpgsql
AS $_$
DECLARE
    user_id UUID;
    settings_id UUID;
    is_admin INTEGER;
BEGIN
    is_admin := active_token_admin($1);

    SELECT t_u_id INTO user_id FROM t_tokens WHERE t_token = $1 AND is_admin = 0;
    IF user_id IS NULL THEN
        RETURN is_admin;
    END IF;

    UPDATE st_settings
    SET st_value = $3
    WHERE st_key = $2
    RETURNING st_id INTO settings_id;

    IF settings_id IS NULL THEN
        RETURN -3;
    END IF;

    RETURN 0;
END;
$_$;

CREATE TRIGGER enforce_audit_data_limit AFTER INSERT ON public.a_audit FOR EACH ROW EXECUTE FUNCTION public.insert_audit_data_limit();
