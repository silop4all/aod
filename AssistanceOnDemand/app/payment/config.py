# -*- coding: utf-8 -*-

from django.conf import settings

__payment__ = {
    "base": {
        "api": settings.PAYMENT_BASE
    },
    "endpoints": {
        "notifications": "/api/v1/notifications/webhooks",
        "payments": "/api/v1/payments/payment",
        "billing_plans": "/api/v1/payments/billing-plans",
        "billing_agreements": "/api/v1/payments/billing-agreements",
    }
}

__paypal__ = {
    "base": {
        "sandbox": "https://api.sandbox.paypal.com",
    },
    "endpoints": {
        "authentication": "/v1/oauth2/token",
        "billing_agreements": "/v1/payments/billing-agreements",
    }
}