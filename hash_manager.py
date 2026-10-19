import hashlib

class HashManager:
    def __init__(self, hash_type: str = 'sha256'):
        self.hash_type = hash_type

    def verify(self, file, hash: str) -> bool:
        return hash == self.calculate_sha256(file)

    def calculate_sha256(self, file) -> str:
        digest = hashlib.sha256()

        with open(file, "rb") as f:
            while chunk := f.read(1024):
                digest.update(chunk)

        return digest.hexdigest()
