### 同一性、相等性和别名
- 对象一旦创建，标识始终不变。可以把标识理解为对象在内存中的地址。`is`运算符比较两个对象的标识，`id()`函数返回对象标识的整数。
- `==`比较两个对象的值是否相等，`is`比较对象的标识
- 使用`is`检查变量绑定的值是不是`None`
  ```python
  x is None
  x is not None
  ```

- `is`比`==`快，因为它不能重载，而是直接比较两个整数ID。

### 默认做浅拷贝
- 构造函数或`[:]`做的是浅拷贝（赋值最外层容器，副本中的项是源容器中项的引用）。

### 为任意对象做浅拷贝或深拷贝
- `copy`模块提供的`copy`和`deepcopy`函数分别对任意对象做浅拷贝和深拷贝
  ```python
  class Bus:
    def __init__(self, passengers=None):
      if passengers is None:
        self.passengers = []
      else:
        self.passengers = list(passengers)
    
    def pick(self, name):
      self.passengers.append(name)

    def drop(self, name):
      self.passengers.remove(name)
  ```
  ```python
  >>> import copy
  >>> bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
  >>> bus2 = copy.copy(bus1)
  >>> bus3 = copy.deepcopy(bus1)
  >>> id(bus1), id(bus2), id(bus3)
  (430149826, 4301499416, 4301499752)
  ```

- 可以通过`__copy__`和`__deepcopy__`控制浅拷贝和深拷贝的行为

### 函数的参数是引用时
- Python唯一支持的参数传递模式是共享传参，函数的形参获得是实参引用的副本。
  ```python
  def f(a, b)
    a += b
    return a
  
  >>> x = 1
  >>> y = 2
  >>> f(x, y)
  3
  >>> x, y
  (1, 2)
  >>> a = [1, 2]
  >>> b = [3, 4]
  >>> f(a, b)
  [1, 2, 3, 4]
  >>> a, b
  ([1,2,3,4], [3,4])
  >>> t = (10, 20)
  >>> u = (30, 40)
  >>> f(t, u)
  (10 ,20, 30, 40)
  >>> t, u
  ((10, 20), (30, 40))
  ```
  - 注意：不要使用可变类型作为参数的默认值，避免一些诡异的问题。默认值在定义函数时求解（通常在加载模块是），因此默认值变成了函数对象的属性。所以，如果默认值是可变的，而且修改了它的值，那么后续的函数调用都会受到影响。

### `del`和垃圾回收
- `del`语句删除引用而不是对象。`del`可能导致对象被当作垃圾回收，当且仅当删除的变量保存的是对象得最后一个引用时。

### Python对不可变类型施的一些trick
- 对于元组来说，`t[:]`和`tuple(t)`不创建副本，而是返回同一对象的引用，还有`.copy()`行为类似。应该说，对于不可变类型都有该逻辑。
