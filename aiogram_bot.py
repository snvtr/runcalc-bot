import logging
#import asyncio
#from types import NoneType

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
#from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode
from aiogram.utils.helper import Helper, HelperMode, ListItem

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config  import TOKEN, MESSAGES, DISTANCES
from get     import *
from calcsrv import *
from grades  import *

logging.basicConfig(format=u'%(filename)s [ln:%(lineno)+3s]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['vdot'])
async def process_start_command(message: types.Message):
    ''' returns VDOT from a race result '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 2:
        await message.reply('vdot(): not enough arguments')
        return
    dist = get_dst(arguments[0]) 
    res  = get_res(arguments[1])
    if dist is None or res is None:
        await message.reply('vdot(): badly formed arguments')
    else:
        await message.reply(build_dist_time(dist, res))

@dp.message_handler(commands=['race'])
async def process_start_command(message: types.Message):
    ''' returns probable race results from VDOT '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 1:
        await message.reply('race(): not enough arguments')
        return
    vdot = get_vdot(arguments[0].replace(',', '.'))
    if vdot is None or vdot > 99.99:
        await message.reply('race(): badly formed arguments')
    else:
        await message.reply(build_vdot(vdot))

@dp.message_handler(commands=['agegraded'])
async def process_start_command(message: types.Message):
    ''' returns age graded percentage of the best time for a given age '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 4:
        await message.reply('agegraded(): not enough arguments')
        return
    dist   = get_dst(arguments[0]) 
    res    = get_res(arguments[1])
    age    = get_age(arguments[2])
    gender = get_gender(arguments[3])
    if dist is None or res is None or age is None or gender is None:
        await message.reply('agegraded(): badly formed arguments')
    else:
        await message.reply(build_agegraded(dist, res, age, gender))

@dp.message_handler(commands=['agedist'])
async def process_start_command(message: types.Message):
    ''' returns age graded percentage of the best time for a given age '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 3:
        await message.reply('agedist(): not enough arguments')
        return
    percent = get_pct(arguments[0]) 
    age     = get_age(arguments[1])
    gender  = get_gender(arguments[2])
    if percent is None or age is None or gender is None:
        await message.reply('agedist(): badly formed arguments')
    else:
        await message.reply(build_agedist(percent, age, gender))

@dp.message_handler(commands=['coopert'])
async def process_start_command(message: types.Message):
    ''' returns cooper test result from time '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 1:
        await message.reply('coopert(): not enough arguments')
        return
    res = get_res(arguments[0])
    if res is not None:
        await message.reply(build_cooper_t(res))
    else:
        await message.reply('coopert(): badly formed arguments')

@dp.message_handler(commands=['cooperd'])
async def process_start_command(message: types.Message):
    ''' returns cooper test result from distance '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 1:
        await message.reply('cooperd(): not enough arguments')
        return
    try:
        dist = float(arguments[0])
    except:
        dist = None
    if dist is not None:
        await message.reply(build_cooper(dist))
    else:
        await message.reply('cooperd(): badly formed arguments')

@dp.message_handler(commands=['balke'])
async def process_start_command(message: types.Message):
    ''' returns cooper test result from distance '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 1:
        await message.reply('balke(): not enough arguments')
        return
    try:
        dist = float(arguments[0])
    except:
        dist = None
    if dist is not None:
        await message.reply(build_balke(dist))
    else:
        await message.reply('balke(): badly formed arguments')

@dp.message_handler(commands=['help', 'start'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['help'])

@dp.message_handler(commands=['helptime'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['helptime'])

@dp.message_handler(commands=['helpdist'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['helpdist'])

@dp.message_handler(commands=['helpvdot'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['helpvdot'])

@dp.message_handler(commands=['helpage'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['helpage'])

@dp.message_handler(commands=['helppercentage'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['helppercentage'])

@dp.message_handler(commands=['helpgender'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['helpgender'])

@dp.message_handler()
async def echo_message(msg: types.Message):
    #await bot.send_message(msg.from_user.id, reply, parse_mode=ParseMode.MARKDOWN)
    await bot.send_message(msg.from_user.id, 'not a valid message. run /help command', parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    executor.start_polling(dp)
