### 装饰器基础
- 装饰器是一种可调用对象，其参数是另一个函数（被装饰的函数）。
  ```python
  # decorate是装饰器
  @decorate  
  def target():
    print("running target()")
  # 等价于
  target = decorate(target)
  ```
- 装饰器的基本性质：
  - 装饰器是一个函数或其他可调用对象。
  - 装饰器可以把被装饰的函数替换成别的函数。
  - 装饰器在加载模块时立即执行。


### 闭包
- 闭包就是延伸了作用域的函数，博爱阔函数（`f`）主体中引用的非全局变量和局部变量。这些变量必须来自包含`f`的外部函数的局部作用域。
  ```python
  def make_averager():
    series = []

    def averager(new_value):
      series.append(new_value)
      total = sum(series)
      return total / len(series)
    
    return averager
  ```
  ```python
  >>> avg = make_averager()
  >>> avg(10)
  10.0
  >>> avg(11)
  10.5
  ```
  - `series`是自由变量（未在局部作用域中绑定的变量）。`averager`函数的闭包延伸到自身的作用域之外，包含自由变量`series`的绑定。
- 对于不可变类型的自由变量，需要通过`nonlocal`声明来帮助绑定。
  ```python
  def make_averager():
    count = 0
    total = 0

    def averager(new_value):
      count += 1
      total += new_value
      return total / count

    return averager
  ```
  ```python
  >>> avg = make_averger()
  >>> avg(10)
  Traceback (most recent call last):
  ...
  UnboundLocalError: local variable 'count' referenced before assignment
  >>>
  ```
  对于数值或任何不可变类型，`count += 1`语句的作用与`count = count + 1`一样。因此实际上在`averager`的主体中为`count`赋值了，这会吧`count`编程局部变量。为解决这个问题python3中引入了`nonlocal`关键字
  ```python
  def make_averager():
    count = 0
    total = 0
    def averager(new_value):
      nonlocal count, total
      count += 1
      total += new_value
      return total /count

    return avarager
  ```

### 变量查找逻辑
Python字节码编译器根据以下规则获取函数主体中出现的变量`x`。
- `global x`声明，则`x`来自模块全局作用域，并赋予那个作用域中`x`的值。
- `nonlocal x`声明，则`x`来自最近一个定义它的外层函数，并赋予那个函数中局部变量`x`的值。
- `x`是参数，或**在函数主体中赋值**，那`x`就是局部变量。
- 如果引用`x`，但没有赋值也不是参数，则遵循：
  - 在外层函数主体的局部作用域（非局部作用域）内查找`x`。
  - 如果未找到，则从模块全局作用域内读取。
  - 如果未知道，则从`__builtins__.__dict__`中读取。


### `functools.wraps`
相较于普通的装饰器，`functools.wraps`会把被装饰函数的相关属性复制到装饰器装饰后的函数上，还能正确处理关键字参数。
  ```python
  imort time
  import functools

  def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
      res = func(*args, **kwargs)
    return clocked
  ```

### 标准库中的装饰器
- `lru_cache`缓存函数执行结果
  ```python
  @functools.lru_cache
  def costly_function(a, b):
    ...
  ```