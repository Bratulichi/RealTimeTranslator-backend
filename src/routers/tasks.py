from fastapi import (
    APIRouter,
    Depends,
)

from base_async.models.filter import FilterResult
from base_async.services import FilterService
from injectors import

router = APIRouter()


@router.api_route("/", methods=["GET", "POST"])
def get_tasks(filter: FilterService = Depends()) -> FilterResult:
    # return await filter.filter_with_json(GTIN, data)