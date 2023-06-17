from venv import logger
import streamlit as st
from simulator.bot import bot_grid_input, bot_one_step_order_input
from simulator.bot.bot_grid import BotGrid
from simulator.bot.bot_one_step_order import BotOneStepOrder
from simulator.report.report import build_report

try:
    build_report(
        {
            # Add any number of new bot(s) here.
            BotOneStepOrder.__name__: lambda: {
                "bot_constructor": BotOneStepOrder,
                "bot_config": bot_one_step_order_input.config(),
            },
            BotGrid.__name__: lambda: {
                "bot_constructor": BotGrid,
                "bot_config": bot_grid_input.config(),
            },
        }
    )

except Exception as e:
    logger.error("Unknown error occured.", e)
    st.error(f"Error: {str(e)}.", icon="🚨")
