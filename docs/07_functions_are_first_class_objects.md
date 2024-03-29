### 一等公民
- 在运行时创建
- 能赋值给变量或数据结构中的元素
- 能作为参数传给函数
- 能作为函数的返回结果

### 把函数视为对象
- 函数对象本身是`function`类的实例
  ```python
  def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)
  >>> factorial.__doc__
  "返回n!"
  >>> type(factorial)
  <class 'function'>
  ```

- `__doc__`属性用于生成对象的帮助文档。

### 高阶函数
- 接受函数作为参数或者把函数作为结果返回的函数是**高阶函数**。
- `map`和`filter`是Python3的内置函数，但由于引入了列表推导式和生成器表达式，这两者就没有那么重要了。
  ```python
  >>> list(map(factorial, range(6)))
  [1, 1, 2, 6, 24, 120]
  >>> [factorial(n) for n in range(6)]
  [1, 1, 2, 6, 24, 120]
  >>> list(map(factorial, filter(lambda n: n % 2, range(6))))
  [1, 6, 120]
  >>> [factorial(n) for n in range(6) if n % 2]
  [1, 6, 120]
  ```
- 使用`reduce`函数求和
  ```python
  >>> from functools import reduce
  >>> from operator import add
  >>> reduce(add, range(100))
  4950
  ```
- 这种把一系列值通过某种操作归约到一个值的函数成为规约函数，内置的规约函数还有`all`和`any`
  - `all(iterable)` - `iterable`中没有表示假值的元素时返回`True`，`all([])`返回`True`，因为空对象没有为`False`的元素
  - `any(iterable)` `iterable`中存在真值就返回`True`。`any([])`返回`False`，因为空对象没有为`True`的元素。
  
### 匿名函数
- `lambda`关键字使用Python表达式创建匿名函数。
- `lambda`函数的主体只能是纯粹的表达式，不能有`while` `try`等Python语句，使用`=`赋值语句也不行。可以有`:=`赋值（不建议使用）。
- 高阶函数的参数列表最适合使用匿名函数
  ```python
  >>> fruits = ['strawberry', 'fig', 'apple', 'cherry]
  >>> sorted(fruits, key=lambda word: word[::-1])
  ['apple', 'fig', 'strawberry', 'cherry']
  ```

### 9种可调用对象（>=Python3.9）
- 除了函数，`()`调用运算符还可以应用到其他对象上。可以使用内置的`callable()`函数判断对象是否可调用。
- 用户自定义函数：使用`def`语句或`lambda`表达式创建的函数。
- 内置函数：使用C语言（CPython）实现的函数，例如`len`或`time.strftime`
- 内置方法：使用C语言实现的方法，如`dict.get`
- 方法：在类主体中定义的函数。
- 类：调用类时运行类的`__new__`方法创建一个实例，然后运行`__init__`方法初始化实例，最后再把实例返回给调用方。Python没有`new`运算符，调用类相当于调用函数。
- 类的实例：如果类定义了`__call__`方法，那么它的实例可以作为函数调用。
- 生成器函数：主体中有`yield`关键字的函数或方法。调用生成器函数返回一个生成器的对象。
- 原生协程函数：使用`async def`定义的函数或方法。调用原生写成函数返回一个写成对象。
- 异步生成器函数：使用`async def`定义且主体中有`yield`关键字的函数或方法。调用异步生成器函数返回一个异步生成器，供`aysnc for`使用。

### 自定义可调用类型
```python
import random

class BingoCage:
  def __init__(self, items):
    self._items = list(items)
    random.shuffle(self._items)

  def pick(self):
    try:
      return self._items.pop()
    except IndexError:
      raise LookupError("pick from empty BingoCage")

  def __call__(self):
    return self.pick()
```
- 调用`bingocage()`相当于`bingocage.pick()`

### 仅限关键字参数
- 定义函数时，如果像指定仅限关键字参数（只能通过关键字参数传参），需要把他们放到前面有`*`的参数后面，如果不想支持数量不定的位置参数，但想支持仅限关键字参数，可以在签名中放一个`*`
  
  ```python
  def (a, *, b):
    return a, b
  
  >>> f(1, b=2)
  (1, 2)
  >>> f(1, 2)
  Traceback (most recent call last):
    ...
  TypeError: f() tasks 1 positional argument but 2 were given
  ```
  - 仅限关键字参数不一定要有默认值，如这个例子中`b`，强制要求传入实参。

### 仅限位置参数
- 从Python3.8开始，用户定义的函数签名可以指定仅限位置参数。内置函数都是如此，例如`divmod(a,b)`只能使用位置参数调用，不能写成`divmod(a=10,b=4)`。
- 通过在参数列表中使用`/`定义仅限位置参数。`/`左边均为仅限位置参数，在`/`后面可以指定其他参数。
  ```python
  def divmod(a, b, /):
    return (a // b, a % b)
  ```

### 支持函数式编程的包
- `operator`模块
  - 为多个算数运算符提供了对应的函数
    ```python
    from functools import reduce
    from operator improt mul

    def factorial(n):
      return reduce(mul, range(1, n + 1))
    ```
  - `operator`模块还有一类函数，即工厂函数`itemgetter`和`attrgetter`，能替代从序列中取出项或读取对象属性的`lambda`表达式。下面的例子`itemgetter(1)`等价于`lambda fields: fields[1]`。
    ```python
    metro_data = [
      ('Tokyo', 'JP', 36)
      ('Delhi NCR', 'IN", 21)
    ]

    from operator import itemgetter
    for city in sorted(metro_data, key=itemgetter(1)):
      print(city)
    ```
    - 如果传给`itemgetter`多个索引参数，那么`itemgetter`构建的函数会返回提取的值构成的元组，以方便根据多个键排序。例如`itemgetter(1, 0)`。
    - `itemgetter`使用`[]`运算符，因此它不仅支持序列，还支持映射和任何实现`__getitem__`方法的类。
  - `attrgetter`创建的函数会根据名称来提取对象的属性，如果传给`attrgetter`多个属性名，它会返回由提取的值构成的元组。此外如果参数名包含`.`那么`attrgetter`会深入嵌套对象，检索属性。

  - `operator.methodcaller`创建的函数会在对象上调用参数指定的方法。
    ```python
    from operator improt mehodcaller
    s = 'The time has come'
    upcase = methodcaller("upper")
    upcase(s)
    ```

- 使用`functools.partial`冻结参数：根据可调用对象产生一个新的可调用对象，为原可调用对象的某些参数绑定预定的值。使用这个函数把接受一个或多个参数的函数改造成需要更少参数的回调的API。
  ```python
  >>> from operator import mul
  >>> from functools import partial
  >>> triple = partial(mul, 3)
  >>> triple(7)
  21
  ```
