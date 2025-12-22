from app.db.session import SessionLocal
from app.models import Policy, Role, Permission
from uuid import uuid4
import json
from pathlib import Path
import argparse
from sqlalchemy.exc import IntegrityError
from .constants import MODEL_MAPPING

class Seeder():
    def __init__(self, models=None):
        self.db = SessionLocal()
        self.models = models

    def close_db_connection(self):
        self.db.close()

    def load_data(self):
        # Get the data folder path
        data_folder = Path.cwd() / 'seeds' / 'data'

        # Load all JSON files
        all_data = []

        files_to_load = (
            [MODEL_MAPPING.get(model) for model in self.models]
            if self.models else ["*"]
        )

        for file in files_to_load:
            for json_file in data_folder.glob(f'{file}.json'):
                with open(json_file, 'r') as f:
                    all_data.append(json.load(f))

        return all_data

    def prepare_data(self, table, data):
        if table == "policies":
            print("data: ", data)
            policies_data = [
                Policy(
                    policy_name=d.get("policy_name"),
                    category=d.get("category"),
                    action=d.get("action")
                )
                for d in data
            ]
            return policies_data
        elif table == "roles":
            roles_data = [
                Role(
                    role=d.get("role")
                )
                for d in data
            ]
            return roles_data
        elif table == "permissions":
            permissions_data = []
            for d in data:
                role = d.get("role")
                policy_names = d.get("policies")
                if policy_names == "*":
                    policies = self.db.query(Policy).all()
                else:
                    policies = self.db.query(Policy).filter(Policy.policy_name in policy_names)
                role_id = self.db.query(Role).filter(Role.role == role).first().id
                permissions_data.extend(
                    [
                        Permission(
                            role_id = role_id,
                            policy_id = policy.id
                        )
                        for policy in policies
                    ]
                )
            return permissions_data
        else:
            print(f"Table '{table}' Not Found.")
            return []


    def handler(self):
        seed_data = self.load_data()
        for data in seed_data:
            self.execute(
                model_data=self.prepare_data(table=data.get("table_name"), data=data.get("data"))
            )

    def execute(self, model_data):
        try:
            self.db.bulk_save_objects(model_data)
            self.db.commit()
            print("Inserted successfully")
        except IntegrityError as e:
            self.db.rollback()
            print(f"Error: {e}")
            print("Continuing with remaining data...")
        except Exception as e:
            self.db.rollback()
            print(f"Error: {e}")
            raise

if __name__ == "__main__":

    # parse seed models
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="pass the model names to seed", type=str)
    args = parser.parse_args()

    model_to_seed = [model.strip() for model in args.model.split(",")] if args.model else False

    seeder = Seeder(models=model_to_seed)
    seeder.handler()
    seeder.close_db_connection()