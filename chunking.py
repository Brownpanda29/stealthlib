import random

class Chunking:
    def __init__(self, min_chunk_size=512 * 1024, max_chunk_size=1024 * 1024):
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size

    def split_data(self, data):
        """
        Splits data into random-sized chunks between min_chunk_size and max_chunk_size.
        """
        if not isinstance(data, (bytes, bytearray)):
            raise ValueError("Data must be in bytes or bytearray format.")
        
        start = 0
        data_length = len(data)
        while start < data_length:
            chunk_size = random.randint(self.min_chunk_size, self.max_chunk_size)
            end = min(start + chunk_size, data_length)
            yield data[start:end]
            start = end

    def join_chunks(self, chunks):
        """
        Reassembles chunks back into the original data.
        """
        if not all(isinstance(chunk, (bytes, bytearray)) for chunk in chunks):
            raise ValueError("All chunks must be in bytes or bytearray format.")
        return b"".join(chunks)
      
