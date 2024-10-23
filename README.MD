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

Once the program is executed, users can choose to encrypt or decrypt text via a menu. The process requires the following steps:

1. **Menu Options:**
    - The user is presented with three options:
      1. Encrypt text
      2. Decrypt text
      3. Exit
2. **Encryption/Decryption Process:**
    - For encryption, the user is prompted to enter the text to encrypt and a 16-character key.
    - For decryption, the user must input the encrypted text and the same 16-character key.
3. **Output:**
    - After providing the required inputs, the program will display the encrypted or decrypted result.

## Project Structure

The project is organized into two main directories: `src` and `tests`.

- **`src`:** Contains the core files needed to run the encryption and decryption system:
  - `Console.py`: Main file that presents the console interface and handles user input for encryption and decryption.
  - `AES.py`: Contains the AES encryption and decryption logic.
  - `GuiSystem.py`: Provides the functions needed to run the system with a GUI built using **Kivy**.
  
- **`tests`:** Contains unit tests that check the system for normal, special, and error cases.

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

### 5. Execute the Program

#### Console Execution:

To run the program via the console, use the following command:

    python src/Console/Console.py

#### GUI Execution:

To execute the program with a graphical interface, use this command:

    python src/GUI/GuiSystem.py

### 6. Running Tests

To verify the system using unit tests, navigate to the `tests` directory and run the corresponding test files:

    python tests/EncryptionAES_test.py
    python tests/DecryptionAES_test.py

## Notes

- The encryption key **must** be exactly 16 characters long for the AES algorithm to function correctly.
- The unit tests validate the program's behavior in both typical and edge cases.
- To use the database functionality, ensure that the `secret_config.py` file is present in the root of the project. This file should contain the necessary configuration for connecting to your database.
- To run the tests, you need to install the `unittest` package by running:

    pip install unittes
