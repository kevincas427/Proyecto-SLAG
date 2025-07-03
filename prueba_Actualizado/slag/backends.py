# slag/backends.py
from django.core.mail.backends.smtp import EmailBackend
import ssl
import certifi

class CustomEmailBackend(EmailBackend):
    def open(self):
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        return super().open()
