# Libraries
import re
import discord
from discord import Embed
from discord import Colour

# Checkings
def is_from_a_supported_service (self, link):
    is_supported = ''
    if is_from_ytb(self, link):
        is_supported = 'ytb'
    #elif is_from_dlm(self, link):
    #    is_supported = 'dlm'
    return(is_supported)

def is_from_ytb (self, link):
    answer = re.search(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', link)
    return answer

#def is_from_dlm(self, link, ctype):
#   answer = re.search(r' dailymotion regex ')