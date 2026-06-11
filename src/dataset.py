"""
Golden Dataset for Prompt Regression Testing.

This module contains 50 hand-crafted, high-quality golden input/output pairs.
Inputs are Python code snippets, and expected_outputs are reference explanations
that represent a high-quality explanation according to our design standards.
"""

GOLDEN_DATASET = [
    # --- Category 1: Basic Python & Control Flow (1-10) ---
    {
        "input": "def is_even(num):\n    return num % 2 == 0",
        "expected_output": "This function, `is_even`, checks if a given integer is even. It returns `True` if the remainder of the number divided by 2 is 0, indicating it is even, and `False` otherwise."
    },
    {
        "input": "for i in range(1, 6):\n    print(i * '*')",
        "expected_output": "This code prints a right-aligned triangle pattern of asterisks. It loops through numbers 1 to 5 (inclusive) and prints a string of asterisks of length equal to the current loop iteration index `i`."
    },
    {
        "input": "x = 10\ny = 20\nx, y = y, x",
        "expected_output": "This snippet swaps the values of variables `x` and `y` using tuple unpacking. `x` becomes 20 and `y` becomes 10 without needing an intermediate temporary variable."
    },
    {
        "input": "try:\n    res = 10 / 0\nexcept ZeroDivisionError:\n    res = None",
        "expected_output": "This snippet demonstrates error handling. It attempts to divide 10 by 0, catches the resulting `ZeroDivisionError`, and sets `res` to `None` to prevent the program from crashing."
    },
    {
        "input": "age = 20\nstatus = 'adult' if age >= 18 else 'minor'",
        "expected_output": "This statement uses a ternary conditional expression to determine status. It assigns the value `'adult'` to `status` if `age` is 18 or greater, and `'minor'` otherwise."
    },
    {
        "input": "def greet(name='Guest'):\n    return f'Hello, {name}!'",
        "expected_output": "This function returns a personalized greeting. It uses a default parameter value of `'Guest'` so that calling it without arguments greets a generic guest, otherwise it greets the specified `name`."
    },
    {
        "input": "with open('file.txt', 'r') as f:\n    content = f.read()",
        "expected_output": "This snippet opens a file named `'file.txt'` in read-only mode using a context manager (`with` statement). The context manager guarantees that the file is automatically and safely closed after reading its content, even if errors occur."
    },
    {
        "input": "import sys\n# Check python version\nif sys.version_info < (3, 10):\n    print('Unsupported')",
        "expected_output": "This script checks if the running Python interpreter's version is less than 3.10. It imports the `sys` module, inspects `sys.version_info`, and prints `'Unsupported'` if the requirement is not met."
    },
    {
        "input": "a = [1, 2, 3]\nwhile a:\n    print(a.pop())",
        "expected_output": "This code pops and prints elements from list `a` in reverse order (LIFO) until the list is empty. The `while` loop checks truthiness of `a`, which evaluates to `False` once all items are popped."
    },
    {
        "input": "def find_max(a, b):\n    return a if a > b else b",
        "expected_output": "This function takes two arguments, `a` and `b`, and returns the larger value using a ternary conditional check."
    },

    # --- Category 2: Data Structures (11-20) ---
    {
        "input": "sq = [x**2 for x in range(10)]",
        "expected_output": "This code uses list comprehension to generate a list containing the squares of numbers from 0 to 9."
    },
    {
        "input": "d = {k: v for k, v in zip(['a', 'b'], [1, 2])}",
        "expected_output": "This statement creates a dictionary `d` using dictionary comprehension. It pairs keys from `['a', 'b']` with values from `[1, 2]` using `zip` to construct the dictionary `{'a': 1, 'b': 2}`."
    },
    {
        "input": "s = set([1, 2, 2, 3, 3, 3])",
        "expected_output": "This snippet converts a list with duplicate numbers into a set `s`, resulting in a collection of unique elements `{1, 2, 3}`."
    },
    {
        "input": "t = (1, 2, [3, 4])\nt[2].append(5)",
        "expected_output": "This code shows that elements inside a tuple are immutable, but mutable elements within the tuple (like the list at index 2) can still be modified in place. It appends `5` to the nested list, changing the tuple to `(1, 2, [3, 4, 5])` without throwing an error."
    },
    {
        "input": "d = {}\nd['key'] = d.get('key', 0) + 1",
        "expected_output": "This code safely increments the frequency counter for `'key'` in dictionary `d`. The `get` method returns the existing value or a default of 0 if the key is missing, avoiding a `KeyError`."
    },
    {
        "input": "from collections import defaultdict\nd = defaultdict(list)\nd['a'].append(1)",
        "expected_output": "This code utilizes a `defaultdict` from Python's standard library to automatically initialize any missing dictionary keys with an empty list, allowing immediate list operations like `append`."
    },
    {
        "input": "a = [1, 2, 3]\nb = a[:]\nb.append(4)",
        "expected_output": "This snippet creates a shallow copy of list `a` using slice notation `[:]` and assigns it to `b`. Modifying `b` by appending `4` does not affect the original list `a`."
    },
    {
        "input": "a = [1, 2]\nb = [3, 4]\na.extend(b)",
        "expected_output": "This code extends the list `a` by appending all elements from list `b` to it in place, resulting in `a` becoming `[1, 2, 3, 4]`."
    },
    {
        "input": "s = 'hello'\nreverse_s = s[::-1]",
        "expected_output": "This snippet reverses a string `s` using slice notation with a step of -1, producing `'olleh'`."
    },
    {
        "input": "matrix = [[0] * 3 for _ in range(3)]",
        "expected_output": "This statement creates a 3x3 matrix initialized with zeros using nested list comprehension. Using a list comprehension prevents referencing the same sublist object in memory."
    },

    # --- Category 3: Functions & Functional Programming (21-30) ---
    {
        "input": "f = lambda x, y: x + y\nprint(f(2, 3))",
        "expected_output": "This code defines an anonymous inline function (lambda function) `f` that accepts two parameters and returns their sum, then calls it with arguments 2 and 3 to print 5."
    },
    {
        "input": "nums = [1, 2, 3]\ndoubled = list(map(lambda x: x * 2, nums))",
        "expected_output": "This statement applies a lambda function that doubles each element in the `nums` list using the `map` function, and then converts the map generator back into a list."
    },
    {
        "input": "nums = [1, 2, 3, 4]\nevens = list(filter(lambda x: x % 2 == 0, nums))",
        "expected_output": "This code filters a list to retrieve only even numbers. It applies a conditional lambda function to each element using `filter`, returning `[2, 4]` after list conversion."
    },
    {
        "input": "def log_calls(func):\n    def wrapper(*args, **kwargs):\n        print('Calling function')\n        return func(*args, **kwargs)\n    return wrapper",
        "expected_output": "This code defines a decorator named `log_calls` that wraps another function to print `'Calling function'` before executing it, using `*args` and `**kwargs` to preserve original function arguments."
    },
    {
        "input": "def add_all(*args):\n    return sum(args)",
        "expected_output": "This function calculates the sum of all positional arguments passed to it. The asterisk `*` gathers all extra inputs into a tuple named `args`."
    },
    {
        "input": "def print_config(**kwargs):\n    for k, v in kwargs.items():\n        print(f'{k}: {v}')",
        "expected_output": "This function takes keyword arguments, packing them into a dictionary named `kwargs`, and then iterates over its items to print key-value configuration pairs."
    },
    {
        "input": "def gen_nums():\n    yield 1\n    yield 2\n    yield 3",
        "expected_output": "This is a generator function that produces values lazily. It uses the `yield` keyword to return values 1, 2, and 3 one at a time, pausing execution between items."
    },
    {
        "input": "def outer():\n    x = 1\n    def inner():\n        nonlocal x\n        x += 1\n        return x\n    return inner",
        "expected_output": "This code implements a closure. The nested function `inner` accesses and increments variable `x` from the parent scope using the `nonlocal` keyword, persisting state across multiple calls."
    },
    {
        "input": "from functools import lru_cache\n@lru_cache(maxsize=None)\ndef fib(n):\n    return n if n < 2 else fib(n-1) + fib(n-2)",
        "expected_output": "This snippet defines a recursive Fibonacci function optimized with memoization. The `@lru_cache` decorator caches previously computed results to avoid redundant calculations, improving execution speed."
    },
    {
        "input": "def apply(f, x):\n    return f(x)",
        "expected_output": "This is a higher-order function that takes another function `f` and a value `x` as arguments, and returns the result of applying `f` to `x`."
    },

    # --- Category 4: OOP & Classes (31-40) ---
    {
        "input": "class Person:\n    def __init__(self, name):\n        self.name = name",
        "expected_output": "This is a simple class definition for `Person`. The constructor `__init__` initializes a new instance of `Person` with a instance variable `name`."
    },
    {
        "input": "class Animal:\n    def speak(self):\n        pass\nclass Dog(Animal):\n    def speak(self):\n        return 'Woof'",
        "expected_output": "This shows class inheritance. `Dog` inherits from parent class `Animal` and overrides the abstract `speak` method to return the string `'Woof'`."
    },
    {
        "input": "class Circle:\n    def __init__(self, radius):\n        self._radius = radius\n    @property\n    def radius(self):\n        return self._radius",
        "expected_output": "This class demonstrates encapsulation. The `radius` property decorator provides controlled, read-only getter access to the protected private variable `_radius`."
    },
    {
        "input": "class Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)",
        "expected_output": "This class defines a 2D Vector and overrides the addition operator `+` by implementing the `__add__` magic method. It returns a new `Vector` instance combining components."
    },
    {
        "input": "class Book:\n    def __init__(self, title):\n        self.title = title\n    def __str__(self):\n        return f'Book: {self.title}'",
        "expected_output": "This class implements the `__str__` dunder method, defining custom string representation when print() or str() is called on a instance of class `Book`."
    },
    {
        "input": "class Database:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance",
        "expected_output": "This code implements the Singleton design pattern using the `__new__` method, ensuring that only one instance of the `Database` class is ever created and shared."
    },
    {
        "input": "class Counter:\n    count = 0\n    def __init__(self):\n        Counter.count += 1",
        "expected_output": "This class defines a class variable `count` shared among all instances, incrementing it every time a new instance of the class is initialized."
    },
    {
        "input": "class MathUtils:\n    @staticmethod\n    def add(a, b):\n        return a + b",
        "expected_output": "This class contains a static method `add` that performs addition. The static method does not require access to instance (`self`) or class (`cls`) state."
    },
    {
        "input": "class Config:\n    @classmethod\n    def from_file(cls, path):\n        return cls()",
        "expected_output": "This snippet defines a factory class method `from_file` that accepts the class itself (`cls`) and returns an instance of it, commonly used for alternative constructors."
    },
    {
        "input": "class CustomError(Exception):\n    pass",
        "expected_output": "This code creates a custom user-defined exception class named `CustomError` by inheriting from the built-in `Exception` base class."
    },

    # --- Category 5: Common Algorithms & Std Lib (41-50) ---
    {
        "input": "import re\nmatch = re.search(r'\\d+', 'User123')",
        "expected_output": "This snippet imports the regular expression module `re` and searches for the first sequence of digits (`\\d+`) in the string `'User123'`, matching `'123'`."
    },
    {
        "input": "import json\ndata = json.loads('{\"name\": \"Alice\"}')",
        "expected_output": "This code imports the `json` module and parses a JSON-formatted string into a corresponding Python dictionary using `json.loads`."
    },
    {
        "input": "from datetime import datetime\nnow = datetime.now()",
        "expected_output": "This snippet retrieves the current local date and time by importing the `datetime` class from the `datetime` module and calling the `now()` method."
    },
    {
        "input": "import math\nres = math.sqrt(16)",
        "expected_output": "This code imports the `math` library and calculates the square root of 16, returning a float value of 4.0."
    },
    {
        "input": "import random\nchoice = random.choice([1, 2, 3])",
        "expected_output": "This snippet imports the `random` module and selects a random element from the list `[1, 2, 3]` using the `random.choice` function."
    },
    {
        "input": "import os\npath_exists = os.path.exists('file.txt')",
        "expected_output": "This code imports the `os` module and uses `os.path.exists` to check if a file or folder named `'file.txt'` exists in the local file system, returning `True` or `False`."
    },
    {
        "input": "import time\ntime.sleep(2)",
        "expected_output": "This snippet imports the `time` module and uses `time.sleep(2)` to pause the execution of the program for exactly 2 seconds."
    },
    {
        "input": "items = ['a', 'b', 'c']\nfor idx, val in enumerate(items):\n    print(idx, val)",
        "expected_output": "This loop uses Python's built-in `enumerate` function to iterate over a list, yielding both index position `idx` and item value `val` simultaneously."
    },
    {
        "input": "keys = ['a', 'b']\nvals = [1, 2]\npairs = list(zip(keys, vals))",
        "expected_output": "This snippet pairs elements from lists `keys` and `vals` index-by-index using `zip`, returning a list of tuples `[('a', 1), ('b', 2)]`."
    },
    {
        "input": "a = [1, 2, 3]\nb = [x for x in a if x > 1]",
        "expected_output": "This code filters list `a` using list comprehension, returning a new list `b` containing only elements that are strictly greater than 1, which results in `[2, 3]`."
    }
]
