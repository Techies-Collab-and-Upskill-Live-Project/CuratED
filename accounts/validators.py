from django.core.exceptions import ValidationError
import re

class PasswordComplexityValidator:
    def validate(self, password, user=None):
        if not re.search('[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search('[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search('[0-9]', password):
            raise ValidationError('Password must contain at least one number.')
        if not re.search('[^A-Za-z0-9]', password):
            raise ValidationError('Password must contain at least one special character.')

    def get_help_text(self):
        return 'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.'
