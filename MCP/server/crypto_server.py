"""MCP server exposing cryptocurrency price and market-data tools, backed by the
public CoinGecko API.

Run standalone via stdio transport - an MCP client (agent.py's MultiServerMCPClient,
Claude Desktop, Claude Code, etc.) spawns this file as a subprocess and talks to it
over stdin/stdout.
"""

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("crypto-price-tracker")

COINGECKO_API = "https://api.coingecko.com/api/v3"
_TIMEOUT = httpx.Timeout(15.0)


@mcp.tool()
async def get_crypto_price(crypto_id: str, currency: str = "usd") -> str:
    """Get the current price of a cryptocurrency in a given currency."""
    crypto_id = crypto_id.strip().lower()
    currency = currency.strip().lower()

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            response = await client.get(
                f"{COINGECKO_API}/simple/price",
                params={"ids": crypto_id, "vs_currencies": currency},
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            # Return the error as text rather than raising: the client is an LLM,
            # and a readable message is more useful to it than a stack trace.
            return f"Could not reach CoinGecko to price {crypto_id}: {exc}"
        data = response.json()

    if crypto_id not in data:
        return (
            f"Unknown cryptocurrency '{crypto_id}'. "
            "Use a CoinGecko ID such as 'bitcoin', 'ethereum' or 'solana'."
        )
    if currency not in data[crypto_id]:
        return f"Unknown currency '{currency}' for {crypto_id}."

    price = data[crypto_id][currency]
    return f"The current price of {crypto_id} is {price} {currency.upper()}"


@mcp.tool()
async def get_crypto_market_info(crypto_ids: str, currency: str = "usd") -> str:
    """Get market info (price, market cap, 24h volume, 24h change) for one or more
    comma-separated CoinGecko cryptocurrency IDs."""
    ids = [c.strip().lower() for c in crypto_ids.split(",") if c.strip()]
    if not ids:
        return "No cryptocurrency IDs provided."
    currency = currency.strip().lower()

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            response = await client.get(
                f"{COINGECKO_API}/coins/markets",
                params={"vs_currency": currency, "ids": ",".join(ids)},
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            return f"Could not reach CoinGecko for market data: {exc}"
        markets = response.json()

    if not markets:
        return f"No market data found for: {', '.join(ids)}."

    unit = currency.upper()
    lines = []
    for coin in markets:
        change = coin.get("price_change_percentage_24h")
        change_text = f"{change:+.2f}%" if change is not None else "n/a"
        lines.append(
            f"{coin.get('name', coin['id'])} ({coin.get('symbol', '').upper()})\n"
            f"  Price:        {coin.get('current_price')} {unit}\n"
            f"  Market cap:   {coin.get('market_cap')} {unit}\n"
            f"  24h volume:   {coin.get('total_volume')} {unit}\n"
            f"  24h change:   {change_text}"
        )

    return "\n\n".join(lines)


if __name__ == "__main__":
    mcp.run(transport="stdio")
