+++
title = "第一章 设置 Go 的开发环境"
date = "2026-03-11"

[taxonomies]
tags = [ "Go","Programming Go" ]
+++

## Go 的工作空间

Go 编译器本身是单个可执行的二进制文件，没有太多依赖项目。甚至我们的代码默认都是静态链接编译的。但是 Go 还是需要一个工作空间的，用于存放使用 `go install` 安装的第三方 Go 工具。默认情况下，工作空间位于 `$HOME/go`。

## 代码格式化

Go 的主要设计目标之一是创建一种能够高效编写代码的语言。大多数语言在代码的编排方式上都有很大的灵活性，而 Go 则不然。强制使用标准格式使得编写操作源代码工具变的非常容易。另一个好处是，避免了开发者在格式之争上一直浪费大量时间。

Go 的开发工具中包含命令 `go fmt`，它可以自动重新格式化代码，使其符合标准格式。还有一个增强版的 `go fmt` 叫做 `goimports`，它也可以清理导入语句，并尝试猜测任何未制定的导入。

可以使用命令 `go install` 去安装它：

```sh
go install golang.org/x/tools/cmd/goimports@latest
```

可以在 cli 下直接使用它：

```sh
goimports -l -w .
```

## 分析与审查

虽然 `go fmt` 可以确保代码格式正确，但这只是确保代码符合 Go 语言管理且高质量的第一步。有一些工具可以使我们的代码更进一步，第一个工具叫做 `golint`。除此之外还有个工具集中来检测非语法的错误。例如格式化方法传递了错误的参数数量，或者给从未使用过的变量赋值。此时可以使用 `go vet` 来检测诸如此类的错误。

此外还可以调用第三方的工具来检查代码格式和扫描潜在的 Bug。`golangci-lint` 就是同时结合了 `golint` 和 `go vet` 的第三方工具集。

可以使用命令来安装：

```bash
# 安装 golangci-lint（代码检查）
# macOS/Linux
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin
# 或使用 go install
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

## Makefile

Makefile 是用于配合 make 构建工具使用的脚本文件，主要用于自动化编译、链接和管理软件项目中的源文件。它定义了目标（targets）、依赖（dependencies）和命令（commands）之间的规则，告诉系统如何从源文件生成可执行文件或库文件。

Makefile 的核心作用是自动化构建和管理软件项目。它通过定义文件之间的依赖关系和生成规则，告诉 make 工具如何从源代码编译、链接并最终生成可执行文件或库文件。

当项目变得复杂，或者需要多人协作、CI/CD 集成时，原生的 go 命令显得不够用，Makefile 能解决以下痛点：

A. 简化复杂的编译参数

原生命令可能很长且难记：

```sh
# 原生命令：长且容易输错
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w -X main.Version=1.0.0" -o bin/myapp cmd/main.go
使用 Makefile 后：
```

```makefile
build:
	go build -ldflags="$(LDFLAGS)" -o bin/myapp cmd/main.go
# 用户只需输入：make build
```

B. 统一工作流（One Command to Rule Them All）

开发人员不需要记住是先跑 lint 还是先跑 test，也不需要记得生成的二进制文件放在哪。

### 参考

这是 Saber 项目的 Makefile。

```makefile
.PHONY: build clean test fmt lint run help

APP_NAME := saber
GIT_MSG := $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
VERSION := 0.0.2
BUILD_DIR := bin
MAIN_FILE := main.go

build: ## Build the binary
	@mkdir -p $(BUILD_DIR)
	go build -tags goolm -ldflags="-X 'main.version=$(VERSION)' -X 'main.gitMsg=$(GIT_MSG)'" -o $(BUILD_DIR)/$(APP_NAME) .

clean: ## Remove build artifacts
	rm -rf $(BUILD_DIR)

test: ## Run tests
	go test -v -tags goolm ./...

fmt: ## Format code with goimports
	goimports -w ./...

lint: ## Run golangci-lint
	golangci-lint run --build-tags goolm ./...

run: ## Run the application
	go run -tags goolm $(MAIN_FILE)

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := build
```

## Build tag

Go 语言的 Build Tags（构建标签，也称为构建约束 build constraints）是 Go 编译器提供的一种机制，允许开发者根据特定的条件（如操作系统、架构、自定义标签等）来决定是否编译某个文件或代码块。
这在编写跨平台代码、区分开发/生产环境、或者为不同配置提供不同实现时非常有用。

在使用一些第三方包的时候可以给编译器传递特定的 `-tags` 参数来指定使用哪些 tag。

```sh
go build -tags goolm .
```

如果启用了 build tags，则也需要为编辑器/IDE 通知，可以通过设置环境变量或通过编辑器的特定设置来为其设置 build tags。

例如 Visual Studio Code 可以使用项目级配置：`.vscode/settings.json`

```json
{
  "go.buildFlags": ["-tags", "goolm"]
}
```
