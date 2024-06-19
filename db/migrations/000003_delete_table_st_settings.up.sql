DROP FUNCTION public.sign_up (
    character varying,
    character varying,
    inet,
    boolean,
    character varying,
    integer []
);
DROP FUNCTION public.update_settings_admin (
    character varying, character varying, character varying
);

DROP TABLE public.st_settings;

CREATE FUNCTION public.sign_up(
    login character varying,
    secret_string character varying,
    reg_ip inet,
    confirm boolean,
    secret_code character varying,
    backup_codes integer [],
    registration_allowed boolean
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
BEGIN
    current_timeu := EXTRACT(EPOCH FROM current_timestamp)::bigint;
    uuid_user_id := gen_random_uuid ();

    IF $7 IS FALSE THEN
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