### 渐进式类型
- 兼容PEP 484的Python类型检查工具：`pytype`、`Mypy`

```python
from typing import Optional

def show_cound(count: int, singular: str, plural: Optional[str] = None) -> str:
  ...
```
- `Optional[str]`表示`plural`值可以是一个`str`或`None`


### 鸭子类型 & 名义类型
- 鸭子类型：对象有类型、但是变量（包括参数）没有类型。只有在运行时尝试操作对象时，才会施行鸭子类型的相关检查。（Smalltalk以及Python、JS、Ruby采用的解读视角。）
- 名义类型：对象和变量都有类型。对象只存在于运行时，类型检查工具只关心使用类型提示注解变量（包括参数）的源码。


## 注解中可用的类型

### `Any`类型
- `Any`类型时渐进式类型系统的基础，是人们熟知的动态类型。`Any`类型支持所有可能的操作。
- 对于没有类型信息的函数，在类型检查工具看来，其具有`Any`类型信息：
  ```python
  def double(x):
    return x * 2

  def double(x: Any) -> Any:
    return x * 2
  ```

### 简单的类型和类
- `int`、`float`、`str`和`bytes`这样简单的类型可以直接在类型提示中使用。标准库、外部包以及自定义的类也可以用于类型提示。
- `int`与`float`相容，`float`与`complex`相容。（虽然彼此之间不是子类，但有相同的操作）

### `Optional`类型和`Union`类型
- `Optinoal[str]`是`Union[str, None]`的简写。
- Python3.10开始，`Union[str, bytes]`可以写成 `str | bytes`
  ```python
  plural: Optional[str] = None
  plural: str | None = None
  ```

### 泛化容器
- 泛型可以用类型参数来声明，以指定可以处理的项的类型。
  ```python
  def tokeinze(text: str) -> list[str]:
    return text.upper().split()
  ```
- `tuple[int, ...]`表示项为`int`类型的元组。

### 泛化映射
- 泛化映射类型使用`MappingType[KeyType, ValueType]`的形式注解。

### 存根文件和Typeshed项目

截至Python3.10，标准库不含注解，但Mypy、PyCharm等可在Typeshed项目中找到所需的类型提示。这些类型提示位于一种存根文件(stub file)中，这是一种特殊的源文件，扩展名为`.pyi`，文件中保存带注解的函数和方法签名，没有实现，类似于C语言的头文件。

- 创建类型别名
  ```python
  FromTo = tuple[str, str]

  # Python3.10
  from typing import TypeAlias
  FromTo: TypeAlias = tuple[str, str]
  ```

### 参数化泛型和`TypeVar`
- 参数化泛型是一种泛型，写作`list[T]`，其中`T`是类型变量，每次使用时会绑定具体的类型。这样可在结果的类型中使用参数的类型。
  ```python
  from collections.abc import Sequence
  from random import shuffle
  from typing import TypeVar

  T = TypeVar('T')

  def sample(population: Sequence[T], size: int) -> list[T]:
    if size < 1:
      raise ValueError("size must be >= 1")
    res = list(population)
    shuffle(res)
    return res[:size]
  ```
  - 如果调用时传入`tuple[int, ...]`类型，则返回类型为`list[int]`
  - 如果传入`str`(与`Sequence[str]`相容)，类型参数为`str`，返回值类型`list[str]`
