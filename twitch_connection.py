from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import asyncio

from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import asyncio

async def main():
     # initialize the twitch instance, this will by default also create a app authentication for you
    twitch = await Twitch('app_id', 'app_secret')
    # call the API for the data of your twitch user
    # this returns a async generator that can be used to iterate over all results
    # but we are just interested in the first result
    # using the first helper makes this easy.
    user = await first(twitch.get_users(logins='your_twitch_user'))
    # print the ID of your user or do whatever else you want with it
    print(user.id)
    await twitch.close()
    
if __name__ == '__main__':
    asyncio.run(main())

