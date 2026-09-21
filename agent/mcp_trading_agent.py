#!/usr/bin/env python3
"""
==============================================================================
Project: robinhood-chain-agentic-trader
Module: AI Agent Trading Controller & Risk Management Engine
Author & System Architect: Eng. Awsan Adel Abdulbari Ahmed Sultan
Location: Sana'a, Yemen
Email: awsan.sultan@gmail.com
Phone: +967 777852433
LinkedIn: https://www.linkedin.com/in/awsan-adel-abdulbari-ahmed-sultan-8aa5a1a9
Copyright (c) 2026 Eng. Awsan Adel Abdulbari Ahmed Sultan. All Rights Reserved.
==============================================================================
"""

import os
import sys
import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# تحميل الإعدادات من ملف .env في المجلد الرئيسي أو الحالي
load_dotenv()

# ضبط التوثيق وسجلات التشغيل (Logging)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("RobinhoodAgenticTrader")


@dataclass
class RiskGuardrails:
    """
    إعدادات وضوابط إدارة المخاطر المالية.
    تدعم الوضع المفتوح (Open Ceiling Mode) بالكامل بناءً على ملف .env.
    """
    enable_limits: bool = os.getenv("ENABLE_RISK_LIMITS", "false").lower() == "true"
    max_position_size_usd: float = float(os.getenv("MAX_TRADE_SIZE_USD", "0"))
    max_daily_loss_usd: float = float(os.getenv("DAILY_STOP_LOSS_USD", "0"))
    supported_assets: tuple = ("STOCK", "CRYPTO", "ETF", "OPTION")


class AgenticTrader:
    """
    وحدة التحكم الرئيسية بالوكيل الذكي لتنفيذ عمليات التداول
    والربط مع خادم Robinhood Agentic Trading MCP.
    """

    def __init__(self, endpoint: Optional[str] = None):
        self.endpoint = endpoint or os.getenv(
            "ROBINHOOD_MCP_ENDPOINT", 
            "https://agent.robinhood.com/mcp/trading"
        )
        self.guardrails = RiskGuardrails()
        self.daily_realized_loss = 0.0

        logger.info(f"Initialized AgenticTrader with MCP Endpoint: {self.endpoint}")
        if not self.guardrails.enable_limits:
            logger.info("Operating Mode: [OPEN CEILING / UNLIMITED] - No trading caps applied.")
        else:
            logger.info(
                f"Operating Mode: [CUSTOM LIMITS] - Max Trade: ${self.guardrails.max_position_size_usd:,.2f}, "
                f"Stop Loss: ${self.guardrails.max_daily_loss_usd:,.2f}"
            )

    def evaluate_risk(self, symbol: str, quantity: float, price: float, asset_type: str) -> bool:
        """
        التحقق من معايير السلامة قبل إرسال أمر التداول إلى خادم MCP.
        """
        asset_type_clean = asset_type.upper().strip()
        total_order_cost = quantity * price

        # التحقق من نوع الأصل
        if asset_type_clean not in self.guardrails.supported_assets:
            logger.error(f"Asset type '{asset_type_clean}' is not supported by this platform.")
            return False

        # إذا كانت القيود معطلة (الوضع المفتوح)، يتم اعتماد الصفقة فوراً دون سقف
        if not self.guardrails.enable_limits:
            logger.info(
                f"Order Approved [Open Mode]: {symbol} ({asset_type_clean}) | "
                f"Qty: {quantity} | Cost: ${total_order_cost:,.2f}"
            )
            return True

        # في حال تفعيل القيود برقم محدد
        if self.guardrails.max_position_size_usd > 0 and total_order_cost > self.guardrails.max_position_size_usd:
            logger.warning(
                f"Order Rejected: Trade value ${total_order_cost:,.2f} exceeds "
                f"configured limit ${self.guardrails.max_position_size_usd:,.2f}"
            )
            return False

        # فحص سقف الخسارة اليومية
        if self.guardrails.max_daily_loss_usd > 0 and self.daily_realized_loss >= self.guardrails.max_daily_loss_usd:
            logger.critical("Circuit Breaker Triggered: Daily stop-loss threshold reached. Trading halted.")
            return False

        logger.info(f"Order Approved: {symbol} | Cost: ${total_order_cost:,.2f}")
        return True

    def build_mcp_payload(self, symbol: str, side: str, quantity: float, price: float, asset_type: str) -> Dict[str, Any]:
        """
        تجهيز حمولة البيانات المتوافقة مع بروتوكول MCP لإرسالها لخادم Robinhood.
        """
        return {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "place_order",
                "arguments": {
                    "symbol": symbol.upper(),
                    "side": side.lower(),
                    "quantity": quantity,
                    "order_type": "market" if price <= 0 else "limit",
                    "price": price if price > 0 else None,
                    "asset_class": asset_type.lower()
                }
            }
        }

    def execute_order(self, symbol: str, side: str, quantity: float, price: float, asset_type: str) -> bool:
        """
        تنفيذ الصفقة بعد تدقيق المخاطر وإرسالها إلى حساب التداول المخصص.
        """
        side_clean = side.upper().strip()
        if not self.evaluate_risk(symbol, quantity, price, asset_type):
            logger.info(f"Execution aborted for order: {side_clean} {symbol}.")
            return False

        payload = self.build_mcp_payload(symbol, side, quantity, price, asset_type)
        total_amount = quantity * price

        logger.info(
            f"Dispatching {side_clean} order to Robinhood MCP: "
            f"{quantity} of {symbol} (~${total_amount:,.2f}) via {self.endpoint}"
        )
        # هنا يتولى عميل بروتوكول MCP تمرير الطلب واستقبال كود التأكيد
        return True


if __name__ == "__main__":
    # تشغيل تجريبي لوحدة التحكم
    print("=" * 70)
    print("Robinhood Chain Agentic Trader - Controller Initialized")
    print("Author: Eng. Awsan Adel Abdulbari Ahmed Sultan")
    print("=" * 70)

    trader = AgenticTrader()

    # مثال 1: صفقة أسهم بسقف مفتوح (مثال: سهم Nvidia)
    trader.execute_order(
        symbol="NVDA", 
        side="buy", 
        quantity=500.0, 
        price=120.50, 
        asset_type="STOCK"
    )

    # مثال 2: صفقة عملات رقمية بسقف مفتوح (مثال: Bitcoin)
    trader.execute_order(
        symbol="BTC", 
        side="buy", 
        quantity=2.0, 
        price=63500.00, 
        asset_type="CRYPTO"
    )

    # مثال 3: صفقة صناديق مؤشرات متداولة (مثال: S&P 500 ETF)
    trader.execute_order(
        symbol="SPY", 
        side="buy", 
        quantity=100.0, 
        price=560.00, 
        asset_type="ETF"
    )
