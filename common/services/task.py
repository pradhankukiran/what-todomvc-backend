from typing import List, Optional

from common.models.task import Task
from common.repositories.factory import RepositoryFactory, RepoType
from common.helpers.exceptions import InputValidationError


class TaskService:

    def __init__(self, config):
        self.config = config
        self.repository_factory = RepositoryFactory(config)
        self.task_repo = self.repository_factory.get_repository(RepoType.TASK)

    def list_tasks(self, person_id: str, status: Optional[str] = None) -> List[Task]:
        filters = {'person_id': person_id}
        if status == 'completed':
            filters['completed'] = True
        elif status == 'active':
            filters['completed'] = False

        return self.task_repo.get_many(filters)

    def create_task(self, person_id: str, title: str, completed: bool = False) -> Task:
        if not title or not title.strip():
            raise InputValidationError("Task title is required.")

        task = Task(title=title.strip(), completed=bool(completed), person_id=person_id)
        return self.task_repo.save(task)

    def _get_task_for_person(self, task_id: str, person_id: str) -> Task:
        task = self.task_repo.get_one({"entity_id": task_id})
        if not task or task.person_id != person_id:
            raise InputValidationError("Task not found.")
        return task

    def update_task(self, task_id: str, person_id: str, title: Optional[str] = None, completed: Optional[bool] = None) -> Task:
        task = self._get_task_for_person(task_id, person_id)

        if title is not None:
            if not title.strip():
                raise InputValidationError("Task title is required.")
            task.title = title.strip()

        if completed is not None:
            task.completed = bool(completed)

        return self.task_repo.save(task)

    def delete_task(self, task_id: str, person_id: str) -> None:
        task = self._get_task_for_person(task_id, person_id)
        self.task_repo.delete(task)
