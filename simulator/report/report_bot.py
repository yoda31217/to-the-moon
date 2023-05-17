from typing import Callable, Type, TypedDict
from bot import bot_one_step_order_input
import streamlit as st

from bot.bot import Bot
from bot.bot_one_step_order import BotOneStepOrder


class ReportBotConfig(TypedDict):
    bot_constructor: Type[Bot]
    bot_config: dict[str, object]


bot_name_to_config_builder: dict[str, Callable[[], ReportBotConfig]] = {
    BotOneStepOrder.__name__: lambda: {
        "bot_constructor": BotOneStepOrder,
        "bot_config": bot_one_step_order_input.config(),
    }
}


def config() -> ReportBotConfig:
    bot_name = BotOneStepOrder.__name__
    st.sidebar.markdown(f"**Name: {bot_name}")
    return bot_name_to_config_builder[bot_name]()
