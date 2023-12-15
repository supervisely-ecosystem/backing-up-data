import os

import supervisely as sly

from dotenv import load_dotenv
from rich.console import Console

console = Console()

print("Script starting...")

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_PATH)
print(f"Absolute path: {ABSOLUTE_PATH}\nParent dir: {PARENT_DIR}")

if sly.is_development():
    # * For convinient development, has no effect in the production.
    local_env_path = os.path.join(PARENT_DIR, "local.env")
    supervisely_env_path = os.path.expanduser("~/supervisely.env")
    print(
        "Running in development mode. Will load .env files...\n"
        f"Local .env path: {local_env_path}, Supervisely .env path: {supervisely_env_path}"
    )

    if os.path.exists(local_env_path) and os.path.exists(supervisely_env_path):
        print("Both .env files exists. Will load them.")
        load_dotenv(local_env_path)
        load_dotenv(supervisely_env_path)
    else:
        print("One of the .env files is missing. It may cause errors.")

TEAM_ID = sly.io.env.team_id()
WORKSPACE_ID = sly.io.env.workspace_id()
print(f"TEAM_ID: {TEAM_ID}, WORKSPACE_ID: {WORKSPACE_ID}")

api: sly.Api = sly.Api.from_env()

print("API instance initialized.")

project_id = sly.env.project_id()
print(f"Project ID: {project_id}")

project_info = api.project.get_info_by_id(project_id)
print(f"Project info: {project_info}")

task_id = api.project.clone(project_id, WORKSPACE_ID, "Cloned project")
print(f"Result: {task_id}")

api.task.wait(task_id, api.task.Status.FINISHED)
print("Task finished successfully!")

task_info = api.task.get_info_by_id(task_id)
print(f"Task info: {task_info}")
dst_project_id = task_info["meta"]["output"]["project"]["id"]
print(f"Cloned project ID: {dst_project_id}")
