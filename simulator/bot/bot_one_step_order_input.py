import streamlit as st


def step_to_price_ratio():
    return (
        st.sidebar.slider(
            "Step to price ratio, %",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="How much price should change in %, to make an action",
        )
        / 100.0
    )


def order_leverage():
    return st.sidebar.slider(
        "Order Leverage",
        min_value=1.0,
        max_value=100.0,
        value=2.0,
        step=1.0,
    )


def order_quantity():
    return st.sidebar.number_input(
        "Order Quantity",
        min_value=0.001,
        max_value=1000.0,
        value=0.01,
        step=0.001,
        format="%0.3f",
    )


def tp_to_entry_price_ratio():
    return (
        st.sidebar.slider(
            "Take Profit to entry price ratio, %",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
        )
        / 100.0
    )


def sl_to_entry_price_ratio():
    return (
        st.sidebar.slider(
            "Stop Loss to entry price ratio, %",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
        )
        / -100.0
    )


def inverted():
    return st.sidebar.checkbox(
        "Inverted",
        value=False,
        help="Change BUY and SELL sides in algorythm",
    )


def config():
    return dict(
        step_to_price_ratio=step_to_price_ratio(),
        tp_to_entry_price_ratio=tp_to_entry_price_ratio(),
        sl_to_entry_price_ratio=sl_to_entry_price_ratio(),
        inverted=inverted(),
        order_quantity=order_quantity(),
        order_leverage=order_leverage(),
    )
