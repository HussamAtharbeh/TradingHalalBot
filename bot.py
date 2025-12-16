import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise SystemExit("❌ Missing BOT_TOKEN env var. Set it first (do NOT paste it in chat).")

ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "1715510088"))

DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)
KNOWLEDGE_FILE = DATA_DIR / "knowledge.json"
USER_FILE = DATA_DIR / "users.json"

TEACH_Q, TEACH_A, TEACH_SRC = 1, 2, 3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TradingHalalBot")

# =========================
# Helpers
# =========================
def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def norm(t: str) -> str:
    t = (t or "").lower().strip()
    for ch in ["؟","!","،",".",",",":","؛","“","”","'","\""]:
        t = t.replace(ch, " ")
    return " ".join(t.split())

def load_knowledge() -> Dict[str, Any]:
    return load_json(KNOWLEDGE_FILE, {})

def save_knowledge(kb: Dict[str, Any]):
    save_json(KNOWLEDGE_FILE, kb)

def load_users():
    return load_json(USER_FILE, {})

def save_users(u):
    save_json(USER_FILE, u)

def add_xp(uid: int, amount: int) -> int:
    users = load_users()
    u = users.get(str(uid), {"xp": 0})
    u["xp"] += amount
    users[str(uid)] = u
    save_users(users)
    return u["xp"]

def get_xp(uid: int) -> int:
    return int(load_users().get(str(uid), {}).get("xp", 0))

def ensure_seed():
    kb = load_knowledge()
    if kb:
        return
    seeds = [
        ("هل التداول حلال؟",
         "التداول مباح بالأصل إذا كان على أصل حقيقي بدون ربا ولا غرر ولا قمار.",
         "تلخيص تعليمي"),
        ("هل الرافعة المالية حلال؟",
         "غالبًا غير جائزة إذا تضمنت فوائد أو قرض ربوي.",
         "تلخيص تعليمي"),
        ("هل السواب حلال؟",
         "رسوم التبييت إذا كانت فوائد فهي ربا محرّم.",
         "تلخيص تعليمي"),
        ("هل CFD حلال؟",
         "غالبًا غير جائز لأنه ليس تملكًا حقيقيًا وفيه غرر.",
         "تلخيص تعليمي"),
        ("هل تداول الأسهم حلال؟",
         "نعم بشروط: نشاط مباح وتجنب الاعتماد العالي على الفوائد.",
         "تلخيص تعليمي"),
    ]
    for q,a,s in seeds:
        kb[norm(q)] = {"question": q, "answer": a, "source": s}
    save_knowledge(kb)

def find_answer(q: str) -> Optional[Dict[str,str]]:
    kb = load_knowledge()
    nq = norm(q)
    if nq in kb:
        return kb[nq]
    for k in kb:
        if k in nq or nq in k:
            return kb[k]
    return None

# =========================
# Commands
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً 👋\nأنا TradingHalalBot لتعليم التداول الحلال.\n\n"
        "جرّب:\n"
        "/ask سؤالك\n"
        "/quiz\n"
        "/me\n",
        parse_mode=ParseMode.MARKDOWN
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start\n/help\n/ask سؤالك\n/quiz\n/me\n/resetme\n/myid\n"
        "للمشرف: /teach",
        parse_mode=ParseMode.MARKDOWN
    )

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(str(update.effective_user.id))

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ensure_seed()
    q = " ".join(context.args).strip()
    if not q:
        await update.message.reply_text("اكتب: /ask هل التداول حلال؟")
        return
    ans = find_answer(q)
    if not ans:
        await update.message.reply_text("ما عندي جواب جاهز. علّمني بـ /teach")
        return
    add_xp(update.effective_user.id, 2)
    await update.message.reply_text(
        f"**سؤال:** {ans['question']}\n\n**الجواب:** {ans['answer']}\n\n_المصدر: {ans['source']}_",
        parse_mode=ParseMode.MARKDOWN
    )

# =========================
# Teach (admin)
# =========================
def is_admin(uid: int) -> bool:
    return ADMIN_USER_ID != 0 and uid == ADMIN_USER_ID

async def teach_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("هذا الأمر للمشرف فقط.")
        return ConversationHandler.END
    await update.message.reply_text("اكتب السؤال:")
    return TEACH_Q

async def teach_q(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q"] = update.message.text
    await update.message.reply_text("اكتب الجواب:")
    return TEACH_A

async def teach_a(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["a"] = update.message.text
    await update.message.reply_text("اكتب المصدر (أو -):")
    return TEACH_SRC

async def teach_s(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ensure_seed()
    kb = load_knowledge()
    q = context.user_data["q"]
    a = context.user_data["a"]
    s = update.message.text or "-"
    kb[norm(q)] = {"question": q, "answer": a, "source": s}
    save_knowledge(kb)
    add_xp(update.effective_user.id, 10)
    await update.message.reply_text("تم الحفظ ✔️")
    return ConversationHandler.END

# =========================
# Quiz
# =========================
QUIZ = [
    ("الرافعة التي فيها فوائد: صح/خطأ", "صح"),
    ("CFD تملك حقيقي: صح/خطأ", "خطأ"),
]

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["qi"] = 0
    await update.message.reply_text(QUIZ[0][0])

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "qi" in context.user_data:
        i = context.user_data["qi"]
        correct = QUIZ[i][1]
        if norm(update.message.text) == norm(correct):
            add_xp(update.effective_user.id, 5)
            await update.message.reply_text("صح ✔️ +5XP")
        else:
            add_xp(update.effective_user.id, 1)
            await update.message.reply_text(f"غلط ❌ الصحيح: {correct}")
        context.user_data["qi"] = (i + 1) % len(QUIZ)
        await update.message.reply_text(QUIZ[context.user_data["qi"]][0])
        return

    ensure_seed()
    ans = find_answer(update.message.text)
    if ans:
        add_xp(update.effective_user.id, 2)
        await update.message.reply_text(
            f"{ans['answer']}\n\n_المصدر: {ans['source']}_",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text("استخدم /ask أو /teach")

async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"XP: {get_xp(update.effective_user.id)}")

async def resetme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    users[str(update.effective_user.id)] = {"xp": 0}
    save_users(users)
    await update.message.reply_text("تم التصفير.")

# =========================
# Main
# =========================
def main():
    ensure_seed()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("me", me))
    app.add_handler(CommandHandler("resetme", resetme))
    app.add_handler(CommandHandler("myid", myid))

    teach_conv = ConversationHandler(
        entry_points=[CommandHandler("teach", teach_entry)],
        states={
            TEACH_Q: [MessageHandler(filters.TEXT & ~filters.COMMAND, teach_q)],
            TEACH_A: [MessageHandler(filters.TEXT & ~filters.COMMAND, teach_a)],
            TEACH_SRC: [MessageHandler(filters.TEXT & ~filters.COMMAND, teach_s)],
        },
        fallbacks=[],
    )
    app.add_handler(teach_conv)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    logger.info("✅ Bot is running (polling)...")
    app.run_polling()

if __name__ == "__main__":
    main()
