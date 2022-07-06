# -*- coding: utf-8 -*-
from typing import Union

from fastapi.responses import JSONResponse


class BaseJSONResponse(JSONResponse):
    message = ""

    def __init__(self, data: Union[str, dict], status_code: int = 200) -> None:
        content = {
            "code": status_code,
            "message": self.message
        }
        if isinstance(data, str):
            content["data"] = data
        elif isinstance(data, dict):
            content = {**content, **data}
        super().__init__(content, status_code, None, None, None)


class SuccessResponse(BaseJSONResponse):
    message = "success"


class ErrorResponse(BaseJSONResponse):
    message = "error"
