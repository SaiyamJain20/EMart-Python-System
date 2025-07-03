import uuid
import hashlib
from src.helperFunctions import is_valid_email

class User:
    """
    Represents a user in the system.

    Attributes:
        user_id (str): Unique identifier for the user.
        username (str): Username of the user.
        email (str): Email address of the user.
        password_hash (str): Hashed password for security.
    """

    def __init__(self, username: str, password: str, email: str):
        """
        Initializes a new user instance.
        """
        username, password, email = username.strip(), password.strip(), email.strip()

        if not username or not password or not email:
            raise ValueError("All fields are required.")
        
        if not is_valid_email(email):
            raise ValueError("Invalid email format.")
        
        self.user_id = uuid.uuid4().hex
        self.username = username
        self.email = email
        self.password_hash = self._hash_password(password)

    def _hash_password(self, password: str) -> str:
        """
        Hashes the password using SHA-256.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, password: str) -> bool:
        """
        Authenticates a user by checking the password.
        """
        return self._hash_password(password) == self.password_hash
