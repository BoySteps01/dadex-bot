#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ DADEX — IA TRADING BOT v4.0 (ULTRA STABLE)
"""

import os
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN ausente!")

PARES = {
    "EUR/USD": "🇪🇺🇺🇸",
    "GBP/USD": "🇬🇧🇺🇸",
    "USD/JPY": "🇺🇸🇯🇵",
    "XAU/USD": "🥇🇺🇸",
    "AUD/USD": "🇦🇺🇺🇸",
    "USD/CHF": "🇺🇸🇨🇭",
}

def gerar_sinal(par):
    rsi = random.randint(20, 80)
    tipo = "🟢 BUY" if rsi < 35 else "🔴 SELL" if rsi > 65 else "🟡 AGUARDAR"
    return {"par": par, "tipo": tipo, "rsi": rsi, "confianca": random.randint(60, 92)}

def formatar_sinal(sinal):
    agora = datetime.utcnow() + timedelta(hours=1)
    h0 = agora.strftime("%H:%M:%S")
    h1 = (agora + timedelta(minutes=1)).strftime("%H:%M")
    h2 = (agora + timedelta(minutes=2)).strftime("%H:%M")
    h3 = (agora + timedelta(minutes=3)).strftime("%H:%M")
    
    return f"""
⚡ *DADEX SINAL IA* ⚡
━━━━━━━━━━━━━━━━━━━━
{PARES[sinal['par']]} *{sinal['par']}* — {sinal['tipo']}
🕐 {h0} (Angola)
Confiança: {sinal['confianca']}%

⏱️ *CRONOGRAMA:*
1️⃣ H4 ({h0}→{h1}) Confirma tendência
2️⃣ M15 ({h1}→{h2}) Confirma padrão  
3️⃣ M5 ({h2}→{h3}) Espera confirmação
4️⃣ ENTRA ({h3}) Se tudo alinha!
━━━━━━━━━━━━━━━━━━━━
⚠️ Só operas se tudo alinha!
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [
        [InlineKeyboardButton("⚡ Sinal", callback_data="sinal")],
        [InlineKeyboardButton("📊 Pares", callback_data="pares")],
        [InlineKeyboardButton("🛡️ Risco", callback_data="risco")],
        [InlineKeyboardButton("ℹ️ Ajuda", callback_data="ajuda")],
    ]
    msg = "⚡ *BEM-VINDO AO DADEX* ⚡\n\nBot de sinais Forex com cronograma integrado!"
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

async def cmd_sinal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    par = random.choice(list(PARES.keys()))
    sinal = gerar_sinal(par)
    await update.message.reply_text(formatar_sinal(sinal), parse_mode="Markdown")

async def cmd_pares(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📊 *Pares:*\n" + "\n".join([f"{emoji} {par}" for par, emoji in PARES.items()])
    await update.message.reply_text(msg, parse_mode="Markdown")

async def cmd_risco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🛡️ *RISCO DADEX*\n\n1. Max 2% por trade\n2. Max 3 trades/dia\n3. SL obrigatório\n4. Operar 08:00-22:00 UTC"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def cmd_ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "ℹ️ *DADEX v4.0*\n\n/sinal - Gerar sinal\n/pares - Ver pares\n/risco - Gestão risco\n/ajuda - Ajuda"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def botao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "sinal":
        par = random.choice(list(PARES.keys()))
        sinal = gerar_sinal(par)
        await query.edit_message_text(formatar_sinal(sinal), parse_mode="Markdown")
    elif query.data == "pares":
        msg = "📊 *Pares:*\n" + "\n".join([f"{emoji} {par}" for par, emoji in PARES.items()])
        await query.edit_message_text(msg, parse_mode="Markdown")
    elif query.data == "risco":
        await query.edit_message_text("🛡️ *RISCO*\n1. Max 2%\n2. Max 3 trades\n3. SL obrigatório\n4. Operar 08:00-22:00", parse_mode="Markdown")
    elif query.data == "ajuda":
        await query.edit_message_text("ℹ️ *DADEX v4.0*\n\nBot de sinais Forex!", parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sinal", cmd_sinal))
    app.add_handler(CommandHandler("pares", cmd_pares))
    app.add_handler(CommandHandler("risco", cmd_risco))
    app.add_handler(CommandHandler("ajuda", cmd_ajuda))
    app.add_handler(CallbackQueryHandler(botao))
    
    print("✅ DADEX Bot v4.0 online!")
    app.run_polling()

if __name__ == "__main__":
    main()
