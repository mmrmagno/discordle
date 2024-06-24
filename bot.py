import discord
from discord.ext import commands
import random
import string
import json

# Load the token from the JSON config file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
TOKEN = config['token']

# List of possible words (you can expand this list)
WORDS = ["apple", "berry", "cherry", "grape", "lemon", "melon", "peach", "plumb"]

# Helper function to format the wordle message
def format_guess(guess, target):
    formatted = ""
    for i, letter in enumerate(guess):
        if letter == target[i]:
            formatted += f"🟩 **{letter.upper()}** "
        elif letter in target:
            formatted += f"🟨 **{letter.upper()}** "
        else:
            formatted += f"⬜ {letter.upper()} "
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

bot = commands.Bot(command_prefix='!')

# Dictionary to keep track of ongoing games
games = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='startwordle')
async def start_wordle(ctx):
    if ctx.author.id in games:
        await ctx.send("You already have an ongoing game! Finish it before starting a new one.")
        return
    
    target_word = random.choice(WORDS)
    games[ctx.author.id] = WordleGame(target_word)
    await ctx.send("Wordle game started! You have 6 attempts to guess the 5-letter word. Use `!guess <word>` to make a guess.")

@bot.command(name='guess')
async def make_guess(ctx, guess: str):
    if ctx.author.id not in games:
        await ctx.send("You don't have an ongoing game. Start one with `!startwordle`.")
        return
    
    game = games[ctx.author.id]
    
    if len(guess) != 5 or not all(c in string.ascii_letters for c in guess):
        await ctx.send("Please enter a valid 5-letter word.")
        return
    
    guess = guess.lower()
    response = game.make_guess(guess)
    
    if game.is_correct(guess):
        await ctx.send(f"Congratulations! You guessed the word: **{guess.upper()}**")
        del games[ctx.author.id]
    elif game.out_of_attempts():
        await ctx.send(f"Sorry, you're out of attempts! The word was: **{game.target_word.upper()}**")
        del games[ctx.author.id]
    else:
        await ctx.send(f"Guess: {response}\nAttempts left: {game.attempts - len(game.guesses)}")

@bot.command(name='endwordle')
async def end_wordle(ctx):
    if ctx.author.id in games:
        del games[ctx.author.id]
        await ctx.send("Your Wordle game has been ended.")
    else:
        await ctx.send("You don't have an ongoing game.")

bot.run(TOKEN)
