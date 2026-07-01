import heapq
import os
import pickle
from collections import Counter
from compressor.node import Node

class HuffmanCoding:
    """Compress and decompress text files using Huffman Coding."""

    def __init__(self) -> None:
        self._reset_state()

    def _reset_state(self) -> None:
        """Reset internal data structures."""
        self.heap = []
        self.codes = {}

    def _read_file(self, path: str) -> str:
        """Read and return the contents of a text file."""
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    
    def _build_frequency_table(self, text):
        return Counter(text)
    
    def _build_heap(self, frequency):
        for char, freq in frequency.items():
            node = Node(char, freq)
            heapq.heappush(self.heap, node)

    def _merge_nodes(self):
        while len(self.heap) > 1:
            left = heapq.heappop(self.heap)
            right = heapq.heappop(self.heap)
            merged = Node(freq=left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(self.heap, merged)


    def _build_codes_helper(self, root: Node, current_code: str) -> None:
        """
        Traverse the Huffman tree using DFS.
        Left edge  -> append '0'
        Right edge -> append '1'
        """
        if root is None:
            return
        if root.char is not None:
            if current_code == "":
                current_code = "0"
            self.codes[root.char] = current_code
            return
        self._build_codes_helper(root.left, current_code + "0")
        self._build_codes_helper(root.right, current_code + "1")

    def _build_codes(self):
        root = heapq.heappop(self.heap)
        self._build_codes_helper(root, "")

    def _get_encoded_text(self, text):
        encoded = []
        for char in text:
            encoded.append(self.codes[char])
        return "".join(encoded)
    
    def _pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        if extra_padding == 8:
            extra_padding = 0
        encoded_text += "0" * extra_padding
        padding_info = f"{extra_padding:08b}" #convert to binary using exactly 8 bits
        return padding_info + encoded_text
    
    def _get_byte_array(self, padded_encoded_text):
        byte_array = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            byte_array.append(int(byte, 2))
        return byte_array
    

    def compress(self, input_path)->None:
        """Compress a text file using Huffman coding."""
        self._reset_state()
        # Read the input file
        text = self._read_file(input_path)
        if not text:
            raise ValueError("Input file is empty.")
        # build Huffman Tree
        frequency = self._build_frequency_table(text)
        self._build_heap(frequency)
        self._merge_nodes()
        self._build_codes()

        # Encode the text
        encoded_text = self._get_encoded_text(text)

        # Pad and convert to bytes
        padded_text = self._pad_encoded_text(encoded_text)
        byte_array = self._get_byte_array(padded_text)

        # Create output file path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(base_dir, "output", f"{filename}.bin")

        # Write compressed file
        with open(output_path, "wb") as output:
            pickle.dump(frequency, output)
            output.write(byte_array)

        print(f"Compressed file saved to {output_path}")
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)

        ratio = original_size / compressed_size
        saved = (1 - compressed_size / original_size) * 100

        print("\nCompression Statistics")
        print("="*25)
        print(f"Original Size   : {original_size} bytes")
        print(f"Compressed Size : {compressed_size} bytes")
        print(f"Compression Ratio : {ratio:.2f}:1")
        print(f"Space Saved     : {saved:.2f}%")


    def _read_compressed_file(self, input_path):
        with open(input_path, "rb") as file:
            frequency = pickle.load(file)
            compressed_bytes = file.read()
        return frequency, compressed_bytes
    
    def _get_bit_string(self, compressed_bytes):
        return "".join(f"{byte:08b}" for byte in compressed_bytes)
    
    def _remove_padding(self, padded_bit_string):
        # First 8 bits store the amount of padding
        padding_info = padded_bit_string[:8]
        extra_padding = int(padding_info, 2)

        # Remove the header
        encoded_text = padded_bit_string[8:]

        # Remove the padding bits
        if extra_padding > 0:
            encoded_text = encoded_text[:-extra_padding]
        return encoded_text
    
    def _decode_text(self, encoded_text: str, root: Node) -> str:
        """Decode the encoded bit string using the Huffman tree."""
        # File contained only one distinct character.
        if root.left is None and root.right is None:
            return root.char * len(encoded_text)

        decoded = []
        current = root
        for bit in encoded_text:
            if bit == "0":
                current = current.left
            else:
                current = current.right
            if current.char is not None:
                decoded.append(current.char)
                current = root
        return "".join(decoded)

    def decompress(self, input_path)->None:
        """Decompress a Huffman encoded binary file."""
        # Read frequency table and compressed bytes
        frequency, compressed_bytes = self._read_compressed_file(input_path)

        # Rebuild Huffman Tree
        self._reset_state()
        self._build_heap(frequency)
        self._merge_nodes()

        root = heapq.heappop(self.heap)

        # Recover encoded bit string
        bit_string = self._get_bit_string(compressed_bytes)
        encoded_text = self._remove_padding(bit_string)

        # Decode
        decoded_text = self._decode_text(encoded_text, root)

        # Output file path
        filename = os.path.splitext(os.path.basename(input_path))[0]
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_dir, "output", f"{filename}_decoded.txt")

        with open(output_path, "w", encoding="utf-8") as output:
            output.write(decoded_text)

        print("\nDecompression Successful!")
        print(f"Recovered file saved to {output_path}")