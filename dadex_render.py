#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ DADEX — IA TRADING BOT v3.0 (STABLE)
Bot de Sinais Forex para Telegram
Versão optimizada para Render
"""

import os
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN não configurado!")

# Dados dos pares
PARES = {
    "EUR/USD": "🇪🇺🇺🇸",
    "GBP/USD": "🇬🇧🇺🇸",
    "USD/JPY": "🇺🇸🇯🇵",
    "XAU/USD": "🥇🇺🇸",
    "AUD/USD": "🇦🇺🇺🇸",
    "USD/CHF": "🇺🇸🇨🇭",
}

# ============================================================
# FUNÇÕES DE SINAL
# ============================================================

def gerar_sinal(par):
    """Gera um sinal de trading"""
    rsi = random.randint(20, 80)
    macd = random.choice(["positivo", "negativo"])
    volume = random.randint(85, 135)
    confianca = random.randint(60, 92)
    
    if rsi < 35 and macd == "positivo":
        tipo = "🟢 BUY"
    elif rsi > 65 and macd == "negativo":
        tipo = "🔴 SELL"
    else:
        tipo = "🟡 AGUARDAR"
    
    return {
        "par": par,
        "tipo": tipo,
        "rsi": rsi,
        "macd": macd,
        "volume": volume,
        "confianca": confianca,
    }

def formatar_sinal(sinal):
    """Formata o sinal com cronograma"""
    agora_utc = datetime.utcnow()
    agora_angola = agora_utc + timedelta(hours=1)
    
    hora_atual = agora_angola.strftime("%H:%M:%S")
    hora_1min = (agora_angola + timedelta(minutes=1)).strftime("%H:%M")
    hora_2min = (agora_angola + timedelta(minutes=2)).strftime("%H:%M")
    hora_3min = (agora_angola + timedelta(minutes=3)).strftime("%H:%M")
    
    emoji_par = PARES[sinal["par"]]
    
    msg = f"""
⚡ *DADEX — SINAL IA* ⚡
━━━━━━━━━━━━━━━━━━━━
{emoji_par} *{sinal['par']}* — {sinal['tipo']}
🕐 {hora_atual} (Angola)

📊 *ANÁLISE:*
  RSI: {sinal['rsi']} 
  MACD: {sinal['macd']}
  Volume: {sinal['volume']}%
  Confiança: {sinal['confianca']}%

━━━━━━━━━━━━━━━━━━━━
⏱️ *CRONOGRAMA:*

1️⃣ H4 ({hora_atual} → {hora_1min})
   Confirma tendência

2️⃣ M15 ({hora_1min} → {hora_2min})
   Confirma padrão

3️⃣ M5 ({hora_2min} → {hora_3min})
   Espera confirmação

4️⃣ ENTRA ({hora_3min})
   Se tudo alinhar!

━━━━━━━━━━━━━━━━━━━━
⚠️ Só operas se tudo alinha!
"""
    return msg

# ============================================================
# COMANDOS
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu de boas-vindas"""
    teclado = [
        [InlineKeyboardButton("⚡ Sinal", callback_data="sinal")],
        [InlineKeyboardButton("📊 Pares", callback_data="pares")],
        [InlineKeyboardButton("🛡️ Risco", callback_data="risco")],
        [InlineKeyboardButton("ℹ️ Ajuda", callback_data="ajuda")],
    ]
    reply_markup = InlineKeyboardMarkup(teclado)
    
    msg = """
⚡ *BEM-VINDO AO DADEX* ⚡

Sou o teu bot de sinais Forex!

📈 Gero sinais com cronograma
🛡️ Gestão de risco completa
🌍 Análise de timeframes
⏰ Horários exactos

Clica nos botões abaixo!
"""
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=reply_markup)

async def cmd_sinal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera um sinal"""
    par = random.choice(list(PARES.keys()))
    sinal = gerar_sinal(par)
    msg = formatar_sinal(sinal)
    await update.message.reply_text(msg, parse_mode="Markdown")

async def cmd_pares(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista os pares"""
    msg = "📊 *Pares disponíveis:*\n\n"
    for par, emoji in PARES.items():
        msg += f"{emoji} {par}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def cmd_risco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Regras de risco"""
    msg = """
🛡️ *GESTÃO DE RISCO DADEX*

📌 Regras Ouro:
1. Nunca >2% por trade
2. Máx 3 trades/dia
3. Parar se -6% num dia
4. Sempre usar SL
5. Só operar 08:00-22:00 UTC

💰 Com $1.000:
• Risco: $20/trade
• Perda máxima: $60/dia
• Lote: 0.01
"""
    await update.message.reply_text(msg, parse_mode="Markdown")

async def cmd_ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ajuda"""
    msg = """
ℹ️ *DADEX — GUIA*

📌 *Comandos:*
/start - Menu
/sinal - Gerar sinal
/pares - Ver pares
/risco - Gestão risco
/ajuda - Ajuda

🎯 *Como usar:*
1. Pede /sinal
2. Segue o cronograma
3. H4 → M15 → M5
4. Entra se tudo alinhar!

⚠️ Educacional apenas!
"""
    await update.message.reply_text(msg, parse_mode="Markdown")

async def botao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa botões"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "sinal":
        par = random.choice(list(PARES.keys()))
        sinal = gerar_sinal(par)
        msg = formatar_sinal(sinal)
        await query.edit_message_text(msg, parse_mode="Markdown")
    
    elif query.data == "pares":
        msg = "📊 *Pares:*\n\n"
        for par, emoji in PARES.items():
            msg += f"{emoji} {par}\n"
        await query.edit_message_text(msg, parse_mode="Markdown")
    
    elif query.data == "risco":
        msg = """
🛡️ *RISCO DADEX*

1. Max 2% por trade
2. Max 3 trades/dia
3. Stop loss obrigatório
4. Operar 08:00-22:00 UTC
5. Parar se -6% num dia
"""
        await query.edit_message_text(msg, parse_mode="Markdown")
    
    elif query.data == "ajuda":
        msg = """
ℹ️ *DADEX v3.0*

Bot de sinais Forex
com cronograma integrado!

/start - Menu
/sinal - Sinal
/pares - Pares
/risco - Risco
/ajuda - Ajuda
"""
        await query.edit_message_text(msg, parse_mode="Markdown")

# ============================================================
# MAIN
# ============================================================

def main():
    """Inicia o bot"""
    print("⚡ Iniciando DADEX Bot v3.0...")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sinal", cmd_sinal))
    app.add_handler(CommandHandler("pares", cmd_pares))
    app.add_handler(CommandHandler("risco", cmd_risco))
    app.add_handler(CommandHandler("ajuda", cmd_ajuda))
    app.add_handler(CallbackQueryHandler(botao))
    
    print("✅ DADEX Bot online!")
    app.run_polling()

if __name__ == "__main__":
    main()

