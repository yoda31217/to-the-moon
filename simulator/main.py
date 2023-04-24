from datetime import date, timedelta
from typing import cast
import streamlit as st
from binance.binance_k_line_loader import BINANCE_SYMBOLS, load_binance_k_lines
from binance.binance_tick_loader import load_binance_ticks

from bot.bot_0_strategy import Bot0Strategy
from report.report import report_profit_chart, report_summary, report_ticks_chart
from trade.trade_simulator import TradeSimulator

st.set_page_config(
    page_title=f"Симулятор торговли бота на крипто бирже",
    initial_sidebar_state="expanded",
)

st.header(f"Симулятор торговли крипто бота")

# with st.expander("Описание", expanded=False):
#     st.write(
#         """
#             Привет!

#             Это бесплатный и открытый симулятор торговли Бота на крипто бирже Binance. 

#             Мы используем реальные данные и соболюдаем все условия торговли. 
#             Все сделано для максимально легкого и оперативного тестирования гипотез.

#             Настраивай симуляцию в панели слева и ожидай результат.

#             Проект открытый. Вот
#             [исходники на GitHub](https://github.com/yoda31217/to-the-moon)
#             проекта и пример 
#             [стратегии Бота](https://github.com/yoda31217/to-the-moon/blob/main/simulator/bot/bot_0_strategy.py).
#         """
#     )

st.sidebar.title("Опции")

st.sidebar.header("Рынок")

st.sidebar.markdown("**Биржа: Binance**")

symbol: str = str(
    st.sidebar.selectbox(
        "Символ", options=BINANCE_SYMBOLS, index=BINANCE_SYMBOLS.index("ETHUSDT")
    )
)

date_from: date = cast(
    date, st.sidebar.date_input("Дата с", date.today() - timedelta(days=2))
)

date_to: date = cast(
    date, st.sidebar.date_input("Дата по", date.today() - timedelta(days=2))
)

symbol_ask_bid_price_difference = st.sidebar.number_input(
    "Разница цены купли-проажи", value=0.01
)

st.sidebar.header("Bot")

st.sidebar.markdown("**Название: Bot0**")

price_step_ratio = (
    st.sidebar.slider(
        "Шаг цены, %",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1,
        help="На сколько должна измениться цена, что бы бот сделал действие",
    )
    / 100.0
)

inverted = st.sidebar.checkbox(
    "Инвертировать", value=False, help="Поменять местами покупку и продажу в алгоритме"
)

try:
    strategy = Bot0Strategy(price_step_ratio, inverted)
    k_lines = load_binance_k_lines(symbol, date_from, date_to)
    ticks = load_binance_ticks(k_lines, symbol_ask_bid_price_difference)
    result = TradeSimulator(ticks).simulate(strategy)

    report_summary(symbol, date_from, date_to, strategy, result)
    report_ticks_chart(ticks)
    report_profit_chart(result)

except Exception as e:
    st.error(f"Ошибка: {str(e)}", icon="🚨")
