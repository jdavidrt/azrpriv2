import json
from typing import Dict, List, cast

from django.http import HttpRequest
from django.utils.datastructures import MultiValueDict

from ninja.types import DictStrAny

__all__ = ["Parser"]


class Parser:
    "Default json parser"

    def parse_body(self, request: HttpRequest) -> DictStrAny:
        return cast(DictStrAny, json.loads(request.body))

    def parse_querydict(
        self, data: MultiValueDict, list_fields: List[str], request: HttpRequest,
        list_field_aliases: Dict[str, str] = None
    ) -> DictStrAny:
        result: DictStrAny = {}
        list_field_aliases = list_field_aliases or {}
        
        # Create reverse mapping of aliases to field names for efficient lookup
        alias_to_field = {alias: field for field, alias in list_field_aliases.items()}
        
        for key in data.keys():
            # Check if this key is a list field directly
            if key in list_fields:
                result[key] = data.getlist(key)
            # Check if this key is an alias for a list field
            elif key in alias_to_field:
                field_name = alias_to_field[key]
                result[field_name] = data.getlist(key)
            else:
                result[key] = data[key]
        return result
