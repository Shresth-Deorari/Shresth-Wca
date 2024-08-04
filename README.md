# WhatsApp Chat Analyzer

## Overview

WhatsApp Chat Analyzer is a Streamlit-based web application that allows users to analyze their WhatsApp chat logs. Users can log in, sign up, or reset their password within the app. Once authenticated, users can upload a WhatsApp chat text file and get insights into their chat history, including statistics, timelines, word clouds, and emoji usage.

## Features

- **User Authentication**: Users can log in, sign up, or reset their password.
- **File Upload**: Upload WhatsApp chat text files for analysis.
- **Chat Statistics**: View total messages, words, media shared, and URLs shared.
- **Timeline Analysis**: Visualize message activity over time.
- **Most Active Users**: Identify the most active users in the chat.
- **Word Cloud**: Generate a word cloud for the most frequently used words.
- **Emoji Analysis**: Display the top 20 most used emojis.

## Getting Started

### Prerequisites

- Python 3.7+
- `pip` package manager

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
    cd whatsapp-chat-analyzer
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your database. Create a `.env` file in the root directory with your database configuration:
    ```
    DATABASE_URL=sqlite:///./test.db
    ```

### Running the Application

1. Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501` to access the application.

### Usage

1. **Login or Sign Up**: If you are a new user, sign up for an account. Existing users can log in with their credentials.
2. **Upload Chat File**: After logging in, upload your WhatsApp chat text file.
3. **Analyze**: Select a user from the chat to analyze and click the "Start Analysis" button.
4. **View Results**: Explore various statistics, timelines, word clouds, and emoji usage.

## Project Structure

```plaintext
whatsapp-chat-analyzer/
├── app.py                   # Main application file
├── database.py              # Database models and session management
├── requirements.txt         # Required packages
├── .env                     # Environment variables for database configuration
├── Data_Processor.py        # Module for processing chat data
├── My_functions.py          # Module for analysis functions
└── README.md                # Project documentation
