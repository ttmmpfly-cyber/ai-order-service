# import re

# def extract_order_id(message:str)->str | None:
#     match = re.search(
#         r"\bA\d{4,}\b",
#         message.upper()
#     )

#     if not match:
#         return None

#     return match.group()
import re

def extract_order_id(message: str) -> str | None:
    # 鍖归厤 A + 4 浣嶆暟瀛?
    # 鍓嶉潰鍏佽涓枃锛屼絾涓嶅厑璁稿叾浠栬嫳鏂囧瓧姣嶆垨鏁板瓧
    match = re.search(
        r"(?<![A-Za-z0-9])A\d{4}(?![A-Za-z0-9])",
        message,
        re.IGNORECASE
    )

    if match:
        return match.group(0).upper()

    return None
