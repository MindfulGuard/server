DROP FUNCTION public.sign_up (
    character varying,
    character varying,
    inet,
    boolean,
    character varying,
    integer [],
    boolean
);

CREATE TABLE public.st_settings (
    st_id uuid NOT NULL PRIMARY KEY,
    st_key character varying NOT NULL,
    st_value character varying NOT NULL
);

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