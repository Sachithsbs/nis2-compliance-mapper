import sqlparse

def parse_sql(file_bytes: bytes) -> str:
    raw = file_bytes.decode("utf-8", errors="ignore")
    formatted = sqlparse.format(raw, reindent=True, keyword_case="upper")
    return formatted

