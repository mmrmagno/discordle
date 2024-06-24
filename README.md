# Discordle
---

![Discordle](https://www.marc-os.com/discordle.webp)

Welcome to the Discordle repository! This bot allows users to play the popular word guessing game, Wordle, directly in a Discord chat.

## Features

- Start a new Wordle game
- Make guesses and receive feedback
- Color-coded responses indicating correct and incorrect letters
- End an ongoing game
- Get help with bot commands

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/wordle-discord-bot.git
    cd wordle-discord-bot
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your configuration:**

    - Create a `config.json` file in the project directory and add your Discord bot token:

    ```json
    {
        "token": "YOUR_DISCORD_BOT_TOKEN"
    }
    ```

5. **Run the bot:**

    ```bash
    python bot.py
    ```

## Usage

### Commands

- `/startwordle` - Starts a new Wordle game.
- `/guess <word>` - Makes a guess for the Wordle game.
- `/endwordle` - Ends the current Wordle game.
- `/helpwordle` - Get help with the Wordle bot commands.

### Example

1. Start a new game:

    ```
    /startwordle
    ```

    The bot will respond:
    ```
    Wordle game started! You have 6 attempts to guess the 5-letter word. Use `/guess <word>` to make a guess.
    ```

2. Make a guess:

    ```
    /guess apple
    ```

    The bot will respond with a formatted message showing the result of your guess.

3. End the game:

    ```
    /endwordle
    ```

    The bot will respond:
    ```
    Your Wordle game has been ended.
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or enhancements.

## Acknowledgements

- [discord.py](https://github.com/Rapptz/discord.py) - A Python wrapper for the Discord API
- Wordle - The original word guessing game

---

Thank you for using the Wordle Discord Bot! Have fun playing Wordle with your friends!
