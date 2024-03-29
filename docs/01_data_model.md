## Python 数据模型

### 魔法函数的例子
```python
import collections

Card = collections.namedtuple("Card", ["rank", "suit"])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11) + list("JQKA")]
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

deck = FrenchDeck()
```
- `__len__` 返回对象长度，可通过`len(deck)`触发

    ```python
    >>> len(deck)
    52
    ```

- `__getitem__` 
    - 支持`[index]` 索引

        ```python
        >>> deck[-1]
        Card(rank='2', suit='spades')
        ```
    - 支持`random.Choice(deck)` 随机返回序列中的一项

        ```python
        >>> from random import Choice
        >>> Choice(deck)
        Card(rank='3', suit='hearts')
        ```
    
    - 支持切片操作

        ```python
        >>> deck[:3]
        [Caard(rank='2', suit='spades'), Card(rank='3', suit='spades'), Card(rank='4', suit='spades')]
        ```

    - 可迭代

        ```python
        for card in deck:
            print(card)
        ```

### 魔法函数的调用

- 通常魔法函数是隐式调用的，由解释器触发，如
    - `len(deck) => deck.__len__()`
    - `for card in deck:  =>  iter(deck)  =>  deck.__iter__()`如果没有实现则`deck.__getitem__()`

### 另一个例子
```python
"""
vector2d.py 向量类，支持

加法::
>>> v1 = Vector(2, 4)
>>> v2 = Vector(2, 1)
>>> v1 + v2
Vector(4, 5)

绝对值::
>>> v = Vector(3, 4)
>>> abs(v)
5.0

标量积::
>>> v * 3
Vector(9, 12)
"""

import math

class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr(self):
        return f"Vector({self.x!r}, {self.y!r}})"

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, other):
        return Vector(self.x * other.x, self.y * other.y)
```
- `Vector`可以乘以一个数，但是一个数不能乘以`Vector`，如果要实现这个功能可以实现`__rmul__`。
- `__repr__`供内置函数`repr`调用。交互式控制台和调试器再表达时求值结果上调用`repr`函数
- `f-string`使用`!r`以标准的表示显示属性。差别在`Vector('2', '3')`还是`Vector(2, 3)`，其中`!r`显示的是后者。
- `__str__`由内置函数`str`调用，供`print`函数使用，输出对终端用户友好的字符串。如果`__repr__`返回的字符串足够友好则无需实现`__str__`。
- [`__str__` VS `__repr__`](https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr)
- 内置函数`bool`会先尝试调用`__bool__`没有则调用`__len__`，都没有则返回`True`。

## Sequence

- 列表推导

    ```python
    >>> seq = 'abc'
    >>> codes = [ord(s) for s in seq]
    >>> codes
    [97, 98, 99]
    ```
- 列表推导和生成器表达式具有局部作用域用于保存`for`子句分配的变量。使用*海象运算符*`:=`分配的变量在这些推导或表达式返回后仍可以访问。*PEP 572* 赋值表达式将`:=`的作用范围定义为封闭函数，除非该目标具有全局或非局部声明。

    ```python
    >>> seq = 'abc'
    >>> codes = [last := ord(s) for s in seq]
    >>> last
    99
    >>> s
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    NameError: name 's' is not defined
    ```

- 高阶方法`filter`和`filter`

    ```python
    f = filter(lambda c: c > 98, map(ord, seq))
    ```

- 生成器表达式：相比列表推导更省内存，使用迭代器协议逐个生成项，而不是构建整个列表只是为了提供给另一个构造函数

    ```python
    >>> a = (ord(s) for s in seq)
    >>> tuple(a)
    (97, 98, 99)
    ```
    - 如果生成器表达式是函数调用中的单个参数，则无需通过`()`括号包裹，否则需要加上

- 列表和元组的方法属性比较

    |   | 作用  | 列表  |  元组  |
    | ------------ | ------------ | ------------ | ------------ |
    | `s.__add__(s2)`   | `s+s2` 拼接 | √  | √  |
    |  `s.__iadd__(s2)` | `s += s2`就地拼接  | √  |   |
    |`s.append(e)`|在最后一个元素后追加元素 |||
    |`s.clear()`|删除所有项 |√||
    |`s.__contains__(e)`|`e in s` |√|√|
    |`s.copy()`|浅拷贝列表 |√||
    |`s.count(e)`|计算元素出现的次数 |√|√|
    |`s.__delitem__(p)`|删除`p`位置上的项 |√||
    |`s.extend(it)`|追加可迭代对象`it`中的项 |√||
    |`s.__getitem__(p)`|`s[p]` 获取指定位置的项|√|√|
    |`s.__getnewargs__()`|支持使用`pickle`优化序列化 ||√|
    |`s.index(e)`|找出`e`首次出现的位置 |√|√|
    |`s.insert(p, e)`|在位置`p`之前插入元素`e` |√||
    |`s.__iter__()`|获取迭代器 |√|√|
    |`s.__len__()`|`len(s)`项数 |√|√|
    |`s.__mul__(n)`|`s * n`重复拼接 |√|√|
    |`s.__imul__(n)`|`s *= n`就地重复拼接|√||
    |`s.__rmul__(n)`| `n * s` 反向重复拼接|√|√|
    |`s.pop([p])`|移除并返回最后一项或可选的位置`p`上的项 |√||
    |`s.remove(e)`|把`e`的值首次出现的位置上移除 |√||
    |`s.reverse()`|就地反转项的顺序 |√||
    |`s.__reversed__()`|获取从后向前遍历项的迭代器 |√||
    |`s.__setitem__(p, e)`|`s[p]=e`把`e`放在位置`p`上，覆盖现有的项 |√||
    |`s.sort([key], [reversed])`|就地对项排序，`key`和`reversed`是可选的关键字参数 |√||

### 序列和可迭代对象拆包
- 拆包形式
    - 并行赋值

        ```python
        t = (12, 4.5)
        a, b = t
        ```
    - 互换变量的值

        ```python
        b, a = a, b
        ```
    - 函数传参通过在参数前加 `*` 来拆包

        ```python
        t = (20, 8)
        divmod(*t)
        ```
- 使用 `*` 获取剩余项
    ```python
    >>> a, b, *rest = range(5)
    >>> a, b, rest
    (0, 1, [2, 3, 4])
    >>> a, b, *rest = range(2)
    (0, 1, [])
    ```
    - 并行赋值时`*`变量可以是任意位置

       ```python
       >>> a, *b, c, d = range(5)
       >>> a, b, c, d
       (0, [1, 2], 3, 4)
       ```
- 在函数调用和序列字面量中使用`*`拆包
    - 在函数调用中多次使用`*`
        ```python
        >>> def fun(a, b, c, d, *rest):
        ...     return a, b, c, d, rest
        ...
        >>> fun(*[1, 2], 3, *range(4, 7))
        (1, 2, 3, 4, (5, 6))
        ```
    - 定义列表、元组或集合字面量时也可以用`*`
        ```python
        >>> [*range(4), 4]
        [0, 1, 2, 3, 4]
        ```
### 序列模式匹配
- Python3.10 通过`match/case` 实现 **PEP 634** 模式匹配。

    ```python
    metro_ares = [
        ("Tokyo", "JP", 36.9, (25.6, 129,1)),
    ]

    def main():
        for record in metro_areas:
            match record:
                case [name, _, _, (lat, lon)] if lon <= 0:
                print(...)
    ```
    - 一个 `case` 子句由两部分组成：一部分是模式，另一部分是`if`关键字指定的卫语句（可选）。一般匹配对象同时满足以下条件才能匹配序列模式：
        - 匹配对象是序列
        - 匹配对象和模式的项数相等
        - 对应的项相互匹配，包括嵌套的项
        - `str`、`bytes`和`bytearray`实例不作为序列处理。`match`把这些序列作为**原子**的值

### 切片
- 为什么切片和区间排除最后一项
    - 同时指定起始和停止位置时，容易计算切片或区间的长度，做个减法即可：`stop - start`
    - 方便在索引`x`处把序列拆成两个不重叠的部分，`my_list[:x]`和`my_list[x:]`

- `s[a:b:c]` 指定`c`让切片操作跳过部分项。步距可以是负数，反向返回项。
    ```python
    >>> s = 'bicycle`
    >>> s[::3]
    'bye'
    >>> s[::-1]
    'elcycib`
    ```
    - `a:b:c`只在`[]`内有效，表示索引或下标运算符，得到的结果是一个切片对象`slice(a,b,c)`。求解表达式`seq[start:stop:step]`，Python调用`seq.__getitem__(slice(start, stop, step))`
- `[]`可以接受多个索引或切片，以逗号分隔。负责处理`[]`运算符的特殊方法`__getitem__`和`__setitem__`把接收到的`a[i, j]`中的索引当作元组，即`a[i,j]`，Python调用的是`a.__getitem__((i, j))`。
- 外部库，如`numpy.ndarray`表示二维数组可以使用`a[i, j]`句法获取数组中的元素，可以使用表达式`a[m:n, k:l]`获得二维切片
- 省略号是`Ellipsis`对象的别名，而`Ellipsis`对象是`ellilpsis`类的单例，可以把省略号作为参数传给函数，也可以卸载切片规范中，如`a[i,...]`。NumPy在处理多维数组切片中把`...`解释为一种快捷句法。例如对思维数组`x`，`x[i,...]`是`x[i,:,:,:]`的快捷句法。
- 为切片赋值
    ```python
    >>> l = list(range(10))
    >>> l
    [0,1,2,3,4,5,6,7,8,9]
    >>> l[2:5] = [20,30]
    >>> l
    [0,1,20,30,5,6,7,8,9]
    >>> del l[5:7]
    >>> l
    [0, 1, 20, 30, 5, 8, 9]
    >>> l[3::2] = [11, 22]
    >>> l
    [0, 1, 20, 11, 5, 22, 9]
    >>> l[2:5] = 1000
    Tracebook (most recent call last):
        File "<stdin>", line 1, in <module>
    TypeError: can only assign an iterable
    >>> l[2:5] = [100]
    >>> l
    [0, 1, 100, 22, 9]
    ```
- 使用`+`和`*`处理序列：创建一个新对象，不更改操作数
    ```python
    >>> l = [1, 2, 3]
    >>> l * 2
    [1, 2, 3, 1, 2, 3]
    >>> 2 * "abc"
    "abcabc"
    ```

### `list.sort`与内置函数`sorted`
- `list.sort`就地排序列表，返回值为`None`。
- Python API约定：就地更改对象的函数或方法应该返回`None`，让调用方清楚知道接收者已被更改，没有创建新对象。
- 内置函数`sorted`返回创建的新列表。
- `list.sort`和`sorted`有两个可选的关键字参数`reverse`和`key`。
    - `key` 值为`True`是降序返回项，默认为`False`。
    - `key`一个只接受一个参数的函数，引用到每个项上作为排序依据。

### 数组
- 如果一个列表只包含数值，使用`array.array`更高效。
- 创建`array`对象时需要提供类型代码，它是一个字母，用来确定底层使用什么C类型存储数组中的项。
    ```python
    >>> from array import array
    >>> from random import random
    floats = array('d', (random() for i in range(10**7))) # 创建double类型数组
    >>> floats[-1]  # 查看数组最后一项
    >>> fp = open("floats.bin", "wb") 
    >>> floats.tofile(fp) # 把数组存入二进制文件
    >>> fp.close()
    >>> floats2 = array('d') @ 创建一个存放double类型的空数组
    >>> fp = open('floats.bin', 'rb')
    >>> floats2.fromfile(fp, 10**7) # 从二进制文件中读取1000万个数
    >>> fp.close()
    >>> floats2 == floats
    ```

## 字典和集合
- 字典推导式
    ```python
    >>> dial_codes = [(880, 'Bangladesh'), (55, "Brazil")]
    >>> country_dail = {country: code for code, country in dial_codes}
    ```
- 映射拆包
    - 调用函数时，不止一个参数可以使用`**`，但是，所有键要是字符串，而且在所有参数中是唯一的
    - `**`可在`dict`字面量总使用，同样可以多次使用
        ```python
        >>> def dump(**kwargs):
        ...     return kwargs
        ...
        >>> dump(**{'x': 1}, y=2, **{'z': 3})
        {'x': 1, 'y': 2, 'z',: 3}

        >>> {'a': 0, **{'x': 1}, 'y': 2, **{'z':3, 'x': 4}}
        {'a': 0, 'x': 4, 'y': 2, 'z': 3}
        ```

    - 使用`|`合并映射
        ```python
        >>> d1={'a':1, 'b':3}
        >>> d2={'a':2, 'b':4,'c':6}
        >>> d1 | d2
        {'a': 2, 'b': 4, 'c': 6}
        ```
        - 如果希望就地合并，则使用`|=`

- 使用模式匹配处理映射
    ```python
    def get_creators(record: dict) -> list:
        match record:
            case {'type': 'boo', 'api': 2, 'authors': [*names]}:
                return names
            case _:
                raise ValueError(f'Invalid record: {record!r}')
    ```

- 可哈希：如果一个对象的哈希码在整个生命周期内不变(依托`__hash__`方法），而且可与其他对象比较（`__eq__`方法），那么这个对象就是可哈希的

- 插入或更新可变的值
    - 当键`k`不存在时，`d[k]`抛出错误，也可以把`d[k]`换成`d.get(k, default)`得到默认值
    ```python
    my_dict.setdefault(word, []).append(new_value)
    # 等价于
    if key not in my_dict:
        my_dict[key] = []
    my_dict[key].append(new_value)
    ```
- 自动处理缺失的键：第一种时把普通的`dict`转换成`defaultdict`，还有一种方式是定义`dict`或其他映射类型的子类，实现`__missing__`方法
    - `defaultdict`
    - `__missing__`

### `collections.OrderedDict`
...

### 集合
...

## Unicode 文本和字节序列
...

## 数据类构造器
```python
class Coordinate:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
```
- `collections.namedtuple`是一个工厂方法，使用指定的名称和字段构建`tuple`的子类
    ```python
    from collections import namedtuple
    Coordinate = namedtuple('Cordinate', 'lat lon')
    issubclass(Coordinate, tuple) # True
    ```
- `typing.NamedTuple`可以为各个字段添加类型注解
    ```python
    import typing
    Coordinate = typing.NamedTuple('Coordinate', [('lat', float), ('lot', float)])
    issubclass(Coordinate, tuple)   # True
    typing.get_type_hints(Coordinate)   # {'at': <class 'float'>, 'lon': <class 'float'>}
    ```

- Python 3.6开始，`typing.NamedTuple`也可以在`class`语句中使用，在`typing.NamedTuple`生成的`__init__`方法中，字段参数的顺序在`class`语句中出现的顺序相同。
    ```python
    from typing import NamedTuple

    class Coordinate(NamedTuple):
        lat: float
        lon: float

        def __str__(self):
            ns = 'N' if self.lat  0 else '5'
            we = 'E' if self.lon >= 0 else 'W'
            return f'{abs{self.lat}:.1f}°{ns}, {abs(self.lon):.1f}°{we}'
    ```
- `dataclasses.dataclass`装饰器也支持使用**PEP526**句法来声明实例属性。`dataclass`装饰器读取变量注解，自动为构建的类生成方法
    ```python
    from dataclasses import dataclass

    @dataclass(frozon=True)
    class Coordinate:
        lat: float
        lon: float

        def __str__(self):
            ns = 'N' if self.lat >= 0 else 'S'
            we = 'E' if self.lon >= 0 else 'W'
            return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'
    ```

- `namedtuple` `typing.NamedTuple` `dataclasses.dataclass`主要功能
    - 可变实例：`collections.namedtuple`和`typing.NamedTuple`构建的类是`tuple`的子类，实例是不可变的，`dataclass`默认构建可变的实例，可以接受关键字参数`frozen`，指定`frozen=True`，初始化实例后，如果为字段赋值，则抛出异常
    - `class`语句句法：只有`typing.NamedTuple`和`dataclass`支持常规的`class`语句句法，方便为构建的类添加方法和文档字符串。
    - 构造字典：两种具名元组提供了构造`dict`对象的实例方法`._asdict`，`dataclasses`模块提供了构造字典的函数`dataclasses.asdict`
    - 获取字段名称和默认值：具名`tuple`的字段和可能配置的默认值在类属性`._fields`和`._fields_defaults`中。对于`dataclasses`装饰器构建的类，这些元数据使用`dataclasses`模块的`fields`函数获取，返回一个由`Field`对象构成的元组，`Field`对象有属性，包括`name`和`default`。
    - 获取字段类型：`typing.NamedTuple`和`@dataclass`定义的类有一个`__annotations__`类属性，值为字段名称到类型的映射。不建议直接使用`__annotations__`属性，而要使用`typing.get_type_hints`函数。
    - 更改之后创建新实例：`x._replace(**kwargs)`根据指定的关键字参数替换某些属性的值，返回一个新实例。模块级函数`dataclasses.replace(x, **kwargs)`与`dataclass`装饰的类具有相同的作用。

    - 运行时定义新类：`namedtuple(...)`、`NamedTuple(...)`，`dataclasses.make_dataclass(...)`

### 典型的具名元组

```python
>>> from collections import namedtuple
>>> City = namedtuple('City', 'name country population coordiantes')
>>> tokyo = City('Tokyo', 'JP', 36.933, (35.68, 139.69))
>>> tokyo
City(name='Tokyo', country='JP', population=36.933, coordinates=(35.68, 139.69))
>>> tokyo.population
36.933
>>> tokyo.coordinates
(35.68, 139.69)
>>> tokyo[1]
'JP'
```
- 创建具名元组需要指定两个参数：类名和字段名称列表。后一个参数可以是产生字符串的可迭代对象，也可以是一整个以空格分隔的字符串。
- 除了继承`tuple`外，具名元组还有一些额外的属性和方法，类属性`_fields`、类方法`_make(iterable)`，实例方法`_asdict()`

### 带类型的具名元组

```python
from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float
    reference: str = "WGS84"
```

### 变量注解句法
- 变量注解基本语法：
    ```python
    var_name: some_type
    ```
- 定义数据类时，最常使用以下类型
    - 具体的类`str`
    - 参数化容器类型，如`list[int]`、`tuple[str, float]`
    - `tying.Optional`，例如`Optional[str]` 
- 为变量指定初始值
    ```python
    var_name: some_type = a_value
    ```

- 变量注解在运行时没有作用。Python在导入（加载模块）时会读取类型提示，构建`__annotations__`字典，供`typing.NamedTuple`和`@dataclass`使用，增强类的功能。
    ```python
    class DemoPlainClass:
        a: int
        b: float = 1.1
        c = 'spam'
    ```
    - `a`出现在`__annotations__`中，但被抛弃了，因为该类没有名为`a`的属性
    - `b`作为注解记录下来，而且是一个类属性
    - `c`是一个普通的类属性，没有注解
    - `a`只作为注解存在，不是类属性，因为没有绑定值
- `typing.NamedTuple`类
    ```python
    import typing

    class DemoNTClass(typing.NamedTuple):
        a: int
        b: float = 1.1
        c = 'spam'
    ```
    ```python
    >>> from demo_nt import DemoNTClass
    >>> DemoNTClass.__annotations__
    {'a': <class 'int'>, 'b': <class 'float'>}
    >>> DemoNTClass.a
    <_collections._tuplegetattr object at 0x101f0f940>
    >>> DemoNTClass.b
    <_collections._tuplegetatter object at 0x101f0f8b0>
    >>> DemoNTClass.c
    'spam'
    ```
    - 类属性`a`和`b`是描述符
- `dataclass`装饰的类
    ```python
    from dataclasses import dataclass

    @dataclass
    class DemoDataClass:
        a: int
        b: float = 1.1
        c = 'spam'
    ```
    ```python
    >>> from demo_dc import DemoDataClass
    >>> DemoDataClass.__annotations__
    {'a': <class 'int'>, 'b': <class 'float'>}
    >>> DemoDataClass.__doc__
    'DemoDataClass(a: int, b: float = 1.1)`
    >>> DemoDataClass.a
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    AttributeError: type object 'DemoDataClass' has no attribute 'a'
    >>> DemoDataClass.b
    1.1
    >>> DemoDataClass.b
    1.1
    >>> DemoDataClass.c
    'spam'
    ```
    - `a` 只在`DemoDataClass`的实例中存在
    ```python
    >>> dc = DemoDataClass(9)
    >>> dc.a
    9
    >>> dc.b
    1.1
    >>> dc.c
    'spam'
    ```
    - `a`和`b`是实例属性，`c`是类属性。

### `@dataclass`详解

`@dataclass`完整签名如下

```python
@dataclass(*, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
```
- 第一个参数位置上的`*`表明后面都是关键字参数
- 声明的字段将作为参数传递给生成的`__init__`方法。Python规定，带默认值的参数后面不能有不带默认值的参数。因此，为一个参数声明默认值后，余下字段都要带上默认值。
- 可变的默认值往往导致bug。如果在函数定义中使用可变默认值，调用函数时很容易破坏默认值，则导致后续调用行为发生变化。
- `@dataclass`拒绝以下方式定义类
    ```python
    @dataclass
    class ClubMember:
        name: str
        guests: list = []
    ```
    ```bash
    $ python3 club_wrong.py
    Traceback (most recent call last):
    File "club_wrong.py", line 4, in <module>
        class ClubMember:
        ...
    ValueError: mutable default <class 'list'> for field guests is not allowed:
    use default_factory
    ```
    - 合法的定义方式
        ```python
        from dataclasses import dataclass field
        @dataclass
        class ClubMember:
            name: str
            guests: list = field(default_factory=list)
        ```
        - `guests`字段的默认值不是列表字面量，而是调用`dataclasses.field`函数，把参数设置为`default_factory=list`以此设置默认值。
        - `default_factory`参数的值可以是一个函数、一个类，或者其他可调用对象，在每次创建数据类的实例时调用（不带参数），构建默认值。
- `@dataclass`生成`__init__`方法只做一件事：把传入的参数及其默认值（入围制定值）赋值给实例属性，变成实例字段。优势初始化实例要做的不只这些，可以提供一个`__post_init__`方法，如果存在这个方法，`@dataclass`将在生成的`__init__`方法最后调用`__post_init__`方法。
- `__post_init__`常用于执行验证，以及根据其他字段计算一个字段的值。