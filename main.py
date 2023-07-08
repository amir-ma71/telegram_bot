import telebot
from telebot import apihelper
import pandas as pd

bot = telebot.TeleBot("6277901417:AAFfXXuCDtBXhgGbiHh_PA_J04ObkBTNU0c")
apihelper.proxy = {
  'http': 'http://proxy.kavosh.org:808',
  'https': 'http://proxy.kavosh.org:808'
}


data = pd.read_csv("data.csv", encoding="utf-8", sep="~")


agree_button = telebot.types.InlineKeyboardButton( "متوجه شدم",callback_data="سلام")
markup = telebot.types.InlineKeyboardMarkup()
markup.add(agree_button)


@bot.callback_query_handler(func= lambda call:True)
def callback(call):
    bot.send_message(call.message.chat.id, "باریکلا، حالا شماره دانشجوئیت رو وارد کن")




@bot.message_handler(commands=["start"])
def send_start(message):
    msg = """ خدا قوت به همتون،البته نه همتون؛ فقط به اونایی که تلاش کردن و وقت گذاشتن برای یاد گرفتن
      قبل از دیدن نمره، توجهت رو به چند تا نکته جلب میکنم:
      1. نمره برگه و نمره نهاییت رو نشونت میدم، نمره نهایی همون نمره ایه که قراره توی سایت ببینی
      2. اختلاف نمره برگه و نهایی برای هر کسی متفاوته و بستگی به اول فعالیت و دوم حضورش سر کلاس داره
      3. همونطوری که گفتم نمره 9.75 صرفا به خاطر معدل ترمت داده شده یعنی نیا بگو استاد 0.25 دیگه بده پاس شم
      4. باز هم همونطور که قبلا هم گفتم خواهشا خواهشا خواهشا از ناله بی مورد ( اعم از سرکار رفتن، مریض بودن، پول نداشتن و ....) بپرهیز چون پاسخی دریافت نخواهی کرد
      5. اگر افتادی، خودت افتادی من ننداختمت؛ ولی اگر پاس شدی ممکنه که من پاست کرده باشم :-))
      6. و در نهایت با تمام این توضیحات اگه مساله ای بود بیا پی وی ببینیم چه میشه کرد ( که 99% کاری نمیشه کرد)
      """
    bot.send_message(message.chat.id,msg, reply_markup=markup)

@bot.message_handler()
def return_score(message):
    try:
        student_id = int(message.text)
        try:
            row = data.loc[data['id'] == student_id].reset_index()
            if row["exam_score"][0] != "absent":
                report = f"نام دانشجو: {row['name'][0] + ' ' + row['family'][0]}\n" \
                         f"شماره دانشجویی: {row['id'][0]}\n" \
                         f"نمره برگه: {row['exam_score'][0]}\n" \
                         f"نمره نهایی: {row['finall_score'][0]}\n"
                bot.send_message(message.chat.id, report)
            else:
                report = f"نام دانشجو: {row['name'][0] + ' ' + row['family'][0]}\n" \
                         f"شماره دانشجویی: {row['id'][0]}\n" \
                         f"غایب در جلسه امتحان"
                bot.send_message(message.chat.id, report)
        except:
            bot.send_message(message.chat.id, "این شماره دانشجوئی در لیست نیست")
    except:
        bot.send_message(message.chat.id, "شماره دانشجوئی رو صحیح وارد کن")



print("Bot is running . . .")
bot.infinity_polling()