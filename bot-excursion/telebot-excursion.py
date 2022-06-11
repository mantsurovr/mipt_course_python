import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def help(update, context):
    update.message.reply_text(f"Это бот-экскурсовод. Для запуска отправьте /start")


def zal_1(update, context):
    reply_keyboard = [['/zal_2', '/close']]
    markup_start = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    text = """
    В данном зале представлены экспонаты экспозиции «Утро космической эры»
    Мы всегда будем гордиться нашей страной, поскольку наша страна является первопроходцем в освоении космоса...
    """
    update.message.reply_text(text, reply_markup=markup_start)


def zal_2(update, context):
    reply_keyboard = [['/zal_3']]
    markup_start = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    text = """
    В данном зале представлены экспонаты экспозиции «Творцы космической эры»
    Зал представлена инсталляция кабинета С. П. Королева и военная форма конструктора. 
    Здесь же экспонируется деревянная веранда дома в Калуге, в котором жил К. Э. Циолковский.
    В мемориальном зале можно увидеть вещи, принадлежавшие основателю изучения реактивного движения Фридриху Артуровичу Цандеру. Это пишущая машинка, гири, весы и ракетный двигатель, созданный ученым в начале прошлого века.
    """
    update.message.reply_text(text, reply_markup=markup_start)


def zal_3(update, context):
    reply_keyboard = [['/zal_1', '/zal_4']]
    markup_start = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    text = """
    В музее экспонируется несколько точных копий ценных технических устройств. Взрослых и детей привлекает большой металлический шар - первый искусственный спутник, запущенный на околоземную орбиту в 1957 году. Неподалеку от него выставлен оранжевый скафандр, в котором летал Гагарин, и скафандр для выхода в открытый космос, впервые использованный космонавтом Леонидом Леоновым.
    В музейных залах находятся копии спускаемых аппаратов, побывавших на Венере и Марсе. Некоторые посетители задерживаются, чтобы получше разглядеть ракетный двигатель и агрегат стыковки космического корабля «Союз».
    """
    update.message.reply_text(text, reply_markup=markup_start)


def zal_4(update, context):
    reply_keyboard = [['/zal_1']]
    markup_start = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    text = """
    Интересно познакомиться с повседневной жизнью космонавтов на орбите. В музее хранятся стоматологический набор, при помощи которого можно лечить зубы в условиях невесомости, а также бортовой холодильник для овощей и фруктов.
    Чем отличаются ракеты-носители «Протон» и «Сатурн»? На что похож стартовый комплекс «Спейс шаттл»? Чтобы ответить на эти вопросы, с ребенком стоит заглянуть в зал, где находятся точно выполненные макеты российских, американских и китайских ракет.
    """
    update.message.reply_text(text, reply_markup=markup_start)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
    )

    logger = logging.getLogger(__name__)

    TOKEN = '0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

    reply_keyboard_start = [['/zal_1']]
    markup_start = ReplyKeyboardMarkup(reply_keyboard_start, one_time_keyboard=False)

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    def start(update, context):
        text = """
        Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб! После можете перейти в первый зал.
        """
        update.message.reply_text(text, reply_markup=markup_start)

    def close_keyboard(update, context):
        text = """
        Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!
        """
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("zal_1", zal_1))
    dp.add_handler(CommandHandler("zal_2", zal_2))
    dp.add_handler(CommandHandler("zal_3", zal_3))
    dp.add_handler(CommandHandler("zal_4", zal_4))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
