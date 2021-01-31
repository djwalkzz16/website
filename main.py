from typing import List

from quart import Quart, redirect, render_template_string, request, url_for

from quart_oauth2_discord_py import DiscordOauth2Client, Guild

app = Quart(__name__)
app.secret_key = b"random bytes representing quart secret key"
app.config['DISCORD_CLIENT_ID'] = "805352822488694794"
app.config['DISCORD_CLIENT_SECRET'] = '1ZVYoTkG6oqbeWnwFvJ5x5hkTTKk31ex'
app.config['SCOPES'] = ['identify', 'guilds']
app.config['DISCORD_REDIRECT_URI'] = 'https://discord.gg'
app.config['DISCORD_BOT_TOKEN'] = 'ODA1MzUyODIyNDg4Njk0Nzk0.YBZpQw.GQqNlUBZZlxOSN3Pa7C6h1DWfOw'

client = DiscordOauth2Client(app)


@app.route('/')
async def index():
    return "Hello!"


@app.route('/login/', methods=['GET'])
async def login():
    return await client.create_session()


@app.route('/callback')
async def callback():
    await client.callback()
    return redirect(url_for('index'))


def return_guild_names_owner(guilds_: List[Guild]):
    # print(list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild()])))
    return list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild()]))


def search_guilds_for_name(guilds_, query):
    # print(list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild() and fetch_guild.name == query])))
    return list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild() and fetch_guild.name == query]))


@app.route('/guilds')
async def guilds():
    template_string = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Guilds</title>
        </head>
        <body>
            <h1>Your guilds: </h1>
            <ol>
            {% for guild_name in guild_names %}
                <li>{{ guild_name }}</li>
            {% endfor %}
            </ol>
        </body>
    </html>
    """
    if request.args.get('guild_name'):
        return await render_template_string(template_string, guild_names=search_guilds_for_name(await client.fetch_guilds(), request.args.get('guild_name')))
    return await render_template_string(template_string, guild_names=return_guild_names_owner(await client.fetch_guilds()))


@app.route('/me')
@client.is_logged_in
async def me():
    user = await client.fetch_user()
    image = user.avatar_url
    # noinspection HtmlUnknownTarget
    return await render_template_string("""
        <html lang="en">
            <body>
                <p>Login Successful</p>
                <img src="{{ image_url }}" alt="Avatar url">
            </body>
        </html>
        """, image_url=image)


if __name__ == '__main__':
    app.run()