from typing import Callable, Type, TypedDict, cast
import streamlit as st

from bot.bot import Bot, BotConfig


BotConstructor = Type[Bot]


class ReportBotConfig(TypedDict):
    bot_constructor: BotConstructor
    bot_config: BotConfig


ReportBotConfigBuilder = Callable[[], ReportBotConfig]

ReportBotRepository = dict[str, ReportBotConfigBuilder]


def config(repository: ReportBotRepository) -> ReportBotConfig:
    bot_name = input_bot_name(repository)
    return repository[bot_name]()


def input_bot_name(repository: ReportBotRepository):
    return cast(
        str,
        st.sidebar.selectbox("Name", options=list(repository.keys()), index=0),
    )
