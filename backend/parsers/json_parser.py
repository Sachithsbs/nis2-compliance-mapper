import json

def parse_json(file_bytes: bytes) -> str:
    data = json.loads(file_bytes.decode("utf-8", errors="ignore"))

    def flatten(obj):
        if isinstance(obj, dict):
            result = []
            for k, v in obj.items():
                result.append(str(k))
                result.extend(flatten(v))
            return result
        elif isinstance(obj, list):
            result = []
            for item in obj:
                result.extend(flatten(item))
            return result
        else:
            return [str(obj)]

    return " ".join(flatten(data))


