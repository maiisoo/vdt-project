import re


def extract_sql(response_text):
    sql_pattern = re.compile(r'--.*?\n|/\*.*?\*/|SELECT.*?;', re.IGNORECASE | re.DOTALL)

    sql_matches = sql_pattern.findall(response_text)

    sql_code = "\n".join(match.strip() for match in sql_matches if match.strip().lower().startswith('select'))

    return sql_code


