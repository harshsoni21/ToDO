from todoApp.src import DbOps
from ToDO.AppLogging import app_logger

class TodoCore:
    @staticmethod
    def get_task_list():
        try:
            tasks = DbOps.fetch_all_tasks()
            app_logger.debug(f"Retrieved task list: {tasks}")
            return tasks
        except Exception as e:
            app_logger.error(f"Failed to fetch task list | error: {e}")
            return []

    @staticmethod
    def create_task(api_info):
        try:
            DbOps.ensure_tasks_table_exists()
            DbOps.create_todo_task(
                api_info["title"],
                api_info.get("description"),
                api_info.get("due_date"),
                api_info.get("status")
            )
            app_logger.info(f"Task created successfully: {api_info}")
            return True
        except Exception as e:
            app_logger.error(f"Failed to create task | error: {e}")
            return False

    @staticmethod
    def get_task(task_id):
        try:
            task = DbOps.get_task_by_id(task_id)
            if task:
                app_logger.debug(f"Retrieved task: {task}")
            else:
                app_logger.warning(f"Task not found: task_id={task_id}")
            return task
        except Exception as e:
            app_logger.error(f"Failed to fetch task | task_id={task_id} | error: {e}")
            return None

    @staticmethod
    def delete_todo_task(task_id):
        try:
            DbOps.remove_task(task_id)
            app_logger.info(f"Task deleted successfully: task_id={task_id}")
            return True
        except Exception as e:
            app_logger.error(f"Failed to delete task | task_id={task_id} | error: {e}")
            return False

    @staticmethod
    def update_todo_task(task_id, api_info):
        try:
            DbOps.modify_task(
                task_id,
                api_info.get("title"),
                api_info.get("description"),
                api_info.get("due_date"),
                api_info.get("status")
            )
            app_logger.info(f"Task updated successfully: task_id={task_id}, data={api_info}")
            return True
        except Exception as e:
            app_logger.error(f"Failed to update task | task_id={task_id} | error: {e}")
            return False
