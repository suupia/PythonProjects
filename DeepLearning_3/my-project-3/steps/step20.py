import numpy as np
import weakref
import contextlib

class Config:
    enable_backprop = True

@contextlib.contextmanager
def using_config(name, value):
      old_vallue = getattr(Config, name)
      setattr(Config, name, value)
      try:
            yield
      finally:
            setattr(Config, name, old_vallue)

def no_grad():
      return using_config('enable_backprop', False)

class Variable:
      def __init__(self, data, name=None):
            if data is not None:
                  if not isinstance(data, np.ndarray):
                        raise TypeError('{} is not supported'.format(type(data)))

            self.data = data
            self.name = name
            self.grad = None
            self.creator = None
            self.generation = 0

      @property
      def shape(self):
            return self.data.shape

      @property
      def ndim(self):
            return self.data.ndim

      @property
      def size(self):
            return self.data.dtype

      def __len__(self):
            return len(self.data)

      def __repr__(self):
            if self.data is None:
                  return 'variable(None)'
            p = str(self.data).replace('\n', '\n' + ' ' * 9)
            return 'variable(' + p + ')'

      def set_creator(self, func):
            self.creator = func
            self.generation = func.generation + 1

      def backward(self, retain_grad=False):
            if self.grad is None:
                  self.grad = np.ones_like(self.data)

            funcs = []
            seen_set = set()

            def add_func(f):
                  if f not in seen_set:
                        funcs.append(f)
                        seen_set.add(f)
                        funcs.sort(key=lambda x: x.generation)

            add_func(self.creator)

            while funcs:  # 再帰処理をループで置き換えた
                f = funcs.pop() # 関数を取得
                # gys = [output.grad for output in f.outputs]
                gys = [output().grad for output in f.outputs]  # outputを弱参照に変えたため()が必要
                gxs = f.backward(*gys)  # アンパッキング Functionのbackwardであることに注意！
                if not isinstance(gxs, tuple):
                      gxs = (gxs, )

                for x , gx in zip(f.inputs, gxs):
                      if x.grad is None:
                            x.grad = gx
                      else:  # Noneでない時は同じ変数であるということだから加算する
                            x.grad = x.grad + gx

                      if x.creator is not None:
                            add_func(x.creator)

                if not retain_grad:
                      for y in f.outputs:
                            y().grad = None  # yはweakref

      def cleargrad(self):
            self.grad = None

def as_array(x):
      if np.isscalar(x):
            return np.array(x)
      return x


def as_variable(obj):
    if isinstance(obj, Variable):
        return obj
    return Variable(obj)


class Function:
      def __call__(self,*inputs):
            inputs = [as_variable(x) for x in inputs]
            xs = [x.data for x in inputs]
            ys = self.forward(*xs)  # アスタリスクをつけてアンパッキング
            # xs = [x0, x1]の場合、self.forward(*xs)とすれば、それはself.forward(x0, x1)として呼び出すことと同じになる
            if not isinstance(ys, tuple):  # タプルではない場合の追加対応
                  ys = (ys, )
            outputs = [Variable(as_array(y)) for y in ys]

            if Config.enable_backprop:
                self.generation = max([x.generation for x in inputs])
                for output in outputs:
                    output.set_creator(self)
                self.inputs = inputs
                self.outputs = [weakref.ref(output) for output in outputs]

            return outputs if len(outputs) > 1 else outputs[0]

      def forward(self,x):
            raise NotImplementedError()

      def backward(self,gy):
            raise NotImplementedError()


class Square(Function):
      def forward(self,x):
            y = x **2
            return y

      def backward(self, gy):
            x = self.inputs[0].data
            gx = 2 * x * gy
            return gx

def square(x):
      return Square()(x)

class Exp(Function):
      def forward(self, x):
            y = np.exp(x)
            return y

      def backward(self, gy):
            x = self.input.data
            gx = np.exp(x) * gy
            return gx

def exp(x):
      return Exp()(x)

class Add(Function):
      def forward(self, x0, x1):
            y = x0 + x1
            return y

      def backward(self, gy):
            return gy, gy

def add(x0, x1):
      return Add()(x0, x1)

class Mul(Function):
      def forward(self, x0, x1):
            y = x0 * x1
            return y

      def backward(self, gy):
            x0 , x1 = self.inputs[0].data, self.inputs[1].data
            return gy * x1, gy * x0

def mul(x0, x1):
      return Mul()(x0, x1)

Variable.__add__ = add
Variable.__mul__ = mul

def numerical_diff(f,x,eps=1e-4):
      x0 = Variable(x.data - eps)
      x1 = Variable(x.data + eps)
      y0 = f(x0)
      y1 = f(x1)
      return (y1.data - y0.data ) / (2 * eps)


x = Variable(np.array(2.0))
y = x + np.array(3.0)
print(y)
