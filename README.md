# OpenAI telegram bot

## Description
A Telegram bot where you choose one of 5 locations and fill out a checklist,
after which you can leave a comment and donate photos. After completing the checklist,
a report is generated that is sent to OpenAI for analysis by artificial intelligence,
and the result is sent to the user in Telegram

# Guideline how to use
1. Open terminal and clone the repo (`git clone https://github.com/prochigor/Telegram-openai-report.git`)
2. Open cloned folder
3. Activate venv on the project Open terminal and write: On Windows: (`python -m venv venv`)
and (`venv\Scripts\activate`) On Mac: (`python3 -m venv venv`) and (`source venv/bin/activate`)
4. Install needed requirements: Write in terminal (`pip install -r requirements.txt`)
5. Create file `.env` and add keys to your telegram token and openai api key, example in file `.env.sample`
6. go to file `bot/handlers.py` and run project
