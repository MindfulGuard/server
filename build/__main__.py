import argparse
import dotenv

PATH_TO_PGSQL_DOT_ENV = "docker/.POSTGRESQL.env"

dotenv.load_dotenv()

parser = argparse.ArgumentParser()

parser.add_argument("--POSTGRES_PASSWORD", help="Password PostgreSQL")
parser.add_argument("--POSTGRES_PASSWORD_USER", help="Username PostgreSQL")
parser.add_argument("--POSTGRES_PASSWORD_PASSWORD", help="User password PostgreSQL")

args = parser.parse_args()

def setup_database():
    if args.POSTGRES_PASSWORD:
        dotenv.set_key(PATH_TO_PGSQL_DOT_ENV, "POSTGRES_PASSWORD", args.POSTGRES_PASSWORD, quote_mode="never")

    file_name = "docker/dumps/pgsql.sql"

    with open(file_name, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        modified_line = line.replace("user_create", args.POSTGRES_PASSWORD_USER).replace("user_password", args.POSTGRES_PASSWORD_PASSWORD)
        modified_lines.append(modified_line)

    with open(file_name, 'w') as file:
        file.writelines(modified_lines)

if __name__ == "__main__":
    setup_database() 
