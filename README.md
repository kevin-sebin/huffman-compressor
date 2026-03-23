# Huffman File Compressor (CLI Tool)

A command-line file compression tool built using Huffman Coding.
This project compresses `.txt` files into a custom `.huff` format and supports full lossless decompression.

---

## Features

* Compress text files using Huffman Coding
* Decompress `.huff` files back to original text
* Tree-based encoding and decoding
* Bit-level compression stored as binary
* Command-line interface (CLI)

---

## How It Works

1. Builds a frequency map of characters
2. Constructs a Huffman Tree using a min-heap
3. Generates prefix-free binary codes
4. Encodes the data into a bit string
5. Converts bits into bytes for storage
6. Serializes the tree for reconstruction during decompression

---

## Usage

### Compress a file

```bash
python main.py compress input.txt output.huff
```

### Decompress a file

```bash
python main.py decompress output.huff output.txt
```

---

## Use case

| File            | Size  |
| --------------- | ----- |
| original.txt    | 27 KB |
| compressed.huff | 15 KB |

~45% space saved using Huffman Coding.

---

## Project Structure

```
huffman-compressor/
│── main.py
│── README.md
│── requirements.txt
│── sample/
```

---

## Notes

* Works best on large text files with repetitive patterns
* Compression ratio depends on data distribution
* Tree metadata is stored along with compressed data

---

