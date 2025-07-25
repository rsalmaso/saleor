import datetime

from django.core.exceptions import ValidationError

from ....channel.models import Channel
from ...core.enums import ChannelErrorCode

DELETE_EXPIRED_ORDERS_MAX_DAYS = 120


def clean_expire_orders_after(expire_orders_after: int) -> int | None:
    if expire_orders_after is None or expire_orders_after == 0:
        return None
    if expire_orders_after < 0:
        raise ValidationError(
            {
                "expire_orders_after": ValidationError(
                    "Expiration time for orders cannot be lower than 0.",
                    code=ChannelErrorCode.INVALID.value,
                )
            }
        )
    return expire_orders_after


def clean_delete_expired_orders_after(
    delete_expired_orders_after: int,
) -> datetime.timedelta:
    if (
        delete_expired_orders_after < 1
        or delete_expired_orders_after > DELETE_EXPIRED_ORDERS_MAX_DAYS
    ):
        raise ValidationError(
            {
                "delete_expired_orders_after": ValidationError(
                    "Delete time for expired orders needs to be in range from 1 to "
                    f"{DELETE_EXPIRED_ORDERS_MAX_DAYS}.",
                    code=ChannelErrorCode.INVALID.value,
                )
            }
        )
    return datetime.timedelta(days=delete_expired_orders_after)


def clean_checkout_ttl_before_releasing_funds(
    checkout_ttl_before_releasing_funds: int,
) -> datetime.timedelta:
    if checkout_ttl_before_releasing_funds <= 0:
        raise ValidationError(
            {
                "checkout_ttl_before_releasing_funds": ValidationError(
                    "The time in hours after which funds for expired checkouts will be released must be greater than 0.",
                    code=ChannelErrorCode.INVALID.value,
                )
            }
        )
    return datetime.timedelta(hours=checkout_ttl_before_releasing_funds)


def clean_input_order_settings(
    order_settings: dict, cleaned_input: dict, instance: Channel
):
    channel_settings = [
        "automatically_confirm_all_new_orders",
        "automatically_fulfill_non_shippable_gift_card",
        "allow_unpaid_orders",
        "include_draft_order_in_voucher_usage",
    ]

    for field in channel_settings:
        if (value := order_settings.get(field)) is not None:
            cleaned_input[field] = value

    if (
        mark_as_paid_strategy := order_settings.get("mark_as_paid_strategy")
    ) is not None:
        cleaned_input["order_mark_as_paid_strategy"] = mark_as_paid_strategy

    if "expire_orders_after" in order_settings:
        expire_orders_after = order_settings["expire_orders_after"]
        cleaned_input["expire_orders_after"] = clean_expire_orders_after(
            expire_orders_after
        )

    if "delete_expired_orders_after" in order_settings:
        delete_expired_orders_after = order_settings["delete_expired_orders_after"]
        cleaned_input["delete_expired_orders_after"] = (
            clean_delete_expired_orders_after(delete_expired_orders_after)
        )

    cleaned_input["prev_include_draft_order_in_voucher_usage"] = (
        instance.include_draft_order_in_voucher_usage
    )

    if "draft_order_line_price_freeze_period" in order_settings:
        cleaned_input["draft_order_line_price_freeze_period"] = order_settings[
            "draft_order_line_price_freeze_period"
        ]

    # For newly created channels, by default use new discount propagation flow
    if instance.pk is None:
        cleaned_input["use_legacy_line_discount_propagation_for_order"] = False

    if order_settings.get("use_legacy_line_discount_propagation") is not None:
        cleaned_input["use_legacy_line_discount_propagation_for_order"] = (
            order_settings["use_legacy_line_discount_propagation"]
        )


def clean_input_checkout_settings(checkout_settings: dict, cleaned_input: dict):
    input_to_model_fields = {
        "use_legacy_error_flow": "use_legacy_error_flow_for_checkout",
        "automatically_complete_fully_paid_checkouts": "automatically_complete_fully_paid_checkouts",
    }
    for input_field, model_field in input_to_model_fields.items():
        if input_field in checkout_settings:
            cleaned_input[model_field] = checkout_settings[input_field]


def clean_input_payment_settings(payment_settings: dict, cleaned_input: dict):
    if default_transaction_strategy := payment_settings.get(
        "default_transaction_flow_strategy"
    ):
        cleaned_input["default_transaction_flow_strategy"] = (
            default_transaction_strategy
        )
    if (
        release_funds_for_expired_checkouts := payment_settings.get(
            "release_funds_for_expired_checkouts"
        )
    ) is not None:
        cleaned_input["release_funds_for_expired_checkouts"] = (
            release_funds_for_expired_checkouts
        )

    if (
        checkout_ttl_before_releasing_funds := payment_settings.get(
            "checkout_ttl_before_releasing_funds"
        )
    ) is not None:
        cleaned_input["checkout_ttl_before_releasing_funds"] = (
            clean_checkout_ttl_before_releasing_funds(
                checkout_ttl_before_releasing_funds
            )
        )

    if "checkout_release_funds_cut_off_date" in payment_settings:
        checkout_release_funds_cut_off_date = payment_settings[
            "checkout_release_funds_cut_off_date"
        ]
        cleaned_input["checkout_release_funds_cut_off_date"] = (
            checkout_release_funds_cut_off_date
        )
