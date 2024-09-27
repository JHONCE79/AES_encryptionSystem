## Authors: 
Paula Meneses y Santiago Tavera

# Text encryption and decryption system
This program is a text encryption and decryption system, which uses the AES algorithm to encrypt and decrypt a text.

### Preconditions
1. Make sure you have Python installed on your computer.

## The repository contains:
The project is divided into two main folders, `src` and a `tests` folder. 

`src` contains the main file of the program, which is the `Console.py` file. This file contains the main menu of the program and the logic to encrypt and decrypt the text. In addition, it contains the `AES.py` file, which contains the functions to encrypt and decrypt the text. Also it has the `GuiSystem.py` file, which contains the functions to encrypt and decrypt the text using a GUI made with **Kivy**. 

`tests` contains the unit `tests` (normal cases, special or extraordinary cases, and error cases). 


## How to run the program:
1. CLone the repository to your computer.

```git clone "https://github.com/PaulaS06/AES_encryptionSystem.git"```

2. Navigate to the folder where the repository was cloned

```src/Console/Console.py```

3. Run the main file to excute the program on the Console:

```python src/Console/Console.py```

4. To run the program with the GUI:

```python src/GUI/GuiSystem.py```

## How does the program work:
When you run the program, you will see a menu with the following options:
```
1. Encrypt text
2. Decrypt text
3. Exit
```
The program will ask you to enter the number of the option you want to select.

4. If you select option 1, the program will ask you to enter the text you want to _encrypt_.

5. If you select option 2, the program will ask you to enter the text you want to _decrypt_.

- If you select option 1 or 2, the program will ask you to enter the key you want to use to encrypt or decrypt the text.
- The key **must** be 16 characters long.


- After entering the text and the key, the program will show you the encrypted or decrypted text.

6. If you select option 3, the program will end.


## Take into account:
- The project includes a set of unit tests that are used to verify compliance with requirements. 
To run the tests, you must install the Unittest dependency.
You can install it by running the following command in the terminal:

```pip install unittest```
