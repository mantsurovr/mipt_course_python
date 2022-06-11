import logging
from statistics import variance
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
import functools


def help(update, context):
    update.message.reply_text("It is a dice game, and a timer")

def roll_one_six_sided_die(update, context):
    update.message.reply_text(f"The number is: {random.randint(1,6)}")

def roll_2_six_sided_dice(update, context):
    update.message.reply_text(f"The numbers are: {random.randint(1,6)}, {random.randint(1,6)}")

def roll_a_20_sided_die(update, context):
    update.message.reply_text(f"The number is: {random.randint(1,20)}")

def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def set_timer(update, context, arg=None):
    """Добавляем задачу в очередь"""
    reply_keyboard_close = [['/close']]
    markup_close = ReplyKeyboardMarkup(reply_keyboard_close, one_time_keyboard=False)
    
    chat_id = update.message.chat_id
    
    if arg:
        timer_sec = arg
    else:
        try:
            timer_sec = context.args[0]
        except (IndexError, ValueError):
            update.message.reply_text('Ошибка с аргументом, попробуйте: /set <секунд>')
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        due = int(timer_sec)
        if due < 0:
            update.message.reply_text('Извините, не умеем возвращаться в прошлое')
            return
        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))
        text = f'засек {due} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        update.message.reply_text(text, reply_markup=markup_close)
    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')

def task(context):
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text=f'Время истекло!')

def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    update.message.reply_text(text)

def main():
    logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
    )

    logger = logging.getLogger(__name__)

    TOKEN = '0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

    reply_keyboard_start = [['/dice', '/timer']]
    reply_keyboard_dice = [['/roll_one_six_sided_die', '/roll_2_six_sided_dice'],
                            ['/roll_a_20_sided_die', '/back']]
    reply_keyboard_timer = [['/30_sec', '/1_min'],
                            ['/5_mins', '/back']]
    

    markup_start = ReplyKeyboardMarkup(reply_keyboard_start, one_time_keyboard=False)
    markup_dice = ReplyKeyboardMarkup(reply_keyboard_dice, one_time_keyboard=False)
    markup_timer = ReplyKeyboardMarkup(reply_keyboard_timer, one_time_keyboard=False)

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    def start(update, context):
        update.message.reply_text("Make a choose", reply_markup=markup_start)

    def dice(update, context):
        update.message.reply_text("Make a choose", reply_markup=markup_dice)

    def close_keyboard(update, context):
        update.message.reply_text("Closed. In case continue start with working bot: /start", reply_markup=ReplyKeyboardRemove())

    def back(update, context):
        update.message.reply_text("Back to start", reply_markup=markup_start)

    def timer(update, context):
        update.message.reply_text("Make a choose", reply_markup=markup_timer)

    dp.add_handler(CommandHandler("help", help, pass_args=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("timer", timer))
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("roll_one_six_sided_die", roll_one_six_sided_die))
    dp.add_handler(CommandHandler("roll_2_six_sided_dice", roll_2_six_sided_dice))
    dp.add_handler(CommandHandler("roll_a_20_sided_die", roll_a_20_sided_die))
    dp.add_handler(CommandHandler("back", back))
    dp.add_handler(CommandHandler("30_sec", functools.partial(set_timer, arg=30), pass_args=True, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("1_min", functools.partial(set_timer, arg=60), pass_args=True, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("5_min", functools.partial(set_timer, arg=300), pass_args=True, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("set", set_timer, pass_args=True, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("close", unset, pass_chat_data=True))
    
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
