+++
title = "Go By Example"
date = "2026-03-11"

[taxonomies]
tags = [ "Go","GoByExample" ]
+++

## Hello World

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello World")
}
```

每个 Go 程序都从 `package main` 开始，这声明了该文件属于一个可执行程序。`import "fmt"` 引入了格式化输入输出的标准库，用于打印文本到控制台。`func main()` 是程序的入口点，`fmt.Println` 则将字符串输出到标准输出并自动添加换行符。

运行程序：

```bash
go run hello.go
```

## Values

```go
package main

import "fmt"

func main() {
	fmt.Println("go" + "lang")
	fmt.Println("1+1 =", 1+1)
	fmt.Println("7.0/3.0 =", 7.0/3.0)

	fmt.Println(true && false)
	fmt.Println(true || false)
	fmt.Println(!true)
}
```

Go 支持多种基本数据类型。字符串使用 `+` 运算符拼接，`"go" + "lang"` 得到 `"golang"`。整数和浮点数支持标准算术运算，`7.0/3.0` 结果为浮点数 `2.333...`。布尔值支持逻辑运算：`&&`（与）、`||`（或）、`!`（非），运算结果为布尔值。

## Variables

```go
package main

import "fmt"

func main() {
	a := "initial"
	fmt.Println(a)

	var b, c int = 1, 2
	fmt.Println(b, c)

	d := true
	fmt.Println(d)

	var e int
	fmt.Println(e)
}
```

Go 提供多种变量声明方式。`:=` 短声明语法自动推断类型，适用于函数内部。`var` 关键字可显式声明类型，如 `var b, c int = 1, 2` 同时声明多个同类型变量。未初始化的变量会获得零值（zero value），例如 `int` 默认为 `0`，`string` 为空字符串，`bool` 为 `false`。

## Constants

```go
package main

import (
	"fmt"
	"math"
)

const s string = "constant"

func main() {
	fmt.Println(s)

	const n = 500000000

	const d = 3e20 / n
	fmt.Println(d)

	fmt.Println(int64(d))

	fmt.Println(math.Sin(n))
}
```

`const` 关键字声明常量，其值在编译时确定且不可修改。常量可在包级别（函数外）或函数内部声明。Go 的常量具有高精度特性，数值常量在没有明确类型前会根据上下文自动确定类型。例如 `3e20 / n` 的结果可以安全转换为 `int64`，也能直接传递给 `math.Sin` 函数。

## For

```go
package main

import "fmt"

func main() {
	i := 1
	for i <= 3 {
		fmt.Println(i)
		i = i + 1
	}

	for j := 0; j < 3; j++ {
		fmt.Println(j)
	}

	for j := range 3 {
		fmt.Println(j)
	}

	for {
		fmt.Println("loop")
		break
	}

	for n := range 6 {
		if n%2 == 0 {
			continue
		}
		fmt.Println(n)
	}
}
```

`for` 是 Go 中唯一的循环结构，但形式灵活多样。`for i <= 3` 省略初始化和后置语句，类似其他语言的 `while` 循环。标准三段式 `for j := 0; j < 3; j++` 包含初始化、条件和迭代。`for j := range 3`（Go 1.22+）简洁地遍历整数序列。`for {}` 创建无限循环，需配合 `break` 退出；`continue` 则跳过当前迭代进入下一轮。

## If/Else

```go
package main

import "fmt"

func main() {
	if 7%2 == 0 {
		fmt.Println("7 is even")
	} else {
		fmt.Println("7 is odd")
	}

	if 8%4 == 0 {
		fmt.Println("8 is divisible by 4")
	}

	if 8%2 == 0 || 7%2 == 0 {
		fmt.Println("either 8 or 7 are even")
	}

	if num := 9; num < 0 {
		fmt.Println(num, "is negative")
	} else if num < 10 {
		fmt.Println(num, "has 1 digit")
	} else {
		fmt.Println(num, "has multiple digits")
	}
}
```

`if/else` 条件语句无需括号包裹条件，但大括号 `{}` 必须保留。`else if` 和 `else` 为可选分支。Go 特色在于 `if` 可在条件前声明变量：`if num := 9; num < 0` 中 `num` 仅在 if-else 链内可见，这种模式常用于错误处理或资源初始化。

## Maps

```go
package main

import (
	"fmt"
	"maps"
)

func main() {
	m := make(map[string]int)

	m["k1"] = 1
	m["k2"] = 2

	fmt.Println("map: ", m)

	v1 := m["k1"]
	fmt.Println("v1:", v1)

	v2 := m["k2"]
	fmt.Println("v2:", v2)

	fmt.Println("len:", len(m))

	delete(m, "k2")
	fmt.Println("map:", m)

	delete(m, "k1")
	fmt.Println("map:", m)

	_, prs := m["k2"]
	fmt.Println("prs:", prs)

	n := map[string]int{"foo": 1, "bar": 2}
	fmt.Println("map:", n)

	n2 := map[string]int{"foo": 1, "bar": 2}
	if maps.Equal(n, n2) {
		fmt.Println("n == n2")
	}
}
```

Map 是 Go 中内置的键值对数据结构。`make(map[string]int)` 创建一个空 map，键为 `string` 类型，值为 `int` 类型。通过 `m["k1"] = 1` 设置键值对，通过 `v := m["k1"]` 获取值。`len(m)` 返回键值对数量，`delete(m, "k2")` 删除指定键。访问不存在的键会返回值类型的零值。使用 "comma ok" 模式 `_, prs := m["k2"]` 可检测键是否存在，`prs` 为布尔值。Map 也可用字面量初始化：`map[string]int{"foo": 1, "bar": 2}`。Go 1.21+ 提供了 `maps.Equal` 函数来比较两个 map 是否相等。
