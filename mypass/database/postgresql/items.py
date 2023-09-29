import json
from uuid import UUID
from mypass.database.postgresql.authentication import Authentication
from mypass.database.postgresql.connection import Connection
from mypass.core.response_status_codes import *
import asyncpg

from mypass.database.postgresql.utils import serialize_uuid

class Item:
    async def create(
            self,
            token:str,
            safe_id:str,
            title:str,
            item,
            notes:str,
            tags:list[str],
            category:str
            ):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT create_item($1, $2, $3, $4, $5, $6, $7, $8)',
                                                  token,safe_id,title,item,notes,tags,category,False)
            if value == 0:
                return OK
            elif value == -1:
                return UNAUTHORIZED
            elif value == -2:
                return INTERNAL_SERVER_ERROR
            else:
                return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ForeignKeyViolationError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError as e:
            print(e)
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()
            
    async def update(
            self,
            token:str,
            safe_id:str,
            item_id:str,
            title:str,
            item,
            notes:str,
            tags:list[str],
            ):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT update_item($1, $2, $3, $4, $5, $6, $7)',
                                                  token,safe_id,item_id,title,item,notes,tags)
            if value == 0:
                return OK
            elif value == -1:
                return UNAUTHORIZED
            elif value == -2:
                return INTERNAL_SERVER_ERROR
            else:
                return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ForeignKeyViolationError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError as e:
            print(e)
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()

    async def get(
            self,
            token:str
            ):
        connection = None
        try:
            connection = await Connection().connect()
            is_auth = await Authentication().is_auth(connection,token)
            if not is_auth:
                return ([],[],[],UNAUTHORIZED)

            items = await connection.fetch('''
            SELECT s.s_id ,r.r_id, r.r_title, r.r_item, r.r_category,r.r_notes,r.r_tags,r.r_favorite, r.r_created_at, r.r_updated_at
            FROM r_records AS r
            JOIN s_safes AS s ON s.s_id = r.r_s_id
            JOIN t_tokens AS t ON t.t_u_id = r.r_u_id
            WHERE t.t_token = $1
            AND active_token($1) = True;
            ''',token)
            print(items)


            result_dict = {"list": []}
            tags_list:list[str] = []
            favorites_list:list[str] = []

            # Creating a dictionary to track records by safe_id
            safe_dict = {}

            # We bypass each record from the result of the SQL query
            for record in items:
                safe_id = record['s_id']
                
                # Converting UUID objects to strings
                safe_id_str = str(safe_id)
                id_str = str(record['r_id'])
                
                # Creating a dictionary for the current entry
                record_dict = {
                    'id': id_str,
                    'title': record['r_title'],
                    'category': record['r_category'],
                    'notes': record['r_notes'],
                    'tags': record['r_tags'],
                    'favorite': record['r_favorite'],
                    'sections': json.loads(record['r_item'])['sections']
                }

                # Check if there is already an entry with such a safe_id in the dictionary
                if safe_id_str in safe_dict:
                    # If the record already exists, add the current record to the existing safe
                    safe_dict[safe_id_str]["items"].append(record_dict)
                    safe_dict[safe_id_str]["count"] += 1
                else:
                    # If there is no such safe yet, create a new one
                    safe_dict[safe_id_str] = {
                        "safe_id": safe_id_str,
                        "count": 1,
                        "items": [record_dict]
                    }
                
                for i in record_dict["tags"]:
                    if i not in tags_list:
                        tags_list.append(i)
                
                for key, value in record_dict.items():
                    if key == "favorite" and value == True:  # Checking if "favorite" is True
                        favorites_list.append(record_dict["id"])  # If True, add "id" to the list


            # Converting a dictionary with safes into a list for the final JSON
            result_dict["list"] = list(safe_dict.values())

            # Output the final JSON using a custom serializer
            result_json = json.dumps(result_dict, indent=2, default=serialize_uuid)
            
            if not result_dict:
                return ([],[],[],OK)
            return (json.loads(result_json), tags_list,favorites_list,OK)
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return ([],[],[],INTERNAL_SERVER_ERROR)
        finally:
            if connection:
                await connection.close()

    async def move(
            self,
            token:str,
            old_safe_id:str,
            new_safe_id:str,
            item_id:str
            ):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT move_item_to_new_safe($1, $2, $3, $4)',
                                                  token,old_safe_id,new_safe_id,item_id)
            if value == 0:
                return OK
            elif value == -1:
                return UNAUTHORIZED
            elif value == -2:
                return INTERNAL_SERVER_ERROR
            else:
                return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ForeignKeyViolationError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError as e:
            print(e)
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()

    async def delete(
            self,
            token:str,
            safe_id:str,
            item_id:str
            ):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT delete_item($1, $2, $3)',
                                                  token,safe_id,item_id)
            if value == 0:
                return OK
            elif value == -1:
                return UNAUTHORIZED
            elif value == -2:
                return INTERNAL_SERVER_ERROR
            else:
                return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ForeignKeyViolationError:
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError as e:
            print(e)
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()

    async def set_favorite(
            self,
            token:str,
            safe_id:str,
            item_id:str
            ):
        connection = None
        try:
            connection = await Connection().connect()
            value:int = await connection.fetchval('SELECT item_favorite($1, $2, $3)',
                                                  token,safe_id,item_id)
            if value == 0:
                return OK
            elif value == -1:
                return UNAUTHORIZED
            elif value == -2:
                return INTERNAL_SERVER_ERROR
            else:
                return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ConnectionDoesNotExistError as e:
            print(e)
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.ForeignKeyViolationError as e:
            print(e)
            return INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError as e:
            print(e)
            return INTERNAL_SERVER_ERROR
        finally:
            if connection:
                await connection.close()