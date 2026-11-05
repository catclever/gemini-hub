# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp"]
# ///
import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.contexts import Context

mcp = FastMCP("TestNotifyServer")

@mcp.tool()
async def trigger_notify(ctx: Context) -> str:
    """Triggers an MCP notification after a short delay."""
    async def delayed():
        await asyncio.sleep(2)
        try:
            ctx.info("This is a standard log notification (info).")
            await ctx.session.send_notification("notifications/message", {"message": "This is a custom message notification."})
        except Exception as e:
            pass
    asyncio.create_task(delayed())
    return "Notification triggered. Did you receive it?"

if __name__ == "__main__":
    mcp.run()
