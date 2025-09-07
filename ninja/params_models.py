from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Type, TypeVar

from django.conf import settings
from django.http import HttpRequest
from pydantic import BaseModel

from ninja.compatibility import get_headers
from ninja.errors import HttpError
from ninja.types import DictStrAny

if TYPE_CHECKING:
    from ninja import NinjaAPI  # pragma: no cover

__all__ = [
    "ParamModel",
    "QueryModel",
    "PathModel",
    "HeaderModel",
    "CookieModel",
    "BodyModel",
    "FormModel",
    "FileModel",
]

TModel = TypeVar("TModel", bound="ParamModel")


class ParamModel(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        pass  # pragma: no cover

    @classmethod
    def resolve(
        cls: Type[TModel],
        request: HttpRequest,
        api: "NinjaAPI",
        path_params: DictStrAny,
    ) -> TModel:
        data = cls.get_request_data(request, api, path_params)
        if data is None:
            return cls()

        varname = getattr(cls, "_single_attr", None)
        if varname:
            data = {varname: data}
        # TODO: I guess if data is not dict - raise an HttpBadRequest
        return cls(**data)


class QueryModel(ParamModel):
    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        list_fields = getattr(cls, "_collection_fields", [])
        list_field_aliases = getattr(cls, "_collection_field_aliases", {})
        
        # Parse the querydict to get the raw field data
        parsed_data = api.parser.parse_querydict(request.GET, list_fields, request, list_field_aliases)
        
        # Check if this is a single Pydantic model case
        annotations = getattr(cls, '__annotations__', {})
        if len(annotations) == 1 and parsed_data:
            field_name = list(annotations.keys())[0]
            field_type = annotations[field_name]
            
            # Check if the field type is a pydantic model
            try:
                from ninja.signature.details import is_pydantic_model
                if is_pydantic_model(field_type):
                    # For pydantic models, we need to pass the raw query dict to let pydantic handle the aliases
                    # Create a dict suitable for pydantic model construction
                    pydantic_data = {}
                    reverse_alias_map = {alias: field for field, alias in list_field_aliases.items()}
                    
                    for key in request.GET.keys():
                        if key in reverse_alias_map:
                            # This is an aliased field - use alias name for pydantic
                            pydantic_data[key] = request.GET.getlist(key) if reverse_alias_map[key] in list_fields else request.GET[key]
                        elif key in list_fields:
                            pydantic_data[key] = request.GET.getlist(key)
                        else:
                            pydantic_data[key] = request.GET[key]
                    
                    return {field_name: pydantic_data}
            except Exception:
                # Fall back to original behavior
                pass
        
        return parsed_data


class PathModel(ParamModel):
    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        return path_params


class HeaderModel(ParamModel):
    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        data = {}
        headers = get_headers(request)
        for name, field in cls.__fields__.items():
            if name in headers:
                data[name] = headers[name]
            elif field.alias in headers:
                data[field.alias] = headers[field.alias]
        return data


class CookieModel(ParamModel):
    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        return request.COOKIES


class BodyModel(ParamModel):
    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        if request.body:
            try:
                return api.parser.parse_body(request)
            except Exception as e:
                msg = "Cannot parse request body"
                if settings.DEBUG:
                    msg += f" ({e})"
                raise HttpError(400, msg)

        return None


class FormModel(ParamModel):
    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        list_fields = getattr(cls, "_collection_fields", [])
        list_field_aliases = getattr(cls, "_collection_field_aliases", {})
        return api.parser.parse_querydict(request.POST, list_fields, request, list_field_aliases)


class FileModel(ParamModel):
    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        list_fields = getattr(cls, "_collection_fields", [])
        list_field_aliases = getattr(cls, "_collection_field_aliases", {})
        return api.parser.parse_querydict(request.FILES, list_fields, request, list_field_aliases)
