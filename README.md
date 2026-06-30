# Huffman File Compressor

A lossless file compressor and decompressor implemented in Python using the Huffman Coding algorithm.

The project compresses text files into a binary format and restores them without any loss of information.

---

## Features

- Lossless text file compression
- Huffman tree construction using a Min Heap
- Binary file generation
- File decompression back to the original text
- Compression statistics
- Modular and object-oriented implementation

---

## Project Structure

```
huffman-compressor/
│
├── compressor/
│   ├── __init__.py
│   ├── node.py
│   └── huffman.py
│
├── input/
│   └── sample.txt
│
├── output/
│
├── main.py
└── README.md 
```

---

## Algorithm

1. Read the input text file.
2. Count the frequency of each character.
3. Build a Min Heap.
4. Construct the Huffman Tree.
5. Generate Huffman Codes using DFS.
6. Encode the input text.
7. Pad the encoded bit string.
8. Store the compressed binary data together with the frequency table.
9. Reconstruct the Huffman Tree during decompression.
10. Decode the bit stream to recover the original text.

---

## How to Run

Clone the repository

```bash
git clone https://github.com/Mayank171006/huffman-file-compressor.git
```

Move into the project directory

```bash
cd huffman-file-compressor
```

Run

```bash
python main.py
```

---

## Sample Output

```
Compressed file saved to output/sample.bin

Compression Statistics
----------------------
Original Size   : 90431 bytes
Compressed Size : 48484 bytes
Compression Ratio : 1.87:1
Space Saved     : 46.39%

Decompression Successful!
Recovered file saved to output/sample_decoded.txt
```

---

## Time Complexity

Let

- **n** = number of characters in the input
- **σ** = number of distinct characters

| Operation | Complexity |
|-----------|------------|
| Frequency Count | O(n) |
| Build Heap | O(σ log σ) |
| Build Huffman Tree | O(σ log σ) |
| Generate Codes | O(σ) |
| Encoding | O(n) |
| Decoding | O(n) |

Overall:

```
Compression : O(n + σ log σ)

Decompression : O(n + σ log σ)
```

---

## Space Complexity

- Frequency Table: **O(σ)**
- Huffman Tree: **O(σ)**
- Encoded Bit Stream: **O(n)**

Overall:

```
O(n + σ)
```

---

## Technologies Used

- Python
- heapq
- Counter
- pickle
- Object-Oriented Programming

---

## Future Improvements

- Replace `pickle` with a custom binary header to reduce metadata overhead.
- Support compression of arbitrary binary files.
- Add a command-line interface.
- Add a graphical user interface.
- Improve compression for very small files.

---

## Author

**Mayank Kumar**
