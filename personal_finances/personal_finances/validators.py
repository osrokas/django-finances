from re import findall
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

# class CustomValidator:
#     def __init__(self, text):
#         self.text = text

#     def validate(self, password, user=None):
#         pass

#     def get_help_text(self):
#         return self.text

class UpperCaseVallidator:
    def __init__(self):
        self.text = _("Your password must contain at least 1 uppercase letter, A-Z.")

    def validate(self, password, user=None):
        if not findall(r"[A-Z]", password):
            raise ValidationError(self.text, code="password_no_upper")

    def get_help_text(self):
        return (self.text)

class NumberValidator:
    def __init__(self) -> None:
        self.text = _("Your password must contain at least one number, 0-9.")

    def validate(self, password, user=None):
        if not findall(r"[0-9]", password):
            raise ValidationError(self.text, code="password_no_number")

    def get_help_text(self):
        return self.text

class SpecialSymbolValidator:
    def __init__(self) -> None:
        self.text = _(
            "Your password must contain at least one special symbol. ! @ # $ % ^ & * are valid symbols."
        )

    def validate(self, password, user=None):
        if not findall(r"[!@#$%^&*]", password):
            raise ValidationError(self.text, code="password_no_special_symbol")

    def get_help_text(self):
        return self.text
