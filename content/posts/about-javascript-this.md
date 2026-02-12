+++
title = "What about this - JavaScript 全面解析"
date = "2022-09-24"
updated = "2022-09-24"

[taxonomies]
tags=["JavaScript"]
+++

## this 全面解析

this 和动态作用域有些许类似，它们都是在执行时决定的。this 是在调用时被绑定的，完全取决于函数的调用位置。

### 确定调用位置

当一个函数被调用时，会创建一个活动记录（执行期上下文）。这个记录会包含函数在哪里被调用（调用栈）、函数的调用方式、传入的参数等信息。this 就是这个记录里的一个属性。

调用位置就是函数在代码中被调用的位置，而不是声明的位置。我们可以通过分析调用栈来确定函数的真正调用位置。

```ts
function foo() {
  // 当前调用栈：foo

  console.log("foo");
  bar();
}
function bar() {
  // 当前调用栈：foo --> bar

  console.log("bar");
  baz();
}
function baz() {
  // 当前调用栈：foo --> bar --> baz

  console.log("baz");
}
foo();
```

### 绑定规则

this 是在运行时动态绑定的，所以在不同的情况下，this 的指向可能会出现各种意料之外的结果。

#### 默认绑定

当函数在全局环境下独立调用时，this 会指向全局对象。

```ts
var a = 123;
function foo() {
  console.log(this.a); // 123
}
```

而当函数处于严格模式下时，则不能将全局对象用于默认绑定，因此 this 会绑定到 `undefined`。

```ts
var a = 123;
function foo() {
  "use strict";
  console.log(this.a); // TypeError: this is undefined
}
```

还有一个微妙的细节：虽然 this 的绑定完全取决于调用位置，但只有 `foo()` 函数本身处于非严格模式时才能绑定到全局对象。如果只是函数执行时所在的环境是严格模式，而函数本身是非严格模式，则不影响默认绑定规则。

```ts
var a = 123;

function foo() {
  console.log(this.a);
}

(() => {
  "use strict";
  foo();
})();
```

> 通常来说不推荐在代码中混用严格模式与非严格模式。

#### 隐式绑定

另一种规则是考虑调用位置是否有上下文对象，或者说某个对象是否包含这个函数。

```ts
function foo(this: typeof obj) {
  console.log(this.name);
}
const obj = {
  name: "xfy",
  foo: foo,
};
obj.foo(); // xfy
```

这种方式可以理解为将 `foo()` 的函数体赋值给了对象 obj 的一个属性，而执行时是从 obj 作为上下文对象来执行的。所以 this 隐式地绑定到了 obj 对象上。

对象属性引用链中只有上一层或者说最后一层在调用位置中起作用。

```ts
function foo(this: typeof obj) {
  console.log(this.name);
}
const obj = {
  name: "xfy",
  foo: foo,
};
obj.foo(); // xfy

const anotherObj = {
  name: "dfy",
  obj: obj,
};
anotherObj.obj.foo(); // xfy
```

**隐式丢失**

既然会有隐式绑定，自然也会出现隐式丢失的问题。

```js
function foo() {
  console.log(this.name);
}

const obj = {
  name: "xfy",
  age: 18,
  foo,
};

const bar = obj.foo; // 函数别名
bar();
```

虽然 bar 是 `obj.foo` 的一个引用，但它引用的是函数体本身。可以理解为将函数体传递给了 bar 这个变量，此时调用 `bar()` 是一个不带任何修饰的函数调用，因此会使用默认绑定。

另一种常见且出乎意料的情况就是在传递回调函数时：

```js
function foo() {
  console.log(this.name);
}

function doFoo(fn) {
  fn();
}

const obj = {
  name: "xfy",
  age: 18,
  foo,
};

doFoo(obj.foo);
```

参数传递其实就是一种隐式赋值，因此我们传入函数时也会被隐式赋值。只要函数体被传递后，且调用时脱离了原有的对象，就会导致 this 的隐式丢失。

包括 `setTimeout()` 方法丢失 this 也是同理。

#### 显式绑定

由于原型的特性，JavaScript 中函数也有自己的属性。大多数宿主环境都会提供 `call()` 与 `apply()` 方法来让我们显式地绑定 this。

```js
function foo() {
  console.log(this.name);
}
const obj = {
  name: "xfy",
  age: 18,
  foo,
};
foo.call(obj);
```

> call 与 apply 只是传参方式不同。

使用显式绑定可以很好地解决传递参数时隐式丢失 this 的问题。

```js
function foo() {
  console.log(this.name);
}
const obj = {
  name: "xfy",
  age: 18,
  foo,
};
function bar() {
  foo.call(obj);
}
setTimeout(bar, 1000);
// 同理
// setTimeout(() => {
//   obj.foo();
// }, 1000);
```

这里在 `bar()` 的内部直接手动显式地把 `foo()` 绑定到了 obj，无论之后怎么调用、在何处调用，都会手动将 obj 绑定在 `foo()` 上。这种绑定称之为**硬绑定**。

不过这种绑定是特意设计的例子，这里手动为 `foo()` 绑定到了 obj。在多数情况下，我们可能需要更灵活的方案。

在 [JavaScript 装饰器模式 🎊 - 🍭Defectink (xfy.plus)](https://xfy.plus/defect/javascript-decorator.html) 中介绍了这种工作模式。通过一个包装器配合显式绑定就能解决大部分情况下的问题。

```js
function foo(msg) {
  console.log(this.name);
  console.log(msg);
}
function wrapper(fn, obj) {
  return (...rest) => {
    fn.apply(obj, rest);
  };
}
const obj = {
  name: "xfy",
  age: 18,
};
const bar = wrapper(foo, obj);
bar("嘤嘤嘤");
```

包装器不仅仅只是用来解决 this 丢失的问题，对于 this 绑定的问题，ES5 提供了内置的方法 `Function.prototype.bind`。

```js
function foo() {
  console.log(this.name);
}
const obj = {
  name: "xfy",
  age: 18,
};
const bar = foo.bind(obj);
bar();
```

#### new 绑定

在传统面向类的语言中，“构造函数”是类中的一些特殊方法，使用类时会调用类中的构造函数。通常类似于这样：

```js
myObj = new MyClass();
```

在 JavaScript 中，所有函数都可以被 new 操作符调用。这种调用称为构造函数调用，实质上并不存在所谓的“构造函数”，只有对于函数的“构造调用”。

使用 new 来进行构造函数调用时，会执行以下操作：

1. 创建（构造）一个新对象。
2. 对新对象执行 `[[Prototype]]` 连接。
3. 将新对象绑定到函数调用的 this。
4. 如果函数没有返回其他对象，那么在 new 调用后自动返回这个新对象。

```js
function Foo(name) {
  this.name = name;
}
const bar = new Foo("xfy");
console.log(bar.name);
```

使用 new 操作符来调用 `foo()` 时，会构造一个新对象并把它绑定到 `foo()` 中的 this 上。new 是最后一种可以影响函数调用时 this 绑定行为的方法，我们称之为 new 绑定。

> ES6 的 class 只是一个语法糖，但它也解决了一些问题。

### 优先级

上述描述的四条规则中，如果某处位置可以应用多条规则时，就要考虑到它们的优先级问题。

毫无疑问，默认绑定肯定是优先级最低的绑定。所以先来考虑隐式绑定与显式绑定之间的优先级，用一个简单的方法就能测试出来：

```js
function foo() {
  console.log(this.age);
}

const xfy = {
  name: "xfy",
  age: 18,
  foo,
};
const dfy = {
  name: "dfy",
  age: 81,
  foo,
};

xfy.foo(); // 18
dfy.foo(); // 81

xfy.foo.call(dfy); // 81
dfy.foo.call(xfy); // 18
```

很明显，显式绑定的优先级更高，也就是说在判断时应当先考虑是否存在显式绑定。

那么 new 绑定与隐式绑定呢？

```js
function foo(msg) {
  this.a = msg;
}

const xfy = {
  name: "xfy",
  foo,
};
xfy.foo("test");
console.log(xfy);

const obj = new xfy.foo("this is obj");
console.log(obj);
```

可以看到，这里对对象 xfy 中隐式绑定的函数进行了 new 操作，而最后的 this 被绑定到了新对象 obj 上，并没有修改 xfy 本身的值。所以 new 绑定的优先级比隐式绑定更高。

那 new 绑定与显式绑定呢？由于 `call/apply` 无法与 new 一起使用，所以无法通过 `new xfy.foo.call(obj)` 来测试优先级，但我们可以通过硬绑定 `bind()` 来测试。

```js
function foo(msg) {
  this.a = msg;
}

const xfy = {
  name: "xfy",
  foo,
};

let obj = {};

const bar = xfy.foo.bind(obj);
bar("obj");
console.log(obj);

// bar was bind to obj
const baz = new bar("this is baz");
console.log(obj);
console.log(baz);
```

可以看到，在硬绑定之后，使用 new 操作时对象 obj 的值并没有被改变，反而对 new 出来的新对象进行了修改。

但这真的说明 new 绑定比硬绑定优先级更高吗？实则不然，上述结果是因为 ES5 中内置的 `Function.prototype.bind()` 方法比较复杂，它会对 new 绑定进行判断，如果是 new 绑定就会使用新创建的 this。

这是来自 [MDN](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Function/bind#polyfill) 的 polyfill bind 方法：

```js
//  Yes, it does work with `new (funcA.bind(thisArg, args))`
if (!Function.prototype.bind)
  (function () {
    var ArrayPrototypeSlice = Array.prototype.slice;
    Function.prototype.bind = function (otherThis) {
      if (typeof this !== "function") {
        // closest thing possible to the ECMAScript 5
        // internal IsCallable function
        throw new TypeError(
          "Function.prototype.bind - what is trying to be bound is not callable",
        );
      }

      var baseArgs = ArrayPrototypeSlice.call(arguments, 1),
        baseArgsLength = baseArgs.length,
        fToBind = this,
        fNOP = function () {},
        fBound = function () {
          baseArgs.length = baseArgsLength; // reset to default base arguments
          baseArgs.push.apply(baseArgs, arguments);
          return fToBind.apply(
            fNOP.prototype.isPrototypeOf(this) ? this : otherThis,
            baseArgs,
          );
        };

      if (this.prototype) {
        // Function.prototype doesn't have a prototype property
        fNOP.prototype = this.prototype;
      }
      fBound.prototype = new fNOP();

      return fBound;
    };
  })();
```

在这几段代码中：

```js
fNOP.prototype.isPrototypeOf(this) ? this : otherThis,
// 以及
if (this.prototype) {
  // Function.prototype doesn't have a prototype property
  fNOP.prototype = this.prototype;
}
fBound.prototype = new fNOP();
```

该 polyfill 检测了是否是使用 new 绑定，并修改 this 为 new 绑定的对象。

#### 判断 this 的步骤

根据上述优先级，可以得出判断 this 的结论（优先级从高到低）：

1. 函数是否在 new 中调用（new 绑定）？
   如果是，this 绑定到新创建的对象。`const bar = new Foo()`

2. 函数是否通过 `call/apply` 或者硬绑定调用（显式绑定）？
   如果是，this 绑定到指定的对象。`const bar = foo.call(baz)`

3. 函数是否在某个上下文对象中调用（隐式绑定）？
   如果是，this 绑定到那个上下文对象上。`const bar = obj.foo()`

4. 上述情况都不满足，那么就会使用默认绑定。

### 绑定例外

凡事都有例外，this 绑定也是如此。在某些情况下，代码看起来可能应用了某种绑定规则，但实际上应用的可能是默认规则。

#### 被忽略的 this

把 null 或者 undefined 作为 this 的绑定对象传入 `call/apply` 与 bind 方法时，这些值会被忽略，从而应用默认绑定规则。

也就是说，`call/apply` 传入 null 或者 undefined 时与直接执行函数本身没有区别。

```js
function foo() {
  console.log(this.name);
}
foo.call(null);
```

这样使用 `call/apply` 的作用是利用它们的特性来解决一些小问题。

例如：展开数组

```js
function bar(a, b) {
  console.log(a, b);
}
bar.apply(null, [1, 2]);
```

当然，在 ES6 中可以使用展开运算符来传递参数：

```js
bar(...[1, 2]);
```

又或是利用 bind 实现柯里化：

```js
function bar(a, b) {
  console.log(a, b);
}

const baz = bar.bind(null, 1);
baz(2);
```

这里都是利用忽略 this 产生的一些副作用，但在某些情况下可能不安全，例如函数可能真的会使用到 this，这在非严格模式下可能会修改全局对象。

如果确实需要使用这种方法，可以创建一个 DMZ（隔离）对象来代替 null。

```js
const dmz = Object.create(null);
foo.call(dmz, arg)
```

#### 间接引用

另外需要注意的是，在某些情况下我们可能会无意地创建一个函数的间接引用。间接引用最容易在赋值期间发生：

```js
function foo() {
  console.log(this.name);
}
const o = {
  foo,
};
const p = {};
(p.foo = o.foo)();
```

赋值表达式 `p.foo = o.foo` 返回的是目标函数的引用，所以在这里调用实际上是在全局环境下直接调用 `foo()`。根据之前的规则，这里会应用默认绑定。
