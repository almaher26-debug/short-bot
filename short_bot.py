# ===== بوت الشورت (Short bot) =====
# فيه الأقسام الشغالة بس (الأقسام المطفية انحذفت من الملف - 9 نوفمبر 2026)
# التشغيل على Railway: python short_bot.py  (المتغيرات: TELEGRAM_TOKEN + ALPACAAPIKEY + ALPACASECRETKEY)
"""
بوت التنبيهات - يشتغل على Railway ويرسل على تيليجرام
=====================================================

(1هـ) الإنفيرجن IFVG - قائمة المراقبة (منقول من gap_scanner) - شغال
    - فريم ساعة: الجلسة الممتدة (4 الفجر - 8 بالليل نيويورك) + 24 ساعة (الليل من ألباكا)، الجاب 16 سنت وفوق
    - فريم 4 ساعات: 24 ساعة (الليل من ألباكا) + الممددة، الجاب 10 سنت وفوق | الرسالة فيها الشموع الأربع
    - تمركز القاما تحت التنبيه (IFVG_GAMMA = False يشيله)
    - ENABLE_WATCH_IFVG = False يطفيه (أو WATCH_IFVG_1H / WATCH_IFVG_4H لكل فريم)

(1) الإنفيرجن IFVG (القديم، مع الشموع) - مطفي: ENABLE_IFVG = False
    - 🟢 صعودي: قاع الشمعة الأولى فوق قمة الثالثة (جاب)، الثانية تغطيه، والرابعة تقفل فوق أعلى الجاب
    - 🔴 هبوطي: نفس الشي بالعكس، والرابعة تقفل تحت أسفل الجاب | لون الشموع ما يهم
    - الجلسة الممتدة بدون الليلي (4 الفجر - 8 بالليل نيويورك)، شموع 4 ساعات: 4-8، 8-12، 12-4، 4-8
    - حجم الجاب: 50 سنت وفوق (ساعة) و1$ وفوق (4 ساعات)، والتنبيه بعد إغلاق الشمعة بدقيقة
    - ENABLE_IFVG = False يطفيه (أو ENABLE_IFVG_1H / ENABLE_IFVG_4H لكل فريم)

(4ج) نزول الشورت المتاح - من Interactive Brokers (نفس ChartExchange)
    - الأسهم: من 1$ إلى 10$ وقيمتها السوقية من 1 إلى 100 مليون
    - تنبيه "📉 نزول الشورت المتاح" لما المتاح ينزل أكثر من 90% عن أعلى رقم خلال آخر 30 يوم، مع حجم الشورت آخر 15 يوم (FINRA)
    - أقصى 48 تنبيه باليوم موزعة على 24 ساعة، وتنبيه واحد لكل سهم كل 7 أيام
    - ENABLE_BORROW_DROP = False يطفيه

(4ب) التجزئة العكسية - أسهم ناسداك
    - كل يوم سوق (بعد 10 الصبح نيويورك): الأسهم اللي سوت تجزئة عكسية جديدة بس
    - كل جمعة: قائمة بتجزئات آخر 7 أيام
    - ENABLE_RSPLIT_SHORT = False يطفيه

(6) كشف خوارزميات التقطيع - من ألباكا
    - الأسهم: أسهم ناسداك اللي سعرها من 1$ إلى 15$ وسوت تجزئة عكسية خلال آخر 3 شهور
    - يدور على صفقات صغيرة (10 أسهم وأقل) بنفس الحجم بالضبط، مثل 1، 1، 1، 1...
    - تنبيه لو تكررت 300 مرة أو أكثر خلال 5 دقايق، وقوي عند 600
    - يقدّر هل غالبها شراء ولا بيع من اتجاه السعر (تقريبي)
    - البيانات من كل البورصات (sip) لحظية بالباقة المدفوعة (ALGO_DELAY_MIN = 0)
    - ALGO_SMALL=0 في Railway يطفيه

(6ج) خوارزميات البني ستوك - نفس منطق (6) بالضبط
    - الأسهم: ناسداك من 1$ إلى 5$ وقيمتها السوقية 40 مليون دولار وتحت (أنشط 300)
    - تنبيه واحد بس لكل سهم كل 24 ساعة (ALGO_PENNY_ONCE_HOURS، ونفسه للقسم (6) ALGO_SMALL_ONCE_HOURS)
    - ALGO_PENNY=0 في Railway يطفيه

(6ب) خوارزميات الأسهم الكبيرة - قائمة المراقبة (WATCH_SYMBOLS) - من ألباكا
    - 300 صفقة أو أكثر ورا بعض بحجم سهم واحد بالضبط، وما بينها ولا صفقة بحجم ثاني، والفاصل 5 ثواني أو أقل
    - ينبه بس لو "شراء كامل" أو "بيع كامل" (الجهة وحدة 90% وفوق) - وقت السوق الرسمي بس
    - ALGO_BIG=0 في Railway يطفيه (أو ALGO_BIG_SYMBOLS لقائمة ثانية)

(6د) الآيس بيرغ - نفس أسهم (6ب) ونفس الصفقات (ما يزيد طلبات على ألباكا)
    - 500 صفقة أو أكثر ورا بعض بنفس الحجم ونفس السعر بالضبط (من سهم إلى 10 أسهم)، والفاصل ثانيتين أو أقل
    - تحديث عند 1000 ثم 2000 ... | ALGO_ICE=0 في Railway يطفيه

(1ك-2) سحب سيولة دعم ومقاومة الأسبوع السابق - فريم 4 ساعات - قائمة المراقبة (WATCH_SYMBOLS)
    - الدعم: شمعة 4 ساعات ذيلها بس نزل تحت قاع الأسبوع السابق، وافتتاحها وإغلاقها فوقه → كول
    - المقاومة: ذيلها بس طلع فوق قمة الأسبوع السابق، وافتتاحها وإغلاقها تحتها → بوت
    - شموع 4 ساعات بدون الجلسة الليلية (4-8 بري، 8-12، 12-4، 4-8 أفتر نيويورك)
    - تنبيه واحد لكل سهم بالأسبوع لكل جهة، يفحص كل 5 دقايق
    - ENABLE_PWL_4H / ENABLE_PWH_4H = False يطفي الدعم / المقاومة | PW4H_WICK_ONLY = False يرجع شرط الإغلاق بس

(11) سحب قمة الجمعة يوم الاثنين ثم سحب دعم الأسبوع السابق (فريم 4 ساعات) → كول
    - الاثنين: السعر يسحب قمة الجمعة ويرجع يختبرها وما يخترقها
    - بعدها ينزل لقاع الأسبوع السابق ويسحب السيولة (ذيل تحت الدعم وإغلاق فوقه)
    - التنبيه: كول مع الأهداف والوقف وعقد كول مدته أسبوعين
    - الأسهم: قائمة المراقبة اللي سعرها 100$-400$ | ENABLE_FRIMON = False يطفيه

(12) سحب السيولة الأسبوعي - فريم 4 ساعات (4-8، 8-12، 12-4، 4-8 نيويورك) + العقد - كل قائمة المراقبة (بدون شرط سعر)
    - الدعم: ذيل الشمعة بس نزل تحت قاع الأسبوع السابق، والافتتاح والإغلاق فوقه → كول
    - المقاومة: ذيل الشمعة بس طلع فوق قمة الأسبوع السابق، والافتتاح والإغلاق تحتها → بوت
    - WKOPT_PUT_ONLY = True = البوت بس (الكول يرجع على (1ك-2) بدون عقد)
    - لو رجع اختبر المستوى وسوى سحب ذيل ثاني → تنبيه ثاني "🔁 إعادة اختبار" (WKOPT_REALERT = False = تنبيه واحد بالأسبوع)
    - العقد: أكثر من 10 أيام، حجم تداول فوق 500، عقود مفتوحة فوق 1000، دلتا فوق 0.1200 + قاما العقد
    - لو ما لقى عقد بالشروط ينبه بدونه | المؤشرات (سباكس) تنبيه بدون عقد | ENABLE_WKOPT = False يطفيه

(15) سحب دعم ومقاومة اليوم السابق - فريم ساعة (الجلسة الممددة) - أسهم القسم (13)
    - 🔴 مقاومة: ذيل شمعة الساعة فوق قمة اليوم السابق والإغلاق تحتها، والسهم هابط (تحت إغلاق أمس)
    - 🟢 دعم: ذيل شمعة الساعة تحت قاع اليوم السابق والإغلاق فوقه، والسهم صاعد (فوق إغلاق أمس)
    - تنبيه واحد باليوم لكل سهم لكل جهة | ENABLE_PDH1H / ENABLE_PDL1H = False يطفي المقاومة / الدعم

(14) اتجاه السوق المتوقع - ناسداك مقابل سباكس على قمة وقاع اليوم السابق (فريم 15 دقيقة)
    - 🔴 هابط: ناسداك سحب قمة اليوم السابق وقفل تحتها، وسباكس ما سحب قمته
    - 🟢 صاعد: ناسداك سحب قاع اليوم السابق وقفل فوقه، وسباكس ما سحب قاعه
    - التنبيه: $SPX | $NDX ← الاتجاه ← تمركز القاما للمؤشرين | ENABLE_SMT = False يطفيه

التشغيل:
  pip install yfinance pandas requests lxml
  python short_bot.py               # يشتغل باستمرار
  python short_bot.py --once        # فحص مرة وحدة بس
  python short_bot.py --algotest    # يجرب كشف خوارزميات التقطيع (بدون نت)
  python short_bot.py --pwltest     # يجرب سحب الأسبوع السابق (بدون نت)
  python short_bot.py --pw4hnow [--send]   # سحب الأسبوع السابق 4 ساعات على بيانات حقيقية
  python short_bot.py --frimontest  # يجرب سحب الجمعة/الاثنين (بدون نت)
  python short_bot.py --wkopttest   # يجرب اختيار العقد للسحب الأسبوعي (بدون نت)
  python short_bot.py --ifvgtest    # يجرب الإنفيرجن (بدون نت)
  python short_bot.py --pdh1htest   # يجرب سحب مقاومة اليوم السابق فريم ساعة (بدون نت)
  python short_bot.py --smttest     # يجرب اتجاه السوق ناسداك/سباكس (بدون نت)
"""

import gc
import io
import json
import logging
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import csv
import math
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from zoneinfo import ZoneInfo

import pandas as pd
import requests

# ================== الإعدادات ==================
# على السيرفر تنحط كمتغيرات (Variables) عشان ما تنكشف في جيتهب
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "ضع_توكن_البوت_هنا")      # من @BotFather
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "ضع_رقم_المحادثة_هنا")  # من @userinfobot
# تقدر تحط أكثر من رقم بينهم فاصلة، مثال:  123456789,-1001234567890
# وأي قروب أو قناة تضيف لها البوت، يلقط رقمها لحاله ويرسل لها التنبيهات
AUTO_ADD_GROUPS = True
CHATS_FILE = "chats.txt"     # يحفظ فيه أرقام القروبات اللي لقطها

LOOP_SLEEP_SEC = 20          # كل كم ثانية يشيك هل جا وقت فحص
NY = "America/New_York"
LOCAL_TZ = "Asia/Riyadh"     # توقيتك المحلي

# ---- الجلسات وبيانات الشموع (تستخدمها أقسام الشموع: سحب الأسبوع السابق 4 ساعات + سحب الجمعة/الاثنين) ----
GAP_EXTENDED = True              # يشمل ما قبل الفتح وبعد الإغلاق (4 الفجر - 8 بالليل نيويورك)

# الجلسة الليلية (8 بالليل - 4 الفجر نيويورك) = إعداد الـ24 ساعة في تريدنج فيو
# ياهو ما يعطيها، فتجي من Tiingo: حط المفتاح كمتغير TIINGO_TOKEN على Railway
TIINGO_TOKEN = os.environ.get("TIINGO_TOKEN", "")
GAP_OVERNIGHT = bool(TIINGO_TOKEN)   # يتفعل لحاله لو حطيت المفتاح

# ⭐ قائمتك الموحدة (قائمة المراقبة) - عليها سحب الأسبوع السابق 4 ساعات وسحب الجمعة/الاثنين
TEST_ON_START = True             # True = يرسل رسالة اختبار كل ما البوت يشتغل | False = بدون
ONE_LIST = False  # True = كل الأقسام على القائمة هذي | False = كل قسم يرجع لأسهمه القديمة
WATCH_SYMBOLS = [   # قائمتك (20 نوفمبر 2026) - 58 سهم + QQQ + SPY + GLD
    "NVDA", "CRM", "AVGO", "META", "TSLA", "SPCX", "AMD", "LITE", "AAPL", "RKLB",
    "UNH", "MU", "LLY", "ADBE", "QCOM", "SHOP", "GOOGL", "GOOG", "MSFT", "MSTR",
    "AMZN", "DDOG", "ACN", "GEV", "LRCX", "PLTR", "OKTA", "ORCL", "INTC", "CRDO",
    "SNDK", "STX", "CRCL", "WDC", "SKHY", "CRWV", "CRWD", "MRVL", "ARM", "PANW",
    "SNOW", "NOW", "DELL", "ABBV", "HAS", "KO", "LULU", "APH", "SNPS", "IBM",
    "HD", "MRNA", "SMCI", "TEAM", "IREN", "RIOT", "TGT", "JNJ",
    # صناديق
    "QQQ", "SPY", "GLD",
]
# المؤشرات ما لها صفقات ولا بيانات في ألباكا، فتنشال من أقسام ألباكا (الخوارزميات، الزخم، الجلسة الليلية)
INDEX_SYMBOLS = {"^GSPC", "^NDX"}
INDEX_NAMES = {"^GSPC": "سباكس S&P 500", "^NDX": "ناسداك 100"}


def stocks_only(syms):
    """القائمة بدون المؤشرات - للأقسام اللي تعتمد على ألباكا."""
    return [x for x in syms if x not in INDEX_SYMBOLS]


GAP_BASE_MIN = 15                # البيانات تنحمّل بشموع 15 دقيقة، وكل الفريمات تنبني منها
GAP_SCAN_AFTER_CLOSE_MIN = (1, 5, 12)   # يفحص بعد الإغلاق بكذا دقيقة (الأولى هي الأساسية)
GAP_SENT_FILE = os.path.join(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "."), "gap_sent.txt")   # في /data عشان ما يعيد نفس التنبيه بعد إعادة التشغيل أو الرفع

# ---- (4ج) نزول الشورت المتاح أكثر من 90% (Interactive Brokers) ----
ENABLE_BORROW_DROP = False  # مطفي (16 نوفمبر 2026) | True = يرجع
BZ_SPREAD_24H = True             # True = التنبيهات تنقسم على 24 ساعة (وحدة كل 24÷BZ_MAX_PER_DAY = 30 دقيقة) | False = ترسل فوراً
BZ_MAX_PER_DAY = 48              # أقصى عدد تنبيهات باليوم | 0 = بدون حد
BZ_COOLDOWN_DAYS = 7             # تنبيه واحد لكل سهم كل كذا يوم | 0 = بدون حد
BZ_MIN_PRICE = 1                 # أقل سعر: الأسهم فوق دولار بس (0 = بدون حد)
BZ_MAX_PRICE = 10                # أعلى سعر (0 = بدون حد)
BZ_MIN_MARKET_CAP = 1_000_000    # أقل قيمة سوقية: 1 مليون
BZ_MAX_MARKET_CAP = 100_000_000  # أعلى قيمة سوقية: 100 مليون (0 = بدون حد)
BZ_FTP_HOSTS = ("ftp2.interactivebrokers.com", "ftp3.interactivebrokers.com")   # ftp2 أول (ftp3 يعلّق)
BZ_FTP_TIMEOUT = 10              # ثواني لكل محاولة (كانت 25 وتضيّع دقيقة كاملة)
BZ_EVERY_MIN = 2                 # كل كم دقيقة يفحص (كانت 15) — يمسك تحديث IBKR خلال دقيقتين
BZ_WARN_AFTER_MIN = 60           # ينبهك لو ملف IBKR ما تحمّل من كذا دقيقة
BZ_UNIVERSE_EVERY_MIN = 60       # كل كم دقيقة يحدث قائمة البني ستوك (السعر والقيمة السوقية)
BZ_DROP_PCT = 90                 # ينبه لما المتاح ينزل أكثر من كذا % عن أعلى رقم بالفترة
BZ_DROP_DAYS = 30                # الفترة: آخر شهر
BZ_DROP_MIN_HIGH = 10_000        # أعلى رقم بالفترة لازم يكون كذا سهم وفوق (يشيل الأسهم اللي متاحها أصلاً قليل)
BZ_SHORT_DAYS = 15               # كم يوم من حجم الشورت يكتب في التنبيه
BZ_STATE_FILE = os.path.join(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "."), "borrow_state.json")   # يُحفظ في /data عشان ما يضيع مع كل رفع




# ---- (1ك-2) سحب سيولة دعم ومقاومة الأسبوع السابق - فريم 4 ساعات - قائمة المراقبة ----
PWL_EVERY_MIN = 5                # كل كم دقيقة يفحص وقت السوق
PWL_MAX_ALERT_DELAY_MIN = 30     # ما ينبه على شمعة قفلت من أكثر من كذا دقيقة
#   الدعم: شمعة 4 ساعات (من هالأسبوع) ذيلها نزل تحت قاع الأسبوع السابق وجسمها كامل فوقه
#   المقاومة: شمعة 4 ساعات ذيلها طلع فوق قمة الأسبوع السابق وجسمها كامل تحتها
#   الشموع بدون الجلسة الليلية: 4-8 بري، 8-12، 12-4 ماركت، 4-8 أفتر (نيويورك)
#   قمة وقاع الأسبوع السابق محسوبة من بري + ماركت + أفتر (4 الفجر - 8 بالليل) بدون الليلي
#   تنبيه واحد لكل سهم بالأسبوع لكل جهة (دعم / مقاومة)
ENABLE_PWL_4H = False  # الدعم: True = شغال | False = مطفي
ENABLE_PWH_4H = False  # المقاومة: True = شغال | False = مطفي
PW4H_WICK_ONLY = True  # True = الذيل بس يكسر المستوى، الافتتاح والإغلاق كلهم بجهته | False = الإغلاق بس

# ---- تأكيد سحب السيولة (للأقسام (1ك-2) و (12) و (13)) ----
#   التنبيه ما يطلع على شمعة السحب نفسها، يطلع على شمعة التأكيد اللي بعدها:
#   🟢 الدعم: شمعة سحب ذيلها بس تحت الدعم (الافتتاح والإغلاق فوقه)، وبعدها شمعة تقفل فوق قمة شمعة السحب
#      أو ترجع تختبر الدعم وما تكسر قاع شمعة السحب → كول
#   🔴 المقاومة: شمعة سحب ذيلها فوق المقاومة، وبعدها شمعة ترجع تختبر المقاومة وما تكسر قمة شمعة السحب
#      ولا تقفل فوق المقاومة → بوت
#   يلغي النموذج: كسر قاع/قمة شمعة السحب، أو إغلاق شمعة بالجهة الثانية من المستوى
SWEEP_CONFIRM = True             # True = يستنى التأكيد | False = ينبه على شمعة السحب نفسها مثل قبل
SWEEP_RETEST_PCT = 0.3           # إعادة الاختبار: السعر يوصل للمستوى أو يقرب منه بكذا % (0 = لازم يلمسه)

# ---- (13) سحب سيولة دعم ومقاومة اليوم السابق - فريم 4 ساعات - قائمة المراقبة ----
#   الدعم: شمعة 4 ساعات (من اليوم) ذيلها نزل تحت قاع اليوم السابق وقفلت فوقه → كول
#   المقاومة: شمعة 4 ساعات ذيلها طلع فوق قمة اليوم السابق وقفلت تحتها → بوت
#   التنبيه بعد إغلاق الشمعة، ويكتب مستويات اليوم السابق والأسبوع السابق (الدعم والمقاومة)
#   قمة وقاع اليوم السابق من بري + ماركت + أفتر (4 الفجر - 8 بالليل نيويورك) بدون الليلي
#   تنبيه واحد لكل سهم بالأسبوع لكل جهة (أول سحب للدعم + أول سحب للمقاومة)
ENABLE_PD4H = True     # True = شغال | False = مطفي
PD4H_SYMBOLS = ["TSLA", "MSFT", "AAPL", "AMD", "META", "NVDA", "GOOGL", "AMZN", "MU"]   # أسهم القسم (لحالها)
PD4H_CHECK_LINE = "🔎 حلل السهم بنفسك وحدد الاتجاه"
PD4H_WICK_ONLY = False # False = الإغلاق بس يرجع فوق الدعم / تحت المقاومة | True = لازم الافتتاح بعد بجهة المستوى

# ---- (15) سحب دعم ومقاومة اليوم السابق - فريم ساعة (مقاومة + هابط / دعم + صاعد) ----
#   شمعة ساعة (من اليوم) ذيلها طلع فوق قمة اليوم السابق وقفلت تحتها، والسهم هابط (الإغلاق تحت إغلاق أمس)
#   الجلسة الممددة (4 الفجر - 8 بالليل نيويورك) بدون الليلي | قمة اليوم السابق من بري + ماركت + أفتر
#   الأسهم: أسهم القسم (13) PD4H_SYMBOLS | تنبيه واحد باليوم لكل سهم | ينبه على شمعة السحب نفسها
ENABLE_PDH1H = True              # المقاومة (هابط): True = شغال | False = مطفي
ENABLE_PDL1H = True              # الدعم (صاعد): ذيل تحت قاع اليوم السابق وإغلاق فوقه، والسهم فوق إغلاق أمس

# ---- (14) اتجاه السوق المتوقع: ناسداك مقابل سباكس على قمة وقاع اليوم السابق ----
#   🔴 هابط: ناسداك سحب قمة اليوم السابق (ذيل فوقها) وقفلت الشمعة تحتها، وسباكس ما وصل قمة يومه السابق
#   🟢 صاعد: ناسداك سحب قاع اليوم السابق (ذيل تحته) وقفلت الشمعة فوقه، وسباكس ما وصل قاع يومه السابق
#   التنبيه: الرموز ← الاتجاه المتوقع ← تمركز القاما للمؤشرين (بدون شرح السحب) | لو ما تحقق الشرط ما فيه تنبيه
#   الجلسة الرسمية 9:30 - 4 نيويورك، تنبيه واحد باليوم لكل اتجاه
ENABLE_SMT = True                # True = شغال | False = مطفي
SMT_FRAME_MIN = 15               # فريم شمعة الإغلاق: 15 = ربع ساعة | 60 = ساعة | 240 = 4 ساعات
SMT_EVERY_MIN = 2                # كل كم دقيقة يفحص
SMT_MAX_ALERT_DELAY_MIN = 30     # ما ينبه على شمعة قفلت من أكثر من كذا دقيقة
SMT_NDX, SMT_SPX = "^NDX", "^GSPC"   # بيانات الأسعار من ياهو
# القاما: (الاسم، رمز عقود المؤشر في ياهو، صندوق احتياطي لو عقود المؤشر ما جات)
SMT_GAMMA = (("سباكس", "SPX", "^SPX", "SPY"), ("ناسداك", "NDX", "^NDX", "QQQ"))
SMT_SENT_FILE = os.path.join(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "."), "smt_sent.txt")
SMT_TEST_ID = "1"                # رسالة تجريبية مرة وحدة بعد الرفع — غيّر الرقم لو تبي وحدة ثانية

# ---- (1) الإنفيرجن IFVG - فريم ساعة و4 ساعات - قائمة المراقبة (WATCH_SYMBOLS) ----
#   نفس نموذج gap_scanner: ثلاث شموع بين ذيل الأولى والثالثة جاب، الثانية تغطي الجاب كامل،
#   والرابعة تقفل وراه (لون الشموع ما يهم)
#   🟢 صعودي: قاع الأولى فوق قمة الثالثة، والرابعة تقفل فوق أعلى الجاب (قاع الأولى)
#   🔴 هبوطي: قمة الأولى تحت قاع الثالثة، والرابعة تقفل تحت أسفل الجاب (قمة الأولى)
#   الجلسة الممتدة بدون الليلي (4 الفجر - 8 بالليل نيويورك)، شموع 4 ساعات: 4-8، 8-12، 12-4، 4-8
#   يفحص بعد إغلاق كل ساعة بدقيقة (ويعيد بعد 5 و12 دقيقة لو بيانات ياهو تأخرت)
ENABLE_IFVG = False              # مطفي (14 نوفمبر 2026) - بداله (1هـ) تحت المنقول من gap_scanner
ENABLE_IFVG_1H = True            # فريم ساعة
ENABLE_IFVG_4H = True            # فريم 4 ساعات
IFVG_1H_MIN_SIZE = 0.50          # أقل حجم للجاب - فريم ساعة (دولار)
IFVG_4H_MIN_SIZE = 1.00          # أقل حجم للجاب - فريم 4 ساعات (دولار)
IFVG_MIN_PRICE = 0               # أقل سعر سهم (0 = بدون شرط)
IFVG_REQUIRE_MIDDLE_COVER = True # الشمعة الثانية لازم تغطي الجاب كامل
IFVG_MAX_ALERT_DELAY_MIN = 30    # ما ينبه على شمعة قفلت من أكثر من كذا دقيقة
IFVG_SHOW_CANDLES = True         # يكتب الشموع الأربع (وقت، أعلى، أقل) في التنبيه

# ---- (1هـ) الإنفيرجن IFVG - قائمة المراقبة (منقول من gap_scanner، نفس تنبيهات COHR) ----
#   نفس النموذج: ثلاث شموع بين ذيل الأولى والثالثة جاب، الثانية تغطيه كامل، والرابعة تقفل وراه
#   فريم ساعة: الجلسة الممتدة (4 الفجر - 8 بالليل نيويورك)، الجاب 16 سنت وفوق
#   فريم 4 ساعات: 24 ساعة نفس تريدنج فيو (الشموع تبدأ 8 بالليل: 8-12، 12-4، 4-8، 8-12، 12-4، 4-8)
#     وبيانات الليل من ألباكا (feed=boats، نفس المفاتيح)، الجاب 10 سنت وفوق
#   الرسالة فيها الشموع الأربع (WATCH_SHOW_CANDLES)
ENABLE_WATCH_IFVG = True         # True = شغال | False = مطفي
WATCH_IFVG_1H = True             # فريم ساعة - الجلسة الممددة (4 الفجر - 8 بالليل نيويورك)
WATCH_IFVG_1H_24H = True         # فريم ساعة - 24 ساعة (مع الليلي من ألباكا) | نفس الشمعة ما تتكرر بالاثنين
WATCH_IFVG_4H = True             # فريم 4 ساعات - 24 ساعة (لو فيه مفاتيح ألباكا)
WATCH_IFVG_4H_EXT = True         # فريم 4 ساعات - الجلسة الممددة (4-8، 8-12، 12-4، 4-8 نيويورك) | نفس الشمعة ما تتكرر بالاثنين
WATCH_MIN_SIZE = 0.16            # حجم الجاب (فريم الساعة): 16 سنت وفوق | 0 = بدون شرط
WATCH4H_MIN_SIZE = 0.10          # حجم الجاب (فريم 4 ساعات): 10 سنت وفوق
WATCH_SHOW_CANDLES = False       # يكتب الشموع الأربع (وقت، لون، أعلى، أقل) في التنبيه - ساعة و4 ساعات | False = بدونها
WATCH_HEAD = False               # False = بدون سطر "للمتابعة" (الرمز أول سطر) | True = يرجع
WATCH_CHECK_LINE = "حلل بنفسك وتأكد من الاتجاه"   # سطر قبل إخلاء المسؤولية | "" = بدونه
IFVG_GAMMA = True                # يضيف تمركز القاما لتنبيهات الإنفيرجن (القسمين) | False = بدون
GAP_4H_24H = True               # فريم 4 ساعات: True = 24 ساعة (يحتاج مفاتيح ألباكا) | False = 4 الفجر - 8 بالليل

# ---- فلتر اتجاه السوق: من تنبيه القسم (14) ناسداك مقابل سباكس ----
#   لو (14) نبه اليوم 🔴 هابط ← ما يرسل كول (سحب الدعم) باقي اليوم
#   لو (14) نبه اليوم 🟢 صاعد ← ما يرسل بوت (سحب المقاومة) باقي اليوم
#   ما نبه (14) اليوم ← كول وبوت عادي | يشمل: (12) الأسبوعي مع العقد، (13) اليوم السابق 4 ساعات، (15) فريم ساعة
MARKET_FILTER = True             # True = شغال | False = كول وبوت دايماً

# ---- (12) سحب السيولة الأسبوعي (دعم ← كول | مقاومة ← بوت) + العقد - الأسهم من 100$ إلى 350$ ----
#   نفس شمعة السحب في (1ك-2)، بس الأسهم اللي سعرها داخل النطاق يجيها تنبيه واحد بالأسبوع (أول سحب، دعم أو مقاومة)
#   ومعه عقد بالشروط تحت. الأسهم برا النطاق تكمل على (1ك-2) مثل قبل.
ENABLE_WKOPT = True              # True = شغال | False = مطفي (كل الأسهم ترجع على (1ك-2) بدون عقد)
WKOPT_PUT_ONLY = False           # True = البوت بس (سحب المقاومة) | False = كول وبوت
                                 #   الكول (سحب الدعم) يرجع على (1ك-2) بدون عقد
WKOPT_FRAME_MIN = 240            # فريم القسم: 240 = 4 ساعات (4-8، 8-12، 12-4، 4-8 نيويورك بدون الليلي) | 360 = 6 ساعات
WKOPT_FRAME_TXT = f"فريم {WKOPT_FRAME_MIN // 60} ساعات"
WKOPT_MIN_PRICE = 0              # سعر السهم من (0 = بدون حد) — الحين كل قائمة المراقبة
WKOPT_MAX_PRICE = 0              # إلى (0 = بدون حد) — مثال: 100 و 350 يرجع النطاق القديم
WKOPT_OPT_MIN_DTE = 10           # العقد أكثر من 10 أيام (يختار أقرب انتهاء بعدها)
WKOPT_OPT_MAX_DTE = 45           # أبعد انتهاء يدوّر فيه
WKOPT_OPT_MIN_VOLUME = 500       # حجم التداول في العقد فوق 500
WKOPT_OPT_MIN_OI = 1000          # العقود المفتوحة (الكمية غير إغلاق المركز) فوق 1000
WKOPT_OPT_MIN_DELTA = 0.12       # الدلتا فوق 0.1200 (للبوت: القيمة المطلقة)
WKOPT_REALERT = True             # True = لو رجع اختبر المستوى وسوى سحب ذيل ثاني = تنبيه ثاني (كل شمعة سحب جديدة)
                                 # False = تنبيه واحد بس لكل سهم بالأسبوع
WKOPT_REQUIRE_CONTRACT = False   # True = ما ينبه إلا لو لقى عقد بالشروط | False = ينبه حتى بدون عقد
# ---- تمركز القاما للعقود مع تنبيه سحب السيولة (1ك-2) و (12) ----
#   من سلسلة عقود ياهو (العقود المفتوحة + IV): قاما كل سترايك × العقود المفتوحة × 100 × السعر² × 1%
#   الكول موجب والبوت سالب. يطلع: جدار الكول، جدار البوت، أعلى السترايكات، صافي القاما، ونقطة الانقلاب
SWEEP_GAMMA = True               # True = يضيف تمركز القاما للتنبيه | False = بدون
GAMMA_MAX_DTE = 30               # الانتهاءات اللي تدخل بالحساب: من اليوم إلى كذا يوم
GAMMA_MAX_EXPS = 4               # أقصى عدد انتهاءات (أقربها)
GAMMA_RANGE_PCT = 20             # السترايكات بس اللي داخل ±كذا % من السعر
GAMMA_TOP_N = 3                  # كم سترايك يكتب في "أعلى تمركز"
SWEEP_CHART = True               # صورة شارت 4 ساعات مع تنبيه السحب (يحتاج matplotlib) | False = نص بس
SWEEP_CHART_BARS = 30            # كم شمعة 4 ساعات تطلع بالصورة

# ---- حساب الدلتا وسعر العقد (يستخدمه سحب الجمعة/الاثنين) ----
PDR_OPT_RATE = 0.04              # الفائدة لحساب الدلتا لو المصدر ما أعطاها

# ---- (4ب) التجزئة العكسية ----
ENABLE_RSPLIT_SHORT = True  # قوائم التجزئة العكسية شغالة
RSPLIT_NEW_DAYS = 4                  # "جديد" = تجزئة صارت خلال آخر كذا يوم (يغطي الويكند) وما انرسلت قبل
RSPLIT_CHECK_AFTER_NY = 10           # الفحص اليومي بعد الساعة 10 الصبح نيويورك (عشان سعر الافتتاح يكون موجود)
RSPLIT_NEW_FILE = "rsplit_new.txt"       # التجزئات الجديدة اللي انرسلت
RSPLIT_WEEKLY = True                 # قائمة كل جمعة بتجزئات آخر 7 أيام
RSPLIT_STATE_FILE = "rsplit_state.txt"   # يحفظ آخر يوم/أسبوع انرسل عشان ما يتكرر

# ---- (6) كشف خوارزميات التنفيذ (أوامر متكررة بنفس الحجم) - من ألباكا ----
# يراقب الصفقات لحظياً (بورصة IEX المجانية) ويدور على صفقات ورا بعض بنفس الحجم بالضبط
# مثال: 1، 1، 1، 1، 1، 1 أو 4، 4، 4، 4، 4، 4 = غالباً خوارزمية تقسيم أو آيس بيرغ
ALPACA_KEY = (os.environ.get("ALPACAAPIKEY") or os.environ.get("ALPACA_API_KEY")
              or os.environ.get("APCA_API_KEY_ID", ""))
ALPACA_SECRET = (os.environ.get("ALPACASECRETKEY") or os.environ.get("ALPACA_SECRET_KEY")
                 or os.environ.get("APCA_API_SECRET_KEY", ""))
ENABLE_ALGO = bool(ALPACA_KEY and ALPACA_SECRET)  # يتفعل لحاله لو المفاتيح موجودة
# sip = كل البورصات (لحظي بالباقة المدفوعة، متأخر 15 دقيقة بالمجانية) | iex = بورصة وحدة صغيرة
# الأسهم الصغيرة تقريباً ما تتداول على IEX، فـ sip أدق بكثير لهالنوع
ALGO_FEED = os.environ.get("ALGO_FEED", "sip").lower()
# باقة ألباكا المدفوعة (Algo Trader Plus) = sip لحظي، فالتأخير صفر
# لو رجعت للباقة المجانية حط في Railway متغير ALGO_DELAY_MIN = 16
ALGO_DELAY_MIN = int(os.environ.get("ALGO_DELAY_MIN", "0"))
# الأسهم: تلقائياً أسهم ناسداك اللي سعرها من 1$ إلى 15$ وسوت تجزئة عكسية خلال آخر 3 شهور
# ولو تبي قائمة ثابتة حطها في Railway بمتغير ALGO_SYMBOLS (بينها فاصلة)
ALGO_SYMBOLS = [s.strip().upper() for s in os.environ.get("ALGO_SYMBOLS", "").split(",") if s.strip()]
ALGO_SMALL = os.environ.get("ALGO_SMALL", "1") != "0"   # 0 = يطفي هالقسم
ALGO_MIN_PRICE = 1                    # أقل سعر سهم
ALGO_MAX_PRICE = 15                   # أعلى سعر سهم
ALGO_MAX_MARKET_CAP = 0               # 0 = بدون شرط قيمة سوقية
ALGO_RSPLIT_DAYS = 92                 # لازم سوى تجزئة عكسية خلال آخر كذا يوم (3 شهور) - 0 = بدون شرط
ALGO_MIN_DAY_VOLUME = 50_000          # يشيل الأسهم الميتة (حجم اليوم)
ALGO_MAX_SYMBOLS = 300                # أقصى عدد أسهم يراقبها (الأنشط أول) - بالعادة أقل من كذا بكثير
ALGO_POLL_SEC = 15                    # كل كم ثانية يسحب الصفقات الجديدة
ALGO_MAX_SIZE = 10                    # الأحجام الصغيرة بس: صفقة حجمها 10 أسهم أو أقل (1، 1، 1...)
ALGO_WINDOW_MIN = 5                   # يعد الصفقات المتكررة خلال آخر كذا دقيقة
ALGO_MIN_STREAK = 300                 # تنبيه عند 300 صفقة بنفس الحجم
ALGO_STRONG_STREAK = 600              # تنبيه قوي عند 600 أو أكثر
ALGO_MIN_VALUE = float(os.environ.get("ALGO_MIN_VALUE", "25000"))   # أقل قيمة بالدولار لمجموع الصفقات المتكررة (0 = بدون شرط)
ALGO_SMALL_ONCE_HOURS = 24            # قسم التجزئة العكسية (1$-15$): تنبيه واحد لكل سهم كل كذا ساعة (0 = بدون حد)
ALGO_ONCE_FILE = "algo_once.txt"      # يحفظ وقت آخر تنبيه لكل سهم عشان ما يعيده لو البوت أعاد التشغيل
ALGO_REALERT_MIN = 15                 # ما يعيد نفس مستوى التنبيه لنفس السهم والحجم قبل كذا دقيقة

# ---- (6ج) خوارزميات البني ستوك: من 1$ إلى 5$ وقيمتها السوقية 40 مليون وتحت ----
# نفس منطق القسم (6) بالضبط: صفقات 10 أسهم وأقل بنفس الحجم، تنبيه 300 وقوي 600 خلال 5 دقايق
# السهم اللي داخل قائمة التجزئة العكسية (6) ما يتكرر هنا
ALGO_PENNY = os.environ.get("ALGO_PENNY", "1") != "0"   # 0 = يطفي هالقسم
ALGO_PENNY_ONCE_HOURS = 24            # تنبيه واحد بس لكل سهم، وبعدها يسكت عنه كذا ساعة (0 = بدون حد)
ALGO_PENNY_MIN_PRICE = 1
ALGO_PENNY_MAX_PRICE = 5
ALGO_PENNY_MAX_MARKET_CAP = 40_000_000
ALGO_PENNY_MAX_SYMBOLS = 300          # الأنشط أول


# ---- (6ب) خوارزميات الأسهم الكبيرة: صفقات متتالية بنفس الحجم ----
# أسهم ناسداك اللي قيمتها السوقية مليار دولار وفوق
# ينبه لما تجي 600 صفقة أو أكثر ورا بعض بنفس الحجم بالضبط، وما بينها ولا صفقة بحجم ثاني
# الأحجام الصغيرة بس: 10 أسهم وأقل (1، 1، 1 ... أو 5، 5، 5 ...)
ALGO_BIG = os.environ.get("ALGO_BIG", "1") != "0"      # 0 = يطفي هالقسم
ALGO_BIG_MIN_MARKET_CAP = 1_000_000_000   # مليار دولار وفوق
ALGO_BIG_MIN_STREAK = 300                 # أقل عدد صفقات متتالية بنفس الحجم
ALGO_BIG_MAX_SIZE = 1                     # حجم الصفقة: سهم واحد بس (1، 1، 1...)
ALGO_BIG_MAX_GAP_SEC = 5                  # لو مر أكثر من كذا ثانية بين صفقتين، تنقطع السلسلة
ALGO_BIG_MAX_SYMBOLS = int(os.environ.get("ALGO_BIG_MAX_SYMBOLS", "250"))   # الأنشط أول
ALGO_BIG_SYMBOLS = ([s.strip().upper() for s in os.environ.get("ALGO_BIG_SYMBOLS", "").split(",")
                     if s.strip()] or stocks_only(WATCH_SYMBOLS))   # الافتراضي: قائمة المراقبة (بدون المؤشرات)
ALGO_BIG_REGULAR_ONLY = True              # وقت السوق الرسمي بس (9:30 - 4 نيويورك)
ALGO_BIG_ONE_SIDE_PCT = 90                # "شراء كامل" أو "بيع كامل": الجهة وحدة 90% وفوق، وإلا ما ينبه
ALGO_BIG_POLL_SEC = 20                    # كل كم ثانية يسحب الصفقات الجديدة
ALGO_BIG_CHUNK = 20                       # كم سهم بكل طلب لألباكا (الكبيرة صفقاتها كثيرة)
ALGO_BIG_REALERT_MIN = 15                 # ما يعيد التنبيه لنفس السهم والحجم قبل كذا دقيقة

# ---- (6د) الآيس بيرغ: صفقات متتالية بنفس الحجم ونفس السعر بالضبط ----
# نفس أسهم (6ب) (ناسداك مليار وفوق) ونفس الصفقات اللي تنسحب لها، فما يزيد طلبات على ألباكا
# مثال: 1، 1، 1 ... (من سهم إلى 10 أسهم) كلها على نفس السعر ورا بعض، وما بينها ولا صفقة ثانية
ALGO_ICE = os.environ.get("ALGO_ICE", "1") != "0"      # 0 = يطفي هالقسم (يشتغل لو (6ب) شغال)
ALGO_ICE_MIN_STREAK = 500                 # أقل عدد صفقات متتالية
ALGO_ICE_MIN_SIZE = 1                     # أقل حجم للصفقة: سهم واحد
ALGO_ICE_MAX_SIZE = 10                    # أعلى حجم للصفقة: 10 أسهم
ALGO_ICE_MAX_GAP_SEC = 2                  # "وقت قصير": أكثر من كذا ثانية بين صفقتين = تنقطع السلسلة
ALGO_ICE_REALERT_MIN = 5                  # ما يعيد التنبيه لنفس السهم ونفس الحجم والسعر قبل كذا دقيقة

# ---- المحتوى التعليمي ----
ADD_EDUCATION = False            # الشرح التعليمي تحت التنبيهات: False = محذوف (رسائل أقصر) | True = يرجع
ADD_DISCLAIMER = True            # يضيف سطر إخلاء المسؤولية تحت كل رسالة
DISCLAIMER = "⚠️ محتوى تعليمي فقط، وليس توصية بيع أو شراء."

SENT_KEEP_LINES = 20000             # ملفات "المرسل" تنقص لآخر كذا سطر عشان ما تكبر للأبد
UNIVERSE_BATCH = 200                # حجم دفعة التحميل لما يفلتر كل الأسهم (أصغر = ذاكرة أقل)
# ===============================================

HEADERS = {"User-Agent": "Mozilla/5.0"}


# ================== أدوات عامة ==================
def log(*a):
    print(*a, flush=True)


class _YFNoise(logging.Filter):
    """يخفي رسائل ياهو المزعجة (مئات الأسطر كل فحص) ويعدّها بدالها."""
    news_fail = 0
    other = 0

    def filter(self, rec):
        try:
            msg = rec.getMessage()
        except Exception:
            msg = ""
        if "Failed to retrieve the news" in msg:
            _YFNoise.news_fail += 1
        else:
            _YFNoise.other += 1
        return False


logging.getLogger("yfinance").addFilter(_YFNoise())
# تحذيرات ياهو مع pandas الجديدة (inplace) تطلع مئات الأسطر وتخلي Railway يحذف رسائل السجل
import warnings
warnings.filterwarnings("ignore", message=".*inplace keyword.*")
warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance")


def free_memory():
    """يرجّع الذاكرة بعد كل فحص كبير."""
    gc.collect()


TG_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
CHATS = set()          # كل المحادثات اللي يرسل لها
_last_update_id = 0


def _resolve_chat(c):
    """@اسم_القناة ← رقمها (-100...) عشان ما تنحسب القناة مرتين (مرة بالاسم ومرة بالرقم)."""
    c = str(c).strip()
    if not c.startswith("@") or "ضع_" in TELEGRAM_TOKEN:
        return c
    try:
        r = requests.get(f"{TG_API}/getChat", params={"chat_id": c}, timeout=10).json()
        if r.get("ok"):
            return str(r["result"]["id"])
        log(f"ما قدرت أجيب رقم {c}: {r.get('description')}")
    except Exception as e:
        log(f"ما قدرت أجيب رقم {c}:", e)
    return c


def _load_chats():
    for c in TELEGRAM_CHAT_ID.split(","):
        c = c.strip()
        if c and "ضع_" not in c:
            CHATS.add(_resolve_chat(c))
    try:
        with open(CHATS_FILE, encoding="utf-8") as f:
            CHATS.update(_resolve_chat(line) for line in f if line.strip())
    except FileNotFoundError:
        pass


def _save_chat(chat_id):
    try:
        with open(CHATS_FILE, "a", encoding="utf-8") as f:
            f.write(chat_id + "\n")
    except Exception:
        pass


def discover_groups():
    """يشوف لو البوت انضاف لقروب أو قناة جديدة، ويضيف رقمها لقائمة الإرسال."""
    global _last_update_id
    if not AUTO_ADD_GROUPS or "ضع_" in TELEGRAM_TOKEN:
        return
    try:
        r = requests.get(f"{TG_API}/getUpdates",
                         params={"offset": _last_update_id + 1, "timeout": 0,
                                 "allowed_updates": '["message","channel_post","my_chat_member"]'},
                         timeout=15).json()
    except Exception as e:
        log("ما قدرت أشيك على القروبات:", e)
        return
    for u in r.get("result", []):
        _last_update_id = max(_last_update_id, u["update_id"])
        box = u.get("my_chat_member") or u.get("message") or u.get("channel_post") or {}
        chat = box.get("chat") or {}
        if chat.get("type") not in ("group", "supergroup", "channel"):
            continue
        cid = str(chat["id"])
        # لو البوت انطرد من القروب نشيله
        status = ((u.get("my_chat_member") or {}).get("new_chat_member") or {}).get("status")
        if status in ("left", "kicked"):
            CHATS.discard(cid)
            continue
        # القروب ترقّى لسوبر قروب وتغيّر رقمه
        new_id = (u.get("message") or {}).get("migrate_to_chat_id")
        if new_id:
            CHATS.discard(cid)
            cid = str(new_id)
        uname = chat.get("username")
        if uname and f"@{uname}" in CHATS:      # نفس القناة محطوطة بالاسم: نبدّله بالرقم بدون إضافة
            CHATS.discard(f"@{uname}")
            CHATS.add(cid)
            continue
        if cid not in CHATS:
            CHATS.add(cid)
            _save_chat(cid)
            title = chat.get("title", "")
            log(f"✅ انضاف قروب/قناة جديد: {title}  الرقم: {cid}")
            log(f"   عشان يثبت دايم، حط هالرقم في TELEGRAM_CHAT_ID على Railway")
            _send_one(cid, "✅ البوت متصل هنا وبيرسل التنبيهات")


def _send_one(chat_id, text):
    try:
        r = requests.post(f"{TG_API}/sendMessage",
                          data={"chat_id": chat_id, "text": text,
                                "disable_web_page_preview": True},
                          timeout=10).json()
        if not r.get("ok"):
            log(f"فشل الإرسال لـ {chat_id}: {r.get('description')}")
            params = r.get("parameters") or {}
            if params.get("migrate_to_chat_id"):   # القروب تغيّر رقمه
                CHATS.discard(chat_id)
                new_id = str(params["migrate_to_chat_id"])
                CHATS.add(new_id)
                _save_chat(new_id)
                _send_one(new_id, text)
    except Exception as e:
        log(f"فشل إرسال التنبيه لـ {chat_id}:", e)


EDUCATION = {
    "sweep": ("📚 للتعلّم - سحب السيولة:\n"
              "تحت كل قاع واضح تتجمع أوامر وقف خسارة. لما السعر ينزل تحتها ويضربها ثم يرجع ويقفل "
              "فوقها، يعني اللي نزّله أخذ السيولة وما قدر يثبّت تحت.\n"
              "يضعف لو رجع السعر وقفل تحت الدعوم، أو كان حجم شمعة السحب ضعيف."),
    "flow": ("📚 للتعلّم - دخول السيولة:\n"
             "الحجم النسبي يقارن تداول اليوم بمعدّله. حجم أضعاف المعتاد مع اختراق قمة وفلوت صغير "
             "يعني طلب غير عادي على سهم قليل المعروض، فالحركة تكون عنيفة.\n"
             "البني ستوك ترتد بسرعة لو ما وراها سبب حقيقي، والسبريد والتذبذب عالي."),
    "rsplit": ("📚 للتعلّم - التجزئة العكسية:\n"
               "الشركة تدمج أسهمها (مثلاً كل 10 أسهم = سهم) عشان ترفع السعر، غالباً لتفادي "
               "الشطب من البورصة. عدد الأسهم يقل والقيمة ما تتغير.\n"
               "كثير منها يكمل نزول بعدها، وأحياناً يتبعها طرح أسهم جديدة."),
    "algo": ("📚 للتعلّم - خوارزميات التقطيع:\n"
             "مئات الصفقات الصغيرة بنفس الحجم بالضبط (سهم، سهم، سهم...) علامة على برنامج "
             "يقسّم أمر كبير على قطع صغيرة عشان ما يحرك السعر ولا يبان.\n"
             "تقدير الشراء/البيع من اتجاه السعر تقريبي، وفي الأسهم الصغيرة ممكن يكون تلاعب أو صانع سوق."),
    "news": ("📚 للتعلّم - الأخبار:\n"
             "التصنيف \"إيجابي\" آلي من كلمات العنوان، مو قراءة للخبر كامل، فاقرأ الخبر قبل أي قرار.\n"
             "كثير من حركة السعر تصير قبل وصول الخبر، وأحياناً السهم ينزل رغم إن الخبر إيجابي."),
}


# ================== القطاع (تقنية، صحة، ...) - يتكتب تحت اسم السهم بالتنبيه ==================
SHOW_SECTOR = True               # True = يكتب قطاع السهم بكل الأقسام
SYMBOL_FIRST = True              # True = رمز السهم أول سطر بالرسالة | False = مثل قبل
SECTOR_FILE = os.path.join(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "."), "sectors.txt")
SECTOR_AR = {
    "technology": "تقنية 💻", "health care": "صحة 🏥", "healthcare": "صحة 🏥",
    "finance": "مالية 🏦", "financial services": "مالية 🏦", "financials": "مالية 🏦",
    "consumer discretionary": "استهلاكية كمالية 🛍️", "consumer cyclical": "استهلاكية كمالية 🛍️",
    "consumer staples": "استهلاكية أساسية 🛒", "consumer defensive": "استهلاكية أساسية 🛒",
    "industrials": "صناعة 🏭", "energy": "طاقة ⛽", "utilities": "مرافق ⚡",
    "real estate": "عقار 🏢", "basic materials": "مواد أساسية ⛏️",
    "telecommunications": "اتصالات 📡", "communication services": "اتصالات وإعلام 📡",
}
SECTOR_ETFS = {"SPY", "QQQ", "SMH", "IWM", "DIA", "SOXX", "XLK", "XLF", "XLE", "XLV", "ARKK", "TQQQ", "SQQQ", "SOXL"}
_SECTORS = {}
_SECTORS_DAY = None
_SECTOR_LOCK = threading.Lock()


def _load_sectors():
    """خريطة السهم ← القطاع من سكرينر ناسداك (ناسداك + نيويورك + أمكس)، مرة باليوم، ومحفوظة بملف."""
    global _SECTORS_DAY
    today = datetime.now().date()
    if _SECTORS_DAY == today and _SECTORS:
        return
    if not _SECTORS:                                  # من الملف أول (لو الموقع ما رد)
        try:
            with open(SECTOR_FILE, encoding="utf-8") as f:
                for line in f:
                    k, _, v = line.rstrip("\n").partition("\t")
                    if k and v:
                        _SECTORS[k] = v
        except FileNotFoundError:
            pass
    got = {}
    for ex in ("nasdaq", "nyse", "amex"):
        url = ("https://api.nasdaq.com/api/screener/stocks"
               f"?tableonly=true&limit=10000&exchange={ex}&download=true")
        try:
            r = requests.get(url, headers={**HEADERS, "Accept": "application/json"}, timeout=30)
            data = r.json().get("data") or {}
            for row in data.get("rows") or (data.get("table") or {}).get("rows") or []:
                sym = str(row.get("symbol", "")).strip().upper()
                sec = str(row.get("sector") or "").strip()
                if sym and sec:
                    got[sym] = sec
        except Exception as e:
            log(f"القطاعات: ما قدرت أجيب {ex.upper()}: {e}")
    if len(got) > 1000:
        _SECTORS.update(got)
        try:
            with open(SECTOR_FILE, "w", encoding="utf-8") as f:
                f.writelines(f"{k}\t{v}\n" for k, v in _SECTORS.items())
        except Exception:
            pass
        log(f"القطاعات: {len(got)} سهم")
    _SECTORS_DAY = today


def sector_of(sym):
    """قطاع السهم بالعربي، أو "" لو ما عرفناه."""
    sym = (sym or "").upper()
    if sym in INDEX_SYMBOLS:
        return "مؤشر 📈"
    if sym in SECTOR_ETFS:
        return "صندوق مؤشرات 📊"
    with _SECTOR_LOCK:
        try:
            _load_sectors()
        except Exception as e:
            log(f"القطاعات: خطأ - {e}")
        sec = _SECTORS.get(sym) or _SECTORS.get(sym.replace(".", "/"))
        if not sec:                                   # احتياطي: ياهو (مرة لكل سهم)
            try:
                import yfinance as yf
                with _YF_LOCK:
                    sec = (yf.Ticker(sym).info or {}).get("sector") or ""
            except Exception:
                sec = ""
            _SECTORS[sym] = sec or "-"
    if not sec or sec == "-":
        return ""
    return SECTOR_AR.get(sec.lower(), sec)


def _with_sector(text, sym):
    """يضيف سطر "القطاع" تحت السطر اللي فيه اسم السهم."""
    sec = sector_of(sym)
    if not sec:
        return text
    lines = text.split("\n")
    tag = f"${sym}"
    for i, ln in enumerate(lines):
        if tag in ln:
            lines.insert(i + 1, f"القطاع: {sec}")
            return "\n".join(lines)
    return f"القطاع: {sec}\n" + text


def sec_tag(sym, sep=" | "):
    """للرسايل اللي فيها أكثر من سهم: يرجع " | القطاع" يتحط بآخر سطر السهم."""
    if not SHOW_SECTOR:
        return ""
    try:
        sec = sector_of(sym)
    except Exception:
        sec = ""
    return f"{sep}{sec}" if sec else ""


def _send_photo_one(chat_id, png, caption=None):
    """يرسل صورة (PNG بايتات) مع نص تحتها لو فيه. يرجع True لو انرسلت."""
    try:
        data = {"chat_id": chat_id}
        if caption:
            data["caption"] = caption
        r = requests.post(f"{TG_API}/sendPhoto", data=data,
                          files={"photo": ("chart.png", png, "image/png")}, timeout=40).json()
        if not r.get("ok"):
            log(f"فشل إرسال الصورة لـ {chat_id}: {r.get('description')}")
            return False
        return True
    except Exception as e:
        log(f"فشل إرسال الصورة لـ {chat_id}:", e)
        return False


def send_telegram(text, kind=None, sym=None, photo=None, head=True):
    if head:                                       # head=False = بدون سطر "للمتابعة" (الرموز أول سطر)
        text = "للمتابعة\n" + text
    if sym and SYMBOL_FIRST:                       # الرمز أول سطر بالرسالة (وينشال سطر "السهم:" المكرر)
        text = f"${sym}\n" + "\n".join(ln for ln in text.split("\n") if ln.strip() != f"السهم: ${sym}")
    if sym and SHOW_SECTOR:
        try:
            text = _with_sector(text, sym)
        except Exception as e:
            log(f"القطاع: {sym}: {e}")
    for code, name in INDEX_NAMES.items():         # $^GSPC ← سباكس S&P 500 (^GSPC)
        text = text.replace(f"${code}", f"{name} ({code})")
    if ADD_EDUCATION and kind in EDUCATION:
        text += "\n\n" + EDUCATION[kind]
    if ADD_DISCLAIMER and "ليست توصية" not in text:
        sep = "\n" if WATCH_CHECK_LINE and text.endswith(WATCH_CHECK_LINE) else "\n\n"
        text += sep + DISCLAIMER
    log(text)
    if "ضع_" in TELEGRAM_TOKEN:
        return  # ما حطيت التوكن، يطبع بالشاشة بس
    fits = len(text.encode("utf-16-le")) // 2 <= 1024      # حد تيليجرام للنص تحت الصورة
    for chat_id in list(CHATS):
        if photo and fits and _send_photo_one(chat_id, photo, text):
            continue                                        # الصورة والتنبيه برسالة وحدة
        if photo:
            _send_photo_one(chat_id, photo)                 # النص طويل: الصورة لحالها وبعدها النص
        _send_one(chat_id, text)


def _session(overnight=None):
    """(بداية تقسيم الشموع، نهاية الجلسة) بالدقايق من منتصف الليل بتوقيت نيويورك.
    نهاية None = 24 ساعة. overnight=True يجبره على 24 ساعة (فريم 4 ساعات)."""
    if overnight is None:
        overnight = GAP_OVERNIGHT
    if overnight:
        return 20 * 60, None          # 24 ساعة، اليوم يبدأ 8 بالليل (نفس تريدنج فيو)
    if GAP_EXTENDED:
        return 4 * 60, 20 * 60
    return 9 * 60 + 30, 16 * 60


def us_market_open(now=None, overnight=None):
    """السوق مفتوح حسب الجلسة المختارة (+ دقايق بعد الإغلاق عشان نلحق نفحص آخر شمعة)."""
    now = now or pd.Timestamp.now(tz=NY)
    if overnight is None:
        overnight = GAP_OVERNIGHT
    wd, m = now.weekday(), now.hour * 60 + now.minute
    # 20 دقيقة: ياهو أحياناً ما يعطي كل شموع الربع ساعة بعد الإغلاق، فالشمعة تعتبر مقفلة
    # بعد 15 دقيقة (only_closed). لو الوقت أقصر من كذا تضيع آخر شمعة باليوم (4-8 بالليل)
    buf = max(max(GAP_SCAN_AFTER_CLOSE_MIN) + 2, 20)
    if overnight:                     # من الأحد 8 بالليل إلى الجمعة 8 بالليل
        if wd == 5:
            return False
        if wd == 6:
            return m >= 20 * 60
        if wd == 4:
            return m <= 20 * 60 + buf
        return True
    if wd >= 5:
        return False
    start, end = _session()
    return start <= m <= end + buf


_YF_LOCK = threading.RLock()   # ياهو ما يتحمل تحميلين بنفس اللحظة من خيطين


def download_batches(tickers, batch_size, **kw):
    """يحمّل بيانات ياهو على دفعات، ويرجع (الرمز، البيانات) لكل سهم."""
    import yfinance as yf

    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i + batch_size]
        try:
            with _YF_LOCK:
                data = yf.download(batch, group_by="ticker", progress=False,
                                   threads=True, auto_adjust=False, **kw)
        except Exception as e:
            log("فشل تحميل دفعة:", e)
            time.sleep(5)
            continue
        for t in batch:
            try:
                if isinstance(data.columns, pd.MultiIndex):
                    if t not in data.columns.get_level_values(0):
                        continue
                    df = data[t]
                else:
                    df = data
                df = df.dropna(subset=["Open", "High", "Low", "Close"])
                if not df.empty:
                    yield t, df
            except Exception:
                continue
        del data
        free_memory()
        time.sleep(1)


# ================== أدوات الشموع والجلسات ==================
def _to_number(x):
    try:
        return float(str(x).replace("$", "").replace(",", "").strip())
    except Exception:
        return 0.0


OHLC = ["Open", "High", "Low", "Close"]


def to_ny(df):
    df = df.dropna(subset=OHLC)
    idx = df.index
    if idx.tz is None:
        idx = idx.tz_localize("UTC")
    return df.set_index(idx.tz_convert(NY))


def _hhmm(m):
    return f"{m // 60:02d}:{m % 60:02d}"


def to_frame(df, minutes, overnight=None, session=None):
    """يحول شموع النص ساعة لشموع أكبر (60 = ساعة، 240 = 4 ساعات) بتوقيت نيويورك،
    بنفس تقسيم تريدنج فيو. كل شمعة معها وقت إغلاقها (end) وعدد الشموع الصغيرة اللي فيها (n).
    overnight=True = 24 ساعة (الشموع تبدأ 8 بالليل)."""
    df = df.dropna(subset=OHLC)
    if df.empty:
        return df
    df = to_ny(df)
    anchor, end_min = session or _session(overnight)   # session = (بداية، نهاية) بالدقايق لو تبي جلسة معينة
    if end_min is not None:                    # مو 24 ساعة: نشيل اللي برا الجلسة
        df = df.between_time(_hhmm(anchor), _hhmm(end_min - 1))
        if df.empty:
            return df
    m = df.index.hour * 60 + df.index.minute
    offset = ((m - anchor) % 1440) % minutes   # كم دقيقة من بداية شمعتها
    start = df.index.floor("min") - pd.to_timedelta(offset, unit="m")
    out = df.groupby(start).agg(Open=("Open", "first"), High=("High", "max"),
                                Low=("Low", "min"), Close=("Close", "last"),
                                n=("Close", "size"))
    ends = []
    for s in out.index:
        e = s + pd.Timedelta(minutes=minutes)
        if end_min is not None:                # آخر شمعة باليوم تقفل مع إغلاق الجلسة
            e = min(e, s.normalize() + pd.Timedelta(minutes=end_min))
        ends.append(e)
    out["end"] = ends
    return out


def only_closed(c, last_bar, now):
    """يخلي الشموع المقفلة بس. الشمعة تعتبر مقفلة لو وقتها خلص، وبياناتها كاملة
    (أو جات بيانات بعدها، أو مر ربع ساعة على إغلاقها)."""
    if c.empty:
        return c
    starts = pd.Series(c.index, index=c.index)
    expected = ((c["end"] - starts).dt.total_seconds() / (GAP_BASE_MIN * 60)).round()
    done = (c["end"] <= now) & ((c["n"] >= expected) | (last_bar >= c["end"])
                                | (now >= c["end"] + pd.Timedelta(minutes=15)))
    return c[done.values]


# ---------- شموع 4 ساعات للجلسة العادية: 9:30-1:30 و 1:30-4:00 نيويورك (يستخدمها سحب الجمعة/الاثنين) ----------
_MKT4H_START, _MKT4H_SPLIT, _MKT4H_END = 9 * 60 + 30, 13 * 60 + 30, 16 * 60


def mkt4h_candles(df):
    """شموع النص ساعة (الجلسة العادية) → شموع 4 ساعات: 9:30-1:30 و 1:30-4:00.
    كل شمعة معها end (وقت الإغلاق) و n (عدد الشموع) و need (المطلوب)."""
    df = to_ny(df)
    if df.empty:
        return df
    m = df.index.hour * 60 + df.index.minute
    df = df[(m >= _MKT4H_START) & (m < _MKT4H_END)]
    if df.empty:
        return df
    m = pd.Series(df.index.hour * 60 + df.index.minute, index=df.index)
    first = m < _MKT4H_SPLIT
    start = df.index.normalize() + pd.to_timedelta(
        first.map({True: _MKT4H_START, False: _MKT4H_SPLIT}).values, unit="m")
    out = df.groupby(start).agg(Open=("Open", "first"), High=("High", "max"),
                                Low=("Low", "min"), Close=("Close", "last"),
                                n=("Close", "size"))
    sm = pd.Series(out.index.hour * 60 + out.index.minute, index=out.index)
    em = sm.map(lambda s: _MKT4H_SPLIT if s == _MKT4H_START else _MKT4H_END)
    out["end"] = out.index.normalize() + pd.to_timedelta(em.values, unit="m")
    out["need"] = ((em - sm) / 30).values
    return out


# ================== قوائم الأسهم (تستخدمها كل الأقسام) ==================
def get_all_us_symbols(include_nyse=True):
    """كل الأسهم المدرجة في ناسداك (وبورصة نيويورك) من ملفات ناسداك الرسمية،
    بدون صناديق ETF ولا وارنتات ولا حقوق ولا وحدات."""
    base = "https://www.nasdaqtrader.com/dynamic/SymDir/"
    bad_name = r"Warrant|Right|Unit|Preferred|Depositary Shares|Notes|Debenture|%"
    symbols = set()

    def read(fname):
        txt = requests.get(base + fname, headers=HEADERS, timeout=30).text
        df = pd.read_csv(io.StringIO(txt), sep="|", dtype=str)
        return df[~df.iloc[:, 0].str.startswith("File Creation", na=False)]

    try:
        n = read("nasdaqlisted.txt")
        n = n[(n["Test Issue"] == "N") & (n["ETF"] == "N")]
        n = n[~n["Security Name"].str.contains(bad_name, case=False, na=False)]
        symbols.update(n["Symbol"].dropna())
    except Exception as e:
        log("ما قدرت أجيب قائمة ناسداك:", e)

    if include_nyse:
        try:
            o = read("otherlisted.txt")
            o = o[(o["Test Issue"] == "N") & (o["ETF"] == "N")]
            o = o[~o["Security Name"].str.contains(bad_name, case=False, na=False)]
            symbols.update(o["ACT Symbol"].dropna())
        except Exception as e:
            log("ما قدرت أجيب قائمة نيويورك:", e)

    return sorted(s for s in symbols if s.isalpha() and len(s) <= 5)


_universe_cache = {}   # (اليوم، مع نيويورك؟) -> {الرمز: (آخر سعر، متوسط الحجم)}


def _universe_stats(include_nyse):
    """آخر سعر ومتوسط الحجم لكل الأسهم. ينحمّل مرة وحدة باليوم ويستخدمه
    الماسح واليومي والشورت كلهم (بدل ما كل واحد يحمّل 3000 سهم لحاله)."""
    key = (pd.Timestamp.now(tz=NY).date(), bool(include_nyse))
    if key in _universe_cache:
        return _universe_cache[key]
    _universe_cache.clear()
    all_syms = get_all_us_symbols(include_nyse)
    log(f"الفلتر: أحمّل أسعار {len(all_syms)} سهم (مرة وحدة باليوم) ...")
    stats = {}
    for t, df in download_batches(all_syms, UNIVERSE_BATCH, period="5d", interval="1d", prepost=False):
        try:
            stats[t] = (float(df["Close"].iloc[-1]), float(df["Volume"].mean()))
        except Exception:
            continue
    _universe_cache[key] = stats
    free_memory()
    return stats


def build_universe(label, min_price, max_price, min_vol, include_nyse):
    """الأسهم اللي آخر سعر لها داخل النطاق وعليها تداول."""
    if ONE_LIST:
        log(f"{label}: {len(WATCH_SYMBOLS)} سهم (القائمة الموحدة)")
        return list(WATCH_SYMBOLS)
    stats = _universe_stats(include_nyse)
    keep = [t for t, (last, avg_vol) in stats.items()
            if min_price <= last <= max_price and avg_vol >= min_vol]
    log(f"{label}: {len(keep)} سهم سعرها {min_price}-{max_price}$ وعليها تداول")
    return keep


# ================== ملفات المرسل (عشان ما يتكرر التنبيه) ==================
def _load_set(path):
    """يقرا ملف المرسل، ويخليه آخر SENT_KEEP_LINES سطر بس عشان ما يكبر للأبد."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return set()
    if len(lines) > SENT_KEEP_LINES:
        lines = lines[-SENT_KEEP_LINES:]
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
        except Exception:
            pass
    return set(lines)


def _append_line(path, line):
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ================== (4ج) نزول الشورت المتاح أكثر من 90% ==================
#   المصدر: ملف Interactive Brokers العام (نفس ChartExchange) يتحدث كل 15 دقيقة
#   + حجم الشورت اليومي آخر 15 يوم من FINRA
def _bz_num(x):
    try:
        return float(str(x).replace("$", "").replace(",", "").strip())
    except Exception:
        return 0.0


BZ_EXCHANGE = {}   # الرمز -> البورصة (لرابط ChartExchange)


def bz_universe():
    """البني ستوك: {الرمز: {"price", "cap"}} من سكرينر ناسداك (ناسداك + نيويورك + أميكس)."""
    out = {}
    for ex in ("nasdaq", "nyse", "amex"):
        url = ("https://api.nasdaq.com/api/screener/stocks"
               f"?tableonly=true&limit=10000&exchange={ex}&download=true")
        try:
            r = requests.get(url, headers={**HEADERS, "Accept": "application/json"}, timeout=40)
            data = r.json().get("data") or {}
            rows = data.get("rows") or (data.get("table") or {}).get("rows") or []
            for row in rows:
                sym = str(row.get("symbol", "")).strip().upper()
                price, cap = _bz_num(row.get("lastsale")), _bz_num(row.get("marketCap"))
                price_ok = (price >= BZ_MIN_PRICE if BZ_MIN_PRICE else price > 0) and \
                           (price <= BZ_MAX_PRICE if BZ_MAX_PRICE else True)
                if ONE_LIST:
                    ok = sym in WATCH_SYMBOLS
                else:
                    ok = (sym.isalpha() and len(sym) <= 5 and price_ok
                          and cap >= BZ_MIN_MARKET_CAP and (cap <= BZ_MAX_MARKET_CAP if BZ_MAX_MARKET_CAP else True))
                if ok:
                    out[sym] = {"price": price, "cap": cap}
                    BZ_EXCHANGE[sym] = ex
        except Exception as e:
            log(f"نزول الشورت: سكرينر {ex} خطأ: {e}")
    return out


def bz_cx_link(sym):
    """رابط صفحة السهم في ChartExchange عشان تتأكد بنفسك."""
    ex = BZ_EXCHANGE.get(sym, "nasdaq")
    return f"https://chartexchange.com/symbol/{ex}-{sym.lower()}/borrow-fee/"


_bz_last_ok = None   # (السيرفر، سلبي؟) اللي نجح آخر مرة — يجربه أول عشان ما يضيع وقت


def bz_download_ibkr():
    """يحمّل ملف IBKR. يبدأ بآخر سيرفر نجح، وبعدها الباقي، ويكتب بالسجل وين وقف بالضبط."""
    import ftplib
    import socket
    global _bz_last_ok
    errors = []
    combos = [(h, p) for h in BZ_FTP_HOSTS for p in (True, False)]
    if _bz_last_ok in combos:
        combos.remove(_bz_last_ok)
        combos.insert(0, _bz_last_ok)
    for host, passive in combos:
        stage = "الاتصال"
        buf = io.BytesIO()
        try:
            ip = socket.gethostbyname(host)
            with ftplib.FTP(timeout=BZ_FTP_TIMEOUT) as ftp:
                ftp.connect(ip, 21)
                stage = "تسجيل الدخول"
                ftp.login("shortstock", "")
                ftp.set_pasv(passive)
                stage = "تحميل الملف"
                ftp.retrbinary("RETR usa.txt", buf.write)
            text = buf.getvalue().decode("utf-8", errors="ignore")
            if text.strip():
                _bz_last_ok = (host, passive)
                if errors:
                    log(f"نزول الشورت: نجح التحميل من {host} ({'سلبي' if passive else 'نشط'}) "
                        f"بعد: {' | '.join(errors)}")
                return text
            errors.append(f"{host}: الملف فاضي")
        except Exception as e:
            errors.append(f"{host} {'سلبي' if passive else 'نشط'} وقف عند {stage}: {e}")
    raise RuntimeError("ما قدرت أحمل ملف IBKR — " + " | ".join(errors))


def bz_parse_ibkr(text):
    """{الرمز: {"available": عدد، "fee": رسوم %}}"""
    out, cols = {}, []
    for line in text.splitlines():
        if not line.strip():
            continue
        if line.startswith("#SYM"):
            cols = [c.strip().lstrip("#").upper() for c in line.split("|")]
            continue
        if line.startswith("#") or not cols:
            continue
        row = dict(zip(cols, line.split("|")))
        sym = row.get("SYM", "").strip().upper()
        raw = row.get("AVAILABLE", "").strip().replace(",", "").lstrip(">")
        try:
            avail = int(float(raw))
        except ValueError:
            continue
        try:
            fee = float(row.get("FEERATE", "") or "nan")
        except ValueError:
            fee = float("nan")
        if sym:
            out[sym] = {"available": avail, "fee": fee}
    return out


_bz_finra = {}


def _bz_finra_day(day):
    if day in _bz_finra:
        return _bz_finra[day]
    try:
        r = requests.get(f"https://cdn.finra.org/equity/regsho/daily/CNMSshvol{day}.txt",
                         headers=HEADERS, timeout=30)
        if r.status_code != 200:
            return None
    except Exception:
        return None
    rows = {}
    for line in r.text.splitlines()[1:]:
        p = line.split("|")
        if len(p) >= 5:
            try:
                rows[p[1].strip().upper()] = (float(p[2]), float(p[4]))
            except ValueError:
                pass
    _bz_finra[day] = rows
    return rows


def bz_short_history_txt(sym):
    out, d, tries = [], datetime.now(ZoneInfo(NY)).date(), 0
    while len(out) < BZ_SHORT_DAYS and tries < BZ_SHORT_DAYS * 2 + 10:
        tries += 1
        if d.weekday() < 5:
            rows = _bz_finra_day(d.strftime("%Y%m%d"))
            if rows is not None and sym in rows:
                sv, tv = rows[sym]
                out.append(f"{d:%m-%d}: {sv:,.0f} من {tv:,.0f} ({(sv / tv * 100 if tv else 0):.0f}%)")
        d -= timedelta(days=1)
    for k in sorted(_bz_finra)[:-(BZ_SHORT_DAYS * 2 + 10)]:
        _bz_finra.pop(k, None)
    if not out:
        return "📊 حجم الشورت آخر 15 يوم: ما فيه بيانات"
    return f"📊 حجم الشورت آخر {len(out)} يوم (FINRA):\n" + "\n".join(out)


def _bz_out(state, kind, text, sym=None):
    """يرسل التنبيه فوراً، أو يحطه بالطابور لو BZ_SPREAD_24H (عشان تنقسم على 24 ساعة)."""
    if not BZ_SPREAD_24H:
        send_telegram(text, sym=sym)
        return
    q = state.get("_queue")
    if not isinstance(q, list):
        q = state["_queue"] = []
    q.append({"k": kind, "t": text, "s": sym, "at": datetime.now(ZoneInfo(LOCAL_TZ)).isoformat()})


def bz_dispatch(state):
    """يرسل تنبيه واحد من الطابور كل (24 ساعة ÷ BZ_MAX_PER_DAY). اللي عمره أكثر من 24 ساعة ينشال."""
    q = state.get("_queue")
    if not BZ_SPREAD_24H or not isinstance(q, list) or not q:
        return
    now = datetime.now(ZoneInfo(LOCAL_TZ))
    q[:] = [x for x in q if now - datetime.fromisoformat(x["at"]) < timedelta(hours=24)]
    gap = timedelta(minutes=24 * 60 / max(BZ_MAX_PER_DAY or 30, 1))
    last = state.get("_last_send")
    if not q or (last and now - datetime.fromisoformat(last) < gap):
        _bz_save_state(state)
        return
    x = q.pop(0)
    send_telegram(x["t"], sym=x["s"])
    state["_last_send"] = now.isoformat()
    _bz_save_state(state)
    log(f"نزول الشورت: انرسل تنبيه من الطابور ({x['s']}) — باقي {len(q)}")


def _bz_load_state():
    try:
        with open(BZ_STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _bz_save_state(state):
    try:
        with open(BZ_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f)
    except Exception as e:
        log(f"نزول الشورت: ما قدرت أحفظ الحالة: {e}")


_bz_last_hash = None   # بصمة آخر ملف IBKR — لو ما تغير ما يعيد الفحص


def bz_check(state, first_run, universe):
    """يرجّع True لو الملف جديد وانفحص، False لو نفس الملف السابق."""
    global _bz_last_hash
    text = bz_download_ibkr()
    h = hash(text)
    if h == _bz_last_hash and not first_run:
        return False          # IBKR ما حدّث الملف للحين
    _bz_last_hash = h
    data = bz_parse_ibkr(text)
    if not data:
        log("نزول الشورت: ملف IBKR فاضي أو صيغته تغيرت")
        return True
    now = datetime.now(ZoneInfo(LOCAL_TZ))
    fee_txt = lambda f: "غير معروف" if f != f else f"{f:.2f}%"
    alerts = 0
    cool = state.get("_cool")
    if not isinstance(cool, dict):
        cool = state["_cool"] = {}

    daily = state.get("_daily")
    today_s = now.strftime("%Y-%m-%d")
    if not isinstance(daily, dict) or daily.get("day") != today_s:
        daily = state["_daily"] = {"day": today_s, "n": 0}

    def cooled(kind, sym):
        """True = مسموح ينبه: ما نبه على هالسهم خلال BZ_COOLDOWN_DAYS، وما وصل حد اليوم BZ_MAX_PER_DAY."""
        if BZ_MAX_PER_DAY and daily["n"] >= BZ_MAX_PER_DAY:
            return False
        key = f"{kind}:{sym}"
        last = cool.get(key)
        if BZ_COOLDOWN_DAYS and last and now - datetime.fromisoformat(last) < timedelta(days=BZ_COOLDOWN_DAYS):
            return False
        cool[key] = now.isoformat()
        daily["n"] += 1
        return True

    for k in [k for k, v in cool.items() if now - datetime.fromisoformat(v) >= timedelta(days=max(BZ_COOLDOWN_DAYS, 1))]:
        del cool[k]
    hist = state.get("_hist")              # {الرمز: {اليوم: أعلى متاح باليوم}} لآخر BZ_DROP_DAYS يوم
    if not isinstance(hist, dict):
        hist = state["_hist"] = {}
    cutoff = (now - timedelta(days=BZ_DROP_DAYS)).strftime("%Y-%m-%d")
    for s_ in list(hist):
        h_ = {d: v for d, v in hist[s_].items() if d >= cutoff}
        if h_:
            hist[s_] = h_
        else:
            del hist[s_]
    for sym, u in universe.items():
        info = data.get(sym)
        prev = state.get(sym)
        if info is None:
            # IBKR يشيل السهم من الملف لما يخلص المتاح = صفر (نفس ملاحظة ChartExchange)
            if not isinstance(prev, (int, float)) or prev <= 0:
                continue
            info = {"available": 0, "fee": float("nan")}
        avail = info["available"]
        # ---- نزول الشورت المتاح عن أعلى رقم بالشهر ----
        sh = hist.get(sym) or {}
        if sh and not first_run and avail > 0:
            top_day, top = max(sh.items(), key=lambda x: x[1])
            drop = (1 - avail / top) * 100 if top else 0
            was_above = prev is None or prev >= top * (1 - BZ_DROP_PCT / 100)   # يعني توه نزل تحت الحد
            if top >= BZ_DROP_MIN_HIGH and drop > BZ_DROP_PCT and was_above and cooled("drop", sym):
                _bz_out(state, "main",
                    f"📉 نزول الشورت المتاح - ${sym}\n"
                    f"نزل {drop:.0f}% من أعلى رقم خلال آخر شهر\n"
                    f"الأسهم المتاحة للشورت: {avail:,}\n"
                    f"أعلى رقم بالشهر: {top:,} (يوم {top_day})\n"
                    f"السعر: {u['price']:.2f}$\n"
                    f"القيمة السوقية: {u['cap'] / 1e6:.1f} مليون$\n"
                    f"رسوم الاستلاف: {fee_txt(info['fee'])}\n"
                    f"الوقت: {now:%Y-%m-%d %H:%M} (توقيتك)\n"
                    f"المصدر: Interactive Brokers\n"
                    f"{bz_cx_link(sym)}\n\n"
                    f"{bz_short_history_txt(sym)}", sym=sym)
                alerts += 1
                time.sleep(0.5)
        if avail > sh.get(today_s, -1):
            hist.setdefault(sym, {})[today_s] = avail
        state[sym] = avail
    _bz_save_state(state)
    log(f"[{datetime.now():%H:%M}] نزول الشورت: {len(universe)} سهم — تنبيهات {alerts}")
    return True


def bz_run_forever():
    price_txt = (f"{BZ_MIN_PRICE:g}-{BZ_MAX_PRICE:g}$" if BZ_MAX_PRICE
                 else f"السعر {BZ_MIN_PRICE:g}$ وفوق" if BZ_MIN_PRICE else "بدون حد سعر")
    log(f"نزول الشورت: بدأ — {price_txt}، " + (f"قيمة سوقية {BZ_MIN_MARKET_CAP / 1e6:g}-{BZ_MAX_MARKET_CAP / 1e6:g} مليون " if BZ_MAX_MARKET_CAP else "بدون حد للقيمة السوقية ")
        + 
        f"— كل {BZ_EVERY_MIN} دقيقة")
    state = _bz_load_state()
    first_run = not state      # أول مرة يسجل الوضع بس عشان ما يجيك سيل تنبيهات
    universe, uni_last = {}, 0.0
    last_ok, warned = time.time(), False
    while True:
        try:
            if not universe or time.time() - uni_last >= BZ_UNIVERSE_EVERY_MIN * 60:
                fresh = bz_universe()
                if fresh:
                    universe, uni_last = fresh, time.time()
                    log(f"نزول الشورت: قائمة البني ستوك {len(universe)} سهم")
            if universe:
                bz_check(state, first_run, universe)
                first_run = False
                bz_dispatch(state)
                if warned:
                    send_telegram("✅ تنبيه نزول الشورت رجع يشتغل (ملف IBKR يتحمل طبيعي)")
                last_ok, warned = time.time(), False
        except Exception as e:
            log(f"نزول الشورت: خطأ {e}")
            if time.time() - last_ok >= BZ_WARN_AFTER_MIN * 60 and not warned:   # ساعة بدون بيانات = يعلمك
                warned = True
                send_telegram("⚠️ تنبيه نزول الشورت واقف: ما قدر يحمل ملف IBKR من ساعة.\n"
                              f"آخر خطأ: {str(e)[:300]}")
        time.sleep(BZ_EVERY_MIN * 60)


# ================== طلبات بيانات ألباكا (تستخدمها سلسلة العقود) ==================
def _alpaca_data_get(path, params=None):
    r = requests.get("https://data.alpaca.markets" + path, params=params or {}, timeout=20,
                     headers={"APCA-API-KEY-ID": ALPACA_KEY, "APCA-API-SECRET-KEY": ALPACA_SECRET,
                              "Accept": "application/json"})
    r.raise_for_status()
    return r.json()


# ================== (1ك-2) سحب سيولة دعم ومقاومة الأسبوع السابق - فريم 4 ساعات ==================


def _week_start(ts):
    """بداية الأسبوع (الاثنين 00:00 بتوقيت نيويورك)."""
    ts = pd.Timestamp(ts)
    return ts.normalize() - pd.Timedelta(days=ts.weekday())


def _prev_week_rows(daily, prev_wk, this_wk):
    d = [pd.Timestamp(i).date() for i in daily.index]
    return daily[[(prev_wk <= x < this_wk) for x in d]]


def prev_week_low(daily, prev_wk, this_wk):
    """(قاع الأسبوع السابق، يومه) من الشموع اليومية، أو None."""
    pw = _prev_week_rows(daily, prev_wk, this_wk)
    if pw.empty:
        return None
    lows = pw["Low"].astype(float)
    return float(lows.min()), pd.Timestamp(lows.idxmin()).date()


def prev_week_high(daily, prev_wk, this_wk):
    """(قمة الأسبوع السابق، يومها) من الشموع اليومية، أو None."""
    pw = _prev_week_rows(daily, prev_wk, this_wk)
    if pw.empty:
        return None
    highs = pw["High"].astype(float)
    return float(highs.max()), pd.Timestamp(highs.idxmax()).date()


def prev_week_ext_levels(df, week_start):
    """قاع وقمة الأسبوع السابق من شموع 15 دقيقة على الجلسة الممتدة (بري + ماركت + أفتر،
    4 الفجر - 8 بالليل نيويورك) بدون الجلسة الليلية.
    يرجع {"low": (القاع، يومه), "high": (القمة، يومها)} أو None."""
    prev = week_start - pd.Timedelta(days=7)
    pw = df[(df.index >= prev) & (df.index < week_start)]
    if pw.empty:
        return None
    pw = pw.between_time("04:00", "19:59")
    if pw.empty:
        return None
    lows, highs = pw["Low"].astype(float), pw["High"].astype(float)
    return {"low": (float(lows.min()), pd.Timestamp(lows.idxmin()).date()),
            "high": (float(highs.max()), pd.Timestamp(highs.idxmax()).date())}


def check_pwl_1h(c1h, support, week_start, wick_only=False):
    """الدعم: آخر شمعة ساعة (من هالأسبوع) ذيلها نزل تحت قاع الأسبوع السابق وقفلت فوقه.
    wick_only=True: الافتتاح بعد لازم فوق الدعم (الذيل بس اللي نزل تحته)."""
    c1h = c1h[c1h.index >= week_start]
    if c1h.empty:
        return None
    last = c1h.iloc[-1]
    low, close = float(last["Low"]), float(last["Close"])
    if not (low < support < close):
        return None
    if wick_only and not float(last["Open"]) > support:
        return None
    before = c1h.iloc[:-1]
    closes_beyond = int((before["Close"] < support).sum()) if len(before) else 0
    return {"open": float(last["Open"]), "high": float(last["High"]), "low": low, "close": close,
            "depth": (support - low) / support * 100, "start": c1h.index[-1], "end": last["end"],
            "closes_beyond": closes_beyond,
            "first_touch": bool(before.empty or before["Low"].min() >= support)}


def check_pwh_1h(c1h, resistance, week_start, wick_only=False):
    """المقاومة: آخر شمعة ساعة (من هالأسبوع) ذيلها طلع فوق قمة الأسبوع السابق وقفلت تحتها.
    wick_only=True: الافتتاح بعد لازم تحت المقاومة (الذيل بس اللي طلع فوقها)."""
    c1h = c1h[c1h.index >= week_start]
    if c1h.empty:
        return None
    last = c1h.iloc[-1]
    high, close = float(last["High"]), float(last["Close"])
    if not (close < resistance < high):
        return None
    if wick_only and not float(last["Open"]) < resistance:
        return None
    before = c1h.iloc[:-1]
    closes_beyond = int((before["Close"] > resistance).sum()) if len(before) else 0
    return {"open": float(last["Open"]), "high": high, "low": float(last["Low"]), "close": close,
            "depth": (high - resistance) / resistance * 100, "start": c1h.index[-1], "end": last["end"],
            "closes_beyond": closes_beyond,
            "first_touch": bool(before.empty or before["High"].max() <= resistance)}


def confirm_sweep(c, lvl, start, side, wick_only=False):
    """تأكيد سحب السيولة (SWEEP_CONFIRM): التنبيه ما يطلع على شمعة السحب نفسها، يطلع على شمعة التأكيد بعدها.
    الدعم (low): شمعة سحب ذيلها بس تحت الدعم (الافتتاح والإغلاق فوقه)، وبعدها شمعة:
        - تقفل فوق قمة شمعة السحب، أو
        - ترجع تختبر الدعم (توصل له أو قريب منه بـ SWEEP_RETEST_PCT) وما تكسر قاع شمعة السحب
    المقاومة (high): شمعة سحب ذيلها فوق المقاومة وإغلاقها تحتها، وبعدها شمعة ترجع تختبر المقاومة
        وما تكسر قمة شمعة السحب ولا تقفل فوق المقاومة
    يلغي النموذج: (دعم) شمعة تكسر قاع شمعة السحب أو تقفل تحت الدعم | (مقاومة) شمعة تكسر قمة شمعة السحب أو تقفل فوق المقاومة
    التنبيه بس لو آخر شمعة مقفلة هي أول شمعة تأكيد. يرجع نفس بيانات شمعة السحب + بيانات التأكيد، أو None."""
    c = c[c.index >= start]
    n = len(c)
    if n < 2:
        return None
    tol = lvl * SWEEP_RETEST_PCT / 100
    fn = check_pwl_1h if side == "low" else check_pwh_1h
    wo = True if side == "low" else wick_only          # الدعم: الذيل بس تحت الدعم
    for si in range(n - 2, -1, -1):                    # آخر شمعة سحب قبل آخر شمعة
        r = fn(c.iloc[:si + 1], lvl, start, wick_only=wo)
        if not r:
            continue
        s_hi, s_lo = r["high"], r["low"]
        for j in range(si + 1, n):
            k = c.iloc[j]
            kh, kl, kc = float(k["High"]), float(k["Low"]), float(k["Close"])
            how = None
            if side == "low":
                if kl < s_lo or kc < lvl:
                    return None                         # كسر قاع شمعة السحب أو قفل تحت الدعم
                if kc > s_hi:
                    how = f"شمعة قفلت فوق قمة شمعة السحب ({kc:.2f} > {s_hi:.2f})"
                elif kl <= lvl + tol:
                    how = (f"إعادة اختبار الدعم: نزلت لـ {kl:.2f} وما كسرت قاع شمعة السحب {s_lo:.2f}"
                           f" وقفلت فوق الدعم ({kc:.2f})")
            else:
                if kh > s_hi or kc > lvl:
                    return None                         # كسر قمة شمعة السحب أو قفل فوق المقاومة
                if kh >= lvl - tol:
                    how = (f"إعادة اختبار المقاومة: طلعت لـ {kh:.2f} وما كسرت قمة شمعة السحب {s_hi:.2f}"
                           f" وقفلت تحت المقاومة ({kc:.2f})")
            if how:
                if j != n - 1:
                    return None                         # التأكيد صار قبل (انرسل أو فات وقته)
                r = dict(r)
                r.update({"sweep_start": r["start"], "start": c.index[j], "end": k["end"],
                          "confirm_close": kc, "confirm_txt": "✅ التأكيد: " + how})
                return r
        return None
    return None


def sweep_check(side, wick_only=False):
    """الدالة اللي تفحص السحب لكل جهة: مع التأكيد (SWEEP_CONFIRM) أو شمعة السحب لحالها مثل قبل."""
    if SWEEP_CONFIRM:
        return lambda c, lvl, start, wick_only=wick_only: confirm_sweep(c, lvl, start, side, wick_only)
    return check_pwl_1h if side == "low" else check_pwh_1h


def _sweep_time_line(r):
    """سطر وقت شمعة السحب لما التنبيه على شمعة التأكيد."""
    if r.get("sweep_start") is None:
        return ""
    t0 = pd.Timestamp(r["sweep_start"]).tz_convert(LOCAL_TZ)
    return f"\n{r['confirm_txt']}\nشمعة السحب: {t0:%Y-%m-%d %H:%M} (توقيتك)"


def _pwl_message(t, side, lvl, lvl_day, r, frame="فريم ساعة", trade=False):
    t1 = pd.Timestamp(r["start"]).tz_convert(LOCAL_TZ)
    color = "خضراء 🟢" if r["close"] > r["open"] else "حمراء 🔴"
    if side == "low":
        head = f"💧 سحب سيولة دعم الأسبوع السابق — {frame}"
        lvl_line = f"الدعم (قاع الأسبوع السابق): {lvl:.2f}  (يوم {lvl_day})"
        wick = f"ذيل الشمعة نزل لـ {r['low']:.2f}  (-{r['depth']:.2f}% تحت الدعم)"
        close = f"الافتتاح {r['open']:.2f} والإغلاق {r['close']:.2f} فوق الدعم | الشمعة {color}"
        word, where = "الدعم", "تحت"
    else:
        head = f"🔻 سحب سيولة مقاومة الأسبوع السابق — {frame}"
        lvl_line = f"المقاومة (قمة الأسبوع السابق): {lvl:.2f}  (يوم {lvl_day})"
        wick = f"ذيل الشمعة طلع لـ {r['high']:.2f}  (+{r['depth']:.2f}% فوق المقاومة)"
        close = f"الافتتاح {r['open']:.2f} والإغلاق {r['close']:.2f} تحت المقاومة | الشمعة {color}"
        word, where = "المقاومة", "فوق"
    note = (f"أول لمس {'للدعم' if side == 'low' else 'للمقاومة'} هالأسبوع" if r["first_touch"] else
            f"قبلها {r['closes_beyond']} شمعة قفلت {where} {word}" if r["closes_beyond"] else
            f"لمس {word} قبل وما قفل {where}{'ه' if side == 'low' else 'ها'}")
    trade_lines = ""
    if trade:
        if side == "low":
            trade_lines = (f"\n📈 الاتجاه المتوقع: كول (صعود)"
                           f"\n🛑 الوقف: الدعم {lvl:.2f}")
        else:
            trade_lines = (f"\n📉 الاتجاه المتوقع: بوت (هبوط)"
                           f"\n🛑 الوقف: المقاومة {lvl:.2f}")
    return (f"{head}\nالسهم: ${t}\n{lvl_line}\n{wick}\n{close}\n{note}"
            f"{trade_lines}{_sweep_time_line(r)}\n"
            f"{'وقت شمعة التأكيد' if r.get('sweep_start') is not None else 'وقت الشمعة'}: "
            f"{t1:%Y-%m-%d %H:%M} (توقيتك)")


def scan_pwl_4h(symbols, sent):
    """(1ك-2) فريم 4 ساعات: سحب الدعم (ENABLE_PWL_4H) والمقاومة (ENABLE_PWH_4H) — تنبيه واحد لكل جهة بالأسبوع."""
    now = pd.Timestamp.now(tz=NY)
    wk0 = _week_start(now)
    checks4h = []
    if ENABLE_PWL_4H or (ENABLE_WKOPT and not WKOPT_PUT_ONLY):
        checks4h.append(("low", "pwl4h", sweep_check("low", PW4H_WICK_ONLY), ENABLE_PWL_4H))
    if ENABLE_PWH_4H or ENABLE_WKOPT:
        checks4h.append(("high", "pwh4h", sweep_check("high", PW4H_WICK_ONLY), ENABLE_PWH_4H))
    if not checks4h and not ENABLE_PD4H and not ENABLE_PDH1H and not ENABLE_PDL1H:
        return
    hits = 0
    for t, df in download_batches(symbols, 100, period="15d", interval=f"{GAP_BASE_MIN}m",
                                  prepost=True):   # 15 يوم عشان الأسبوع السابق كامل + بري وأفتر
        try:
            df = to_ny(df)[OHLC]
            if df.empty:
                continue
            if ENABLE_PD4H and t in PD4H_SYMBOLS:   # (13) سحب اليوم السابق - أسهمه بس، نفس البيانات
                try:
                    hits += pd4h_check(t, df, now, sent)
                except Exception as e:
                    log(f"سحب اليوم السابق: {t}: خطأ - {e}")
            if (ENABLE_PDH1H or ENABLE_PDL1H) and t in PD4H_SYMBOLS:  # (15) سحب مقاومة اليوم السابق - فريم ساعة
                try:
                    hits += pdh1h_check(t, df, now, sent)
                except Exception as e:
                    log(f"سحب مقاومة أمس (ساعة): {t}: خطأ - {e}")
            if t not in WATCH_SYMBOLS:              # سهم من قائمة (13) بس: باقي الأقسام ما تفحصه
                continue
            # مستويات الأسبوع السابق من البري + الماركت + الأفتر (بدون الليلي)
            lv4 = prev_week_ext_levels(df, wk0)
            if not lv4:
                continue
            # overnight=False: شموع 4-8، 8-12، 12-4، 4-8 (بري + ماركت + أفتر) بدون الليلي
            c4h = only_closed(to_frame(df, 240, overnight=False), df.index.max(), now)
            # (12) فريم 6 ساعات (WKOPT_FRAME_MIN): 4-10، 10-4، 4-8 نيويورك بدون الليلي
            cwk = (only_closed(to_frame(df, WKOPT_FRAME_MIN, overnight=False), df.index.max(), now)
                   if ENABLE_WKOPT else c4h)
            spot = float(df["Close"].iloc[-1])
            wk_key = f"{t}-wkopt-{wk0:%Y%m%d}"     # (12) تنبيه واحد لكل سهم بالأسبوع (لو WKOPT_REALERT = False)
            for side, tag, fn, old_on in checks4h:
                if market_blocks(side, now):            # فلتر اتجاه السوق (14)
                    continue
                # WKOPT_REALERT: كل شمعة سحب جديدة (إعادة اختبار بنفس السلوك) = تنبيه جديد
                side_pref = f"{t}-wkopt-{side}-{wk0:%Y%m%d}-"
                lvl, lvl_day = lv4[side]
                # ---- (12) الأسهم من 100$ إلى 350$: تنبيه واحد بالأسبوع + العقد (البوت بس لو WKOPT_PUT_ONLY) ----
                if wkopt_in_range(spot) and (side == "high" or not WKOPT_PUT_ONLY):
                    r = fn(cwk, lvl, wk0, wick_only=PW4H_WICK_ONLY)
                    if not r or (now - pd.Timestamp(r["end"])).total_seconds() / 60 > PWL_MAX_ALERT_DELAY_MIN:
                        continue
                    if WKOPT_REALERT:
                        key = f"{side_pref}{pd.Timestamp(r['start']):%m%d%H%M}"
                        if key in sent:
                            continue
                        nth = sum(1 for k in sent if k.startswith(side_pref)) + 1
                    else:
                        if wk_key in sent:
                            break
                        key, nth = wk_key, 1
                    put = side == "high"
                    opt = None
                    try:
                        if t not in INDEX_SYMBOLS:      # المؤشرات (سباكس) ما لها عقود: تنبيه بدون عقد
                            opt = wkopt_pick_option(t, r["close"], put)
                    except Exception as e:
                        log(f"سحب أسبوعي + عقد: {t}: العقد: {e}")
                    if opt is None and WKOPT_REQUIRE_CONTRACT:
                        log(f"سحب أسبوعي + عقد: {t}: فيه سحب {'مقاومة' if put else 'دعم'} بس ما فيه عقد بالشروط")
                        continue
                    sent.add(key)
                    _append_line(GAP_SENT_FILE, key)
                    hits += 1
                    send_telegram(with_gamma(wkopt_message(t, side, lvl, lvl_day, r, opt, nth), t, r["close"]),
                                  kind="sweep", sym=t)
                    if WKOPT_REALERT:
                        continue
                    break
                r = fn(c4h, lvl, wk0, wick_only=PW4H_WICK_ONLY)
                if not r or (now - pd.Timestamp(r["end"])).total_seconds() / 60 > PWL_MAX_ALERT_DELAY_MIN:
                    continue
                key = f"{t}-{tag}-{wk0:%Y%m%d}"
                if old_on and key not in sent:
                    sent.add(key)
                    _append_line(GAP_SENT_FILE, key)
                    hits += 1
                    send_telegram(with_gamma(_pwl_message(t, side, lvl, lvl_day, r, frame="فريم 4 ساعات",
                                                          trade=True), t, r["close"]),
                                  kind="sweep", sym=t)
        except Exception as e:
            log(f"سحب دعم/مقاومة الأسبوع السابق: {t}: خطأ - {e}")
    free_memory()
    if hits:
        log(f"[{datetime.now():%H:%M}] سحب دعم/مقاومة الأسبوع السابق (4 ساعات): {hits} تنبيه")


# ================== فلتر اتجاه السوق (من تنبيه القسم 14) ==================
_SMT_TODAY = {}                  # تاريخ اليوم (نيويورك) YYYYMMDD -> "bear"/"bull" (آخر تنبيه للقسم 14)


def _smt_today_load():
    """بعد إعادة التشغيل: يرجع اتجاه اليوم من ملف تنبيهات (14). لو فيه الاثنين ما يعرف الأخير فيتركه."""
    for k in _load_set(SMT_SENT_FILE):
        try:
            _, side, day = k.split("-")
        except ValueError:
            continue
        _SMT_TODAY[day] = None if _SMT_TODAY.get(day, side) != side else side


def market_blocks(side, now=None):
    """True = لا ترسل: "low" (كول) و(14) قال هابط اليوم، أو "high" (بوت) و(14) قال صاعد اليوم."""
    if not MARKET_FILTER:
        return False
    now = now or pd.Timestamp.now(tz=NY)
    d = _SMT_TODAY.get(f"{pd.Timestamp(now).tz_convert(NY):%Y%m%d}")
    return (side == "low" and d == "bear") or (side == "high" and d == "bull")


# ================== (13) سحب سيولة دعم ومقاومة اليوم السابق - فريم 4 ساعات ==================
def prev_day_ext_levels(df, day_start):
    """قاع وقمة آخر يوم تداول قبل day_start (بري + ماركت + أفتر، بدون الليلي).
    يرجع {"low": (القاع، اليوم), "high": (القمة، اليوم)} أو None."""
    pw = df[df.index < day_start]
    if pw.empty:
        return None
    pw = pw.between_time("04:00", "19:59")
    if pw.empty:
        return None
    last_day = pw.index[-1].normalize()
    pd_ = pw[pw.index >= last_day]
    lows, highs = pd_["Low"].astype(float), pd_["High"].astype(float)
    d = last_day.date()
    return {"low": (float(lows.min()), d), "high": (float(highs.max()), d)}


def _pd4h_message(t, side, lvl, r, pd_lv, pw_lv):
    t1 = pd.Timestamp(r["start"]).tz_convert(LOCAL_TZ)
    t2 = pd.Timestamp(r["end"]).tz_convert(LOCAL_TZ)
    color = "خضراء 🟢" if r["close"] > r["open"] else "حمراء 🔴"
    if side == "low":
        head = "💧 سحب سيولة دعم اليوم السابق — فريم 4 ساعات"
        wick = f"ذيل الشمعة نزل لـ {r['low']:.2f}  (-{r['depth']:.2f}% تحت الدعم)"
        close = f"الإغلاق {r['close']:.2f} رجع فوق الدعم | الشمعة {color}"
        trade = ("📈 الاتجاه المتوقع: كول (صعود)\n"
                 f"❌ كسر قاع شمعة السحب {r['low']:.2f} يفشل الاتجاه")
        note = ("أول لمس للدعم اليوم" if r["first_touch"] else
                f"قبلها {r['closes_beyond']} شمعة قفلت تحت الدعم" if r["closes_beyond"] else
                "لمس الدعم قبل وما قفل تحته")
    else:
        head = "🔻 سحب سيولة مقاومة اليوم السابق — فريم 4 ساعات"
        wick = f"ذيل الشمعة طلع لـ {r['high']:.2f}  (+{r['depth']:.2f}% فوق المقاومة)"
        close = f"الإغلاق {r['close']:.2f} رجع تحت المقاومة | الشمعة {color}"
        trade = ("📉 الاتجاه المتوقع: بوت (هبوط)\n"
                 f"❌ كسر قمة شمعة السحب {r['high']:.2f} يفشل الاتجاه")
        note = ("أول لمس للمقاومة اليوم" if r["first_touch"] else
                f"قبلها {r['closes_beyond']} شمعة قفلت فوق المقاومة" if r["closes_beyond"] else
                "لمس المقاومة قبل وما قفل فوقها")
    px = r["close"]
    dist = lambda x: f"{(x / px - 1) * 100:+.1f}%"
    (pdl, pdd), (pdh, _) = pd_lv["low"], pd_lv["high"]
    levels = ["📊 المستويات:",
              f"مقاومة اليوم السابق ({pdd:%m-%d}): {pdh:.2f} ({dist(pdh)})",
              f"دعم اليوم السابق ({pdd:%m-%d}): {pdl:.2f} ({dist(pdl)})"]
    if pw_lv:      # كول ← مقاومة الأسبوع (الهدف فوق) | بوت ← دعم الأسبوع (الهدف تحت)
        if side == "low":
            pwh, pwhd = pw_lv["high"]
            levels.append(f"مقاومة الأسبوع السابق ({pwhd:%m-%d}): {pwh:.2f} ({dist(pwh)})")
        else:
            pwl, pwld = pw_lv["low"]
            levels.append(f"دعم الأسبوع السابق ({pwld:%m-%d}): {pwl:.2f} ({dist(pwl)})")
    return (f"{head}\nالسهم: ${t}\n"
            f"{'الدعم (قاع' if side == 'low' else 'المقاومة (قمة'} اليوم السابق): {lvl:.2f}\n"
            f"{wick}\n{close}\n{note}{_sweep_time_line(r)}\n"
            f"{'شمعة التأكيد' if r.get('sweep_start') is not None else 'الشمعة'}: "
            f"{t1:%H:%M} - {t2:%H:%M} (توقيتك)\n\n"
            + "\n".join(levels) + f"\n\n{trade}")


def pd4h_check(t, df, now, sent):
    """يفحص سهم واحد (df = شموع 15 دقيقة نيويورك) ويرسل التنبيه لو تحقق. يرجع عدد التنبيهات."""
    day0 = now.normalize()
    pd_lv = prev_day_ext_levels(df, day0)
    if not pd_lv:
        return 0
    pw_lv = prev_week_ext_levels(df, _week_start(now))
    c4h = only_closed(to_frame(df, 240, overnight=False), df.index.max(), now)
    hits = 0
    for side, fn in (("low", sweep_check("low", PD4H_WICK_ONLY)), ("high", sweep_check("high", PD4H_WICK_ONLY))):
        if market_blocks(side, now):                     # فلتر اتجاه السوق (14)
            continue
        lvl = pd_lv[side][0]
        r = fn(c4h, lvl, day0, wick_only=PD4H_WICK_ONLY)       # شموع اليوم بس
        if not r or (now - pd.Timestamp(r["end"])).total_seconds() / 60 > PWL_MAX_ALERT_DELAY_MIN:
            continue
        key = f"{t}-pd4h-{side}-w{_week_start(now):%Y%m%d}"   # تنبيه واحد بالأسبوع لكل جهة (دعم / مقاومة)
        if key in sent:
            continue
        sent.add(key)
        _append_line(GAP_SENT_FILE, key)
        hits += 1
        send_telegram(with_gamma(_pd4h_message(t, side, lvl, r, pd_lv, pw_lv), t, r["close"])
                      + "\n\n" + PD4H_CHECK_LINE, kind="sweep", sym=t)
    return hits


# ================== (15) سحب مقاومة اليوم السابق - فريم ساعة - السهم هابط ==================
def prev_day_close(df, day_start):
    """إغلاق آخر يوم تداول قبل day_start (إغلاق الجلسة الرسمية 4 العصر نيويورك) أو None."""
    pw = df[df.index < day_start].between_time("09:30", "15:59")
    if pw.empty:
        return None
    return float(pw["Close"].iloc[-1])


def _pdh1h_message(t, side, lvl, lvl_day, pdc, r):
    t1 = pd.Timestamp(r["start"]).tz_convert(LOCAL_TZ)
    t2 = pd.Timestamp(r["end"]).tz_convert(LOCAL_TZ)
    chg = f"{(r['close'] / pdc - 1) * 100:+.1f}%"
    if side == "high":
        return (f"🔻 سحب سيولة مقاومة اليوم السابق — فريم ساعة\n"
                f"السهم: ${t}\n"
                f"المقاومة (قمة {lvl_day:%m-%d}): {lvl:.2f}\n"
                f"ذيل الشمعة طلع لـ {r['high']:.2f} (+{r['depth']:.2f}%) وقفلت تحت المقاومة على {r['close']:.2f}\n"
                f"السهم هابط: تحت إغلاق أمس {pdc:.2f} ({chg})\n"
                f"الشمعة: {t1:%H:%M} - {t2:%H:%M} (توقيتك)\n\n"
                f"📉 الاتجاه المتوقع: هابط\n"
                f"❌ كسر قمة شمعة السحب {r['high']:.2f} يفشل الاتجاه")
    return (f"💧 سحب سيولة دعم اليوم السابق — فريم ساعة\n"
            f"السهم: ${t}\n"
            f"الدعم (قاع {lvl_day:%m-%d}): {lvl:.2f}\n"
            f"ذيل الشمعة نزل لـ {r['low']:.2f} (-{r['depth']:.2f}%) وقفلت فوق الدعم على {r['close']:.2f}\n"
            f"السهم صاعد: فوق إغلاق أمس {pdc:.2f} ({chg})\n"
            f"الشمعة: {t1:%H:%M} - {t2:%H:%M} (توقيتك)\n\n"
            f"📈 الاتجاه المتوقع: صاعد\n"
            f"❌ كسر قاع شمعة السحب {r['low']:.2f} يفشل الاتجاه")


def pdh1h_check(t, df, now, sent):
    """يفحص سهم واحد (df = شموع 15 دقيقة نيويورك) على الجهتين. يرجع عدد التنبيهات.
    مقاومة: ذيل فوق قمة أمس وإغلاق تحتها، والإغلاق تحت إغلاق أمس (هابط).
    دعم: ذيل تحت قاع أمس وإغلاق فوقه، والإغلاق فوق إغلاق أمس (صاعد)."""
    day0 = now.normalize()
    lv = prev_day_ext_levels(df, day0)
    pdc = prev_day_close(df, day0)
    if not lv or not pdc:
        return 0
    c1h = only_closed(to_frame(df, 60, overnight=False), df.index.max(), now)
    hits = 0
    for side, on, fn in (("high", ENABLE_PDH1H, check_pwh_1h), ("low", ENABLE_PDL1H, check_pwl_1h)):
        if not on or market_blocks(side, now):           # فلتر اتجاه السوق (14)
            continue
        lvl, lvl_day = lv[side]
        r = fn(c1h, lvl, day0)                           # آخر شمعة: ذيل برا المستوى وإغلاق داخله
        if not r:
            continue
        if (side == "high" and r["close"] >= pdc) or (side == "low" and r["close"] <= pdc):
            continue                                     # الاتجاه مو مطابق (هابط للمقاومة / صاعد للدعم)
        if (now - pd.Timestamp(r["end"])).total_seconds() / 60 > PWL_MAX_ALERT_DELAY_MIN:
            continue
        key = f"{t}-pd{'h' if side == 'high' else 'l'}1h-{day0:%Y%m%d}"   # تنبيه واحد باليوم لكل سهم لكل جهة
        if key in sent:
            continue
        sent.add(key)
        _append_line(GAP_SENT_FILE, key)
        msg = with_gamma(_pdh1h_message(t, side, lvl, lvl_day, pdc, r), t, r["close"])
        if WATCH_CHECK_LINE:
            msg += "\n\n" + WATCH_CHECK_LINE
        send_telegram(msg, kind="sweep", sym=t, head=WATCH_HEAD)
        hits += 1
    return hits


def pdh1h_self_test():
    """python short_bot.py --pdh1htest — يجرب (15) بدون نت."""
    global with_gamma, send_telegram
    ny = ZoneInfo(NY)
    m15 = pd.date_range("2026-11-19 04:00", "2026-11-20 11:45", freq="15min", tz=ny)
    m15 = m15[(m15.hour >= 4) & (m15.hour < 20)]
    df = pd.DataFrame({"Open": 283.0, "High": 283.5, "Low": 282.5, "Close": 283.0}, index=m15)
    df.loc[pd.Timestamp("2026-11-19 11:00", tz=ny), "High"] = 284.97           # قمة أمس
    df.loc[pd.Timestamp("2026-11-19 15:45", tz=ny), "Close"] = 284.0           # إغلاق أمس
    df.loc[pd.Timestamp("2026-11-20 10:15", tz=ny), "High"] = 286.1            # ذيل فوق القمة
    now = pd.Timestamp("2026-11-20 11:02", tz=ny)
    got = []
    saved = (with_gamma, send_telegram)
    with_gamma = lambda m, t, s: m
    send_telegram = lambda m, **k: got.append(m)
    try:
        assert pdh1h_check("GOOGL", df, now, set()) == 1, "ما نبه"
        print("✅ ذيل 286.10 فوق قمة أمس 284.97 والإغلاق 283 تحتها وتحت إغلاق أمس 284 = تنبيه")
        print(got[0] + "\n")
        up = df.copy(); up.loc[pd.Timestamp("2026-11-20 10:45", tz=ny), "Close"] = 284.5
        assert pdh1h_check("GOOGL", up, now, set()) == 0
        print("✅ الإغلاق فوق إغلاق أمس (مو هابط) = ما فيه تنبيه")
        br = df.copy(); br.loc[pd.Timestamp("2026-11-20 10:45", tz=ny), "Close"] = 285.5
        assert pdh1h_check("GOOGL", br, now, set()) == 0
        print("✅ قفل فوق المقاومة (اختراق) = ما فيه تنبيه")
        sent = {"GOOGL-pdh1h-20261120"}
        assert pdh1h_check("GOOGL", df, now, sent) == 0
        print("✅ تنبيه واحد باليوم")
        su = pd.DataFrame({"Open": 285.0, "High": 285.5, "Low": 284.5, "Close": 285.0}, index=m15)
        su.loc[pd.Timestamp("2026-11-19 11:00", tz=ny), "Low"] = 282.0            # قاع أمس
        su.loc[pd.Timestamp("2026-11-19 15:45", tz=ny), "Close"] = 284.0          # إغلاق أمس
        su.loc[pd.Timestamp("2026-11-20 10:15", tz=ny), "Low"] = 281.2            # ذيل تحت القاع
        got.clear()
        assert pdh1h_check("GOOGL", su, now, set()) == 1, "الدعم ما نبه"
        print("✅ دعم: ذيل 281.20 تحت قاع أمس 282 والإغلاق 285 فوقه وفوق إغلاق أمس 284 = تنبيه")
        print(got[0] + "\n")
        dn = su.copy(); dn.loc[pd.Timestamp("2026-11-20 10:45", tz=ny), "Close"] = 283.5
        assert pdh1h_check("GOOGL", dn, now, set()) == 0
        print("✅ دعم بس الإغلاق تحت إغلاق أمس (مو صاعد) = ما فيه تنبيه")
        _SMT_TODAY["20261120"] = "bear"
        assert pdh1h_check("GOOGL", su, now, set()) == 0
        print("✅ (14) قال هابط اليوم ← تنبيه الدعم (صاعد) ما يرسل")
        assert pdh1h_check("GOOGL", df, now, set()) == 1
        print("✅ (14) قال هابط اليوم ← تنبيه المقاومة (هابط) يرسل")
        _SMT_TODAY["20261120"] = "bull"
        assert pdh1h_check("GOOGL", df, now, set()) == 0 and pdh1h_check("GOOGL", su, now, set()) == 1
        print("✅ (14) قال صاعد اليوم ← المقاومة ما ترسل والدعم يرسل")
        _SMT_TODAY.clear()
        print("PDH1H TEST OK")
    finally:
        with_gamma, send_telegram = saved


PD4H_TEST_ID = "1"   # رسالة تجريبية مرة وحدة بعد الرفع — غيّر الرقم لو تبي وحدة ثانية


def pd4h_send_test_once():
    """يرسل تنبيه تجريبي لقسم (13) مرة وحدة (يتذكرها في /data عشان ما تتكرر مع كل تشغيل)."""
    if not ENABLE_PD4H:
        return
    marker = os.path.join(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "."), "pd4h_test_sent.txt")
    try:
        with open(marker, encoding="utf-8") as f:
            if f.read().strip() == PD4H_TEST_ID:
                return
    except Exception:
        pass
    now = pd.Timestamp.now(tz=NY)
    t = "NVDA"                          # سهم حقيقي عشان القاما تنحسب من عقوده
    spot = 183.45
    try:
        import yfinance as yf
        with _YF_LOCK:
            h = yf.Ticker(t).history(period="5d", interval="1d")
        if not h.empty:
            spot = float(h["Close"].iloc[-1])
    except Exception as e:
        log(f"سحب اليوم السابق: رسالة التجربة: ما قدرت أجيب سعر {t}: {e}")
    k = spot / 183.45                   # المستويات الوهمية تتحجم على سعره الحقيقي
    yday, wk = (now - pd.Timedelta(days=1)).date(), (now - pd.Timedelta(days=6)).date()
    pd_lv = {"low": (178.40 * k, yday), "high": (184.20 * k, yday)}
    pw_lv = {"low": (172.90 * k, wk), "high": (189.60 * k, wk)}
    r = {"open": 183.10 * k, "high": 185.05 * k, "low": 182.70 * k, "close": spot, "depth": 0.46,
         "start": now.floor("h") - pd.Timedelta(hours=4), "end": now.floor("h"),
         "closes_beyond": 0, "first_touch": True}
    send_telegram("🧪 رسالة تجريبية - هذا مو تنبيه حقيقي (المستويات وهمية، القاما حقيقية)\n\n"
                  + with_gamma(_pd4h_message(t, "high", 184.20 * k, r, pd_lv, pw_lv), t, spot)
                  + "\n\n" + PD4H_CHECK_LINE
                  + "\n\nلو وصلتك هالرسالة، تنبيهات القسم الحقيقية بتوصل لنفس المكان.",
                  kind="sweep", sym=t)
    try:
        with open(marker, "w", encoding="utf-8") as f:
            f.write(PD4H_TEST_ID)
    except Exception as e:
        log(f"سحب اليوم السابق: ما قدرت أحفظ علامة الرسالة التجريبية: {e}")


def pd4h_self_test():
    """python short_bot.py --pd4htest — يجرب (13) بدون نت."""
    ny = ZoneInfo(NY)
    m15 = pd.date_range("2026-11-09 00:00", "2026-11-18 23:45", freq="15min", tz=ny)
    df = pd.DataFrame({"Open": 100.0, "High": 100.5, "Low": 99.5, "Close": 100.0}, index=m15)
    df.loc[pd.Timestamp("2026-11-12 10:00", tz=ny), ["High", "Low"]] = [104.0, 96.0]  # الأسبوع السابق
    df.loc[pd.Timestamp("2026-11-17 11:00", tz=ny), "High"] = 102.0                   # قمة أمس
    df.loc[pd.Timestamp("2026-11-17 14:00", tz=ny), "Low"] = 98.0                     # قاع أمس
    df.loc[pd.Timestamp("2026-11-17 22:00", tz=ny), ["High", "Low"]] = [110, 90]      # ليلي = ما يدخل
    df.loc[pd.Timestamp("2026-11-18 09:00", tz=ny), "High"] = 102.6                   # سحب قمة أمس
    df = df[df.index < pd.Timestamp("2026-11-18 12:00", tz=ny)]
    now = pd.Timestamp("2026-11-18 12:02", tz=ny)
    lv = prev_day_ext_levels(df, now.normalize())
    assert lv["high"][0] == 102.0 and lv["low"][0] == 98.0, lv
    c4h = only_closed(to_frame(df, 240, overnight=False), df.index.max(), now)
    r = check_pwh_1h(c4h, 102.0, now.normalize())
    assert r and r["high"] == 102.6 and r["close"] < 102.0, r
    assert check_pwl_1h(c4h, 98.0, now.normalize()) is None
    print("✅ (13) قمة أمس 102 انسحبت (102.6) والإغلاق تحتها، والليلي ما دخل")
    print(_pd4h_message("TEST", "high", 102.0, r, lv, prev_week_ext_levels(df, _week_start(now))))


# ================== (14) اتجاه السوق المتوقع: ناسداك مقابل سباكس على قمة وقاع اليوم السابق ==================
_SMT_SESSION = (9 * 60 + 30, 16 * 60)       # المؤشرات: الجلسة الرسمية بس


def smt_levels(df, now):
    """(قمة اليوم السابق، قاعه، شموع اليوم المقفلة بفريم SMT_FRAME_MIN) أو None."""
    df = to_ny(df)[OHLC].between_time("09:30", "15:59")
    day0 = now.normalize()
    prev = df[df.index < day0]
    if prev.empty:
        return None
    p = prev[prev.index >= prev.index[-1].normalize()]          # آخر يوم تداول قبل اليوم
    c = only_closed(to_frame(df, SMT_FRAME_MIN, session=_SMT_SESSION), df.index.max(), now)
    return float(p["High"].max()), float(p["Low"].min()), c[c.index >= day0]


def smt_check(ndx_df, spx_df, now):
    """آخر شمعة مقفلة لناسداك اليوم:
    هابط = ذيلها فوق قمة اليوم السابق وإغلاقها تحتها، وسباكس (من الافتتاح لين نفس الشمعة) ما وصل قمته السابقة.
    صاعد = ذيلها تحت قاع اليوم السابق وإغلاقها فوقه، وسباكس ما وصل قاعه السابق.
    يرجع {"side": "bear"/"bull", ...} أو None."""
    a, b = smt_levels(ndx_df, now), smt_levels(spx_df, now)
    if not a or not b:
        return None
    (n_pdh, n_pdl, nc), (s_pdh, s_pdl, sc) = a, b
    if nc.empty or sc.empty:
        return None
    last = nc.iloc[-1]
    s_upto = sc[sc.index <= nc.index[-1]]
    if s_upto.empty or s_upto.index[-1] != nc.index[-1]:     # لازم سباكس عنده نفس الشمعة
        return None
    h, l, cl = float(last["High"]), float(last["Low"]), float(last["Close"])
    bear = h > n_pdh and cl < n_pdh and float(s_upto["High"].max()) <= s_pdh
    bull = l < n_pdl and cl > n_pdl and float(s_upto["Low"].min()) >= s_pdl
    if bear == bull:                                          # ما فيه شرط، أو الاثنين بنفس الشمعة
        return None
    return {"side": "bear" if bear else "bull", "start": nc.index[-1], "end": last["end"],
            "ndx": cl, "spx": float(s_upto["Close"].iloc[-1])}


def _smt_etf_spot(sym):
    import yfinance as yf
    with _YF_LOCK:
        h = yf.Ticker(sym).history(period="5d", interval="1d")
    return float(h["Close"].iloc[-1]) if not h.empty else None


def smt_gamma_text(name, code, opt_sym, etf, spot):
    """تمركز القاما للمؤشر من عقوده، ولو ما جات يستخدم الصندوق (SPY / QQQ)."""
    src, g = f"{code}", ""
    try:
        g = gamma_block(opt_sym, spot)
    except Exception as e:
        log(f"اتجاه السوق: قاما {opt_sym}: {e}")
    if not g and etf:
        try:
            etf_spot = _smt_etf_spot(etf)
            g = gamma_block(etf, etf_spot) if etf_spot else ""
            src = f"{code} من عقود {etf}"
        except Exception as e:
            log(f"اتجاه السوق: قاما {etf}: {e}")
    if not g:
        return f"🧲 قاما {name} ({code}): ما فيه بيانات الحين"
    lines = g.split("\n")
    lines[0] = lines[0].replace("🧲 تمركز القاما", f"🧲 قاما {name} ({src})")
    return "\n".join(lines)


def smt_message(r):
    bear = r["side"] == "bear"
    t = pd.Timestamp(r["end"]).tz_convert(LOCAL_TZ)
    spots = {"SPX": r["spx"], "NDX": r["ndx"]}
    parts = ["$SPX | $NDX",
             ("📉 اتجاه السوق المتوقع: هابط 🔴" if bear else "📈 اتجاه السوق المتوقع: صاعد 🟢"),
             f"⏰ {t:%Y-%m-%d %H:%M} (توقيتك)"]
    for name, code, opt_sym, etf in SMT_GAMMA:
        parts += ["", smt_gamma_text(name, code, opt_sym, etf, spots[code])]
    parts += ["", "⚠️ تحليل فني — ليست توصية بيع أو شراء."]
    return "\n".join(parts)


def smt_market_open(now=None):
    now = now or pd.Timestamp.now(tz=NY)
    m = now.hour * 60 + now.minute
    return now.weekday() < 5 and _SMT_SESSION[0] + SMT_FRAME_MIN <= m <= _SMT_SESSION[1] + 20


def scan_smt(sent, now=None):
    now = now or pd.Timestamp.now(tz=NY)
    data = dict(download_batches([SMT_NDX, SMT_SPX], 2, period="5d",
                                 interval=f"{GAP_BASE_MIN}m", prepost=False))
    if SMT_NDX not in data or SMT_SPX not in data:
        log("اتجاه السوق: ما جات بيانات ناسداك/سباكس من ياهو")
        return 0
    r = smt_check(data[SMT_NDX], data[SMT_SPX], now)
    if not r or (now - pd.Timestamp(r["end"])).total_seconds() / 60 > SMT_MAX_ALERT_DELAY_MIN:
        return 0
    key = f"SMT-{r['side']}-{now:%Y%m%d}"            # تنبيه واحد باليوم لكل اتجاه
    if key in sent:
        return 0
    sent.add(key)
    _append_line(SMT_SENT_FILE, key)
    _SMT_TODAY[f"{now:%Y%m%d}"] = r["side"]           # فلتر اتجاه السوق يمشي على هذا باقي اليوم
    send_telegram(smt_message(r), kind="smt", head=False)
    log(f"[{datetime.now():%H:%M}] اتجاه السوق: تنبيه {'هابط' if r['side'] == 'bear' else 'صاعد'}")
    return 1


def smt_send_test_once():
    """رسالة تجريبية مرة وحدة (الاتجاه وهمي، القاما حقيقية)."""
    marker = os.path.join(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "."), "smt_test_sent.txt")
    try:
        with open(marker, encoding="utf-8") as f:
            if f.read().strip() == SMT_TEST_ID:
                return
    except Exception:
        pass
    spots = {}
    for code, sym in (("spx", SMT_SPX), ("ndx", SMT_NDX)):
        try:
            spots[code] = _smt_etf_spot(sym)
        except Exception as e:
            log(f"اتجاه السوق: رسالة التجربة: سعر {sym}: {e}")
    r = {"side": "bear", "end": pd.Timestamp.now(tz=NY), "spx": spots.get("spx"), "ndx": spots.get("ndx")}
    send_telegram("🧪 رسالة تجريبية - مو تنبيه حقيقي (الاتجاه وهمي، القاما حقيقية)\n\n"
                  + smt_message(r), kind="smt", head=False)
    try:
        with open(marker, "w", encoding="utf-8") as f:
            f.write(SMT_TEST_ID)
    except Exception as e:
        log(f"اتجاه السوق: ما قدرت أحفظ علامة الرسالة التجريبية: {e}")


def smt_run_forever():
    smt_send_test_once()
    sent = _load_set(SMT_SENT_FILE)
    log(f"اتجاه السوق (ناسداك مقابل سباكس، اليوم السابق): بدأ — فريم {SMT_FRAME_MIN} دقيقة، كل {SMT_EVERY_MIN} دقيقة")
    while True:
        try:
            if smt_market_open():
                scan_smt(sent)
        except Exception as e:
            log(f"اتجاه السوق: خطأ {e}")
        time.sleep(SMT_EVERY_MIN * 60)


def smt_self_test():
    """python short_bot.py --smttest — يجرب (14) بدون نت."""
    global gamma_block
    ny = ZoneInfo(NY)
    idx = pd.date_range("2026-11-18 09:30", "2026-11-19 15:45", freq="15min", tz=ny)
    idx = idx[(idx.hour * 60 + idx.minute >= 570) & (idx.hour * 60 + idx.minute < 960)]

    def mk(base):
        return pd.DataFrame({"Open": base, "High": base + 5, "Low": base - 5, "Close": base}, index=idx)

    ndx, spx = mk(21000.0), mk(6800.0)
    # أمس: قمة ناسداك 21050 وقاعه 20950 | سباكس 6820 و 6780
    ndx.loc[pd.Timestamp("2026-11-18 11:00", tz=ny), ["High", "Low"]] = [21050, 20950]
    spx.loc[pd.Timestamp("2026-11-18 11:00", tz=ny), ["High", "Low"]] = [6820, 6780]
    k = pd.Timestamp("2026-11-19 10:30", tz=ny)
    now = pd.Timestamp("2026-11-19 10:46", tz=ny)
    cut = lambda d: d[d.index <= k]
    saved = gamma_block
    gamma_block = lambda t, s: f"🧲 تمركز القاما (أقرب 4 انتهاء، لين 12-19):\nجدار الكول: {round(s, -1):g}"
    try:
        # 🔴 ناسداك سحب قمة أمس وقفل تحتها، وسباكس ما وصل قمته
        n1 = ndx.copy(); n1.loc[k, ["High", "Close"]] = [21060, 21010]
        r = smt_check(cut(n1), cut(spx), now)
        assert r and r["side"] == "bear", r
        msg = smt_message(r)
        assert msg.startswith("$SPX | $NDX") and "هابط" in msg and "سحب" not in msg
        print("✅ هابط: ناسداك سحب قمة أمس وقفل تحتها، وسباكس ما سحب\n" + msg + "\n")
        # سباكس كمان سحب قمته = ما فيه تنبيه
        s1 = spx.copy(); s1.loc[k, "High"] = 6825
        assert smt_check(cut(n1), cut(s1), now) is None
        print("✅ سباكس سحب نفس القمة = ما فيه تنبيه")
        # ناسداك قفل فوق القمة (اختراق مو سحب) = ما فيه تنبيه
        n2 = ndx.copy(); n2.loc[k, ["High", "Close"]] = [21060, 21055]
        assert smt_check(cut(n2), cut(spx), now) is None
        print("✅ ناسداك قفل فوق القمة = ما فيه تنبيه")
        # 🟢 ناسداك سحب قاع أمس وقفل فوقه، وسباكس ما وصل قاعه
        n3 = ndx.copy(); n3.loc[k, ["Low", "Close"]] = [20940, 20990]
        r = smt_check(cut(n3), cut(spx), now)
        assert r and r["side"] == "bull", r
        print("✅ صاعد: ناسداك سحب قاع أمس وقفل فوقه، وسباكس ما سحب")
        # ما صار شي = ما فيه تنبيه
        assert smt_check(cut(ndx), cut(spx), now) is None
        print("✅ بدون سحب = ما فيه تنبيه")
        print("SMT TEST OK")
    finally:
        gamma_block = saved


# ================== (1) الإنفيرجن IFVG - فريم ساعة و4 ساعات ==================
def check_ifvg(c):
    """آخر 4 شموع مقفلة بالاتجاهين. يرجع تفاصيل النموذج لو تحقق، وإلا None.
    لون الشموع ما يهم - المهم الجاب بين ذيل الأولى والثالثة، والثانية تغطي الجاب كامل،
    والرابعة تقفل وراه."""
    if len(c) < 4:
        return None
    c1, c2, c3, c4 = (c.iloc[i] for i in (-4, -3, -2, -1))
    info = {"price": float(c4["Close"]), "open": float(c4["Open"]), "candle_time": c.index[-1],
            "end": c4["end"] if "end" in c else c.index[-1], "candles": c.iloc[-4:]}
    # 🟢 صعودي: قاع الأولى فوق قمة الثالثة، والرابعة تقفل فوق أعلى الجاب
    if c1["Low"] > c3["High"]:
        bottom, top = float(c3["High"]), float(c1["Low"])
        covered = c2["High"] >= top and c2["Low"] <= bottom
        if (covered or not IFVG_REQUIRE_MIDDLE_COVER) and c4["Close"] > top:
            return {"side": "bull", "gap_bottom": bottom, "gap_top": top, **info}
    # 🔴 هبوطي: قمة الأولى تحت قاع الثالثة، والرابعة تقفل تحت أسفل الجاب
    if c1["High"] < c3["Low"]:
        bottom, top = float(c1["High"]), float(c3["Low"])
        covered = c2["High"] >= top and c2["Low"] <= bottom
        if (covered or not IFVG_REQUIRE_MIDDLE_COVER) and c4["Close"] < bottom:
            return {"side": "bear", "gap_bottom": bottom, "gap_top": top, **info}
    return None


def _ifvg_message(t, res, frame):
    lo, hi, px = (round(float(res[k]), 2) for k in ("gap_bottom", "gap_top", "price"))
    if res["side"] == "bull":
        head, line = f"🟢 Inversion Gap - {frame}", f"الشمعة قفلت فوق أعلى الـ IFVG ({hi})"
    else:
        head, line = f"🔴 Inversion Gap - {frame}", f"الشمعة قفلت تحت أسفل الـ IFVG ({lo})"
    closed_at = pd.Timestamp(res["end"]).tz_convert(LOCAL_TZ)
    msg = (f"{head}\n"
           f"السهم: ${t}\n"
           f"IFVG: {lo} ← {hi}  (حجمه {hi - lo:.2f}$)\n"
           f"{line}\n"
           f"سعر الإغلاق: {px}\n"
           f"وقت الإغلاق: {closed_at:%H:%M} (توقيتك)")
    cs = res.get("candles")
    if IFVG_SHOW_CANDLES and cs is not None:
        rows = []
        for k, (ts, r) in enumerate(cs.iterrows(), 1):
            lt = pd.Timestamp(ts).tz_convert(LOCAL_TZ)
            col = "🟢" if r["Close"] > r["Open"] else "🔴"
            rows.append(f"{k}) {lt:%m/%d %H:%M} {col} أعلى {r['High']:.2f} | أقل {r['Low']:.2f}")
        msg += "\nالشموع (بتوقيتك):\n" + "\n".join(rows)
    return msg


def ifvg_scan_due(now, last_run):
    """بعد إغلاق كل ساعة بدقيقة (وإعادة بعد 5 و12 دقيقة). يرجع وقت الجولة لو جا وقتها."""
    boundary = now.floor("h")
    for off in sorted(GAP_SCAN_AFTER_CLOSE_MIN, reverse=True):
        slot = boundary + pd.Timedelta(minutes=off)
        if now >= slot:
            return slot if (last_run is None or last_run < slot) else None
    return None


def scan_ifvg(symbols, sent, now=None):
    """(1) IFVG فريم ساعة و4 ساعات على الجلسة الممتدة (بدون الليلي)."""
    now = now or pd.Timestamp.now(tz=NY)
    frames = [(ENABLE_IFVG_4H, 240, "ifvg4h", "فريم 4 ساعات", IFVG_4H_MIN_SIZE),
              (ENABLE_IFVG_1H, 60, "ifvg1h", "فريم ساعة", IFVG_1H_MIN_SIZE)]
    frames = [f for f in frames if f[0]]
    if not frames:
        return
    hits = 0
    for t, df in download_batches(symbols, 100, period="7d", interval=f"{GAP_BASE_MIN}m", prepost=True):
        try:
            df = to_ny(df)[OHLC]
            if df.empty or float(df["Close"].iloc[-1]) < IFVG_MIN_PRICE:
                continue
            last_bar = df.index.max()
            for _, minutes, tag, label, min_size in frames:
                res = check_ifvg(only_closed(to_frame(df, minutes, overnight=False), last_bar, now))
                if not res or round(res["gap_top"] - res["gap_bottom"], 2) < min_size:
                    continue
                if (now - pd.Timestamp(res["end"])).total_seconds() / 60 > IFVG_MAX_ALERT_DELAY_MIN:
                    continue                    # شمعة قديمة، مو إغلاق جديد
                key = f"{t}-{tag}-{res['side']}-{res['candle_time']}"
                if key in sent:
                    continue
                sent.add(key)
                _append_line(GAP_SENT_FILE, key)
                hits += 1
                msg = _ifvg_message(t, res, label)
                if IFVG_GAMMA:
                    msg = with_gamma(msg, t, res["price"])
                send_telegram(msg, kind="gap", sym=t)
        except Exception as e:
            log(f"الإنفيرجن: {t}: خطأ - {e}")
    free_memory()
    log(f"[{datetime.now():%H:%M}] الإنفيرجن (ساعة + 4 ساعات): خلص الفحص - {hits} تنبيه جديد")


def ifvg_self_test():
    """python short_bot.py --ifvgtest — يجرب النموذج على شموع وهمية بدون نت."""
    # (فتح، أعلى، أقل، إغلاق) لكل شمعة 4 ساعات (نفس مثال NVDA في gap_scanner)
    times = ("2026-09-25 08:00", "2026-09-25 12:00", "2026-09-25 16:00", "2026-09-28 04:00")
    prices = [(225.00, 225.40, 224.87, 224.95),   # الأولى - قاعها 224.87
              (225.05, 225.80, 223.75, 223.80),   # الثانية تغطي الجاب
              (223.80, 224.33, 223.00, 223.10),   # الثالثة - قمتها 224.33
              (223.50, 228.30, 222.90, 228.08)]   # الرابعة - تقفل فوق 224.87
    rows = []
    for s, (o, h, l, c) in zip(times, prices):
        s = pd.Timestamp(s, tz=NY)
        path = [o + (c - o) * k / 15 for k in range(16)]
        for k in range(16):
            op = path[k - 1] if k else o
            rows.append((s + pd.Timedelta(minutes=15 * k), op,
                         h if k == 6 else max(op, path[k]), l if k == 10 else min(op, path[k]), path[k]))
    df = pd.DataFrame(rows, columns=["t"] + OHLC).set_index("t")
    for label, now, want in (("قبل إغلاق الرابعة", "2026-09-28 07:59", False),
                             ("بعد الإغلاق بدقيقة", "2026-09-28 08:01", True)):
        now = pd.Timestamp(now, tz=NY)
        part = df[df.index <= now - pd.Timedelta(minutes=15)]
        c = only_closed(to_frame(part, 240, overnight=False), part.index.max(), now)
        res = check_ifvg(c)
        assert bool(res) == want, (label, res)
        print(f"✅ {label}: " + ("تنبيه صعودي" if res else "ما فيه تنبيه"))
        if res:
            assert res["side"] == "bull" and res["gap_top"] == 224.87 and res["gap_bottom"] == 224.33
            print(_ifvg_message("NVDA", res, "فريم 4 ساعات"))
    # هبوطي: نفس الأرقام مقلوبة
    idx = pd.date_range("2026-10-13 04:00", periods=4, freq="4h", tz=NY)
    bear = pd.DataFrame({"Open": [100, 100.2, 101.3, 101.5], "High": [100.5, 101.6, 102, 101.8],
                         "Low": [99.8, 100.1, 101.1, 99.5], "Close": [100.2, 101.4, 101.6, 99.9]}, index=idx)
    bear["end"] = bear.index + pd.Timedelta(hours=4)
    r = check_ifvg(bear)
    assert r and r["side"] == "bear" and r["gap_bottom"] == 100.5 and r["gap_top"] == 101.1, r
    print("✅ هبوطي: الرابعة قفلت تحت قمة الأولى (100.5)")
    nocov = bear.copy(); nocov.iloc[1, nocov.columns.get_loc("High")] = 100.9
    assert check_ifvg(nocov) is None
    print("✅ الثانية ما غطت الجاب = ما فيه تنبيه")
    c4 = to_frame(pd.DataFrame({"Open": 1.0, "High": 1.0, "Low": 1.0, "Close": 1.0},
                               index=pd.date_range("2026-10-13 00:00", "2026-10-13 23:45",
                                                   freq="15min", tz=NY)), 240, overnight=False)
    assert [f"{x:%H}" for x in c4.index] == ["04", "08", "12", "16"]
    c1 = to_frame(pd.DataFrame({"Open": 1.0, "High": 1.0, "Low": 1.0, "Close": 1.0},
                               index=pd.date_range("2026-10-13 00:00", "2026-10-13 23:45",
                                                   freq="15min", tz=NY)), 60, overnight=False)
    assert f"{c1.index[0]:%H}" == "04" and f"{c1.index[-1]:%H}" == "19" and len(c1) == 16
    print("✅ شموع 4 ساعات 4-8-12-4 وشموع الساعة من 4 الفجر لين 8 بالليل (بدون الليلي)")
    assert ifvg_scan_due(pd.Timestamp("2026-10-13 10:00:30", tz=NY), None) is None
    s1 = ifvg_scan_due(pd.Timestamp("2026-10-13 10:01:10", tz=NY), None)
    assert s1 is not None and ifvg_scan_due(pd.Timestamp("2026-10-13 10:03", tz=NY), s1) is None
    assert ifvg_scan_due(pd.Timestamp("2026-10-13 10:05", tz=NY), s1) is not None
    print("✅ وقت الفحص: بعد الساعة بدقيقة، ويعيد بعد 5 و12 دقيقة")
    print("IFVG TEST OK")
    watch_ifvg_self_test()


# ================== (1هـ) الإنفيرجن IFVG - قائمة المراقبة (منقول من gap_scanner) ==================
def night_4h():
    """فريم 4 ساعات يشتغل 24 ساعة؟ (الإعداد شغال + فيه مفاتيح ألباكا لبيانات الليل)"""
    return GAP_4H_24H and bool(ALPACA_KEY and ALPACA_SECRET)


def _watch_message(t, res, frame):
    """رسالة قائمة المراقبة: IFVG مع الاتجاه 🟢 صعودي / 🔴 هبوطي (بدون الشموع)."""
    lo, hi, px = (round(float(res[k]), 2) for k in ("gap_bottom", "gap_top", "price"))
    closed_at = pd.Timestamp(res["end"]).tz_convert(LOCAL_TZ)
    if res["side"] == "bull":
        head, side = "🟢 Inversion Gap", f"الشمعة قفلت فوق أعلى الـ IFVG ({hi})"
    else:
        head, side = "🔴 Inversion Gap", f"الشمعة قفلت تحت أسفل الـ IFVG ({lo})"
    msg = (f"{head} - {frame}\n"
           f"السهم: ${t}\n"
           f"IFVG: {lo} ← {hi}  (حجمه {hi - lo:.2f}$)\n"
           f"{side}\n"
           f"سعر الإغلاق: {px}\n"
           f"وقت الإغلاق: {closed_at:%H:%M} (توقيتك)")
    cs = res.get("candles")
    if WATCH_SHOW_CANDLES and cs is not None:
        rows = []
        for k, (ts, r) in enumerate(cs.iterrows(), 1):
            lt = pd.Timestamp(ts).tz_convert(LOCAL_TZ)
            col = "🟢" if r["Close"] > r["Open"] else "🔴"
            rows.append(f"{k}) {lt:%m/%d %H:%M} {col} أعلى {r['High']:.2f} | أقل {r['Low']:.2f}")
        msg += "\nالشموع (بتوقيتك):\n" + "\n".join(rows)
    return msg


# ---------- الجلسة الليلية من ألباكا (8 بالليل - 4 الفجر نيويورك) ----------
_night_cache = {}   # الرمز -> (وقت الجلب، البيانات)


def _alpaca_night_stale(fetched, now):
    if fetched is None:
        return True
    if now.hour >= 20 or now.hour * 60 + now.minute < 4 * 60 + 20:
        return fetched < now.floor(f"{GAP_BASE_MIN}min")   # وقت الليل: نجدد كل ربع ساعة
    return fetched < now.normalize() + pd.Timedelta(hours=4, minutes=20)   # بعد الليل: نسخة وحدة تكفي


def fetch_alpaca_night(symbols, now):
    """شموع ربع ساعة للجلسة الليلية (8 بالليل - 4 الفجر) من ألباكا (feed=boats) لمجموعة أسهم.
    يرجع {الرمز: DataFrame} أو None لو فشل."""
    headers = {"APCA-API-KEY-ID": ALPACA_KEY, "APCA-API-SECRET-KEY": ALPACA_SECRET}
    start = (now - pd.Timedelta(days=7)).tz_convert("UTC")
    params = {"symbols": ",".join(symbols), "timeframe": f"{GAP_BASE_MIN}Min", "feed": "boats",
              "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"), "limit": 10000, "adjustment": "raw"}
    if ALGO_DELAY_MIN:      # الباقة المجانية: بيانات الليل متأخرة 15 دقيقة
        end = (now - pd.Timedelta(minutes=max(ALGO_DELAY_MIN, 16))).tz_convert("UTC")
        params["end"] = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    raw = {}
    for _ in range(50):                          # صفحات
        _alpaca_wait()
        try:
            r = requests.get("https://data.alpaca.markets/v2/stocks/bars",
                             headers=headers, params=params, timeout=30)
        except Exception as e:
            log("ألباكا (الليل): فشل الاتصال -", e)
            return None
        if r.status_code == 429:
            time.sleep(10)
            continue
        if r.status_code != 200:
            log(f"ألباكا (الليل): خطأ {r.status_code} - {r.text[:200]}")
            return None
        data = r.json()
        for sym, bars in (data.get("bars") or {}).items():
            raw.setdefault(sym, []).extend(bars or [])
        token = data.get("next_page_token")
        if not token:
            break
        params["page_token"] = token
    out = {}
    for sym in symbols:
        bars = raw.get(sym) or []
        if not bars:
            out[sym] = pd.DataFrame(columns=OHLC)
            continue
        df = pd.DataFrame(bars)
        idx = pd.DatetimeIndex(pd.to_datetime(df["t"], utc=True)).tz_convert(NY)
        df = df.rename(columns={"o": "Open", "h": "High", "l": "Low", "c": "Close"})
        df = df.set_index(idx)[OHLC].astype(float).dropna()
        h = df.index.hour
        out[sym] = df[(h >= 20) | (h < 4)]       # الليل بس، الباقي من ياهو
    return out


def load_night(tickers, now):
    """بيانات الليل لكل الأسهم (المؤشرات ما لها جلسة ليلية) - تتخزن وتتجدد بس لما تقدم."""
    tickers = stocks_only(tickers)
    need = [t for t in tickers if _alpaca_night_stale((_night_cache.get(t) or (None,))[0], now)]
    got = 0
    for i in range(0, len(need), 200):
        res = fetch_alpaca_night(need[i:i + 200], now)
        if res is None:
            continue
        for t, df in res.items():
            _night_cache[t] = (now, df)
            got += 1
    if need:
        log(f"الجلسة الليلية: جددت {got} سهم من ألباكا")
    return {t: v[1] for t, v in _night_cache.items()}


def watch_4h_due(now):
    """شمعة 4 ساعات تقفل كل 4 ساعات بالضبط (0، 4، 8، 12، 16، 20 نيويورك) - أول نص ساعة بعدها."""
    return now.hour % 4 == 0 and now.minute < 30


def scan_watch_ifvg(symbols, sent, now=None, do_1h=True, do_4h=True, do_1h24=False, do_4h_ext=False):
    """(1هـ) IFVG قائمة المراقبة: ساعة (الجلسة الممتدة) + 4 ساعات (24 ساعة مع الليل من ألباكا)."""
    now = now or pd.Timestamp.now(tz=NY)
    ov4 = night_4h()
    frames = [(do_4h_ext and WATCH_IFVG_4H_EXT, 240, "w4h", "فريم 4 ساعات (ممدد)", WATCH4H_MIN_SIZE, False),
              # نفس المفتاح "w4h": لو الممدد نبه على نفس الشمعة ما يتكرر من الـ24 ساعة
              (do_4h and WATCH_IFVG_4H, 240, "w4h",
               "فريم 4 ساعات (24 ساعة)" if ov4 else "فريم 4 ساعات (ممدد)", WATCH4H_MIN_SIZE, ov4),
              (do_1h and WATCH_IFVG_1H, 60, "w1h", "فريم ساعة (ممدد)", WATCH_MIN_SIZE, False),
              # نفس المفتاح "w1h": لو الممدد نبه على نفس الشمعة ما يتكرر من الـ24 ساعة
              (do_1h24 and WATCH_IFVG_1H_24H and night_4h(), 60, "w1h", "فريم ساعة (24 ساعة)",
               WATCH_MIN_SIZE, True)]
    frames = [f for f in frames if f[0]]
    if not frames:
        return
    night = load_night(symbols, now) if any(f[5] for f in frames) else {}
    hits = 0
    for t, df in download_batches(symbols, 100, period="7d", interval=f"{GAP_BASE_MIN}m", prepost=True):
        try:
            df = to_ny(df)[OHLC]
            if df.empty:
                continue
            last_bar = df.index.max()
            n = night.get(t)
            df24 = df
            if n is not None and not n.empty:
                df24 = pd.concat([df, n])
                df24 = df24[~df24.index.duplicated(keep="first")].sort_index()
            for _, minutes, tag, label, min_size, ov in frames:
                src = df24 if ov else df
                res = check_ifvg(only_closed(to_frame(src, minutes, overnight=ov), src.index.max(), now))
                if not res or round(res["gap_top"] - res["gap_bottom"], 2) < min_size:
                    continue
                if (now - pd.Timestamp(res["end"])).total_seconds() / 60 > IFVG_MAX_ALERT_DELAY_MIN:
                    continue                    # شمعة قديمة، مو إغلاق جديد
                key = f"{t}-{tag}-{res['side']}-{res['candle_time']}"
                if key in sent:
                    continue
                sent.add(key)
                _append_line(GAP_SENT_FILE, key)
                hits += 1
                msg = _watch_message(t, res, label)
                if IFVG_GAMMA:
                    msg = with_gamma(msg, t, res["price"])
                if WATCH_CHECK_LINE:
                    msg += "\n\n" + WATCH_CHECK_LINE
                send_telegram(msg, kind="gap", sym=t, head=WATCH_HEAD)
        except Exception as e:
            log(f"الإنفيرجن (قائمة المراقبة): {t}: خطأ - {e}")
    free_memory()
    log(f"[{datetime.now():%H:%M}] الإنفيرجن (قائمة المراقبة): خلص الفحص - {hits} تنبيه جديد")


def watch_ifvg_self_test():
    """يجرب (1هـ) بدون نت: الرسالة وشموع 4 ساعات 24 ساعة ووقت الفحص."""
    flat = pd.DataFrame({"Open": 1.0, "High": 1.0, "Low": 1.0, "Close": 1.0},
                        index=pd.date_range("2026-10-13 00:00", "2026-10-13 23:45", freq="15min", tz=NY))
    hrs = [f"{x:%H}" for x in to_frame(flat, 240, overnight=True).index]
    assert hrs == ["00", "04", "08", "12", "16", "20"], hrs
    print("✅ (1هـ) شموع 4 ساعات 24 ساعة: تبدأ 8 بالليل نيويورك (8، 12، 4، 8، 12، 4)")
    assert watch_4h_due(pd.Timestamp("2026-10-13 08:01", tz=NY))
    assert not watch_4h_due(pd.Timestamp("2026-10-13 09:01", tz=NY))
    print("✅ (1هـ) فريم 4 ساعات يفحص بس بعد إغلاق شمعته")
    idx = pd.date_range("2026-11-13 00:00", periods=4, freq="4h", tz=NY)
    c = pd.DataFrame({"Open": [193, 193.2, 192.3, 192.2], "High": [193.5, 193.4, 192.48, 196.2],
                      "Low": [192.8, 192.3, 191.9, 192.0], "Close": [193.1, 192.5, 192.2, 195.9]}, index=idx)
    c["end"] = c.index + pd.Timedelta(hours=4)
    r = check_ifvg(c)
    assert r and r["side"] == "bull" and round(r["gap_top"] - r["gap_bottom"], 2) == 0.32, r
    assert round(r["gap_top"] - r["gap_bottom"], 2) >= WATCH4H_MIN_SIZE
    msg = _watch_message("COHR", r, "فريم 4 ساعات")
    assert ("الشموع" in msg) == WATCH_SHOW_CANDLES
    print("✅ (1هـ) جاب 0.32$ على 4 ساعات = ينبه:")
    print(msg)


# ================== (12) سحب السيولة الأسبوعي (فريم 4 ساعات) + العقد ==================
def wkopt_in_range(price):
    p = float(price)
    return (ENABLE_WKOPT and (not WKOPT_MIN_PRICE or p >= WKOPT_MIN_PRICE)
            and (not WKOPT_MAX_PRICE or p <= WKOPT_MAX_PRICE))


def wkopt_pick_option(t, spot, put):
    """كول (سحب دعم) أو بوت (سحب مقاومة): أكثر من 10 أيام، حجم فوق 500، عقود مفتوحة فوق 1000،
    دلتا فوق 0.12. يختار أقرب انتهاء فيه عقد بالشروط، وفيه الأرخص (أقل دلتا فوق الحد).
    يرجع (العقد، الحجم، العقود المفتوحة) أو None."""
    today = pd.Timestamp.now(tz=NY).date()
    d1 = today + timedelta(days=WKOPT_OPT_MIN_DTE + 1)        # أكثر من 10 أيام
    d2 = today + timedelta(days=WKOPT_OPT_MAX_DTE)
    ok = []
    for x in _pdr1h_option_rows(t, put, spot, d1, d2):
        exp, k, delta, bid, ask, sym, iv, gamma, vol, src = x
        if delta is None or abs(delta) <= WKOPT_OPT_MIN_DELTA or not ask:
            continue
        if (vol or 0) <= WKOPT_OPT_MIN_VOLUME:
            continue
        if (exp - today).days <= WKOPT_OPT_MIN_DTE:
            continue
        ok.append(x)
    for exp in sorted({x[0] for x in ok}):                     # أقرب انتهاء أول
        for x in sorted((x for x in ok if x[0] == exp), key=lambda x: abs(x[2])):
            oi = _opt_open_interest(t, x) or 0
            if oi > WKOPT_OPT_MIN_OI:
                return x, x[8], oi
    return None


def wkopt_message(t, side, lvl, lvl_day, r, opt, nth=1):
    put = side == "high"
    kind = "بوت" if put else "كول"
    head = ("🔴 سحب سيولة — مقاومة الأسبوع السابق (ذيل الشمعة) — بوت" if put
            else "🟢 سحب سيولة — دعم الأسبوع السابق (ذيل الشمعة) — كول")
    if nth > 1:
        head = f"🔁 إعادة اختبار — السحب رقم {nth} هالأسبوع\n" + head
    lines = [head,_pwl_message(t, side, lvl, lvl_day, r, frame=WKOPT_FRAME_TXT, trade=True), ""]
    if opt:
        c, vol, oi = opt
        exp, k, delta, bid, ask, sym, iv, gamma = c[:8]
        days = (exp - pd.Timestamp.now(tz=NY).date()).days
        mid = (bid + ask) / 2 if bid else ask
        g_src = ""
        if not gamma:                                   # المصدر ما أعطاها (ياهو) → بلاك شولز
            gamma = _bs_gamma(float(r["close"]), k, _opt_years(exp), iv) or None
            g_src = " (محسوبة)" if gamma else ""
        g_line = ""
        if gamma:
            g_line = (f"القاما: {gamma:.4f}{g_src} — كل 1$ حركة بالسهم تغيّر الدلتا "
                      f"{gamma:.4f} (≈ {gamma * 100:.2f} دلتا للعقد كامل)")
        lines += [f"📄 العقد: {t} {kind} {k:g} — انتهاء {exp:%Y-%m-%d} ({days} يوم)",
                  f"السعر الحين: {mid:.2f}$ (العقد كامل {mid * 100:,.0f}$) | بيد {bid or 0:.2f} / أسك {ask:.2f}",
                  f"الدلتا: {delta:.4f}" + (f" | IV: {iv * 100:.0f}%" if iv else "")]
        if g_line:
            lines.append(g_line)
        lines.append(f"حجم التداول: {int(vol):,} | العقود المفتوحة: {int(oi):,}")
    elif t in INDEX_SYMBOLS:
        lines.append("📄 العقد: مؤشر — ما فيه عقد (الاتجاه بس)")
    else:
        lines.append(f"📄 العقد: ما لقيت {kind} بالشروط")
    if t not in INDEX_SYMBOLS:
        lines.append(f"(شروط العقد: أكثر من {WKOPT_OPT_MIN_DTE} أيام، حجم فوق {WKOPT_OPT_MIN_VOLUME}، "
                     f"عقود مفتوحة فوق {WKOPT_OPT_MIN_OI:,}، دلتا فوق {WKOPT_OPT_MIN_DELTA:.4f})")
    lines += ["", WKOPT_CHECK_LINE, "", "⚠️ محتوى تعليمي — تداول وهمي، ليست توصية للشراء."]
    return "\n".join(lines)


WKOPT_CHECK_LINE = "🔎 حلل السهم وتأكد من الاتجاه"


WKOPT_TEST_ID = "4" # رسالة تجريبية مرة وحدة بعد الرفع — غيّر الرقم لو تبي وحدة ثانية


def wkopt_send_test_once():
    """يرسل تنبيه تجريبي للقسم (12) مرة وحدة (يتذكرها في /data عشان ما تتكرر مع كل تشغيل)."""
    if not ENABLE_WKOPT:
        return
    marker = os.path.join(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "."), "wkopt_test_sent.txt")
    try:
        with open(marker, encoding="utf-8") as f:
            if f.read().strip() == WKOPT_TEST_ID:
                return
    except Exception:
        pass
    now = pd.Timestamp.now(tz=NY)
    lvl_day = (now - pd.Timedelta(days=6)).date()
    exp = (now + pd.Timedelta(days=12)).date()
    r_low = {"open": 181.2, "high": 182.6, "low": 178.9, "close": 181.8, "depth": 0.72,
             "start": now.floor("h"), "end": now, "closes_beyond": 0, "first_touch": True}
    call = ((exp, 185.0, 0.3120, 2.35, 2.45, "TEST", 0.36, 0.03, 1840, "test"), 1840, 6250)
    r_high = {"open": 247.0, "high": 251.9, "low": 246.1, "close": 247.6, "depth": 0.85,
              "start": now.floor("h"), "end": now, "closes_beyond": 0, "first_touch": True}
    put = ((exp, 245.0, -0.2870, 3.10, 3.25, "TEST", 0.41, 0.03, 960, "test"), 960, 3400)
    note = "🧪 رسالة تجريبية - هذا مو تنبيه حقيقي (السهم والأرقام وهمية)\n\n"
    if not WKOPT_PUT_ONLY:
        send_telegram(note + wkopt_message("TEST", "low", 180.20, lvl_day, r_low, call), kind="sweep")
        time.sleep(1)
    send_telegram(note + wkopt_message("TEST", "high", 249.80, lvl_day, r_high, put)
                  + "\n\nلو وصلتك هالرسالة، تنبيهات القسم الحقيقية بتوصل لنفس المكان.", kind="sweep")
    try:
        with open(marker, "w", encoding="utf-8") as f:
            f.write(WKOPT_TEST_ID)
    except Exception as e:
        log(f"سحب أسبوعي + عقد: ما قدرت أحفظ علامة الرسالة التجريبية: {e}")


def wkopt_self_test():
    """python short_bot.py --wkopttest — يجرب اختيار العقد والرسالة بدون نت."""
    global _pdr1h_option_rows, _opt_open_interest
    today = pd.Timestamp.now(tz=NY).date()
    e9, e12, e19 = (today + timedelta(days=d) for d in (9, 12, 19))
    fake_rows = [   # (انتهاء، سترايك، دلتا، bid، ask، رمز، IV، جاما، حجم، مصدر)
        (e9, 200, -0.30, 2.0, 2.1, "A", 0.4, 0.02, 5000, "t"),    # 9 أيام = يترفض
        (e12, 190, -0.10, 0.5, 0.6, "B", 0.4, 0.02, 5000, "t"),   # دلتا 0.10 = يترفض
        (e12, 195, -0.18, 1.0, 1.1, "C", 0.4, 0.02, 400, "t"),    # حجم 400 = يترفض
        (e12, 197, -0.22, 1.5, 1.6, "D", 0.4, 0.02, 900, "t"),    # عقود مفتوحة 800 = يترفض
        (e12, 198, -0.27, 1.9, 2.0, "E", 0.4, 0.02, 1200, "t"),   # ✅
        (e19, 195, -0.20, 2.2, 2.4, "F", 0.4, 0.02, 3000, "t"),   # انتهاء أبعد
    ]
    oi = {"A": 9000, "B": 9000, "C": 9000, "D": 800, "E": 1500, "F": 9000}
    saved = (_pdr1h_option_rows, _opt_open_interest)
    _pdr1h_option_rows = lambda t, put, spot, d1, d2: [x for x in fake_rows if d1 <= x[0] <= d2]
    _opt_open_interest = lambda t, x: oi[x[5]]
    try:
        got = wkopt_pick_option("TEST", 200, True)
        assert got and got[0][5] == "E" and got[2] == 1500, got
        print("✅ العقد: أكثر من 10 أيام + حجم فوق 500 + مفتوحة فوق 1000 + دلتا فوق 0.12 → E")
        if WKOPT_MIN_PRICE and WKOPT_MAX_PRICE:
            assert wkopt_in_range(WKOPT_MIN_PRICE) and not wkopt_in_range(WKOPT_MAX_PRICE + 1)
            print(f"✅ نطاق السعر {WKOPT_MIN_PRICE}$-{WKOPT_MAX_PRICE}$")
        else:
            assert wkopt_in_range(5) and wkopt_in_range(900)
            print("✅ بدون شرط سعر: كل قائمة المراقبة")
        r = {"open": 201.0, "high": 203.5, "low": 199.8, "close": 200.4, "depth": 0.9,
             "start": pd.Timestamp.now(tz=NY).floor("h"), "end": pd.Timestamp.now(tz=NY),
             "closes_beyond": 0, "first_touch": True}
        print()
        print(wkopt_message("TEST", "high", 201.7, today, r, got))
    finally:
        _pdr1h_option_rows, _opt_open_interest = saved


def pw4h_now(symbols, send=False):
    """تجربة حقيقية لفريم 4 ساعات: يطلع كل شموع السحب (دعم ومقاومة) من بداية هالأسبوع
    على قائمة المراقبة، بدون شرط وقت التنبيه وبدون ملف المرسل. send=True يرسلها تيليجرام."""
    now = pd.Timestamp.now(tz=NY)
    wk0 = _week_start(now)                      # بالويكند = الأسبوع اللي خلص (الاثنين اللي راح)
    print(f"تجربة سحب سيولة الأسبوع السابق - 4 ساعات | الأسبوع من {wk0:%Y-%m-%d} | {len(symbols)} رمز")
    found = 0
    for t, df in download_batches(symbols, 100, period="20d", interval=f"{GAP_BASE_MIN}m", prepost=True):
        try:
            df = to_ny(df)[OHLC]
            lv4 = prev_week_ext_levels(df, wk0)
            if not lv4:
                continue
            c4h = only_closed(to_frame(df, 240, overnight=False), df.index.max(), now)
            c4h = c4h[(c4h.index >= wk0) & (c4h.index < wk0 + pd.Timedelta(days=7))]
            for i in range(len(c4h)):
                part = c4h.iloc[:i + 1]
                for side in ("low", "high"):
                    fn = sweep_check(side, PW4H_WICK_ONLY)
                    lvl, lvl_day = lv4[side]
                    r = fn(part, lvl, wk0, wick_only=PW4H_WICK_ONLY)
                    if r:
                        found += 1
                        msg = with_gamma(_pwl_message(t, side, lvl, lvl_day, r, frame="فريم 4 ساعات",
                                                      trade=True), t, r["close"])
                        print(msg + "\n")
                        if send:
                            send_telegram("🧪 تجربة\n" + msg, kind="sweep", sym=t)
        except Exception as e:
            print(f"{t}: خطأ - {e}")
    print(f"المجموع: {found} شمعة سحب")


def pwl_self_test():
    """يجرب (1ك) الدعم والمقاومة على بيانات مصنوعة بدون نت."""
    ny = ZoneInfo(NY)
    # يومي: الأسبوع السابق قاعه 100 يوم الأربعاء، وقمته 106 يوم الجمعة
    days = pd.to_datetime(["2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08", "2026-10-09",
                           "2026-10-12"])
    daily = pd.DataFrame({"Open": [105, 104, 102, 103, 104, 103], "High": [105.5, 105, 104, 105, 106, 107],
                          "Low": [103, 102, 100, 101, 102, 99], "Close": [104, 103, 101, 104, 105, 102]},
                         index=days)
    pw0, wk = datetime(2026, 10, 5).date(), datetime(2026, 10, 12).date()
    lvl, day = prev_week_low(daily, pw0, wk)
    assert lvl == 100 and str(day) == "2026-10-07", (lvl, day)
    hi, hday = prev_week_high(daily, pw0, wk)
    assert hi == 106 and str(hday) == "2026-10-09", (hi, hday)
    print(f"✅ قاع الأسبوع السابق {lvl} ({day}) | قمته {hi} ({hday}) - شموع هالأسبوع ما دخلت")

    wk0 = pd.Timestamp("2026-10-12", tz=ny)
    idx = pd.to_datetime(["2026-10-13 10:00", "2026-10-13 11:00", "2026-10-13 12:00"]).tz_localize(ny)

    def frame(o, h, l, c):
        f = pd.DataFrame({"Open": o, "High": h, "Low": l, "Close": c}, index=idx)
        f["end"] = f.index + pd.Timedelta(hours=1)
        return f

    # ---- الدعم ----
    ok = frame([102, 101, 100.5], [102.5, 101.5, 101.8], [101, 100.2, 99.4], [101.2, 100.6, 101.5])
    r = check_pwl_1h(ok, lvl, wk0)
    assert r and r["first_touch"], r
    print(f"✅ دعم: نزل لـ {r['low']} وقفل {r['close']} فوق {lvl} (أول لمس)")
    bad = ok.copy(); bad.iloc[-1, bad.columns.get_loc("Close")] = 99.8
    assert check_pwl_1h(bad, lvl, wk0) is None
    nos = ok.copy(); nos.iloc[-1, nos.columns.get_loc("Low")] = 100.1
    assert check_pwl_1h(nos, lvl, wk0) is None
    assert check_pwl_1h(ok, lvl, pd.Timestamp("2026-10-19", tz=ny)) is None
    print("✅ دعم: قفل تحته / ما نزل تحته / أسبوع قديم = ما فيه تنبيه")

    # ---- المقاومة ----
    ok = frame([104, 105, 105.5], [104.8, 105.8, 106.7], [103.5, 104.5, 105], [104.9, 105.4, 105.2])
    r = check_pwh_1h(ok, hi, wk0)
    assert r and r["first_touch"], r
    print(f"✅ مقاومة: طلع لـ {r['high']} وقفل {r['close']} تحت {hi} (أول لمس)")
    bad = ok.copy(); bad.iloc[-1, bad.columns.get_loc("Close")] = 106.2
    assert check_pwh_1h(bad, hi, wk0) is None
    nos = ok.copy(); nos.iloc[-1, nos.columns.get_loc("High")] = 105.9
    assert check_pwh_1h(nos, hi, wk0) is None
    assert check_pwh_1h(ok, hi, pd.Timestamp("2026-10-19", tz=ny)) is None
    print("✅ مقاومة: قفل فوقها / ما طلع فوقها / أسبوع قديم = ما فيه تنبيه")

    # ---- 4 ساعات: الذيل بس (الافتتاح والإغلاق بجهة المستوى) ----
    assert check_pwh_1h(ok, hi, wk0, wick_only=True)          # افتتح 105.5 تحت 106 = ذيل بس
    body = ok.copy(); body.iloc[-1, body.columns.get_loc("Open")] = 106.3
    assert check_pwh_1h(body, hi, wk0) and check_pwh_1h(body, hi, wk0, wick_only=True) is None
    sup = frame([102, 101, 100.5], [102.5, 101.5, 101.8], [101, 100.2, 99.4], [101.2, 100.6, 101.5])
    assert check_pwl_1h(sup, lvl, wk0, wick_only=True)
    sbody = sup.copy(); sbody.iloc[-1, sbody.columns.get_loc("Open")] = 99.7
    assert check_pwl_1h(sbody, lvl, wk0) and check_pwl_1h(sbody, lvl, wk0, wick_only=True) is None
    print("✅ 4 ساعات: الجسم دخل تحت الدعم / فوق المقاومة = ما فيه تنبيه، الذيل بس = تنبيه")

    # ---- 4 ساعات بدون الجلسة الليلية ----
    m15 = pd.date_range("2026-10-13 00:00", "2026-10-13 23:45", freq="15min", tz=ny)
    raw = pd.DataFrame({"Open": 100.0, "High": 101.0, "Low": 99.0, "Close": 100.0}, index=m15)
    c4 = to_frame(raw, 240, overnight=False)
    hrs = [f"{x:%H:%M}" for x in c4.index]
    assert hrs == ["04:00", "08:00", "12:00", "16:00"], hrs
    print(f"✅ شموع 4 ساعات بدون الليلي (نيويورك): {', '.join(hrs)}")

    # ---- مستويات الأسبوع السابق: بري + ماركت + أفتر، والليلي ما يدخل ----
    m15w = pd.date_range("2026-10-05 00:00", "2026-10-13 23:45", freq="15min", tz=ny)
    w = pd.DataFrame({"Open": 100.0, "High": 101.0, "Low": 99.0, "Close": 100.0}, index=m15w)
    w.loc[pd.Timestamp("2026-10-06 05:00", tz=ny), ["High", "Low"]] = [101.5, 97.0]   # بري = يدخل
    w.loc[pd.Timestamp("2026-10-07 18:00", tz=ny), ["High", "Low"]] = [104.0, 99.5]   # أفتر = يدخل
    w.loc[pd.Timestamp("2026-10-08 22:00", tz=ny), ["High", "Low"]] = [110.0, 90.0]   # ليلي = ما يدخل
    w.loc[pd.Timestamp("2026-10-13 10:00", tz=ny), ["High", "Low"]] = [120.0, 80.0]   # هالأسبوع = ما يدخل
    ev = prev_week_ext_levels(w, wk0)
    assert ev["low"] == (97.0, datetime(2026, 10, 6).date()), ev
    assert ev["high"] == (104.0, datetime(2026, 10, 7).date()), ev
    print(f"✅ الأسبوع السابق (بري + أفتر بدون الليلي): قاع {ev['low'][0]} | قمة {ev['high'][0]}")
    print()
    print(_pwl_message("TEST", "high", hi, hday, r))


# ================== العقود: الدلتا والسعر واختيار العقد (يستخدمها سحب الجمعة/الاثنين) ==================


def _bs_delta(spot, strike, years, iv, put):
    """دلتا بلاك شولز (لو المصدر ما أعطى الدلتا)."""
    if not (spot and strike and years > 0 and iv and iv > 0.01):
        return None
    d1 = (math.log(spot / strike) + (PDR_OPT_RATE + iv * iv / 2) * years) / (iv * math.sqrt(years))
    n = 0.5 * (1 + math.erf(d1 / math.sqrt(2)))
    return n - 1 if put else n


def _bs_price(spot, strike, years, iv, put):
    """سعر بلاك شولز للعقد."""
    if not (spot and strike and years > 0 and iv and iv > 0.01):
        return None
    sq = iv * math.sqrt(years)
    d1 = (math.log(spot / strike) + (PDR_OPT_RATE + iv * iv / 2) * years) / sq
    d2 = d1 - sq
    N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    disc = strike * math.exp(-PDR_OPT_RATE * years)
    return disc * N(-d2) - spot * N(-d1) if put else spot * N(d1) - disc * N(d2)


def _opt_years(exp):
    end = pd.Timestamp(exp).tz_localize(NY) + pd.Timedelta(hours=16)
    return max((end - pd.Timestamp.now(tz=NY)).total_seconds(), 60) / (365 * 24 * 3600)


def _pdr1h_option_rows(t, put, spot, d1, d2):
    """كل العقود بين التاريخين: (انتهاء، سترايك، دلتا، bid، ask، رمز، IV، جاما، حجم التداول، المصدر)."""
    import re
    rows = []
    if ALPACA_KEY and ALPACA_SECRET:
        try:
            token = None
            for _ in range(10):
                p = {"feed": "indicative", "type": "put" if put else "call", "limit": 1000,
                     "expiration_date_gte": d1.isoformat(), "expiration_date_lte": d2.isoformat()}
                if token:
                    p["page_token"] = token
                _alpaca_wait()
                js = _alpaca_data_get(f"/v1beta1/options/snapshots/{t}", p)
                for sym, sn in (js.get("snapshots") or {}).items():
                    m = re.match(r"^(.+?)(\d{6})([CP])(\d{8})$", sym)
                    if not m:
                        continue
                    exp = datetime.strptime(m.group(2), "%y%m%d").date()
                    k = int(m.group(4)) / 1000
                    q, g = sn.get("latestQuote") or {}, sn.get("greeks") or {}
                    iv = sn.get("impliedVolatility")
                    delta = g.get("delta")
                    if delta is None:
                        delta = _bs_delta(spot, k, _opt_years(exp), iv, put)
                    vol = (sn.get("dailyBar") or {}).get("v") or 0
                    rows.append((exp, k, delta, q.get("bp"), q.get("ap"), sym, iv, g.get("gamma"), vol, "Alpaca"))
                token = js.get("next_page_token")
                if not token:
                    break
        except Exception as e:
            log(f"عقد الساعة: {t}: Alpaca: {e}")
    if not rows:
        try:
            import yfinance as yf
            with _YF_LOCK:
                tk = yf.Ticker(t)
                exps = [e for e in (tk.options or []) if d1 <= pd.Timestamp(e).date() <= d2]
            for e in sorted(exps)[:4]:
                with _YF_LOCK:
                    ch = tk.option_chain(e)
                df = ch.puts if put else ch.calls
                exp = pd.Timestamp(e).date()
                yrs = _opt_years(exp)
                for x in df.itertuples():
                    iv = float(x.impliedVolatility or 0)
                    vol = 0 if pd.isna(x.volume) else int(x.volume)
                    _OI_CACHE[x.contractSymbol] = 0 if pd.isna(x.openInterest) else int(x.openInterest)
                    rows.append((exp, float(x.strike), _bs_delta(spot, float(x.strike), yrs, iv, put),
                                 float(x.bid or 0), float(x.ask or 0), x.contractSymbol, iv, None, vol,
                                 "Yahoo (دلتا محسوبة)"))
        except Exception as e:
            log(f"عقد الساعة: {t}: Yahoo: {e}")
    return rows


_OI_CACHE = {}


def _opt_open_interest(t, x):
    """العقود المفتوحة للعقد. ألباكا ما يعطيها بالسناب شوت، فنجيبها من ياهو (سلسلة الانتهاء مرة وحدة)."""
    sym = x[5]
    if sym in _OI_CACHE:
        return _OI_CACHE[sym]
    try:
        import yfinance as yf
        with _YF_LOCK:
            ch = yf.Ticker(t).option_chain(x[0].isoformat())
        for df in (ch.calls, ch.puts):
            for y in df.itertuples():
                _OI_CACHE[y.contractSymbol] = 0 if pd.isna(y.openInterest) else int(y.openInterest)
    except Exception as e:
        log(f"العقود المفتوحة: {t} {x[0]}: {e}")
    if len(_OI_CACHE) > 50000:
        _OI_CACHE.clear()
    return _OI_CACHE.setdefault(sym, None)


# ================== تمركز القاما (يستخدمه سحب السيولة) ==================
def _bs_gamma(spot, strike, years, iv):
    """قاما بلاك شولز (نفسها للكول والبوت)."""
    if not (spot and strike and years > 0 and iv and iv > 0.01):
        return 0.0
    sq = iv * math.sqrt(years)
    d1 = (math.log(spot / strike) + (PDR_OPT_RATE + iv * iv / 2) * years) / sq
    return math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi) / (spot * sq)


GAMMA_CACHE_MIN = 30             # سلسلة العقود لكل سهم تتخزن كذا دقيقة (الإنفيرجن ينبه كثير، فما نعيد التحميل كل مرة)
_GAMMA_CACHE = {}                # الرمز -> (وقت التحميل، [(سترايك، انتهاء، IV، مفتوحة، كول؟)]، الانتهاءات)


def _gamma_chain(t):
    """سلسلة عقود ياهو لأقرب الانتهاءات (محفوظة GAMMA_CACHE_MIN دقيقة)."""
    hit = _GAMMA_CACHE.get(t)
    if hit and time.time() - hit[0] < GAMMA_CACHE_MIN * 60:
        return hit[1], hit[2]
    import yfinance as yf
    today = pd.Timestamp.now(tz=NY).date()
    last = today + timedelta(days=GAMMA_MAX_DTE)
    with _YF_LOCK:
        tk = yf.Ticker(t)
        exps = [e for e in (tk.options or []) if today <= pd.Timestamp(e).date() <= last]
    exps = sorted(exps)[:GAMMA_MAX_EXPS]
    chain = []
    for e in exps:
        with _YF_LOCK:
            ch = tk.option_chain(e)
        exp = pd.Timestamp(e).date()
        for df, is_call in ((ch.calls, True), (ch.puts, False)):
            for x in df.itertuples():
                oi = 0 if pd.isna(x.openInterest) else int(x.openInterest)
                iv = 0 if pd.isna(x.impliedVolatility) else float(x.impliedVolatility)
                if oi > 0 and iv > 0.01:
                    chain.append((float(x.strike), exp, iv, oi, is_call))
    if len(_GAMMA_CACHE) > 500:
        _GAMMA_CACHE.clear()
    _GAMMA_CACHE[t] = (time.time(), chain, exps)
    return chain, exps


def _gamma_rows(t, spot):
    """[(سترايك، سنوات، IV، العقود المفتوحة، كول؟)] داخل ±GAMMA_RANGE_PCT% من السعر، والانتهاءات المستخدمة."""
    chain, exps = _gamma_chain(t)
    lo, hi = spot * (1 - GAMMA_RANGE_PCT / 100), spot * (1 + GAMMA_RANGE_PCT / 100)
    yrs = {e: _opt_years(e) for e in {x[1] for x in chain}}
    rows = [(k, yrs[e], iv, oi, c) for k, e, iv, oi, c in chain if lo <= k <= hi]
    return rows, exps


def _gex_at(rows, s):
    """صافي القاما بالدولار لكل 1% حركة لو السعر = s."""
    tot = 0.0
    for k, yrs, iv, oi, is_call in rows:
        g = _bs_gamma(s, k, yrs, iv) * oi * 100 * s * s * 0.01
        tot += g if is_call else -g
    return tot


def _fmt_usd(v):
    a = abs(v)
    sgn = "-" if v < 0 else ""
    if a >= 1e9:
        return f"{sgn}{a / 1e9:.2f}B$"
    if a >= 1e6:
        return f"{sgn}{a / 1e6:.1f}M$"
    if a >= 1e3:
        return f"{sgn}{a / 1e3:.0f}K$"
    return f"{sgn}{a:.0f}$"


def gamma_block(t, spot):
    """نص تمركز القاما للتنبيه، أو "" لو ما فيه بيانات."""
    if not SWEEP_GAMMA or not spot:
        return ""
    rows, exps = _gamma_rows(t, float(spot))
    if not rows:
        return ""
    spot = float(spot)
    calls, puts = {}, {}
    for k, yrs, iv, oi, is_call in rows:
        g = _bs_gamma(spot, k, yrs, iv) * oi * 100 * spot * spot * 0.01
        d = calls if is_call else puts
        d[k] = d.get(k, 0.0) + g
    pct = lambda k: f"{(k / spot - 1) * 100:+.1f}%"
    lines = [f"🧲 تمركز القاما (أقرب {len(exps)} انتهاء، لين {pd.Timestamp(exps[-1]):%m-%d}):"]
    if calls:
        kc = max(calls, key=calls.get)
        lines.append(f"جدار الكول: {kc:g} ({pct(kc)}) — {_fmt_usd(calls[kc])}")
    if puts:
        kp = max(puts, key=puts.get)
        lines.append(f"جدار البوت: {kp:g} ({pct(kp)}) — {_fmt_usd(-puts[kp])}")
    total = {k: calls.get(k, 0.0) + puts.get(k, 0.0) for k in set(calls) | set(puts)}
    top = sorted(total, key=total.get, reverse=True)[:GAMMA_TOP_N]
    if top:
        lines.append("أعلى تمركز: " + " | ".join(f"{k:g} ({pct(k)})" for k in top))
    net = _gex_at(rows, spot)
    lines.append(f"صافي القاما: {_fmt_usd(net)} لكل 1% — "
                 + ("موجب ← حركة أهدى والسعر ينشد للسترايكات الكبيرة" if net >= 0
                    else "سالب ← الحركة أقوى وأسرع"))
    # نقطة الانقلاب: أقرب سعر للسعر الحالي يتغير عنده صافي القاما من سالب لموجب
    grid = [spot * (1 + i / 200) for i in range(-30, 31)]       # ±15% بخطوة 0.5%
    vals = [_gex_at(rows, s) for s in grid]
    flips = [(grid[i] + grid[i + 1]) / 2 for i in range(len(grid) - 1) if (vals[i] < 0) != (vals[i + 1] < 0)]
    if flips:
        f = min(flips, key=lambda x: abs(x - spot))
        lines.append(f"نقطة الانقلاب: {f:.2f} ({pct(f)}) — "
                     + ("السعر فوقها" if spot > f else "السعر تحتها"))
    return "\n".join(lines)


def with_gamma(msg, t, spot):
    """يضيف تمركز القاما للتنبيه (قبل سطر التنبيه ⚠️ لو موجود)."""
    try:
        g = gamma_block(t, spot)
    except Exception as e:
        log(f"تمركز القاما: {t}: {e}")
        return msg
    if not g:
        return msg
    if "\n" + WKOPT_CHECK_LINE in msg:                 # القاما قبل سطر "حلل السهم" عشان يكون بالأخير
        a, b = msg.rsplit("\n" + WKOPT_CHECK_LINE, 1)
        return a.rstrip() + "\n\n" + g + "\n\n" + WKOPT_CHECK_LINE + b
    if "\n⚠️" in msg:
        a, b = msg.rsplit("\n⚠️", 1)
        return a.rstrip() + "\n\n" + g + "\n\n⚠️" + b
    return msg + "\n\n" + g


# ================== (4ب) التجزئة العكسية ==================
def load_rsplits(tickers):
    """كل التجزئات العكسية آخر سنة.
    يرجع {الرمز: {"splits": [(التاريخ، النسبة، سعر الافتتاح يومها)], "last": آخر سعر}}"""
    out = {}
    for t, df in download_batches(tickers, UNIVERSE_BATCH, period="1y", interval="1d",
                                  prepost=False, actions=True):
        try:
            if "Stock Splits" not in df:
                continue
            sp = df["Stock Splits"].fillna(0)
            rev = sp[(sp > 0) & (sp < 1)]
            if rev.empty:
                continue
            splits = [(pd.Timestamp(i).date(), float(r), float(df.loc[i, "Open"]))
                      for i, r in rev.items()]
            out[t] = {"splits": splits, "last": float(df["Close"].iloc[-1])}
        except Exception:
            continue
    free_memory()
    return out


def _rsplit_line(t, info, split):
    d, ratio, opn = split
    return (f"• ${t}{sec_tag(t)}\n"
            f"   تاريخ التجزئة: {d:%Y-%m-%d} | النسبة: كل {1 / ratio:g} أسهم = سهم\n"
            f"   افتتح بعد التجزئة على: {opn:.2f}$ | السعر الحين: {info['last']:.2f}$\n"
            f"   عدد التجزئات العكسية آخر سنة: {len(info['splits'])}")


def _send_rsplit_list(title, items):
    """items = [(الرمز، البيانات، التجزئة)]. يرسلها على رسايل (كل رسالة 15 سهم)."""
    items = sorted(items, key=lambda x: x[2][0], reverse=True)       # الأحدث فوق
    for i in range(0, len(items), 15):
        part = items[i:i + 15]
        head = title + (f" ({i // 15 + 1})" if len(items) > 15 else "")
        send_telegram(head + "\n\n" + "\n\n".join(_rsplit_line(*x) for x in part), kind="rsplit")
        time.sleep(2)


def splits_between(data, start, end):
    """التجزئات اللي تاريخها من start لين end (تواريخ)."""
    return [(t, info, sp) for t, info in data.items() for sp in info["splits"]
            if start <= sp[0] <= end]


def scan_rsplit_new(data, already_sent):
    """يرسل التجزئات الجديدة بس. لو ما فيه جديد، ما يرسل شي."""
    today = pd.Timestamp.now(tz=NY).date()
    since = today - pd.Timedelta(days=RSPLIT_NEW_DAYS)
    new = []
    for t, info, sp in splits_between(data, since, today):
        key = f"{t}-{sp[0]:%Y-%m-%d}"
        if key in already_sent:
            continue
        already_sent.add(key)
        _append_line(RSPLIT_NEW_FILE, key)
        new.append((t, info, sp))
    if new:
        _send_rsplit_list(f"🆕 تجزئة عكسية جديدة - {len(new)} سهم", new)
    log(f"[{datetime.now():%H:%M}] التجزئة العكسية: {len(new)} سهم جديد")
    return new


def _rsplit_state():
    st = {}
    for line in _load_set(RSPLIT_STATE_FILE):
        k, _, v = line.partition("=")
        st[k] = v
    return st


def _save_rsplit_state(st):
    try:
        with open(RSPLIT_STATE_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(f"{k}={v}" for k, v in st.items()) + "\n")
    except Exception:
        pass


def rsplit_job(state, new_sent, force=False):
    """مرة باليوم (أيام السوق، بعد 10 الصبح نيويورك):
    الجديد كل يوم + قائمة الأسبوع يوم الجمعة."""
    now = pd.Timestamp.now(tz=NY)
    today = now.date()
    if not force and (now.weekday() >= 5 or now.hour < RSPLIT_CHECK_AFTER_NY):
        return
    if not force and state.get("day") == str(today):
        return
    tickers = build_universe("التجزئة العكسية", 0.01, 100_000, 0, include_nyse=False)
    data = load_rsplits(tickers)
    log(f"التجزئة العكسية: {len(data)} سهم سوى تجزئة عكسية آخر سنة")

    scan_rsplit_new(data, new_sent)

    week = f"{today.isocalendar()[0]}-W{today.isocalendar()[1]:02d}"
    if RSPLIT_WEEKLY and now.weekday() == 4 and state.get("week") != week:     # الجمعة
        items = splits_between(data, today - pd.Timedelta(days=6), today)
        if items:
            _send_rsplit_list(f"📋 قائمة الأسبوع - تجزئات عكسية آخر 7 أيام ({len(items)} سهم)", items)
        state["week"] = week

    state["day"] = str(today)
    _save_rsplit_state(state)
    free_memory()


# ================== (11) سحب قمة الجمعة يوم الاثنين ثم سحب دعم الأسبوع السابق (فريم 4 ساعات) → كول ==================
#   1) يوم الاثنين: السعر يسحب قمة الجمعة (ذيل فوقها) ويرجع يختبرها وما يخترقها (ولا شمعة 4 ساعات تقفل فوقها)
#   2) بعدها ينزل لقاع الأسبوع السابق (الدعم) ويسحب السيولة: شمعة 4 ساعات ذيلها تحت الدعم وإغلاقها فوقه
#   3) التنبيه: كول، الأهداف (قمة الجمعة ثم قمة الاثنين)، الوقف تحت شمعة السحب، وعقد كول مدته أسبوعين
#   الأسهم: القائمة الموحدة (WATCH_SYMBOLS) اللي سعرها 100$-400$
ENABLE_FRIMON = False            # True = شغال | False = مطفي
FRIMON_MIN_PRICE = 100
FRIMON_MAX_PRICE = 400
FRIMON_OPT_DTE = 14              # مدة العقد: أسبوعين (يختار أقرب انتهاء لـ 14 يوم)
FRIMON_OPT_MIN_DTE = 10          # يدوّر بين 10 و18 يوم
FRIMON_OPT_MAX_DTE = 18
FRIMON_OPT_MIN_VOLUME = 300      # حجم التداول في العقد فوق 300
FRIMON_OPT_MIN_OI = 1000         # العقود المفتوحة (الكمية غير إغلاق المركز) فوق 1000
FRIMON_OPT_MIN_DELTA = 0.15      # الدلتا فوق 0.1500
FRIMON_SCAN_AFTER_MIN = 3        # يفحص بعد إغلاق شمعة 4 ساعات بكم دقيقة (1:30 و 4:00 العصر نيويورك)
FRIMON_SCAN_WINDOW_MIN = 40
FRIMON_TEST_ID = "1"             # رسالة تجريبية مرة وحدة بعد الرفع — غيّر الرقم لو تبي وحدة ثانية
FRIMON_SENT_FILE = os.path.join(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "."), "frimon_sent.txt")


def frimon_resistance_above(daily, this_wk, level, bars=2):
    """أقرب مقاومة يومية فوق المستوى: قمة شمعة يومية أعلى من الشمعتين قبلها والشمعتين بعدها
    (قبل الأسبوع الحالي). يرجع السعر أو None."""
    d = daily[[pd.Timestamp(i).date() < this_wk for i in daily.index]]
    hi = d["High"].astype(float).tolist()
    piv = [hi[i] for i in range(bars, len(hi) - bars)
           if hi[i] >= max(hi[i - bars:i]) and hi[i] >= max(hi[i + 1:i + 1 + bars])]
    above = [h for h in piv if h > level * 1.002]
    return min(above) if above else None


def frimon_check(daily, c4, now):
    """daily = شموع يومية (آخر شهر)، c4 = شموع 4 ساعات (mkt4h_candles)، now = الوقت (نيويورك).
    يرجع تفاصيل النموذج لو تحقق على آخر شمعة 4 ساعات مقفلة، وإلا None."""
    if daily is None or daily.empty or c4 is None or c4.empty:
        return None
    this_wk = _week_start(now).date()
    prev_wk = this_wk - timedelta(days=7)
    pw = _prev_week_rows(daily, prev_wk, this_wk)
    if pw.empty:
        return None
    fri = pw.iloc[-1]                                   # آخر يوم بالأسبوع السابق (الجمعة)
    fh, fri_day = float(fri["High"]), pd.Timestamp(pw.index[-1]).date()
    lows = pw["Low"].astype(float)
    pwl, pwl_day = float(lows.min()), pd.Timestamp(lows.idxmin()).date()

    c = c4[(c4["end"] <= now).values]                   # الشموع المقفلة بس
    days = pd.Series([pd.Timestamp(i).date() for i in c.index], index=c.index)
    c = c[(days >= this_wk).values]
    if len(c) < 2:
        return None
    first_day = min(pd.Timestamp(i).date() for i in c.index)
    if first_day.weekday() != 0:                        # لازم يوم الاثنين موجود (مو عطلة)
        return None
    cdays = [pd.Timestamp(i).date() for i in c.index]
    mon = c[[d == first_day for d in cdays]]
    if mon.empty or float(mon["High"].max()) <= fh:     # 1) سحب قمة الجمعة يوم الاثنين
        return None
    mon_high = float(mon["High"].max())
    sweep_i = list(c.index).index(mon["High"].astype(float).idxmax())
    # إعادة اختبار وعدم اختراق: ولا شمعة من الاثنين لين الحين قفلت فوق قمة الجمعة
    if (c["Close"].astype(float) > fh).any():
        return None
    sig = c.iloc[-1]                                    # 2) آخر شمعة مقفلة = شمعة سحب الدعم
    if len(c) - 1 <= sweep_i:
        return None                                     # لازم بعد سحب القمة
    lo, cl = float(sig["Low"]), float(sig["Close"])
    if not (lo < pwl < cl):
        return None
    # أول سحب للدعم بعد سحب القمة (ما نعيد على شمعة ثانية)
    mid = c.iloc[sweep_i + 1:-1]
    if (mid["Low"].astype(float) < pwl).any():
        return None
    if not (FRIMON_MIN_PRICE <= cl <= FRIMON_MAX_PRICE):
        return None
    pwh = float(pw["High"].astype(float).max())
    near = frimon_resistance_above(daily, this_wk, fh)
    cands = [("مقاومة الجمعة", fh), ("قمة الأسبوع السابق", pwh)]
    if near:
        cands.insert(1, ("أقرب مقاومة يومية فوقها", near))
    targets = []
    for name, px in sorted(cands, key=lambda x: x[1]):
        if px > cl and (not targets or px - targets[-1][1] > cl * 0.002):
            targets.append((name, px))
    if not targets:
        return None
    return {"fh": fh, "fri_day": fri_day, "pwl": pwl, "pwl_day": pwl_day, "mon_high": mon_high,
            "entry": cl, "stop": lo, "sig_start": c.index[-1], "sig_end": sig["end"], "targets": targets}


def _frimon_opt_px(c, spot, new_spot):
    """سعر العقد التقديري لو السهم راح لـ new_spot (بلاك شولز بنفس IV، بدون حساب مرور الوقت)."""
    exp, k, delta, bid, ask, sym, iv, gamma = c[:8]
    mid = (bid + ask) / 2 if bid else ask
    yrs = _opt_years(exp)
    p0, p1 = _bs_price(spot, k, yrs, iv, False), _bs_price(new_spot, k, yrs, iv, False)
    if p0 is not None and p1 is not None:
        px = mid + (p1 - p0)
    else:
        ds = new_spot - spot
        px = mid + delta * ds + 0.5 * (gamma or 0) * ds * ds
    return max(round(px, 2), 0.01), mid


def frimon_pick_option(t, spot):
    """عقد كول: أقرب انتهاء لأسبوعين، حجم فوق 300، عقود مفتوحة فوق 1000، دلتا فوق 0.15.
    يرجع (العقد، الحجم، العقود المفتوحة) أو None."""
    today = pd.Timestamp.now(tz=NY).date()
    d1, d2 = today + timedelta(days=FRIMON_OPT_MIN_DTE), today + timedelta(days=FRIMON_OPT_MAX_DTE)
    ok = []
    for x in _pdr1h_option_rows(t, False, spot, d1, d2):
        exp, k, delta, bid, ask, sym, iv, gamma, vol, src = x
        if delta is None or delta <= FRIMON_OPT_MIN_DELTA or not ask:
            continue
        if (vol or 0) <= FRIMON_OPT_MIN_VOLUME:
            continue
        ok.append(x)
    if not ok:
        return None
    target = today + timedelta(days=FRIMON_OPT_DTE)
    exp = min({x[0] for x in ok}, key=lambda e: abs((e - target).days))
    cands = sorted((x for x in ok if x[0] == exp), key=lambda x: x[2])   # الأرخص (أقل دلتا) أول
    for x in cands:
        oi = _opt_open_interest(t, x) or 0
        if oi > FRIMON_OPT_MIN_OI:
            return x, x[8], oi
    return None


def frimon_message(t, r, opt):
    entry, stop = r["entry"], r["stop"]
    risk = entry - stop
    lines = [f"🟢 كول — سحب قمة الجمعة ثم سحب دعم الأسبوع السابق (فريم 4 ساعات)",
             f"السهم: ${t}{sec_tag(t, ' — ')}",
             f"قمة الجمعة ({r['fri_day']:%m-%d}): {r['fh']:.2f} ← انسحبت يوم الاثنين ({r['mon_high']:.2f}) وما انخترقت",
             f"دعم الأسبوع السابق ({r['pwl_day']:%m-%d}): {r['pwl']:.2f} ← انسحب والإغلاق فوقه",
             f"شمعة السحب: {r['sig_start'].tz_convert(LOCAL_TZ):%m-%d %H:%M} (توقيتك)",
             "",
             f"🛑 وقف الخسارة: {stop:.2f} (تحت شمعة سحب الدعم) — {risk / entry * 100:.1f}%"]
    for i, (name, px) in enumerate(r["targets"], 1):
        lines.append(f"🎯 الهدف {i}: {px:.2f} — +{(px / entry - 1) * 100:.1f}%"
                     + (f" | {(px - entry) / risk:.1f}R" if risk > 0 else ""))
    lines.append("")
    if opt:
        c, vol, oi = opt
        exp, k, delta, bid, ask, sym, iv = c[:7]
        days = (exp - pd.Timestamp.now(tz=NY).date()).days
        stop_px, mid = _frimon_opt_px(c, entry, stop)
        lines += [f"📄 العقد: {t} كول {k:g} — انتهاء {exp:%Y-%m-%d} ({days} يوم)",
                  f"السعر الحين: {mid:.2f}$ (العقد كامل {mid * 100:,.0f}$) | بيد {bid or 0:.2f} / أسك {ask:.2f}",
                  f"الدلتا: {delta:.4f}" + (f" | IV: {iv * 100:.0f}%" if iv else ""),
                  f"حجم التداول: {int(vol):,} | العقود المفتوحة: {int(oi):,}",
                  f"🛑 وقف العقد: {stop_px:.2f}$ ({(stop_px / mid - 1) * 100:+.0f}%) لو السهم وصل {stop:.2f}"]
        for i, (name, px) in enumerate(r["targets"], 1):
            tp, _ = _frimon_opt_px(c, entry, px)
            lines.append(f"🎯 العقد عند الهدف {i} ({px:.2f}): تقريباً {tp:.2f}$ ({(tp / mid - 1) * 100:+.0f}%)")
        lines.append("(أسعار العقد عند الوقف والأهداف تقديرية — بلاك شولز بنفس IV، وما تحسب مرور الوقت)")
    else:
        lines.append(f"📄 العقد: ما لقيت كول بالشروط (أسبوعين، حجم فوق {FRIMON_OPT_MIN_VOLUME}، "
                     f"عقود مفتوحة فوق {FRIMON_OPT_MIN_OI:,}، دلتا فوق {FRIMON_OPT_MIN_DELTA:.4f})")
    lines += ["", "⚠️ ليست توصية بيع أو شراء — للتعليم والتداول الوهمي فقط."]
    return "\n".join(lines)


def frimon_scan(symbols, sent, now=None):
    now = now or pd.Timestamp.now(tz=NY)
    wk = f"{now.isocalendar()[0]}-W{now.isocalendar()[1]:02d}"
    daily = {t: df for t, df in download_batches(symbols, 100, period="6mo", interval="1d", prepost=False)}
    cands = [t for t, df in daily.items()
             if FRIMON_MIN_PRICE * 0.9 <= float(df["Close"].iloc[-1]) <= FRIMON_MAX_PRICE * 1.1
             and f"{t}-{wk}" not in sent]
    hits = 0
    for t, df in download_batches(cands, 50, period="10d", interval="30m", prepost=False):
        try:
            r = frimon_check(daily[t], mkt4h_candles(df), now)
            if not r:
                continue
            key = f"{t}-{wk}"
            sent.add(key)
            _append_line(FRIMON_SENT_FILE, key)
            opt = None
            try:
                opt = frimon_pick_option(t, r["entry"])
            except Exception as e:
                log(f"سحب الجمعة/الاثنين: {t}: العقد: {e}")
            send_telegram(frimon_message(t, r, opt), kind="frimon")
            hits += 1
        except Exception as e:
            log(f"سحب الجمعة/الاثنين: {t}: {e}")
    log(f"[{datetime.now():%H:%M}] سحب الجمعة/الاثنين: فحص {len(cands)} سهم — {hits} تنبيه")
    free_memory()


def frimon_send_test_once():
    """يرسل تنبيه تجريبي للقسم مرة وحدة (يتذكرها في /data عشان ما تتكرر مع كل تشغيل)."""
    marker = os.path.join(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "."), "frimon_test_sent.txt")
    try:
        with open(marker, encoding="utf-8") as f:
            if f.read().strip() == FRIMON_TEST_ID:
                return
    except Exception:
        pass
    tz = NY
    now = pd.Timestamp.now(tz=tz)
    r = {"fh": 156.00, "fri_day": (now - pd.Timedelta(days=5)).date(), "pwl": 147.50,
         "pwl_day": (now - pd.Timedelta(days=8)).date(), "mon_high": 157.20, "entry": 148.40,
         "stop": 147.00, "sig_start": now.floor("h"),
         "targets": [("مقاومة الجمعة", 156.00), ("أقرب مقاومة يومية فوقها", 159.40), ("قمة الأسبوع السابق", 161.80)]}
    exp = (now + pd.Timedelta(days=14)).date()
    fake = (exp, 155.0, 0.32, 1.80, 1.95, "TEST", 0.38, 0.03, 850, "test")
    send_telegram("🧪 رسالة تجريبية - هذا مو تنبيه حقيقي (السهم والأرقام وهمية)\n\n"
                  + frimon_message("TEST", r, (fake, 850, 2400))
                  + "\n\nلو وصلتك هالرسالة، تنبيهات القسم الحقيقية بتوصل لنفس المكان.", kind="frimon")
    try:
        with open(marker, "w", encoding="utf-8") as f:
            f.write(FRIMON_TEST_ID)
    except Exception as e:
        log(f"سحب الجمعة/الاثنين: ما قدرت أحفظ علامة الرسالة التجريبية: {e}")


def frimon_run_forever():
    frimon_send_test_once()
    sent = _load_set(FRIMON_SENT_FILE)
    done = set()
    symbols = stocks_only(WATCH_SYMBOLS)
    log(f"سحب الجمعة/الاثنين (4 ساعات): بدأ — {len(symbols)} سهم من القائمة، السعر {FRIMON_MIN_PRICE}$-{FRIMON_MAX_PRICE}$")
    while True:
        try:
            now = pd.Timestamp.now(tz=NY)
            if now.weekday() < 5:
                for end_m in (_MKT4H_SPLIT, _MKT4H_END):
                    end = now.normalize() + pd.Timedelta(minutes=end_m)
                    key = f"{now.date()}-{end_m}"
                    if (key not in done and end + pd.Timedelta(minutes=FRIMON_SCAN_AFTER_MIN) <= now
                            <= end + pd.Timedelta(minutes=FRIMON_SCAN_WINDOW_MIN)):
                        done.add(key)
                        frimon_scan(symbols, sent, now)
        except Exception as e:
            log(f"سحب الجمعة/الاثنين: خطأ {e}")
        time.sleep(60)


def frimon_self_test():
    """python short_bot.py --frimontest — يجرب النموذج على بيانات وهمية بدون نت."""
    tz = NY
    days = pd.to_datetime(["2026-10-15", "2026-10-16", "2026-10-19", "2026-10-20", "2026-10-21",
                           "2026-10-22", "2026-10-23",
                           "2026-10-26", "2026-10-27", "2026-10-28", "2026-10-29", "2026-10-30"]).tz_localize(tz)
    daily = pd.DataFrame({"Open":  [155, 156, 157, 158, 157, 156, 156, 158, 152, 151, 153, 154],
                          "High":  [156, 157, 159.4, 158, 157.5, 157, 158, 161.8, 154, 152, 155, 156],
                          "Low":   [154, 155, 156, 156, 155, 155, 155, 151, 147.5, 149, 150, 152],
                          "Close": [156, 157, 158, 157, 156, 156, 157, 152, 151, 151, 154, 155]}, index=days)
    rows = []   # (اليوم، بداية الشمعة، O,H,L,C)
    data = [("2026-11-02", "09:30", 155, 157.2, 154.5, 155.5),   # الاثنين: سحب قمة الجمعة 156
            ("2026-11-02", "13:30", 155.5, 156.3, 153, 153.5),   # إعادة اختبار وما قفل فوقها
            ("2026-11-03", "09:30", 153.5, 154, 150, 150.5),
            ("2026-11-03", "13:30", 150.5, 151, 148.5, 149),
            ("2026-11-04", "09:30", 149, 150, 147.0, 148.4)]     # سحب دعم 147.5 والإغلاق فوقه
    for d, h, o, hi, lo, cl in data:
        st = pd.Timestamp(f"{d} {h}").tz_localize(tz)
        end = st + (pd.Timedelta(hours=4) if h == "09:30" else pd.Timedelta(minutes=150))
        rows.append((st, o, hi, lo, cl, end))
    c4 = pd.DataFrame([{"Open": o, "High": hi, "Low": lo, "Close": cl, "end": e, "n": 8, "need": 8}
                       for st, o, hi, lo, cl, e in rows], index=[r[0] for r in rows])
    now = pd.Timestamp("2026-11-04 13:35").tz_localize(tz)
    r = frimon_check(daily, c4, now)
    print("النموذج:", "✅ تحقق" if r else "❌ ما تحقق")
    if r:
        fake = (pd.Timestamp("2026-11-18").date(), 155.0, 0.32, 1.80, 1.95, "TEST261118C00155000",
                0.38, 0.03, 850, "test")
        print(frimon_message("TEST", r, (fake, 850, 2400)))
    # لو شمعة قفلت فوق قمة الجمعة → ما ينبه
    c4b = c4.copy(); c4b.iloc[1, c4b.columns.get_loc("Close")] = 156.5
    print("إغلاق فوق قمة الجمعة:", "❌ ما ينبه (صح)" if not frimon_check(daily, c4b, now) else "⚠️ نبه (غلط)")


# ================== (6) كشف خوارزميات التنفيذ - ألباكا ==================
from collections import deque

ALGO_URL = "https://data.alpaca.markets/v2/stocks/trades"


def trading_hours(now=None):
    """4 الفجر - 8 بالليل نيويورك، أيام الأسبوع."""
    now = now or pd.Timestamp.now(tz=NY)
    m = now.hour * 60 + now.minute
    return now.weekday() < 5 and 4 * 60 <= m <= 20 * 60


_alpaca_lock = threading.Lock()
_alpaca_next = [0.0]
ALPACA_MIN_GAP_SEC = 0.35    # ≈ 170 طلب بالدقيقة (حد الباقة المجانية 200) - للقسمين مع بعض


def _alpaca_wait():
    """القسمين (الصغيرة والكبيرة) يشتركون بنفس حد الطلبات، فنوزعها بالدور."""
    with _alpaca_lock:
        now = time.time()
        wait = _alpaca_next[0] - now
        _alpaca_next[0] = max(now, _alpaca_next[0]) + ALPACA_MIN_GAP_SEC
    if wait > 0:
        time.sleep(wait)


def fetch_alpaca_trades(symbols, start, end=None):
    """الصفقات من وقت start لين الحين لمجموعة أسهم. يرجع {الرمز: [صفقات]} أو None لو فشل."""
    headers = {"APCA-API-KEY-ID": ALPACA_KEY, "APCA-API-SECRET-KEY": ALPACA_SECRET}
    params = {"symbols": ",".join(symbols), "start": start.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
              "feed": ALGO_FEED, "limit": 10000, "sort": "asc"}
    if end is not None:
        params["end"] = end.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    out = {}
    for _ in range(20):                          # صفحات (لو الصفقات كثيرة)
        _alpaca_wait()
        try:
            r = requests.get(ALGO_URL, headers=headers, params=params, timeout=20)
        except Exception as e:
            log("ألباكا: فشل الاتصال -", e)
            return None
        if r.status_code == 403 and "subscription" in r.text.lower():
            log("ألباكا: الاشتراك ما يسمح ببيانات sip اللحظية - تأكد إن المفاتيح من الحساب المشترك،"
                " أو حط ALGO_DELAY_MIN = 16 في Railway")
            return None
        if r.status_code in (401, 403):
            log(f"ألباكا: المفاتيح مرفوضة ({r.status_code}) - تأكد من ALPACAAPIKEY و ALPACASECRETKEY")
            return None
        if r.status_code == 429:
            log("ألباكا: طلبات كثيرة، أستنى شوي")
            time.sleep(10)
            continue
        if r.status_code != 200:
            log(f"ألباكا: خطأ {r.status_code} - {r.text[:200]}")
            return None
        data = r.json()
        for sym, trades in (data.get("trades") or {}).items():
            out.setdefault(sym, []).extend(trades or [])
        token = data.get("next_page_token")
        if not token:
            break
        params["page_token"] = token
    return out


class AlgoDetector:
    """يعد الصفقات الصغيرة اللي بنفس الحجم بالضبط خلال آخر ALGO_WINDOW_MIN دقيقة لكل سهم.
    ويقدّر الشراء/البيع من اتجاه السعر: صفقة أعلى من اللي قبلها = شراء، أقل = بيع (تقريبي)."""
    def __init__(self):
        self.win = {}         # (الرمز، الحجم) -> deque[(الوقت، السعر، الجهة)]
        self.seen = {}
        self.last_px = {}
        self.last_side = {}
        self.alerted = {}

    def add(self, sym, trade):
        tid = trade.get("i")
        seen = self.seen.setdefault(sym, deque(maxlen=50000))
        if tid is not None:
            if tid in seen:
                return None
            seen.append(tid)
        size = float(trade.get("s") or 0)
        price = float(trade.get("p") or 0)
        if size <= 0 or price <= 0:
            return None
        prev = self.last_px.get(sym)
        side = self.last_side.get(sym, 0)
        if prev is not None and price != prev:
            side = 1 if price > prev else -1          # نفس السعر = نفس جهة اللي قبلها
        self.last_px[sym], self.last_side[sym] = price, side
        if size > ALGO_MAX_SIZE:
            return None
        ts = pd.Timestamp(trade["t"])
        q = self.win.setdefault((sym, size), deque())
        q.append((ts, price, side))
        cutoff = ts - pd.Timedelta(minutes=ALGO_WINDOW_MIN)
        while q and q[0][0] < cutoff:
            q.popleft()
        n = len(q)
        level = ("strong" if n >= ALGO_STRONG_STREAK else
                 "normal" if n >= ALGO_MIN_STREAK else None)
        if level is None:
            return None
        if ALGO_MIN_VALUE and sum(x[1] for x in q) * size < ALGO_MIN_VALUE:
            return None                                # المبلغ صغير: مو أمر كبير متقطع
        k = (sym, size, level)
        last = self.alerted.get(k)
        if last is not None and ts - last < pd.Timedelta(minutes=ALGO_REALERT_MIN):
            return None
        self.alerted[k] = ts
        prices = [x[1] for x in q]
        buys = sum(1 for x in q if x[2] > 0)
        sells = sum(1 for x in q if x[2] < 0)
        return {"size": size, "count": n, "first_t": q[0][0], "last_t": ts,
                "low": min(prices), "high": max(prices), "last": price,
                "buys": buys, "sells": sells, "level": level}


def _side_lines(b, s_, total, size):
    """الشراء والبيع مع بعض (تقدير من اتجاه السعر: صفقة أعلى من اللي قبلها = شراء، أقل = بيع)."""
    pct = lambda x: f"{x / total * 100:.0f}%" if total else "0%"
    n = total - b - s_
    return (f"🟢 شراء: {b:,} صفقة ({pct(b)}) = {b * size:,.0f} سهم\n"
            f"🔴 بيع: {s_:,} صفقة ({pct(s_)}) = {s_ * size:,.0f} سهم\n"
            + (f"⚪ بدون اتجاه: {n:,} صفقة\n" if n else ""))


def _algo_message(sym, a, cap=None, section="", note=""):
    strength = "🔥 قوي" if a["level"] == "strong" else "⚡ رصد"
    mins = max((a["last_t"] - a["first_t"]).total_seconds() / 60, 0.1)
    b, s_, total = a["buys"], a["sells"], a["count"]
    return (f"🤖 خوارزمية تقطيع محتملة — {strength}\n"
            + (f"القسم: {section}\n" if section else "")
            + f"السهم: ${sym}\n"
            f"السعر: ${a['last']:.4g} (من {a['low']:.4g} إلى {a['high']:.4g})\n"
            f"الحجم المتكرر: {a['size']:g} سهم\n"
            f"التكرار: {total} صفقة خلال {mins:.1f} دقيقة\n"
            + _side_lines(b, s_, total, a["size"])
            + (f"القيمة السوقية: {_cap_txt(cap)}\n" if cap else "")
            + (f"{note}\n" if note else "")
            + f"المصدر: {ALGO_FEED.upper()} عبر Alpaca"
            + (f" (متأخر {ALGO_DELAY_MIN - 1} دقيقة)" if ALGO_DELAY_MIN else "") + "\n"
            f"وقت آخر صفقة: {a['last_t'].tz_convert(LOCAL_TZ):%H:%M:%S} (توقيتك)")


FLOAT_CACHE_SEC = 6 * 60 * 60    # تحديث بيانات الفلوت كل 6 ساعات (يستخدمها ماسح السيولة)
_algo_float_cache = {}


def get_algo_float(sym):
    now = time.time(); old = _algo_float_cache.get(sym)
    if old and now - old[0] < FLOAT_CACHE_SEC:
        return old[1]
    try:
        import yfinance as yf
        info = yf.Ticker(sym).info or {}; val = info.get("floatShares")
        val = float(val) if val is not None else None
    except Exception:
        val = None
    _algo_float_cache[sym] = (now, val)
    return val


def _cap_txt(cap):
    return f"{cap / 1e9:.2f} مليار$" if cap >= 1e9 else f"{cap / 1e6:.1f} مليون$"


def _nasdaq_rows():
    """كل أسهم ناسداك من السكرينر الرسمي: [(الرمز، القيمة السوقية، حجم اليوم، السعر)]."""
    url = ("https://api.nasdaq.com/api/screener/stocks"
           "?tableonly=true&limit=10000&exchange=nasdaq&download=true")
    r = requests.get(url, headers={**HEADERS, "Accept": "application/json"}, timeout=30)
    data = r.json().get("data") or {}
    rows = data.get("rows") or (data.get("table") or {}).get("rows") or []
    out = []
    for row in rows:
        sym = str(row.get("symbol", "")).strip().upper()
        if sym.isalpha() and len(sym) <= 5:
            out.append((sym, _to_number(row.get("marketCap")), _to_number(row.get("volume")),
                        _to_number(row.get("lastsale"))))
    return out


RSPLIT_ALGO_SYMS = set()   # أسهم قسم التجزئة العكسية (عشان قسم البني ستوك ما يكررها)


def _recent_rsplits(syms, days):
    """{الرمز: (تاريخ آخر تجزئة عكسية، النسبة)} للي سوت تجزئة عكسية خلال آخر days يوم."""
    since = pd.Timestamp.now(tz=NY).date() - pd.Timedelta(days=days)
    out = {}
    for t, df in download_batches(sorted(syms), UNIVERSE_BATCH, period="6mo", interval="1d",
                                  prepost=False, actions=True):
        try:
            if "Stock Splits" not in df:
                continue
            sp = df["Stock Splits"].fillna(0)
            rev = sp[(sp > 0) & (sp < 1)]
            rev = [(pd.Timestamp(i).date(), float(r)) for i, r in rev.items()
                   if pd.Timestamp(i).date() >= since]
            if rev:
                out[t] = rev[-1]
        except Exception:
            continue
    free_memory()
    return out


def _price_universe(min_px, max_px, max_cap, max_n):
    """أسهم ناسداك داخل نطاق السعر (وتحت حد القيمة السوقية لو فيه)، الأنشط أول.
    يرجع [(الرمز، القيمة السوقية)]."""
    picks = []
    for sym, cap, vol, px in _nasdaq_rows():
        if not (min_px <= px <= max_px) or vol < ALGO_MIN_DAY_VOLUME:
            continue
        if max_cap and not (0 < cap <= max_cap):
            continue
        picks.append((vol, sym, cap))
    picks.sort(reverse=True)
    return [(sym, cap) for _, sym, cap in picks[:max_n]]


def get_microcaps():
    """قسم (6): 1$-15$ وسوت تجزئة عكسية آخر 3 شهور. يرجع {الرمز: (القيمة السوقية، ملاحظة)}."""
    global RSPLIT_ALGO_SYMS
    if ONE_LIST:
        return {sym: (None, "") for sym in stocks_only(WATCH_SYMBOLS)}
    try:
        base = _price_universe(ALGO_MIN_PRICE, ALGO_MAX_PRICE, ALGO_MAX_MARKET_CAP, 100_000)
        if not ALGO_RSPLIT_DAYS:
            return {sym: (cap, "") for sym, cap in base[:ALGO_MAX_SYMBOLS]}
        log(f"كشف الخوارزميات: أدور التجزئات العكسية بين {len(base)} سهم سعرها "
            f"{ALGO_MIN_PRICE:g}$-{ALGO_MAX_PRICE:g}$ ...")
        rs = _recent_rsplits([sym for sym, _ in base], ALGO_RSPLIT_DAYS)
        out = {}
        for sym, cap in base:                         # base مرتبة بالأنشط
            if sym in rs and len(out) < ALGO_MAX_SYMBOLS:
                d, ratio = rs[sym]
                out[sym] = (cap, f"تجزئة عكسية: {d:%Y-%m-%d} (كل {1 / ratio:g} أسهم = سهم)")
        RSPLIT_ALGO_SYMS = set(out)
        return out
    except Exception as e:
        log("كشف الخوارزميات: ما قدرت أجيب قائمة الأسهم -", e)
        return {}


def get_pennies():
    """قسم (6ج): 1$-5$ وقيمتها 40 مليون وتحت. يرجع {الرمز: (القيمة السوقية، ملاحظة)}."""
    if ONE_LIST:
        return {}          # نفس منطق (6) بالضبط، فلو اشتغل على نفس القائمة بيكرر التنبيهات
    try:
        return {sym: (cap, "") for sym, cap in _price_universe(
            ALGO_PENNY_MIN_PRICE, ALGO_PENNY_MAX_PRICE, ALGO_PENNY_MAX_MARKET_CAP,
            ALGO_PENNY_MAX_SYMBOLS)}
    except Exception as e:
        log("البني ستوك: ما قدرت أجيب قائمة الأسهم -", e)
        return {}


# ================== (6ب) خوارزميات الأسهم الكبيرة + (6د) الآيس بيرغ ==================
def get_bigcaps():
    """أسهم ناسداك اللي قيمتها السوقية مليار وفوق، الأنشط تداولاً أول. يرجع {الرمز: القيمة السوقية}."""
    if ONE_LIST:
        return {sym: None for sym in stocks_only(WATCH_SYMBOLS)}
    try:
        picks = [(vol, sym, cap) for sym, cap, vol, px in _nasdaq_rows()
                 if cap >= ALGO_BIG_MIN_MARKET_CAP and vol > 0]
        picks.sort(reverse=True)
        return {sym: cap for _, sym, cap in picks[:ALGO_BIG_MAX_SYMBOLS]}
    except Exception as e:
        log("خوارزميات الكبيرة: ما قدرت أجيب القيم السوقية من ناسداك -", e)
        return {}


def _ts_sec(t):
    """وقت الصفقة بالثواني (سريع، لأن الأسهم الكبيرة فيها آلاف الصفقات بكل سحبة)."""
    if isinstance(t, str) and len(t) >= 19:
        base = datetime.fromisoformat(t[:19]).replace(tzinfo=timezone.utc).timestamp()
        frac = t[19:].split("+")[0].rstrip("Z")
        if frac.startswith(".") and len(frac) > 1:
            base += float("0" + frac[:10])
        return base
    return pd.Timestamp(t).timestamp()


class StreakDetector:
    """يعد الصفقات المتتالية بنفس الحجم لكل سهم: أي صفقة بحجم مختلف (أو فاصل أكثر من
    ALGO_BIG_MAX_GAP_SEC ثانية) تقطع السلسلة وتبدأ وحدة جديدة.
    ينبه عند ALGO_BIG_MIN_STREAK، ثم كل ما تتضاعف (600، 1200، 2400 ...).
    same_price=True = لازم نفس السعر بعد (الآيس بيرغ)."""
    def __init__(self, min_streak=None, min_size=0, max_size=None, max_gap=None,
                 realert_min=None, same_price=False):
        self.min_streak = min_streak or ALGO_BIG_MIN_STREAK
        self.min_size = min_size
        self.max_size = ALGO_BIG_MAX_SIZE if max_size is None else max_size   # 0 = بدون حد
        self.max_gap = ALGO_BIG_MAX_GAP_SEC if max_gap is None else max_gap
        self.realert = (ALGO_BIG_REALERT_MIN if realert_min is None else realert_min) * 60
        self.same_price = same_price
        self.st = {}          # الرمز -> السلسلة الحالية
        self.recent = {}      # الرمز -> (deque[(الوقت، رقم الصفقة)], set) لآخر 60 ثانية - لمنع التكرار
        self.alerted = {}     # (الرمز، الحجم) -> وقت آخر تنبيه

    def _dup(self, sym, tid, ts):
        if tid is None:
            return False
        q, ids = self.recent.setdefault(sym, (deque(), set()))
        while q and q[0][0] < ts - 60:
            ids.discard(q.popleft()[1])
        if tid in ids:
            return True
        q.append((ts, tid))
        ids.add(tid)
        return False

    def add(self, sym, trade):
        ts = _ts_sec(trade["t"])
        if self._dup(sym, trade.get("i"), ts):
            return None
        size = float(trade.get("s") or 0)
        price = float(trade.get("p") or 0)
        if size <= 0 or price <= 0:
            return None
        s = self.st.get(sym)
        side = s["side"] if s else 0
        if s and price != s["px"]:
            side = 1 if price > s["px"] else -1       # نفس السعر = نفس جهة اللي قبلها
        moment = round(ts, 3)                         # "نفس اللحظة" = نفس الملي ثانية
        prev_px = s["px"] if s else None
        if s and s["size"] == size and ts - s["last"] <= self.max_gap \
                and (not self.same_price or price == prev_px):
            s["n"] += 1
            s["same"] = s["same"] + 1 if moment == s["moment"] else 1
            s["max_same"] = max(s["max_same"], s["same"])
            s["low"], s["high"] = min(s["low"], price), max(s["high"], price)
            s["value"] += size * price
        else:
            s = {"size": size, "n": 1, "first": ts, "low": price, "high": price,
                 "value": size * price, "buys": 0, "sells": 0, "same": 1, "max_same": 1,
                 "next_alert": self.min_streak}
            self.st[sym] = s
        s["buys"] += side > 0
        s["sells"] += side < 0
        s["last"], s["px"], s["side"], s["moment"] = ts, price, side, moment
        if s["n"] < s["next_alert"] or size < self.min_size \
                or (self.max_size and size > self.max_size):
            return None
        s["next_alert"] *= 2
        k = (sym, size, price if self.same_price else None)
        first_alert = s["n"] == self.min_streak
        last = self.alerted.get(k)
        if first_alert and last is not None and ts - last < self.realert:
            return None
        self.alerted[k] = ts
        return {"size": size, "count": s["n"], "first_t": s["first"], "last_t": ts,
                "low": s["low"], "high": s["high"], "last": price, "value": s["value"],
                "buys": s["buys"], "sells": s["sells"], "max_same": s["max_same"],
                "update": not first_alert}


def _ice_message(sym, a, cap=None):
    secs = a["last_t"] - a["first_t"]
    b, s_, total = a["buys"], a["sells"], a["count"]
    t1 = pd.Timestamp(a["first_t"], unit="s", tz="UTC").tz_convert(LOCAL_TZ)
    t2 = pd.Timestamp(a["last_t"], unit="s", tz="UTC").tz_convert(LOCAL_TZ)
    head = ("🔁 تحديث: الآيس بيرغ مستمر" if a["update"] else
            "🧊 آيس بيرغ — صفقات متتالية بنفس الحجم ونفس السعر")
    return (f"{head}\n"
            f"السهم: ${sym}\n"
            + (f"القيمة السوقية: {_cap_txt(cap)}\n" if cap else "")
            + f"الحجم: {a['size']:g} سهم × {total:,} صفقة ورا بعض\n"
            f"السعر: {a['last']:.2f} (نفس السعر كلها)\n"
            f"المبلغ: ≈ {a['value']:,.0f}$ ({a['size'] * total:,.0f} سهم)\n"
            f"خلال: {secs:.1f} ثانية | أكثر عدد صفقات بنفس اللحظة: {a['max_same']}\n"
            + _side_lines(b, s_, total, a["size"])
            + f"المصدر: {ALGO_FEED.upper()} عبر Alpaca (كل البورصات)"
            + (f" - متأخر {ALGO_DELAY_MIN - 1} دقيقة" if ALGO_DELAY_MIN else "") + "\n"
            f"من {t1:%H:%M:%S} إلى {t2:%H:%M:%S} (توقيتك)")


def _big_message(sym, a, cap=None):
    secs = max(a["last_t"] - a["first_t"], 0.001)
    b, s_, total = a["buys"], a["sells"], a["count"]
    t1 = pd.Timestamp(a["first_t"], unit="s", tz="UTC").tz_convert(LOCAL_TZ)
    t2 = pd.Timestamp(a["last_t"], unit="s", tz="UTC").tz_convert(LOCAL_TZ)
    if a.get("one_side") == "buy":
        head = "🟢🤖 خوارزمية شراء كامل — صفقات سهم واحد متتالية"
    elif a.get("one_side") == "sell":
        head = "🔴🤖 خوارزمية بيع كامل — صفقات سهم واحد متتالية"
    else:
        head = ("🔁 تحديث: السلسلة مستمرة" if a["update"] else
                "🏦🤖 خوارزمية على سهم كبير — صفقات متتالية بنفس الحجم")
    return (f"{head}\n"
            f"السهم: ${sym}\n"
            + (f"القيمة السوقية: {_cap_txt(cap)}\n" if cap else "")
            + f"الحجم المتكرر: {a['size']:g} سهم\n"
            f"عدد الصفقات المتتالية: {total:,} (ولا صفقة بحجم ثاني بينها)\n"
            f"المدة: {secs:.1f} ثانية (≈ {total / secs:.0f} صفقة/ثانية)\n"
            f"أكثر عدد صفقات بنفس اللحظة: {a['max_same']}\n"
            f"قيمتها: ≈ {a['value']:,.0f}$\n"
            f"السعر: ${a['last']:.2f} (من {a['low']:.2f} إلى {a['high']:.2f})\n"
            + _side_lines(b, s_, total, a["size"])
            + f"المصدر: {ALGO_FEED.upper()} عبر Alpaca"
            + (f" (متأخر {ALGO_DELAY_MIN - 1} دقيقة)" if ALGO_DELAY_MIN else "") + "\n"
            f"من {t1:%H:%M:%S} إلى {t2:%H:%M:%S} (توقيتك)")


def algo_big_loop():
    det = StreakDetector()
    ice = (StreakDetector(ALGO_ICE_MIN_STREAK, ALGO_ICE_MIN_SIZE, ALGO_ICE_MAX_SIZE,
                          ALGO_ICE_MAX_GAP_SEC, ALGO_ICE_REALERT_MIN, same_price=True)
           if ALGO_ICE else None)
    last_end, was_on = None, None
    caps, caps_day = {}, None
    while True:
        try:
            now = pd.Timestamp.now(tz="UTC")
            end = now - pd.Timedelta(minutes=ALGO_DELAY_MIN)
            end_ny = end.tz_convert(NY)
            on = (end_ny.weekday() < 5 and (9, 30) <= (end_ny.hour, end_ny.minute) < (16, 0)
                  if ALGO_BIG_REGULAR_ONLY else trading_hours(end_ny))
            if on != was_on:
                log("خوارزميات الكبيرة: " + ("بدأ المراقبة" if on else "السوق مسكر، أنتظر"))
                was_on = on
            if not on:
                last_end = None
                time.sleep(60)
                continue
            today = pd.Timestamp.now(tz=NY).date()
            if caps_day != today or not caps:
                caps = (get_bigcaps() if ONE_LIST or not ALGO_BIG_SYMBOLS
                        else {s_: None for s_ in ALGO_BIG_SYMBOLS})
                caps_day = today
                log(f"خوارزميات الكبيرة: يراقب {len(caps)} سهم (قائمة المراقبة) - شراء كامل/بيع كامل - تنبيه عند "
                    f"{ALGO_BIG_MIN_STREAK} صفقة متتالية بنفس الحجم ({ALGO_BIG_MAX_SIZE:g} أسهم وأقل)"
                    + (f" | الآيس بيرغ: {ALGO_ICE_MIN_STREAK} صفقة متتالية بنفس الحجم والسعر" if ALGO_ICE else ""))
            syms = list(caps)
            if not syms:
                time.sleep(300)
                continue
            start = last_end or end - pd.Timedelta(seconds=60)
            got = None
            for i in range(0, len(syms), ALGO_BIG_CHUNK):
                part = fetch_alpaca_trades(syms[i:i + ALGO_BIG_CHUNK], start, end)
                if part is not None:
                    got = got or {}
                    got.update(part)
            if got is not None:
                last_end = end
                for sym, trades in got.items():
                    for tr in sorted(trades, key=lambda x: x.get("t", "")):
                        res = det.add(sym, tr)
                        if res and not res["update"]:      # تنبيه واحد لكل سلسلة
                            directional = res["buys"] + res["sells"]
                            need = ALGO_BIG_ONE_SIDE_PCT / 100
                            if directional and res["buys"] / directional >= need:
                                res["one_side"] = "buy"
                            elif directional and res["sells"] / directional >= need:
                                res["one_side"] = "sell"
                            else:
                                res = None                 # مخلوطة بيع وشراء: ما ينبه
                            if res:
                                send_telegram(_big_message(sym, res, caps.get(sym)), kind="algo_big", sym=sym)
                        if ice is not None:
                            res = ice.add(sym, tr)
                            if res:
                                send_telegram(_ice_message(sym, res, caps.get(sym)), kind="ice", sym=sym)
                del got
        except Exception as e:
            log("خوارزميات الكبيرة: خطأ -", e)
        time.sleep(ALGO_BIG_POLL_SEC)


def _once_load(tag):
    """آخر تنبيه لكل سهم في هالقسم: {الرمز: الوقت}."""
    out = {}
    for line in _load_set(ALGO_ONCE_FILE):
        try:
            t, sym, ts = line.split("|")
            if t == tag:
                ts = pd.Timestamp(ts)
                out[sym] = max(ts, out.get(sym, ts))
        except Exception:
            continue
    return out


def algo_loop(name, section, get_universe, fixed=None, exclude=None, once_hours=0,
              det_cls=None, msg_fn=None):
    """يشتغل بخيط لحاله في الخلفية، عشان ما يتأخر بسبب الفحوصات الثانية الطويلة.
    get_universe يرجع {الرمز: (القيمة السوقية، ملاحظة)} - تتجدد مرة باليوم.
    exclude = دالة ترجع أسهم ما نراقبها هنا (موجودة بقسم ثاني).
    once_hours = تنبيه واحد بس لكل سهم، وبعدها يسكت عنه كذا ساعة (0 = بدون حد)."""
    det = (det_cls or AlgoDetector)()
    msg_fn = msg_fn or _algo_message
    once_tag = section
    once_last = _once_load(once_tag) if once_hours else {}
    last_end = None
    was_on = None
    caps, caps_day = {}, None
    while True:
        try:
            now = pd.Timestamp.now(tz="UTC")
            end = now - pd.Timedelta(minutes=ALGO_DELAY_MIN)
            on = trading_hours(end.tz_convert(NY))
            if on != was_on:
                log(f"{name}: " + ("بدأ المراقبة" if on else "السوق مسكر، أنتظر"))
                was_on = on
            if not on:
                last_end = None
                time.sleep(60)
                continue
            today = pd.Timestamp.now(tz=NY).date()
            if caps_day != today or not caps:
                caps = {s_: (None, "") for s_ in fixed} if fixed else get_universe()
                caps_day = today
                log(f"{name}: ألباكا ({ALGO_FEED}"
                    + (f"، متأخر {ALGO_DELAY_MIN - 1} دقيقة" if ALGO_DELAY_MIN else "، لحظي")
                    + f") - يراقب {len(caps)} سهم ({section}): "
                    + ", ".join(list(caps)[:30]) + (" ..." if len(caps) > 30 else ""))
                if not caps:
                    time.sleep(600)                   # ما لقى أسهم، يعيد المحاولة بعد 10 دقايق
                    caps_day = None
                    continue
            skip = exclude() if exclude else set()
            syms = [x for x in caps if x not in skip]
            if not syms:
                time.sleep(300)
                continue
            # نرجع شوي لورا عشان الصفقات المتأخرة، والتكرار ينشال بأرقام الصفقات
            start = (last_end or end - pd.Timedelta(seconds=60)) - pd.Timedelta(seconds=5)
            got = None
            for i in range(0, len(syms), 30):
                part = fetch_alpaca_trades(syms[i:i + 30], start, end)
                if part is not None:
                    got = got or {}
                    got.update(part)
            if got is not None:
                last_end = end
                for sym, trades in got.items():
                    for tr in sorted(trades, key=lambda x: x.get("t", "")):
                        res = det.add(sym, tr)
                        if res:
                            if once_hours:
                                now_utc = pd.Timestamp.now(tz="UTC")
                                prev = once_last.get(sym)
                                if prev is not None and now_utc - prev < pd.Timedelta(hours=once_hours):
                                    continue        # جاه تنبيه خلال آخر 24 ساعة، يسكت
                                once_last[sym] = now_utc
                                _append_line(ALGO_ONCE_FILE, f"{once_tag}|{sym}|{now_utc.isoformat()}")
                            cap, note = caps.get(sym, (None, ""))
                            send_telegram(msg_fn(sym, res, cap, section, note), kind="algo", sym=sym)
        except Exception as e:
            log(f"{name}: خطأ -", e)
        time.sleep(ALGO_POLL_SEC)


def start_algo_thread():
    if not ENABLE_ALGO:
        log("كشف الخوارزميات: مطفي (حط ALPACAAPIKEY و ALPACASECRETKEY في Railway عشان يشتغل)")
        return
    if ALGO_SMALL:
        sec = (f"{ALGO_MIN_PRICE:g}$-{ALGO_MAX_PRICE:g}$"
               + (f" + تجزئة عكسية آخر {ALGO_RSPLIT_DAYS} يوم" if ALGO_RSPLIT_DAYS else ""))
        threading.Thread(target=algo_loop, daemon=True, name="algo",
                         args=("كشف الخوارزميات (تجزئة عكسية)", sec, get_microcaps, ALGO_SYMBOLS,
                               None, ALGO_SMALL_ONCE_HOURS)).start()
    if ALGO_PENNY:
        sec = (f"بني ستوك {ALGO_PENNY_MIN_PRICE:g}$-{ALGO_PENNY_MAX_PRICE:g}$ وقيمتها "
               f"{ALGO_PENNY_MAX_MARKET_CAP / 1e6:g} مليون وتحت")
        threading.Thread(target=algo_loop, daemon=True, name="algo_penny",
                         args=("خوارزميات البني ستوك", sec, get_pennies, None,
                               lambda: RSPLIT_ALGO_SYMS, ALGO_PENNY_ONCE_HOURS)).start()
    if ALGO_BIG:
        threading.Thread(target=algo_big_loop, daemon=True, name="algo_big").start()


def algo_self_test():
    global ALGO_MIN_VALUE
    t0 = pd.Timestamp("2026-01-02T15:00:00Z")
    # شرط القيمة: 300 صفقة بسهم واحد على 2.27$ = 681$ بس، فما ينبه
    det = AlgoDetector()
    small = [det.add("YJ", {"i": k + 1, "s": 1, "p": 2.27, "t": t0 + pd.Timedelta(milliseconds=k * 700)})
             for k in range(320)]
    assert not any(small), "تنبيه على مبلغ صغير"
    print(f"ALGO TEST OK: 300 trades worth ~681$ ignored (min {ALGO_MIN_VALUE:,.0f}$)")
    saved, ALGO_MIN_VALUE = ALGO_MIN_VALUE, 0
    det = AlgoDetector(); alerts = []
    for k in range(650):          # 650 صفقة بحجم سهم واحد خلال 3 دقايق وشوي، السعر يطلع
        tr = {"i": k + 1, "s": 1, "p": 0.50 + (k % 5) * 0.001,
              "t": t0 + pd.Timedelta(milliseconds=k * 300)}
        a = det.add("TEST", tr)
        if a: alerts.append(a)
    for k in range(400):          # صفقات حجمها كبير = تتجاهل
        a = det.add("BIG", {"i": k + 1, "s": 500, "p": 1.0, "t": t0 + pd.Timedelta(seconds=k)})
        assert a is None
    assert [a["count"] for a in alerts] == [300, 600], [a["count"] for a in alerts]
    ALGO_MIN_VALUE = saved
    print("ALGO TEST OK: 300 / 600 same-size trades")
    print(_algo_message("TEST", alerts[-1], 12_300_000))

    # (6ب) الكبيرة: 1100 صفقة متتالية بحجم سهم واحد (كل 3 ورا بعض بنفس اللحظة)، ثم صفقة بحجم ثاني تقطعها
    det = StreakDetector(); big = []
    for k in range(1100):
        tr = {"i": k + 1, "s": 1, "p": 180.00 - (k // 50) * 0.01,
              "t": (t0 + pd.Timedelta(milliseconds=(k // 3) * 40)).strftime("%Y-%m-%dT%H:%M:%S.%f000Z")}
        a = det.add("BIGCAP", tr)
        if a: big.append(a)
    assert det.add("BIGCAP", {"i": 1101, "s": 1, "p": 180, "t": "2026-01-02T15:00:00.000000000Z"}) is None  # مكرر
    det.add("BIGCAP", {"i": 9999, "s": 37, "p": 179.9, "t": "2026-01-02T15:00:10Z"})   # حجم ثاني = تنقطع
    for k in range(ALGO_BIG_MIN_STREAK - 1):   # أقل من الحد بوحدة = ما ينبه
        a = det.add("BIGCAP", {"i": 10000 + k, "s": 1, "p": 179.9, "t": t0 + pd.Timedelta(seconds=11 + k * 0.01)})
        assert a is None
    # تنبيه عند الحد (300)، وعند الضعف (600) تحديث - والتشغيل يرسل الأول بس (تنبيه واحد لكل سلسلة)
    assert [a["count"] for a in big] == [ALGO_BIG_MIN_STREAK, ALGO_BIG_MIN_STREAK * 2], [a["count"] for a in big]
    assert not big[0]["update"] and big[1]["update"]
    for k in range(1300):         # حجم 100 (أكبر من 10) = يتجاهل
        assert det.add("BIG100", {"i": k + 1, "s": 100, "p": 50, "t": t0 + pd.Timedelta(milliseconds=k * 10)}) is None
    assert big[0]["max_same"] == 3
    print(f"ALGO BIG TEST OK: {ALGO_BIG_MIN_STREAK} consecutive same-size trades")

    # (6د) آيس بيرغ: 600 صفقة × سهم واحد على 228.15 ورا بعض (بعد صفقة أقل سعر = شراء)
    ice = StreakDetector(ALGO_ICE_MIN_STREAK, ALGO_ICE_MIN_SIZE, ALGO_ICE_MAX_SIZE,
                         ALGO_ICE_MAX_GAP_SEC, ALGO_ICE_REALERT_MIN, same_price=True)
    ice.add("NVDA", {"i": 1, "s": 13, "p": 228.10, "t": t0})
    got = [a for k in range(600) if (a := ice.add("NVDA", {"i": k + 2, "s": 1, "p": 228.15,
                                                         "t": t0 + pd.Timedelta(milliseconds=50 * k)}))]
    assert [a["count"] for a in got] == [500] and got[0]["buys"] == 500, got
    # حجم 70 (أكبر من 10) = يتجاهل
    for k in range(300):
        assert ice.add("MSFT", {"i": k, "s": 70, "p": 400, "t": t0 + pd.Timedelta(milliseconds=50 * k)}) is None
    # نفس الحجم بس السعر تغير = تنقطع
    ice2 = StreakDetector(ALGO_ICE_MIN_STREAK, ALGO_ICE_MIN_SIZE, ALGO_ICE_MAX_SIZE,
                          ALGO_ICE_MAX_GAP_SEC, ALGO_ICE_REALERT_MIN, same_price=True)
    for k in range(1000):
        assert ice2.add("AMD", {"i": k, "s": 1, "p": 150 + (k % 2) * 0.01,
                                "t": t0 + pd.Timedelta(milliseconds=50 * k)}) is None
    # فاصل أكثر من ثانيتين = تنقطع
    for k in range(1000):
        assert ice2.add("AAPL", {"i": k, "s": 1, "p": 200, "t": t0 + pd.Timedelta(seconds=3 * k)}) is None
    print("ICEBERG TEST OK: 500 same-size same-price trades (1-10 shares)")
    print(_ice_message("NVDA", got[0], 5_500_000_000_000))
    print(_big_message("BIGCAP", big[0], 45_600_000_000))



def main():
    if "--algotest" in sys.argv:
        algo_self_test()
        return
    if "--pwltest" in sys.argv:
        pwl_self_test()
        return
    if "--pw4hnow" in sys.argv:   # تجربة حقيقية: python short_bot.py --pw4hnow [--send]
        _load_chats()
        pw4h_now(list(WATCH_SYMBOLS), send="--send" in sys.argv)
        return
    if "--pd4htest" in sys.argv:
        pd4h_self_test()
        return
    if "--pdh1htest" in sys.argv:
        pdh1h_self_test()
        return
    if "--smttest" in sys.argv:
        smt_self_test()
        return
    if "--frimontest" in sys.argv:
        frimon_self_test()
        return
    if "--wkopttest" in sys.argv:
        wkopt_self_test()
        return
    if "--ifvgtest" in sys.argv:
        ifvg_self_test()
        return
    once = "--once" in sys.argv
    _load_chats()
    discover_groups()
    log(f"التنبيهات بتروح لـ {len(CHATS)} محادثة: {', '.join(CHATS) or 'ولا وحدة'}")
    if TEST_ON_START and not once:
        pw4h = [n for on, n in ((ENABLE_PWL_4H, "دعم"), (ENABLE_PWH_4H, "مقاومة")) if on]
        pw4h_txt = (f" + سحب {' و'.join(pw4h)} الأسبوع السابق 4 ساعات (كول/بوت، {len(WATCH_SYMBOLS)} رمز)"
                    if pw4h else "")
        if ENABLE_WKOPT:
            pw4h_txt += (f" + سحب السيولة الأسبوعي {WKOPT_FRAME_MIN // 60} ساعات مع عقد{' بوت بس' if WKOPT_PUT_ONLY else ''} "
                         + (f"(الأسهم {WKOPT_MIN_PRICE}$-{WKOPT_MAX_PRICE}$، " if WKOPT_MAX_PRICE else "(كل القائمة، ")
                         + "تنبيه واحد لكل سهم بالأسبوع)")
        if ENABLE_PD4H:
            pw4h_txt += f" + سحب دعم/مقاومة اليوم السابق 4 ساعات مع القاما ({', '.join(PD4H_SYMBOLS)})"
        if ENABLE_PDH1H or ENABLE_PDL1H:
            pw4h_txt += f" + سحب دعم/مقاومة اليوم السابق فريم ساعة ({len(PD4H_SYMBOLS)} أسهم)"
        if ENABLE_SMT:
            pw4h_txt += f" + اتجاه السوق (ناسداك مقابل سباكس، فريم {SMT_FRAME_MIN} دقيقة)"
        if ENABLE_IFVG and (ENABLE_IFVG_1H or ENABLE_IFVG_4H):
            fr = [n for on, n in ((ENABLE_IFVG_1H, "ساعة"), (ENABLE_IFVG_4H, "4 ساعات")) if on]
            pw4h_txt += f" + الإنفيرجن IFVG فريم {' و'.join(fr)} ({len(WATCH_SYMBOLS)} رمز)"
        if ENABLE_WATCH_IFVG and (WATCH_IFVG_1H or WATCH_IFVG_1H_24H or WATCH_IFVG_4H or WATCH_IFVG_4H_EXT):
            fr = [n for on, n in ((WATCH_IFVG_1H, "ساعة ممدد"), (WATCH_IFVG_1H_24H, "ساعة 24 ساعة"),
                                  (WATCH_IFVG_4H, "4 ساعات 24 ساعة"),
                                  (WATCH_IFVG_4H_EXT, "4 ساعات ممدد")) if on]
            pw4h_txt += f" + الإنفيرجن IFVG قائمة المراقبة فريم {' و'.join(fr)} ({len(WATCH_SYMBOLS)} رمز)"
        send_telegram("🧪 رسالة اختبار - بوت الشورت اشتغل\n"
                      "الأقسام: " + ("نزول الشورت المتاح 90% + " if ENABLE_BORROW_DROP else "") + "خوارزميات التقطيع"
                      + (" + خوارزميات البني ستوك" if ALGO_PENNY else "")
                      + (" + خوارزميات الأسهم الكبيرة" if ALGO_BIG else "")
                      + (" + الآيس بيرغ" if ALGO_BIG and ALGO_ICE else "")
                      + (" + سحب الجمعة/الاثنين (كول)" if ENABLE_FRIMON else "") + " + التجزئة العكسية"
                      f"{pw4h_txt}\n"
                      f"الوقت: {pd.Timestamp.now(tz=LOCAL_TZ):%Y-%m-%d %H:%M} (توقيتك)")
    if not once:
        pd4h_send_test_once()
        start_algo_thread()
        if ENABLE_SMT:           # (14) اتجاه السوق: ناسداك مقابل سباكس على اليوم السابق
            _smt_today_load()
            threading.Thread(target=smt_run_forever, daemon=True, name="smt").start()
        if ENABLE_FRIMON:        # (11) سحب قمة الجمعة/الاثنين + دعم الأسبوع السابق → كول
            threading.Thread(target=frimon_run_forever, daemon=True, name="frimon").start()
        if ENABLE_BORROW_DROP:   # نزول الشورت المتاح أكثر من 90%
            threading.Thread(target=bz_run_forever, daemon=True, name="borrow_drop").start()

    pwl_last = 0.0
    ifvg_last = None
    watch_last = None
    was_open = None
    gap_sent = _load_set(GAP_SENT_FILE)       # مفاتيح تنبيهات سحب الأسبوع السابق (4 ساعات)
    rsplit_new_sent = _load_set(RSPLIT_NEW_FILE)
    rsplit_state = _rsplit_state()

    while True:
        discover_groups()

        # (1ك-2) سحب سيولة دعم ومقاومة الأسبوع السابق - فريم 4 ساعات - كل 5 دقايق وقت السوق
        if (ENABLE_PWL_4H or ENABLE_PWH_4H or ENABLE_WKOPT or ENABLE_PD4H or ENABLE_PDH1H or ENABLE_PDL1H) \
                and (once or us_market_open()) and time.time() - pwl_last >= PWL_EVERY_MIN * 60:
            scan_pwl_4h(list(dict.fromkeys(list(WATCH_SYMBOLS)
                                           + (PD4H_SYMBOLS if ENABLE_PD4H or ENABLE_PDH1H or ENABLE_PDL1H else []))),
                        gap_sent)
            pwl_last = time.time()

        # (1) الإنفيرجن IFVG - فريم ساعة و4 ساعات - بعد إغلاق كل ساعة بدقيقة
        if ENABLE_IFVG and (ENABLE_IFVG_1H or ENABLE_IFVG_4H):
            now_ny = pd.Timestamp.now(tz=NY)
            slot = ifvg_scan_due(now_ny, ifvg_last)
            if once or (slot is not None and us_market_open(now_ny, overnight=False)):
                scan_ifvg(list(WATCH_SYMBOLS), gap_sent, now_ny)
                ifvg_last = slot or now_ny

        # (1هـ) الإنفيرجن IFVG - قائمة المراقبة (من gap_scanner) - بعد إغلاق كل ساعة بدقيقة
        #   ساعة: الممددة + 24 ساعة | 4 ساعات: الممددة + 24 ساعة بعد إغلاق كل شمعة 4 ساعات
        if ENABLE_WATCH_IFVG and (WATCH_IFVG_1H or WATCH_IFVG_1H_24H or WATCH_IFVG_4H or WATCH_IFVG_4H_EXT):
            now_ny = pd.Timestamp.now(tz=NY)
            slot = ifvg_scan_due(now_ny, watch_last)
            if once or slot is not None:
                day = us_market_open(now_ny, overnight=False)
                do_4h = watch_4h_due(now_ny) and (day or (night_4h() and us_market_open(now_ny, overnight=True)))
                do_1h24 = night_4h() and us_market_open(now_ny, overnight=True)
                do_4h_ext = watch_4h_due(now_ny) and day
                if once or day or do_4h or do_1h24:
                    scan_watch_ifvg(list(WATCH_SYMBOLS), gap_sent, now_ny,
                                    do_1h=once or day, do_4h=once or do_4h, do_1h24=once or do_1h24,
                                    do_4h_ext=once or do_4h_ext)
                watch_last = slot or now_ny

        # (4ب) التجزئة العكسية - الجديد كل يوم، وقائمة كل جمعة
        if ENABLE_RSPLIT_SHORT:
            rsplit_job(rsplit_state, rsplit_new_sent, force=once)

        is_open = us_market_open()
        if not is_open and was_open is not False:
            log(f"[{datetime.now():%H:%M}] السوق مسكر، أنتظر...")
        was_open = is_open

        if once:
            break
        time.sleep(LOOP_SLEEP_SEC)


if __name__ == "__main__":
    main()
