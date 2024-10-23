# Text Encryption and Decryption System

## Original Authors:

Paula Meneses  
Santiago Tavera

## Fork Authors:

Tomás Córdoba  
Samuel Villa

## Purpose

This project provides a text encryption and decryption tool using the AES (Advanced Encryption Standard) algorithm. It allows users to securely encrypt a piece of text and decrypt it later using the same key. The system offers both a console-based and a graphical user interface (GUI) for performing these operations.

## How does it work?

The system uses the AES algorithm to encrypt and decrypt text. The AES algorithm is a symmetric key encryption algorithm that uses a 128-bit block size and a key size of 128, 192, or 256 bits. The system uses a 128-bit key to encrypt and decrypt text.

## Project Structure

The project is divided into three main components:

1. **Console**: Contains the console-based system for encrypting and decrypting text and database operations.

2. **GUI**: Contains the graphical user interface for the system.

3. **Controller**: Contains the database controller for storing and retrieving encrypted text.

## Installation and Use

### 1. Clone the Repository:

Run the following command in your terminal:

    git clone "https://github.com/T-cordoba/AES_encryptionSystem.git"

### 2. Navigate to the Project Directory:

Change your directory to where the repository was cloned:

    cd path\to\AES_encryptionSystem

### 3. Create a Virtual Environment (Optional)

It is recommended to create a virtual environment for the project:

#### Windows:

    py -m venv .venv
    .venv\Scripts\activate

#### macOS/Linux:

    python3 -m venv venv
    source venv/bin/activate

### 4. Install Requirements

Install additional dependencies using the `requirements.txt` file:

    pip install -r requirements.txt

### 5. Fill config_sample.py credentials

To use the database functionality, fill the `config_sample.py` file with the necessary credentials and rename it to `config.py`.

### 6. Execute the Program

#### Console Execution:

To run the program via the console, use the following command:

    python src/Console/console.py

To run the database console execution, use the following command:

    python src/Console/db_console_execution.py

#### GUI Execution:

To execute the program with a graphical interface, use this command:

    python src/GUI/GUISystem.py

### 6. Running Tests

To verify the system using unit tests, navigate to the `tests` directory and run the corresponding test files:

    python tests/EncryptionAES_test.py
    python tests/DecryptionAES_test.py
    python tests/DB_test.py

## Notes

- The encryption key **must** be exactly 16, 24 or 32 characters long for the AES algorithm to function correctly.
- The unit tests validate the program's behavior in both typical and edge cases.
- To run the tests, you need to install the `unittest` package by running:

    pip install unittest
