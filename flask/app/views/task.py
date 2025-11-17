from flask_restx import Namespace, Resource
from flask import request

from app.helpers.decorators import login_required
from app.helpers.response import (
    get_success_response,
    get_failure_response,
    parse_request_body,
)
from common.services import TaskService
from common.app_config import config

task_api = Namespace('task', description="Task-related APIs")


def _get_task_service():
    return TaskService(config)


@task_api.route('')
class TaskList(Resource):

    @login_required()
    def get(self, person):
        status = request.args.get('status')
        status = status if status in ('active', 'completed') else None

        task_service = _get_task_service()
        tasks = task_service.list_tasks(person.entity_id, status)
        return get_success_response(tasks=[task.as_dict() for task in tasks])

    @task_api.expect(
        {'type': 'object', 'properties': {
            'title': {'type': 'string'},
            'completed': {'type': 'boolean'},
        }}
    )
    @login_required()
    def post(self, person):
        parsed_body = parse_request_body(request, ['title', 'completed'])
        title = parsed_body.get('title')
        completed = parsed_body.get('completed', False)

        task_service = _get_task_service()
        task = task_service.create_task(person.entity_id, title, completed)
        return get_success_response(task=task.as_dict())


@task_api.route('/<string:task_id>')
class TaskDetail(Resource):

    @task_api.expect(
        {'type': 'object', 'properties': {
            'title': {'type': 'string'},
            'completed': {'type': 'boolean'},
        }}
    )
    @login_required()
    def put(self, task_id, person):
        parsed_body = parse_request_body(request, ['title', 'completed'])
        # Require at least one field
        if parsed_body.get('title') is None and parsed_body.get('completed') is None:
            return get_failure_response(message="No fields provided to update.", status_code=400)

        task_service = _get_task_service()
        task = task_service.update_task(
            task_id,
            person.entity_id,
            title=parsed_body.get('title'),
            completed=parsed_body.get('completed'),
        )
        return get_success_response(task=task.as_dict())

    @login_required()
    def delete(self, task_id, person):
        task_service = _get_task_service()
        task_service.delete_task(task_id, person.entity_id)
        return get_success_response(message="Task deleted.")
