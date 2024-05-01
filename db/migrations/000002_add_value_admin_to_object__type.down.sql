CREATE TYPE public.temp_object_ AS ENUM (
    'user',
    'safe',
    'item',
    'file'
);

ALTER TABLE public.a_audit
ALTER COLUMN a_object
TYPE public.temp_object_
USING a_object::text::public.temp_object_;

DROP PROCEDURE public.create_audit_item(
    character varying,
    inet,
    public.object_,
    public.action_status,
    character varying
);
DROP TYPE public.object_;
ALTER TYPE public.temp_object_ RENAME TO object_;

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
