from dataclasses import dataclass
from typing import ClassVar

from rococo.models.versioned_model import VersionedModel


@dataclass
class Task(VersionedModel):
    """
    Simple task model tied to a person (owner).
    """
    TABLE_NAME: ClassVar[str] = "task"

    title: str = ""
    completed: bool = False
    person_id: str = ""
