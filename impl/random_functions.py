import random
from typing import List, Any

from jmespath import functions


class RandomFunctions(functions.Functions):
    @functions.signature({"types": ["array"]})
    def _func_one_of(self, array):
        return random.choice(array)

    @functions.signature({"types": ["array"]}, {"types": ["number"]})
    def _func_some_of(self, array, number) -> List[Any]:
        return random.sample(array, number if number <= len(array) else len(array))
