# Shreyas's AI Tasks

This repository contains three Python projects:

1. CodBot - Chatbot using Tkinter  
2. Tic Tac Toe - Game using Pygame  
3. Book Recommendation System - Using machine learning techniques  

---

*1. CodBot - Chatbot using Tkinter

CodBot is a simple rule-based chatbot created using Python's `tkinter` library. It responds to user messages and provides useful replies like greetings, jokes, time, date, and more.

### Features
- User-friendly graphical interface
- Detects basic questions using keyword matching
- Gives time, date, jokes, and motivational quotes
- Replies are based on predefined logic
- Easy to extend with more questions and answers

### How to Run
Make sure Python is installed. Then run:

```bash
python codbot.py
```

---

## 2. Tic Tac Toe - Python Game using Pygame

This is a Tic Tac Toe game where the player plays as 'X' and the computer plays as 'O'. It is created using the `pygame` library.

### Features
- Graphical user interface with clean layout
- Smart computer opponent using basic strategy
- Shows winning line when a player wins
- "New Game" button to restart the match
- Good for practicing Python and game development

### How to Run
1. Make sure Python is installed.
2. Install pygame if not already:

```bash
pip install pygame
```

3. Run the game:

```bash
python tictactoe.py
```

---

## 3. Book Recommendation System - Python Project

This is a content-based book recommendation system. It uses book features like title, author, category, and year to recommend similar books.

### Features
- Reads book data from a CSV file
- Combines features using TF-IDF vectorization
- Calculates similarity between books using cosine similarity
- Matches user input with closest title
- Shows top 5 similar books

### Requirements
- Python 3.x
- pandas
- numpy
- scikit-learn

Install required packages using:

```bash
pip install pandas numpy scikit-learn
```

### How to Run
1. Place `recommender.py` and `data.csv` in the same folder.
2. Run the script:

```bash
python recommender.py
```

3. Enter your favorite book title when asked.

### Note
Make sure the CSV file has the following columns:
- `title`
- `authors`
- `categories`
- `published_year`
- `index`
