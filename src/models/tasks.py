import enum
from base_module import (
    Model,
    ValuedEnum,
)
from sqlmodel import Field
from base_async.models import BaseOrmModel


class ErrorCode(enum.auto):
    """."""

    NO_ERROR = 0
    UNEXPECTED_ERROR = 1
    UNEXPECTED_TEMPLATE = 2
    TEMPLATE_ERROR = 3
    EMAIL_SENDING_ERROR = 4
    SMTP_UNCONFIGURED = 5


class TaskStatus(ValuedEnum):
    """."""

    IN_QUEUE = 'in_queue'
    PROCESSING = 'processing'
    SENT = 'sent'
    PARTIALLY_SENT = 'partially_sent'
    ERROR = 'error'
    SKIPPED = 'skipped'


class TaskCreation(Model):
    """."""

    message_type: str = Field()
    payload: dict = Field()
    priority: int = Field()(default=Priorities.LEAST)


class Task(BaseOrmModel):
    """."""

    __tablename__ = 'tasks'

    task_id: int | None = dc.field(
        metadata={
            'sa': sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        }
    )
    status: TaskStatus = dc.field(
        metadata={'sa': sa.Column(sa.Enum(TaskStatus))}
    )
    priority: int = dc.field(metadata={'sa': sa.Column(sa.Integer)})
    payload: dict = dc.field(
        metadata={'sa': sa.Column("email_payload", sa.JSON)}
    )

    recipients: list[int] = dc.field(
        metadata={'sa': sa.Column(sa.ARRAY(sa.Integer))}
    )

    message_type: str = dc.field(
        metadata={'sa': sa.Column(sa.String)}
    )
    recipients_summary: dict[str , int] = dc.field(
        default_factory=dict,
        metadata={'sa': sa.Column(sa.JSON())}
    )

    created_at: datetime = dc.field(
        default_factory=datetime.now,
        metadata={'sa': sa.Column(sa.TIMESTAMP)}
    )
    updated_at: datetime | None = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.TIMESTAMP)}
    )
    duration: float = dc.field(default=0, metadata={'sa': sa.Column(sa.Float)})

    def touch(self):
        self.updated_at = datetime.now()

    @classmethod
    def from_creation(
            cls,
            creation: TaskCreation,
    ) -> 'Task':
        created_at = datetime.now()

        return cls(
            task_id=None,
            status=TaskStatus.IN_QUEUE,
            priority=creation.priority,
            payload=creation.payload,
            recipients=[],
            message_type=creation.message_type,
            created_at=created_at,
            updated_at=None,
        )

