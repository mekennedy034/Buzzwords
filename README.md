# Buzzwords

Buzzwords is a clone of the New York Times' Spelling Bee puzzle, created with pygames 2.0.1 for Python 3.9.5. It's mostly a learning project for myself and not intended for commercial distribution.

## Files

```buzzwords.py``` is the main game file. 

```bee_dict.txt``` is the game's dictionary of legit words. It was scraped from William Shunn's archive of Spelling Bee puzzles (https://www.shunn.net/bee/) with a few personal additions. The Spelling Bee uses a curated dictionary that excludes proper nouns, hyphenated or open compounds, and words deemed offensive or obscure.

```pangrams.txt``` is a subset of ```bee_dict.txt``` containing only words made of exactly seven unique letters. This is uses to generate puzzles in Buzzwords.

```hive_board.bmp``` is the honeycomb-patterned "board" for Buzzwords (and Spelling Bee).

## How To Play

Run ```buzzwords.py``` from the command line or double-click on the file (assuming you have compatible versions of Python and pygames installed). The gui for the game will pop up in a separate window. Click on the gray bar to enter a word; correct guesses will be displayed to the right of the board, and error messages will be displayed below the text entry bar. 

Buzzwords puzzles consist of a "hive" of seven letters. The goal is to create as many words as possible using these letters. Words must be at least 4 letters in length and must contain the center letter on the board. The same letter can be used repeatedly. 

Scoring words as follows:
* 1 point for each 4-letter word
* Longer words give one point per letter
* A pangram grants an additional 7-point bonus. Pangrams are words that use all the letters in the hive at least once, and every puzzle has at least one pangram.

The status bar directly below the board reports your current score, as well as how many words you have found.

## Known Bugs
* The list of found words sometimes overruns the edges of the screen.
* The list of found words is not correctly updated when the final word is entered.

"This word isn't accepted as an answer" is not a bug; just add it to ```bee_dict.txt``` yourself if you think it should be included. 

## Contributing
This is a learning project not intended for widespread distribution. 

## License
[MIT](https://choosealicense.com/licenses/mit/)
