import discord
from discord.ext import commands
from discord import app_commands
import random
import json

# Load the token from the JSON config file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
TOKEN = config['token']

# Load words from the external word list
with open('words.txt', 'r') as word_file:
    WORDS = [line.strip() for line in word_file.readlines()]

# Helper function to format the wordle message
def format_guess(guess, target):
    formatted = ""
    for i, letter in enumerate(guess):
        if letter == target[i]:
            formatted += f"🟩\u200B{letter.upper()}\u200B"
        elif letter in target:
            formatted += f"🟨\u200B{letter.upper()}\u200B"
        else:
            formatted += f"⬜\u200B{letter.upper()}\u200B"
    return formatted

class WordleGame:
    def __init__(self, target_word):
        self.target_word = target_word
        self.attempts = 6
        self.guesses = []

    def make_guess(self, guess):
        self.guesses.append(guess)
        return format_guess(guess, self.target_word)

    def is_correct(self, guess):
        return guess == self.target_word

    def out_of_attempts(self):
        return len(self.guesses) >= self.attempts

# Initialize the bot with the MESSAGE_CONTENT intent
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
tree = bot.tree

# Dictionary to keep track of ongoing games
games = {}

@bot.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {bot.user}')

@tree.command(name='startwordle', description='Start a new Wordle game')
async def start_wordle(interaction: discord.Interaction):
    if interaction.user.id in games:
        await interaction.response.send_message("You already have an ongoing game! Finish it before starting a new one.", ephemeral=True)
        return

    target_word = random.choice(WORDS)
    games[interaction.user.id] = WordleGame(target_word)
    embed = discord.Embed(title="Wordle Game Started!", description="You have 6 attempts to guess the 5-letter word.\nUse `/guess <word>` to make a guess.", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

@tree.command(name='guess', description='Make a guess in the Wordle game')
@app_commands.describe(guess='Your 5-letter guess')
async def make_guess(interaction: discord.Interaction, guess: str):
    if interaction.user.id not in games:
        await interaction.response.send_message("You don't have an ongoing game. Start one with `/startwordle`.", ephemeral=True)
        return

    if len(guess) != 5 or not guess.isalpha():
        await interaction.response.send_message("Please enter a valid 5-letter word.", ephemeral=True)
        return

    game = games[interaction.user.id]
    guess = guess.lower()
    response = game.make_guess(guess)

    if game.is_correct(guess):
        embed = discord.Embed(title="Congratulations!", description=f"You guessed the word: **{guess.upper()}**", color=discord.Color.gold())
        await interaction.response.send_message(embed=embed)
        del games[interaction.user.id]
    elif game.out_of_attempts():
        embed = discord.Embed(title="Game Over", description=f"Sorry, you're out of attempts! The word was: **{game.target_word.upper()}**", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        del games[interaction.user.id]
    else:
        embed = discord.Embed(title="Guess", description=f"{response}\nAttempts left: {game.attempts - len(game.guesses)}", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

@tree.command(name='endwordle', description='End the current Wordle game')
async def end_wordle(interaction: discord.Interaction):
    if interaction.user.id in games:
        del games[interaction.user.id]
        await interaction.response.send_message("Your Wordle game has been ended.")
    else:
        await interaction.response.send_message("You don't have an ongoing game.", ephemeral=True)

@tree.command(name='helpwordle', description='Get help with the Wordle bot commands')
async def help_wordle(interaction: discord.Interaction):
    embed = discord.Embed(title="Wordle Bot Help", description="Here are the available commands for the Wordle bot:", color=discord.Color.purple())
    embed.add_field(name="/startwordle", value="Start a new Wordle game.", inline=False)
    embed.add_field(name="/guess <word>", value="Make a guess in the Wordle game.", inline=False)
    embed.add_field(name="/endwordle", value="End the current Wordle game.", inline=False)
    embed.add_field(name="/helpwordle", value="Get help with the Wordle bot commands.", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
