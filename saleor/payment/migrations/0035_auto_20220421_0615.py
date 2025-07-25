# Generated by Django 3.2.12 on 2022-04-21 06:15

from decimal import Decimal

import django.contrib.postgres.fields
import django.contrib.postgres.indexes
import django.db.models.deletion
from django.db import migrations, models

import saleor.core.utils.json_serializer


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0137_alter_orderevent_type"),
        ("checkout", "0042_rename_created_checkout_created_at"),
        ("payment", "0034_auto_20220414_1051"),
    ]

    operations = [
        migrations.CreateModel(
            name="TransactionItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "private_metadata",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                        null=True,
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("status", models.CharField(blank=True, default="", max_length=512)),
                ("type", models.CharField(blank=True, default="", max_length=512)),
                ("reference", models.CharField(blank=True, default="", max_length=512)),
                (
                    "available_actions",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("capture", "Capture payment"),
                                ("refund", "Refund payment"),
                                ("void", "Void payment"),
                            ],
                            max_length=128,
                        ),
                        default=list,
                        size=None,
                    ),
                ),
                ("currency", models.CharField(max_length=3)),
                (
                    "captured_value",
                    models.DecimalField(
                        decimal_places=3, default=Decimal(0), max_digits=12
                    ),
                ),
                (
                    "authorized_value",
                    models.DecimalField(
                        decimal_places=3, default=Decimal(0), max_digits=12
                    ),
                ),
                (
                    "refunded_value",
                    models.DecimalField(
                        decimal_places=3, default=Decimal(0), max_digits=12
                    ),
                ),
                (
                    "voided_value",
                    models.DecimalField(
                        decimal_places=3, default=Decimal(0), max_digits=12
                    ),
                ),
                (
                    "checkout",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="payment_transactions",
                        to="checkout.checkout",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payment_transactions",
                        to="order.order",
                    ),
                ),
            ],
            options={
                "ordering": ("pk",),
            },
        ),
        migrations.CreateModel(
            name="TransactionEvent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("success", "Success"),
                            ("failure", "Failure"),
                        ],
                        default="success",
                        max_length=128,
                    ),
                ),
                ("reference", models.CharField(blank=True, default="", max_length=512)),
                ("name", models.CharField(blank=True, default="", max_length=512)),
                (
                    "transaction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="payment.transactionitem",
                    ),
                ),
            ],
            options={
                "ordering": ("pk",),
            },
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="transactionitem",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["private_metadata"], name="transactionitem_p_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="transactionitem",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["metadata"], name="transactionitem_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="transactionitem",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["order_id", "status"], name="payment_tra_order_i_e783c4_gin"
            ),
        ),
    ]
