from typing import Callable, Type, TypedDict, cast
import streamlit as st

from bot.bot import Bot


BotConstructor = Type[Bot]


class ReportBotConfig(TypedDict):
    bot_constructor: BotConstructor
    bot_config: dict[str, object]


ReportBotConfigBuilder = Callable[[], ReportBotConfig]

ReportBotRepository = dict[BotConstructor, ReportBotConfigBuilder]


def config(repository: ReportBotRepository) -> ReportBotConfig:
    bot_constructor = input_bot_constructor(repository)
    return repository[bot_constructor]()


def input_bot_constructor(repository: ReportBotRepository):
    return cast(
        BotConstructor,
        st.sidebar.selectbox("Name", options=list(repository.keys()), index=0),
    )
