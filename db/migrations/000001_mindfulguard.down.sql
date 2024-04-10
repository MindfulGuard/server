DROP TRIGGER enforce_audit_data_limit ON public.a_audit;

DROP FUNCTION public.sign_up(character varying, character varying, inet, boolean, character varying, integer[]);
DROP FUNCTION public.sign_in(character varying, character varying, character varying, character varying, inet, bigint, boolean);
DROP FUNCTION public.sign_out(character varying, uuid);
DROP FUNCTION public.active_token(character varying);
DROP FUNCTION public.active_token_admin(character varying);
DROP FUNCTION public.update_token_info(character varying, character varying, inet);
DROP FUNCTION public.create_safe(character varying, character varying, character varying);
DROP FUNCTION public.update_safe(character varying, uuid, character varying, character varying);
DROP FUNCTION public.delete_safe(character varying, uuid);
DROP FUNCTION public.safe_and_element_exists(character varying, uuid);
DROP FUNCTION public.create_item(character varying, uuid, character varying, json, character varying, character varying[], character varying, boolean);
DROP FUNCTION public.update_item(character varying, uuid, uuid, character varying, json, character varying, character varying[], character varying);
DROP FUNCTION public.move_item_to_new_safe(character varying, uuid, uuid, uuid);
DROP FUNCTION public.item_favorite(character varying, uuid, uuid);
DROP FUNCTION public.delete_item(character varying, uuid, uuid);
DROP PROCEDURE public.create_audit_item(character varying, inet, public.object_, public.action_status, character varying);
DROP FUNCTION public.insert_audit_data_limit();
DROP FUNCTION public.update_c_codes_code(character varying, character varying, integer[]);
DROP FUNCTION public.update_c_codes_code(character varying, character varying, character varying);
DROP FUNCTION public.update_secret_string(character varying, character varying, character varying);
DROP FUNCTION public.delete_user(uuid);
DROP FUNCTION public.delete_user(character varying, character varying, boolean);
DROP FUNCTION public.update_settings_admin(character varying, character varying, character varying);

DROP TABLE public.st_settings;
DROP TABLE public.c_codes;
DROP TABLE public.r_records;
DROP TABLE public.s_safes;
DROP TABLE public.a_audit;
DROP TABLE public.t_tokens;
DROP TABLE public.u_users;

DROP TYPE public.object_;
DROP TYPE public.action_status;