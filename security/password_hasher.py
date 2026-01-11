import hashlib
import os



class PasswordHasher:
    """
    Responsible for secure password hashing and verification.
    """

    ITERATIONS = 200_000
    SALT_SIZE = 16 # bytes


    @staticmethod
    def hash_password(password: str) -> tuple[str, str]:
        """
        Hash a password using PBKDF2-HMAC-SG+HA256.
        
        Returns:
            (salt_hex, hash_hex)
        """

        if not password:
            raise ValueError("Password must not be empty")
        

        salt = os.urandom(PasswordHasher.SALT_SIZE)

        hash_bytes = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            PasswordHasher.ITERATIONS,
        )

        return salt.hex(), hash_bytes.hex()
    


    @staticmethod
    def verify(password: str, salt_hex: str, hash_hex:str) -> bool:
        """
        Verify a password against an existing salt and hash.
        """
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)


        test_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            PasswordHasher.ITERATIONS,
        )

        return test_hash == expected_hash