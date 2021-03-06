""" Cryptographic Signing Module """
from cryptography.fernet import Fernet

from masonite.exceptions import InvalidSecretKey


class Sign:
    """Cryptographic signing class.
    """

    def __init__(self, key=None):
        """Sign constructor
        
        Keyword Arguments:
            key {string} -- The secret key to use. If nothing is passed it then it will use
                            the secret key from the config file. (default: {None})
        
        Raises:
            InvalidSecretKey -- Thrown if the secret key does not exist.
        """

        if key:
            self.key = key
        else:
            from config import application
            self.key = application.KEY

        if not self.key:
            raise InvalidSecretKey("The encryption key passed in is: None. Be sure there is a secret key present in your .env file or your config/application.py file.")

        self.encryption = None

    def sign(self, value):
        """Sign a value using the secret key.
        
        Arguments:
            value {string} -- The value to be encrypted.
        
        Returns:
            string -- Returns the encrypted value.
        """

        f = Fernet(self.key)
        self.encryption = f.encrypt(bytes(value, 'utf-8'))
        return self.encryption.decode('utf-8')

    def unsign(self, value=None):
        """Unsigns the value using the secret key.
        
        Keyword Arguments:
            value {string} -- The value to be unencrypted. (default: {None})
        
        Returns:
            string -- Returns the unencrypted value.
        """
        
        f = Fernet(self.key)

        if not value:
            return f.decrypt(self.encryption).decode('utf-8')
        return f.decrypt(bytes(value, 'utf-8')).decode('utf-8')
