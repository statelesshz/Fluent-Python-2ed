def factorial(n):
  """返回n!"""
  return 1 if n < 2 else n * factorial(n - 1)

print(factorial.__doc__)
