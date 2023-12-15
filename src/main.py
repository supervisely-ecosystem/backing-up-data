import os
import supervisely as sly
from dotenv import load_dotenv


if sly.is_development():
    # Learn more about evnironment variables in our docs:
    # https://developer.supervisely.com/getting-started/environment-variables
    load_dotenv(os.path.expanduser("~/supervisely.env"))
    load_dotenv("local.env")

# Read environment variables and create an API client.
team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
api: sly.Api = sly.Api.from_env()

# Read project ID from the environment variables.
project_id = sly.env.project_id()

# * Option 1: save project (images and annotations) locally.
save_dir = "my_saved_data"
sly.Project.download(
    api, project_id, save_dir, save_image_info=True, save_image_meta=True
)
print(f"Project has been downloaded to {save_dir}")

# Now the project is saved locally. We can archive it and then save in another place.
archive_path = f"{project_id}_archive.zip"
sly.fs.archive_directory(save_dir, archive_path)
print(f"Project has been archived to {archive_path}")

# * Option 2: clone the project on the server.

# Launch the cloning task, the method returns the task ID.
task_id = api.project.clone(project_id, workspace_id, "my_cloned_project")

# Wait until the task is finished.
api.task.wait(task_id, api.task.Status.FINISHED)

# Now the project is cloned and we can retrieve its ID.
task_info = api.task.get_info_by_id(task_id)
dst_project_id = task_info["meta"]["output"]["project"]["id"]
print(f"Project has been cloned. New project ID is {dst_project_id}")
