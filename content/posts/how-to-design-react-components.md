+++
title = "如何设计 React 组件"
date = "2026-02-28"

[taxonomies]
tags = [ "React", "TypeScript", "JavaScript" ]
+++

设计 React 组件不仅是编写 JSX，更是一门关于解耦、复用和可维护性的艺术。优秀的组件设计能让项目在规模扩大时依然易于管理。在考虑组件设计时，不仅要关注可复用性，还要警惕过度封装的风险。

## 核心设计原则

在动手编码前，需要明确并遵循以下核心原则：

1. **单一职责原则**
   - 理想情况下，一个组件只负责一件事。如果一个组件既负责数据获取、复杂逻辑处理，又负责 UI 渲染，那它就过于“臃肿”了。
   - 做法：拆分。将数据获取、复杂逻辑计算抽离到自定义 Hook 或工具函数中，组件只负责“组装”和“展示”。

2. **展示组件 vs 容器组件**（React 经典设计模式）
   - 展示组件：只关注 UI 呈现。接收 Props，渲染 DOM，不关心数据来源。通常是无副作用的函数组件。
   - 容器组件：关注逻辑和数据。负责获取数据、管理状态，并将数据传递给展示组件。
   - 现代演变：随着 Hooks 的普及，界限变得模糊，但核心思想依然重要——将逻辑与 UI 解耦。

3. **组合优于继承**
   - React 推荐使用组合而非继承。不要试图通过继承 BaseComponent 来复用逻辑，而应使用组合或 Hooks。

在设计组件前，先思考其职责：

| 思考点           | 建议                                                                                                 |
| :--------------- | :--------------------------------------------------------------------------------------------------- |
| **单一职责**     | 一个组件只做一件事（例如：渲染列表、显示弹窗、处理表单输入）。如果功能变多，考虑拆分为更小的子组件。 |
| **可复用性**     | 思考「这段 UI/逻辑」是否可能在其他页面或业务中使用。若是，则抽离成独立组件。                         |
| **组合优于继承** | 使用 `props.children`、render props、函数子组件实现“插槽”式组合。                                    |
| **命名规范**     | 名称要语义化、简短、清晰。如 `<UserAvatar />`、`<OrderList />`、`<CreateOrderForm />`。              |

## 组件 API 设计

组件的“接口”设计直接决定了其易用性。

### Props 设计原则

- **命名语义化**：例如 `isDisabled` 比 `disabled` 更能明确表示这是一个布尔值开关。
- **避免传递复杂对象**：尽量只传递组件需要的数据，不要传递整个庞大的 `user` 对象，而是只传 `userName` 和 `avatarUrl`。
- **提供默认值**：使用默认参数或解构赋值，降低使用门槛。
- **深层传递优化**：3 层以上的 props 传递可以考虑 Context、状态管理（如 Redux/Zustand）或自定义 Hook。

### 统一的 Props 命名规范

- 事件回调：`onXxx`（如 `onSubmit`、`onCancel`）
- 布尔开关：`isXxx` / `hasXxx`（如 `isLoading`、`hasError`）
- 数据集合：`items`（列表）或 `data`（单条）

```tsx
// 好的设计：解构赋值 + 默认值 + 明确的类型注释
const Button = ({
  type = "primary",
  onClick,
  children,
  loading = false,
}: ButtonProps) => {
  // ...
};
```

### 利用 `children` 和插槽

不要把所有内容都通过 props 传递。对于布局组件或容器类组件，优先使用 `children`：

```tsx
// 坏设计：写死内容结构
<Card title="标题" content="内容" />

// 好设计：灵活的组合
<Card>
  <Card.Header>标题</Card.Header>
  <Card.Body>任意复杂的内容</Card.Body>
</Card>
```

### 受控 vs 非受控组件

- **受控组件**：由父组件完全控制状态，通过 props 接收 `value` 和 `onChange`。
- **非受控组件**：内部管理自己的状态，只在需要时通知父组件（通过 ref 暴露方法）。
- **最佳实践**：编写同时支持两种模式的组件（例如 Ant Design 的 Input，既可以受控也可以非受控）。

## 逻辑复用与状态管理

### 状态下沉原则

- 状态应尽量放在离它最近的共同父组件中（局部状态）。
- 不要随意引入 Redux/Zustand，对于模态框开关、表单输入等 UI 状态，保留在组件内部或父组件即可。

### 逻辑抽离：自定义 Hooks

这是现代 React 设计的灵魂。如果组件中充斥着 `useEffect`、`useState` 和复杂的数据转换，应将它们抽离出来：

```tsx
// 组件内逻辑混杂
const UserList = () => {
  const [users, setUsers] = useState([]);
  useEffect(() => { fetch... }, []);
  // ... 渲染逻辑
};

// 优秀设计：逻辑抽离
const useUsers = () => {
  const [users, setUsers] = useState([]);
  useEffect(() => { fetch... }, []);
  return { users, loading: !users.length };
};

const UserList = () => {
  const { users, loading } = useUsers();
  // 现在组件只关心渲染
  if (loading) return <Spinner />;
  return <ul>...</ul>;
};
```

## 性能优化意识

设计组件时要有“防患于未然”的性能优化意识：

### 避免不必要的渲染

- **React.memo**：对于接收相同 props 但渲染开销较大的组件，使用 `React.memo` 进行浅比较优化。
- **useCallback / useMemo**：如果传递给子组件的 props 是函数或对象，在父组件中使用 `useCallback` 或 `useMemo` 包裹，防止引用变化导致子组件无效刷新。

### 合理的代码分割

对于大型组件（如复杂的图表、编辑器），使用 `React.lazy` 和 `Suspense` 进行懒加载：

```tsx
const HeavyChart = React.lazy(() => import("./HeavyChart"));

const Dashboard = () => (
  <Suspense fallback={<Skeleton />}>
    <HeavyChart />
  </Suspense>
);
```

## 实战案例：设计一个健壮的列表组件

假设我们要设计一个加载用户数据的列表。

### 设计思路

- **分离关注点**：数据获取与 UI 展示分离。
- **可配置性**：列表项如何渲染应由使用者决定。
- **健壮性**：处理加载态、空态和错误态。

```tsx
interface User {
  id: string;
  name: string;
  age: number;
}

const useUserList = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetch("/api/users")
      .then((res) => res.json())
      .then((data) => {
        setUsers(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err);
        setLoading(false);
      });
  }, []);

  return { users, loading, error };
};

interface UserListProps {
  renderItem?: (user: User) => React.ReactNode;
}

const UserList = ({ renderItem }: UserListProps) => {
  const { users, loading, error } = useUserList();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (users.length === 0) return <div>No users found.</div>;

  return (
    <ul className="user-list">
      {users.map((user) => (
        <li key={user.id}>
          {/* 默认渲染逻辑，允许被覆盖 */}
          {renderItem ? renderItem(user) : user.name}
        </li>
      ))}
    </ul>
  );
};

export default UserList;
```

## 总结

设计优秀的 React 组件需要综合考虑多个维度：

| 维度         | 检查点             | 详细说明 / 最佳实践                                                                 |
| :----------- | :----------------- | :---------------------------------------------------------------------------------- |
| **职责单一** | 组件只做一件事？   | 是否可以进一步拆分？是否存在逻辑过重的“巨型组件”？                                  |
| **API 友好** | Props 设计质量     | props 命名是否直观、语义化？是否有合理的默认值？是否实现了类型安全（TypeScript）？  |
| **可测试性** | 测试覆盖能力       | 是否可以用 React Testing Library (RTL) 直接渲染并模拟交互？                         |
| **可复用性** | 业务数据解耦程度   | 是否只依赖 props / context，而不硬编码业务数据？逻辑是否通用？                      |
| **性能优化** | 渲染效率           | 是否需要 `React.memo` / `useMemo` / `useCallback`？列表渲染是否使用了唯一的 `key`？ |
| **样式管理** | 样式封装方式       | 样式是否被封装（模块化 CSS 或 CSS-in-JS）？是否抽离了主题 token（颜色、间距等）？   |
| **可访问性** | Accessibility 支持 | 是否有必要的 `aria-*` 属性和 `role`？键盘导航是否完整可访问？                       |
| **错误处理** | 健壮性             | 是否有 `ErrorBoundary` 包裹？异常状态（如接口报错）是否有友好提示？                 |
| **文档建设** | 示例与文档         | 是否提供 Storybook story 或清晰的文档示例代码？                                     |
| **组织规范** | 目录结构           | 组件是否存放在对应的 `features/` 或 `components/` 目录下？                          |

### 设计要点回顾

1. **职责拆分**：让每个组件只负责“一件事”。
2. **函数组件 + Hooks**：用函数组件和 Hooks 来组织 UI 与逻辑，保持代码简洁、可组合。
3. **Props 设计**：精心设计 props，确保语义化、类型安全，并提供合理的默认值。
4. **状态管理**：分层管理（展示 ↔ 容器），使用 Context 或 Hooks 进行状态共享。
5. **样式处理**：抽离样式，使用 CSS Modules、Styled-Components、Tailwind 或 UI 框架。
6. **性能优化**：使用 `React.memo`、虚拟列表、代码分割等手段。
7. **测试覆盖**：确保测试到位，使用 RTL + Storybook + E2E 测试。
8. **遵循规范**：遵循目录结构和设计检核表，保证项目长期可维护。
