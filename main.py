from compressor.huffman import HuffmanCoding
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

coder = HuffmanCoding()
input_path = os.path.join(BASE_DIR, "input", "sample.txt")
output_path = os.path.join(BASE_DIR, "output", "sample.bin")

coder.compress(input_path)
coder.decompress(output_path)