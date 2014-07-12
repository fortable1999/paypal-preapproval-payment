"""
Paypal currency code
defined at:
    https://developer.paypal.com/docs/classic/api/currency_codes/
"""
CURRENCY_CODE_CHOICES = (
    ('AUD', 'Australian Dollar'),

    # This currency is supported as a payment currency and a currency balance for in-country PayPal accounts only.
    ('BRL', 'Brazilian Real'),

    ('CAD', 'Canadian Dollar'),

    ('CZK', 'Czech Koruna'),

    ('DKK', 'Danish Krone'),

    ('EUR', 'Euro'),

    ('HKD', 'Hong Kong Dollar'),

    # Decimal amounts are not supported for this currency
    ('HUF', 'Hungarian Forint'),

    ('HKD', 'Hong Kong Dollar'),

    ('ILS', 'Israeli New Sheqel'),


    # This currency does not support decimals. Passing a decimal amount will throw an error.
    # max 1,000,000
    ('JPY', 'Japanese Yen'),

    # This currency is supported as a payment currency and a currency balance for in-country PayPal accounts only.
    ('MYR', 'Malaysian Ringgit '),

    ('MXN', 'Mexican Peso'),

    ('NOK', 'Norwegian Krone'),

    ('NZD', 'New Zealand Dollar'),

    ('PHP', 'Philippine Peso'),

    ('PLN', 'Polish Zloty'),

    ('GBP', 'Pound Sterling'),

    ('RUB', 'Russian Ruble'),

    ('SGD', 'Singapore Dollar'),

    ('SEK', 'Swedish Krona'),

    ('CHF', 'Swiss Franc'),

    # Decimal amounts are not supported for this currency. Passing a decimal amount will throw an error.
    ('TWD', 'Taiwan New Dollar'),

    ('THB', 'Thai Baht'),

    # This currency is supported as a payment currency and a currency balance for in-country PayPal accounts only.
    ('TRY', 'Turkish Lira'),

    ('USD', 'U.S. Dollar'),
)

