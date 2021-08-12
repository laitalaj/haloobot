import asyncio
import functools
from inspect import iscoroutinefunction

def return_if_silent(func):

    @functools.wraps(func)
    def wrapper_ris(self, *args, **kwargs):
        if self.settings['silence']:
            print('Tried to /%s while silent' % self.comtext)
            return 'I\'m silent!'

        return func(self, *args, **kwargs)
    
    @functools.wraps(func)
    async def async_wrapper_ris(self, *args, **kwargs):
        if self.settings['silence']:
            print('Tried to /%s while silent' % self.comtext)
            return 'I\'m silent!'

        return await func(self, *args, **kwargs)

    return async_wrapper_ris if asyncio.iscoroutinefunction(func) else wrapper_ris
