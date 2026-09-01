#!/usr/bin/env python3
import os
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

PARES = {"EUR/USD": "🇪🇺🇺🇸", "GBP/USD": "🇬🇧🇺🇸", "USD/JPY": "🇺🇸🇯🇵", "XAU/USD": "🥇🇺🇸", "AUD/USD": "🇦🇺🇺🇸", "USD/CHF": "🇺🇸🇨🇭"}

def gerar_sinal(par):
    return {"par": par, "tipo": "🟢 BUY" if random.randint(1,100) > 50 else "🔴 SELL", "conf": random.randint(60, 92)}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("⚡ Sinal", callback_data="sinal")], [InlineKeyboardButton("📊 Pares", callback_data="pares")], [InlineKeyboardButton("ℹ️ Ajuda", callback_data="ajuda")]]
    await update.message.reply_text("⚡ *DADEX BOT* ⚡\nSinais Forex!", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def sinal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    par = random.choice(list(PARES.keys()))
    s = gerar_sinal(par)
    await update.message.reply_text(f"⚡ {PARES[par]} {par}\n{s['tipo']}\nConf: {s['conf']}%", parse_mode="Markdown")

async def pares(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📊 *Pares:*\n" + "\n".join([f"{e} {p}" for p, e in PARES.items()])
    await update.message.reply_text(msg, parse_mode="Markdown")

async def botao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "sinal":
        par = random.choice(list(PARES.keys()))
        s = gerar_sinal(par)
        await q.edit_message_text(f"⚡ {PARES[par]} {par}\n{s['tipo']}\nConf: {s['conf']}%", parse_mode="Markdown")
    elif q.data == "pares":
        msg = "📊 *Pares:*\n" + "\n".join([f"{e} {p}" for p, e in PARES.items()])
        await q.edit_message_text(msg, parse_mode="Markdown")
    else:
        await q.edit_message_text("ℹ️ DADEX v6 - Bot de sinais Forex", parse_mode="Markdown")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sinal", sinal))
    app.add_handler(CommandHandler("pares", pares))
    app.add_handler(CallbackQueryHandler(botao))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
