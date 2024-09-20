# CONFIG
# -----------------------------------------------------
token = "tokey"  # INSERT BOT TOKEN HERE
counting_channel = "1283144240481697879"  # INSERT CHANNEL ID HERE
delay = [2, 4]  # DELAY BETWEEN COUNTING
selfbot = True  # Change this if using BOT ACCOUNT
last_number = ""  # Optional, it starts counting from this number

mode = "INCREMENTAL"  # CHOOSE MODE OF COUNTING
# You can choose from: INCREMENTAL or BINARY
# -----------------------------------------------------

try:
    import discord, random, sys, asyncio
except ImportError as e:
    print(e)
    exit()

from discord.ext import commands

if sys.version_info[0] < 3:
    print("Python 3 or a more recent version is required.")
    exit()

# Initialize the bot
bot = commands.Bot(command_prefix='!', self_bot=selfbot)
bot.remove_command("help")

print("Logging in...")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}, time to start counting!')


async def counting_task():
    global last_number
    await bot.wait_until_ready()  # Ensure the bot is ready before starting the loop
    channel = bot.get_channel(int(counting_channel))

    while not bot.is_closed():
        async for message in channel.history(limit=1):
            if bot.user.id != message.author.id:
                try:
                    # Initialize the number if it's not set
                    if last_number == "" and mode == "INCREMENTAL":
                        last_number = int(message.content)
                    elif last_number == "" and mode == "BINARY":
                        last_number = int(message.content, 2)
                except ValueError:
                    pass  # Ignore non-numeric messages
                else:
                    # Delay before responding
                    await asyncio.sleep(random.uniform(delay[0], delay[1]))

                    if mode == "INCREMENTAL":
                        # Increment the number by 1
                        num = int(message.content)
                        next_number = num + 1
                        last_number = next_number

                        # Send the next number
                        await channel.send(str(next_number))
                        print(f"SENDING: {next_number}")
                        print(f"NEXT NUMBER: {last_number}")

                    elif mode == "BINARY":
                        # Increment the binary number
                        num = int(message.content, 2)
                        next_binary = "{0:b}".format(num + 1)
                        last_number = num + 1

                        # Send the next binary number
                        await channel.send(next_binary)
                        print(f"SENDING: {next_binary}")
                        print(f"NEXT NUMBER: {last_number:b}")

        # Random delay between 14 minutes 30 seconds to 15 minutes 30 seconds
        random_delay = random.uniform(870, 930)
        print(f"Waiting for {random_delay / 60:.2f} minutes before checking again...")
        await asyncio.sleep(random_delay)  # Wait between 870 and 930 seconds


async def main():
    # Start the background counting task
    asyncio.create_task(counting_task())
    await bot.start(token)


# Run the bot using asyncio
try:
    asyncio.run(main())
    print("\nExiting, have a nice day!")
except discord.errors.LoginFailure as e:
    print("Error: " + str(e))
