import asyncio
await update.message.reply_text("Дата в формате YYYY-MM-DD")
return
with db() as conn:
u1 = conn.execute("SELECT id FROM users WHERE name=?", (name1,)).fetchone()
u2 = conn.execute("SELECT id FROM users WHERE name=?", (name2,)).fetchone()
if not u1 or not u2 or u1["id"] == u2["id"]:
await update.message.reply_text("Проверь имена (нужно два разных участника).")
return
# Снимаем прошлое назначение (и откатываем счётчики) — для простоты делаем только перезапись без отката
apply_assignment(conn, duty_date, u1["id"], u2["id"], "override")
await update.message.reply_text("Назначение принудительно установлено.")


async def settime_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
# /settime HH:MM (МСК)
if not context.args:
await update.message.reply_text("Текущая команда: /settime HH:MM (МСК)")
return
t = context.args[0]
try:
h, m = time_str_to_hm(t)
assert 0 <= h < 24 and 0 <= m < 60
except Exception:
await update.message.reply_text("Формат времени HH:MM")
return
with db() as conn:
conn.execute("UPDATE settings SET announce_time=? WHERE id=1", (t,))
await update.message.reply_text(f"Время объявления изменено на {t} МСК (вступит в силу после перезапуска планировщика).")


async def reset_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
# Ручной сброс лимитов на новый месяц
with db() as conn:
new_m = ym_today()
ensure_counters(conn, new_m)
conn.execute("DELETE FROM counters WHERE month!=?", (new_m,))
await update.message.reply_text("Лимиты сброшены на текущий месяц.")




def schedule_daily(app: Application):
# Читаем время из БД
with db() as conn:
t = get_settings(conn)["announce_time"] # 'HH:MM'
h, m = time_str_to_hm(t)
when = time(hour=h, minute=m, tzinfo=TZ)
app.job_queue.run_daily(plan_and_announce, when, name="announce")
logger.info(f"Планировщик запущен: ежедневно в {t} МСК")




async def main():
await init_db()
app = ApplicationBuilder().token(BOT_TOKEN).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("today", today_cmd))
app.add_handler(CommandHandler("month", month_cmd))
app.add_handler(CommandHandler("absent", absent_cmd))
app.add_handler(CommandHandler("present", present_cmd))
app.add_handler(CommandHandler("override", override_cmd))
app.add_handler(CommandHandler("settime", settime_cmd))
app.add_handler(CommandHandler("reset", reset_cmd))


schedule_daily(app)


await app.initialize()
await app.start()
logger.info("Bot started")
try:
await app.updater.start_polling(drop_pending_updates=True)
await asyncio.Event().wait()
finally:
await app.updater.stop()
await app.stop()
await app.shutdown()


if __name__ == "__main__":
asyncio.run(main())
