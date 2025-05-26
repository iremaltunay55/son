#!/usr/bin/env python3
"""
MCP Server Test Script
"""

import asyncio
import json
import sys
from app import server, get_weather_data

async def test_mcp_server():
    """MCP server'ı test et"""

    print("🧪 MCP Server Test Başlatılıyor...")

    # Tools listesini test et
    print("\n1️⃣ Tools listesi test ediliyor...")
    try:
        from app import handle_list_tools
        tools = await handle_list_tools()
        print(f"✅ {len(tools)} tool bulundu:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
    except Exception as e:
        print(f"❌ Tools listesi hatası: {e}")
        return

    # Weather API'yi test et
    print("\n2️⃣ Weather API test ediliyor...")
    test_cities = ["Istanbul", "Ankara", "London"]

    for city in test_cities:
        try:
            weather_data = await get_weather_data(city)
            print(f"✅ {city}: {weather_data['temperature']}°C, {weather_data['description']}")
        except Exception as e:
            print(f"❌ {city} hatası: {e}")

    # Tool call test et
    print("\n3️⃣ Tool call test ediliyor...")
    try:
        from app import handle_call_tool
        result = await handle_call_tool("get_weather", {"city": "Istanbul"})
        print(f"✅ Tool call başarılı:")
        print(f"   {result[0].text[:100]}...")
    except Exception as e:
        print(f"❌ Tool call hatası: {e}")

    print("\n🎉 Test tamamlandı!")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
