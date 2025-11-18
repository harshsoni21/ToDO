import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from todoApp.src import validator
from todoApp.src.TodoCore import TodoCore
from ToDO.AppLogging import app_logger
from django.shortcuts import render

# =========================== Helper Functions =========================================

def _restapi_request_decode(request):
    return json.loads(request.body.decode("utf-8"))


# =================== Main Functions ==================================

@csrf_exempt
def todo_app_page(request):
    tasks = TodoCore.get_task_list()
    return render(request, "TodoPage.html",{"tasks":tasks})


@csrf_exempt
def todo_list_create_tasks(request):
    app_logger.debug(f"api_list_create_tasks: request={request}")
    try:
        if request.method == "GET":
            app_logger.info("Todo App Get Task List API Requested")
            return JsonResponse({"tasks": TodoCore.get_task_list()})

        elif request.method == "POST":
            api_info = _restapi_request_decode(request)
            app_logger.debug(f"api_info -- {api_info}")

            if not validator.todo_api_schema_validation(api_info, "task_create_api"):
                app_logger.error(f"Validation Failed while creating task")
                return JsonResponse({"error": "Schema validation failed"}, status=400)

            success = TodoCore.create_task(api_info)
            if not success:
                return JsonResponse({"error": "Task creation failed"}, status=400)

            tasks = TodoCore.get_task_list()
            return JsonResponse({"task": tasks}, status=201)

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except Exception as e:
        app_logger.error(f"Create Task API Failed | error : {e}")
        return JsonResponse({"error": "internal server error"}, status=500)


@csrf_exempt
def todo_get_delete_task(request, task_id):
    app_logger.debug(f"api_get_delete_task: request_method={request.method}, task_id={task_id}")
    try:
        if request.method == "GET":
            app_logger.info(f"Todo App Get Task API Requested for task_id={task_id}")

            if not validator.todo_api_schema_validation({"task_id": task_id}, "task_get_api"):
                app_logger.error(f"Validation Failed for task_id={task_id}")
                return JsonResponse({"error": "Invalid ID"}, status=400)

            task = TodoCore.get_task(task_id)
            if not task:
                return JsonResponse({"error": "Not found"}, status=404)

            return JsonResponse(task)

        elif request.method == "DELETE":
            app_logger.info(f"Todo App Delete Task API Requested for task_id={task_id}")

            if not validator.todo_api_schema_validation({"task_id": task_id}, "task_delete_api"):
                app_logger.error(f"Validation Failed for task deletion: task_id={task_id}")
                return JsonResponse({"error": "Invalid ID"}, status=400)

            success = TodoCore.delete_todo_task(task_id)
            if not success:
                return JsonResponse({"error": "Delete operation failed"}, status=500)

            return JsonResponse({"message": "Deleted"})

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except Exception as e:
        app_logger.exception(f"Get/Delete Task API Failed | task_id={task_id} | error: {e}")
        return JsonResponse({"error": "internal server error"}, status=500)
    

@csrf_exempt
def todo_update_task(request, task_id):
    app_logger.debug(f"api_update_task: request_method={request.method}, task_id={task_id}")
    try:
        if request.method != "POST":
            app_logger.warning(f"Method Not Allowed: {request.method}")
            return JsonResponse({"error": "Method not allowed"}, status=405)

        api_info = _restapi_request_decode(request)
        app_logger.debug(f"Update payload for task_id={task_id}: {api_info}")

        if not validator.todo_api_schema_validation(api_info, "task_update_api"):
            app_logger.error(f"Validation Failed for task update: task_id={task_id}")
            return JsonResponse({"error": "Schema validation failed"}, status=400)

        task_exists = TodoCore.get_task(task_id)
        if not task_exists:
            return JsonResponse({"error": "Task not found"}, status=404)

        success = TodoCore.update_todo_task(task_id, api_info)
        if not success:
            return JsonResponse({"error": "Task update failed"}, status=500)

        updated_task = TodoCore.get_task(task_id)
        return JsonResponse({"task": updated_task}, status=200)

    except Exception as e:
        app_logger.exception(f"Update Task API Failed | task_id={task_id} | error: {e}")
        return JsonResponse({"error": "internal server error"}, status=500)