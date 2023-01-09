schema = {
    "permissions": {
        "type": list
    }
}


def validate_parameters(parameters=[], requiredFields=[]):
    errors = []
    for p in parameters:
        key = p.get("key")
        value = p.get("value")
        if key in requiredFields:
            requiredFields.remove(key)
        schemaObject = schema.get(key)
        if not schemaObject:
            continue
        if schemaObject.get("type") != type(value):
            errors.append({"message": "type does not match schema"})

    if len(requiredFields) > 0 or len(errors) > 0:
        return {
            "success": False,
            "errors": errors
        }
    return {
        "success": True
    }
