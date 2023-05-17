from typing import Type, TypedDict
from bot import bot_one_step_order_input

from bot.bot import Bot
from bot.bot_one_step_order import BotOneStepOrder


class ReportBotConfig(TypedDict):
    bot_name: str
    bot_constructor: Type[Bot]
    bot_config: dict[str, object]


def config() -> ReportBotConfig:
    return {
        "bot_name": "One Step & Order",
        "bot_constructor": BotOneStepOrder,
        "bot_config": bot_one_step_order_input.config(),
    }
