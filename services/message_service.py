import re

def extract_order_id(message:str)->str | None:
    match = re.search(
        r"\bA\d{4,}\b",
        message.upper()
    )

    if not match:
        return None
    
    return match.group()