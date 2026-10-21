import json
import os

from mcp import Client

MCP_URL = os.getenv(
    "MCP_URL",
    "http://127.0.0.1:8001/mcp"
)

async def get_order_via_mcp(
    order_id:str
)->dict:

   async with Client(MCP_URL) as client:
       result = await client.call_tool(
           "get_order",
           {
               "order_id":order_id
           }
       )

       if result.is_error:
           return{
                "found": False,
                "error": "MCP tool call failed"
           }
        
       text = result.content[0].text

       return json.loads(text)

async def check_refund_via_mcp(order_id: str) -> dict:

     async with Client(MCP_URL) as client:
        result = await client.call_tool(
            "check_refund",
            {
                "order_id": order_id
            }
         )
        
        if result.is_error:
            return{
                "eligible": False,
                "error": "MCP tool call failed"
            }
        text = result.content[0].text
        return json.loads(text)

async def refund_order_via_mcp(
    order_id:str,
    reason:str
)-> dict:
   
   async with Client(MCP_URL) as client:
       result = await client.call_tool(
            "refund_order",
            {
                "order_id": order_id,
                "reason": reason
            }
       )

       if result.is_error:
           return{
                "success": False,
                "error": "MCP tool call failed"
           }
       text = result.content[0].text

       return json.loads(text)