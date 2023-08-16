# -*- coding: utf-8 -*-
from typing import Union

from fastapi.responses import JSONResponse


class BaseJSONResponse(JSONResponse):
    message = ""
    status_code = 200

    def __init__(self, data: Union[str, dict]) -> None:
        content = {
            "message": self.message
        }
        if isinstance(data, str):
            content["data"] = data
        elif isinstance(data, dict):
            content = {**content, **data}
        super().__init__(content, self.status_code, None, None, None)


class SuccessResponse(BaseJSONResponse):
    message = "success"


class ErrorResponse(BaseJSONResponse):
    message = "error"
    status_code = 400
