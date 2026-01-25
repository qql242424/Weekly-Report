# muduo库学习所得

## Reactor模型

**多 Reactor 多进程 / 线程方案的示意图**

![](https://i-blog.csdnimg.cn/direct/788ce8fa44e84c2a978c3cdff205b7c9.png)

 ### **一、MainReactor与SubReactor的区别**

| **维度**     | **MainReactor**                            | **SubReactor**                                        |
| ------------ | ------------------------------------------ | ----------------------------------------------------- |
| **核心职责** | 仅处理**新连接建立事件**（`OP_ACCEPT`）    | 处理**已建立连接的I/O事件**（如`OP_READ`/`OP_WRITE`） |
| **线程数量** | 通常为**单线程**（高并发场景可能少量线程） | **多线程**（通常为CPU核数的1~2倍）                    |
| **性能目标** | 快速响应连接请求，避免成为瓶颈             | 高效处理数据读写，避免I/O阻塞影响新连接接入           |
| **资源管理** | 监听全局`ServerSocketChannel`              | 管理**分配到的`SocketChannel`连接队列**               |
| **设计意义** | 解决连接接入的**突发流量压力**             | 解决数据传输的**持续高并发压力**                      |

> **关键引用**：
>
> - MainReactor仅暴露一个服务端口，通过`accept()`获取新连接并分配至SubReactor [][][]。
> - SubReactor维护已注册的Socket连接，执行非阻塞读写及事件分发 [][][]。

### **二、`select`操作的区别**

**1. MainReactor中的`select`**

- **监听事件类型**：**仅`OP_ACCEPT`（连接建立事件）** [][][]。
- **触发条件**：客户端发起TCP握手（SYN包）时，内核通知就绪。
- **后续动作**：通过`dispatch`将新连接**分配给SubReactor** [][][]。

**2. SubReactor中的`select`**

- **监听事件类型**：**`OP_READ`（读就绪）和`OP_WRITE`（写就绪）** [][][]。
- **触发条件**：已建立连接的Socket有数据到达内核缓冲区或可写。
- **后续动作**：调用对应的`Handler`处理数据，可能将计算任务提交至**Worker线程池** [][][]。

| **组件**        | `select`目标事件 | 线程模型    | 核心任务                  |
| --------------- | ---------------- | ----------- | ------------------------- |
| **MainReactor** | `OP_ACCEPT`      | 单/少量线程 | 高效接收新连接并分配      |
| **SubReactor**  | `OP_READ/WRITE`  | 多线程      | 处理已连接Socket的I/O事件 |

## 知识点扩充

### **LT和ET模式的区别：**

- **LT 模式（水平触发）**：像“唠叨的闹钟”——事件没处理完就一直提醒你，直到你搞定为止。
- **ET 模式（边缘触发）**：像“高冷的通知员”——事件发生时只提醒一次，爱理不理随你便，漏了后果自负。

**静态库和动态库后缀**

| **库类型** | **Linux 后缀** | **Windows 后缀** |
| ---------- | -------------- | ---------------- |
| **静态库** | `.a`           | `.lib`           |
| **动态库** | `.so`          | `.dll`           |

### **Cmake中set（静态/动态）库分析**

1. **静态库必用** `CMAKE_ARCHIVE_OUTPUT_DIRECTORY`
2. **共享库使用** `CMAKE_LIBRARY_OUTPUT_DIRECTORY`
3. 项目路径规范:
   - `/lib` 存放静态库和导入库
   - `/bin` 存放共享库和可执行文件

~~~cmake
# 静态库(.a/.lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
# 共享库(.so/.dll)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)  
# 可执行文件 
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
~~~

## 框架体系

**reactor模型**中具体部分：

* **Event** ：事件   （包含：读/写/错误事件）
* **Reactor** ：反应堆
* **Demultiplex** ：多路事件分发器
* **EventHandler** ：事件处理器
* **EventLoop** :  **subReactor** （包含一个**Poller事件分发器**和多个**Channer(事件)**）

![](https://i-blog.csdnimg.cn/direct/f0d767415ce84d96be02998bb696b2c1.png)

这里面的**EventLoop**就是**subreactor**，其中包含**一个Poller**(多路事件分发器)和**多个Channel**（**event事件集合**-----**读/写**一类的）

其中一个**EventLoop**在一个**线程**中（实现了**one loop per thread**）

![](https://i-blog.csdnimg.cn/direct/e2225acc618d4865bf8ecf9414c5ea4a.png)

由于使用的是**多 Reactor 多进程 / 线程方案**（用来解决**并发压力**），所以使用类似于**Nginx**相似的操作，一个**main reactor**通过**accept**组件负责处理**新的客户端**连接，并分给各个**sub reactor**，每个**sub reactor**负责一个连接的读写等工作。

![](https://i-blog.csdnimg.cn/direct/25d26a8b414141789d3eb194dbeec6a4.png)

## Channel代码分析

**EventLoop**  =  **一个Poller**(多路事件分发器)   +   **多个Channel**（**event事件集合**-----**读/写**一类的）

**Poller** ----> **事件监听器**（专门用来观察**文件描述符**所要发生的事件）
**本职：服务员**，负责盯着**自己负责的桌子**，看哪个桌子的顾客有需求（事件），然后报告

------

**Channel**理解为**通道**  通俗理解 —> **“文件描述符的智能管家”** 
封装了**sockfd**和其感兴趣的  **event**  如**EPOLLIN**、**EPOLLOUT**事件 还绑定了**poller返回的具体事件**

> #### Channel 具体做什么？（3 个核心功能）
>
> 1. **替 `fd` 记住“关心的事件”**
>    比如某个 `fd` 只关心“收到数据”（读事件），Channel 会帮它记下来：“这个 `fd` 只听‘收数据’的消息”。
> 2. **替 `fd` 对接“监控系统”**
>    Channel 会把 `fd` 和它关心的事件，统一注册到“监控系统”（比如 `epoll`），不用你手动调用 `epoll_ctl` 这种复杂命令。
> 3. **替 `fd` 保存“事件处理方法”**
>    比如某个 `fd` 收到数据后，应该调用 `onRead()` 函数处理，Channel 会提前存好这个函数，等事件发生时直接“按按钮”执行。

**Channel = 给 `fd` 配了个“秘书”**，秘书负责记需求、对接监控、执行任务，你（程序员）只需要指挥秘书干活就行！

~~~cpp
#pragma once

#include <functional>
#include <memory>

#include "noncopyable.h"
#include "Timestamp.h"

class EventLoop;

/**
 * 理清楚 EventLoop、Channel、Poller之间的关系  Reactor模型上对应多路事件分发器
 * Channel理解为通道 封装了sockfd和其感兴趣的event 如EPOLLIN、EPOLLOUT事件 还绑定了poller返回的具体事件
 **/
class Channel : noncopyable
{
public:
    using EventCallback = std::function<void()>; // muduo仍使用typedef
    using ReadEventCallback = std::function<void(Timestamp)>;

    Channel(EventLoop *loop, int fd);
    ~Channel();

    // fd得到Poller通知以后 处理事件 handleEvent在EventLoop::loop()中调用
    void handleEvent(Timestamp receiveTime);

    // 设置回调函数对象
    void setReadCallback(ReadEventCallback cb) { readCallback_ = std::move(cb); }
    void setWriteCallback(EventCallback cb) { writeCallback_ = std::move(cb); }
    void setCloseCallback(EventCallback cb) { closeCallback_ = std::move(cb); }
    void setErrorCallback(EventCallback cb) { errorCallback_ = std::move(cb); }

    // 防止当channel被手动remove掉 channel还在执行回调操作
    void tie(const std::shared_ptr<void> &);

    int fd() const { return fd_; }
    int events() const { return events_; }
    void set_revents(int revt) { revents_ = revt; }

    // 设置fd相应的事件状态 相当于epoll_ctl add delete
    void enableReading() { events_ |= kReadEvent; update(); }
    void disableReading() { events_ &= ~kReadEvent; update(); }
    void enableWriting() { events_ |= kWriteEvent; update(); }
    void disableWriting() { events_ &= ~kWriteEvent; update(); }
    void disableAll() { events_ = kNoneEvent; update(); }

    // 返回fd当前的事件状态
    bool isNoneEvent() const { return events_ == kNoneEvent; }
    bool isWriting() const { return events_ & kWriteEvent; }
    bool isReading() const { return events_ & kReadEvent; }

    int index() { return index_; }
    void set_index(int idx) { index_ = idx; }

    // one loop per thread
    EventLoop *ownerLoop() { return loop_; }
    void remove();
private:

    void update();
    void handleEventWithGuard(Timestamp receiveTime);

    static const int kNoneEvent;
    static const int kReadEvent;
    static const int kWriteEvent;

    EventLoop *loop_; // 事件循环
    const int fd_;    // fd，Poller监听的对象
    int events_;      // 注册fd感兴趣的事件
    int revents_;     // Poller返回的具体发生的事件
    int index_;

    std::weak_ptr<void> tie_;
    bool tied_;

    // 因为channel通道里可获知fd最终发生的具体的事件events，所以它负责调用具体事件的回调操作
    ReadEventCallback readCallback_;
    EventCallback writeCallback_;
    EventCallback closeCallback_;
    EventCallback errorCallback_;
};
~~~

### **核心功能定位**

- **事件封装层**
  封装文件描述符（`fd_`）及其关联的事件（读/写/错误/关闭），是 **Reactor 模式**中事件分发的核心单元。
- **回调机制**
  提供四类事件回调函数（读/写/错误/关闭），实现事件触发与业务逻辑解耦。
- **生命周期管理**
  通过 `tie()` 机制绑定 `shared_ptr`，确保事件处理期间对象不被意外销毁。

### weak_ptr和shared_ptr区别

 **1. 所有权与生命周期控制**

| **类型**     | **所有权** | **影响引用计数** | **资源释放条件**             |
| ------------ | ---------- | ---------------- | ---------------------------- |
| `shared_ptr` | ✅ 强所有权 | 增加引用计数     | 所有 `shared_ptr` 销毁时释放 |
| `weak_ptr`   | ❌ 无所有权 | 不增加引用计数   | 不参与生命周期管理           |

**2. 资源访问方式**

| **操作**         | `shared_ptr`            | `weak_ptr`                              |
| ---------------- | ----------------------- | --------------------------------------- |
| **直接访问资源** | ✅ 通过 `operator*`/`->` | ❌ 不允许直接访问                        |
| **安全访问机制** | -                       | ✅ 必须调用 `lock()` 升级为 `shared_ptr` |
| **访问失败处理** | -                       | 检查 `lock()` 返回的指针是否为空        |

~~~cpp
if (auto tmp = wp.lock()) { // 升级成功则对象存活  
  std::cout << *tmp;        // 安全访问  
} else {  
  std::cout << "对象已销毁";  
}  
~~~

**智能指针的使用**情况判断：

1. **默认选择 `shared_ptr`**：需要管理资源生命周期时使用
2. **打破循环用 `weak_ptr`**：存在双向引用风险时替换单向指针
3. **回调安全必绑 `weak_ptr`**：避免异步回调时对象已销毁（如网络库 `Channel::tie` 机制）

[上述三个原则的理解](https://www.n.cn/share/r1/6fdf30c5e8a042f39409492ea5d9125d?from=web)

**weak_ptr**用处：

用`weak_ptr`绑定回调，相当于给异步操作加了个 **“对象存活检测器”**：
**“您依赖的对象已下班，本次回调服务已自动取消”**
避免强行访问已销毁对象导致的崩溃，是C++高性能程序的**安全气囊**

### using与typedef使用区别

~~~c++
using EventCallback = std::function<void()>; // muduo仍使用typedef
using ReadEventCallback = std::function<void(Timestamp)>;

//等效写法
typedef std::function<void()> EventCallback;          // 等效于 using 版本1 
typedef std::function<void(Timestamp)> ReadEventCallback; // 等效于 using 版本2 
~~~

- 代码注释 `// muduo仍使用typedef`   旧版 muduo 使用 `typedef`，但现代 C++（C++11 起）**推荐使用 `using`**。
- `using` 的优势：
  - 语法更清晰，尤其是对**函数指针**或**模板别名**。
  - 支持模板别名（`template using MyVec = std::vector;`），而 `typedef` 不支持。 

### std::function <void()>

- **实际类型**：`std::function`
- 含义：
  - 这是一个**通用事件回调函数**，不接收任何参数，也无返回值（`void`）。
  - 当某个事件（如连接关闭、定时器到期等）发生时，调用此回调函数。
- 典型应用场景：
  - **定时器**超时回调。
  - 连接关闭后的**清理操作**。
  - 其他无需**额外数据**的事件通知。

~~~c++
using EventCallback = std::function<void()>; 

EventCallback callback = []{ 
    std::cout << "Event occurred!" << std::endl; 
};
callback(); // 输出 "Event occurred!"
~~~

## Poller代码分析

**Poller**里面是muduo库中**多路事件分发器**的核心IO复用模块

**Poller** ----> **事件监听器**（专门用来观察**文件描述符**所要发生的事件）
**本职：服务员**，负责盯着**自己负责的桌子**，看哪个桌子的顾客有需求（事件），**然后报告**
核心在于**报告**（即上传自己**监听到的事件**）

### Poller中核心函数

~~~c++
 // 给所有IO复用保留统一的接口
 virtual Timestamp poll(int timeoutMs, ChannelList *activeChannels) = 0;
 virtual void updateChannel(Channel *channel) = 0;
 virtual void removeChannel(Channel *channel) = 0;
~~~

核心功能：

- `updateChannel`：**添加/修改**监听的通道事件
- `removeChannel`：**移除已监听**的通道
- 对应 **epoll_ctl** 的 ADD/MOD/DEL 操作

`virtual void updateChannel(Channel *channel) = 0;` 中的 `= 0` 语法表示这是一个**纯虚函数**

1. **抽象接口声明**
   `= 0` 表明该函数是**抽象方法**，只有声明没有实现（即无函数体）。它强制要求所有继承该类的子类**必须重写此函数**并提供具体实现。

2. **抽象类标识**
   包含纯虚函数的类自动成为**抽象基类（Abstract Base Class）**，无法直接实例化对象。例如 `Poller` 类作为抽象基类，需通过子类（如 `EPollPoller`）实现功能：

   ```cpp
   class Poller {  // 抽象基类
     virtual void updateChannel(Channel* channel) = 0;  // 纯虚函数
   };
   class EPollPoller : public Poller { 
     void updateChannel(Channel* channel) override;  // 子类必须实现 
   };
   ```

3. **多态行为基础**
   通过基类指针调用 `updateChannel()` 时，实际执行的是子类的实现，实现运行时多态。例如：

   ```cpp
   Poller* poller = new EPollPoller();  // 基类指针指向子类对象 
   poller->updateChannel(channel);      // 调用 EPollPoller 的实现 
   ```

使用纯虚函数好处：新增多路复用机制（如 kqueue）只需继承 `Poller` 并重写纯虚函数，无需修改现有代码

### 函数传参（）使用*指针

~~~c++
using ChannelList = std::vector<Channel *>;
virtual Timestamp poll(int timeoutMs, ChannelList *activeChannels) = 0;
ChannelList *activeChannels
~~~

数组传参，要想**修改传递的值**可以通过**指针或引用**来修改
所以上述代码传递的**vector<Channel *>数组**必须得要**指针**才能更改对应**里面的值**。

## EPoller代码分析

~~~cpp
class Channel;

class EPollPoller : public Poller
{
public:
    //初始化epollfd_(epoll_create)，epoll_events事件个数
    EPollPoller(EventLoop *loop);
    //关闭epollfd_操控epoll实例
    ~EPollPoller() override;

    //用来等待最终监控事件（读写or）的返回个数
    Timestamp poll(int timeoutMs, ChannelList *activeChannels) override;
    // 重写基类Poller的抽象方法
    void updateChannel(Channel *channel) override;	//用来更新CTL_ADD还是CTL_MOD
    void removeChannel(Channel *channel) override;	//用来移除Channel控制的文件描述符

private:
    static const int kInitEventListSize = 16;

    // 填写活跃的连接，也就是epoll_wait中响应的文件个数
    void fillActiveChannels(int numEvents, ChannelList *activeChannels) const;
    // 更新channel通道 其实就是调用epoll_ctl
    void update(int operation, Channel *channel);

    using EventList = std::vector<epoll_event>; // C++中可以省略struct 直接写epoll_event即可

    int epollfd_;      // epoll_create创建返回的fd保存在epollfd_中
    EventList events_; // 用于存放epoll_wait返回的所有发生的事件的文件描述符事件集
};
~~~



### epoll整个模拟流程

1. 想象你住在一个大型小区（**服务器程序**），小区里有个快递驿站（**epoll 实例**，由 `epoll_create` 创建，对应 `epfd`）。
   每家每户（**每个 Socket 连接**）的快递（**网络数据**）都会送到这个驿站。

2. `epoll_ctl(ADD)` 就像 **住户到驿站登记需求**：把自家门牌号（`sockfd`）和关注的事件（如 `EPOLLIN`）绑定到驿站的监控系统（`epfd`），之后驿站才会帮你盯快递！

3.  `epoll_wait` 就像**驿站监控值班**

   驿站保安盯着监控屏（调用`epoll_wait`），一旦发现：

   * **202住户的大件快递到了** → 系统标记“202有事件！”
   * **202住户的快递被退回** → 系统标记“202有异常！”

**通知住户取件**
保安生成一张取件条（**返回 `events` 数组**），上面写着：
`[ 门牌号：202, 事件：大件到了 ]`
你凭条就能知道：“哦！我家快递到了，该去拿了！”

 **events 数组本质区别**

| **函数**         | **events参数角色**     | **数据流向** | **内容含义**                       |
| ---------------- | ---------------------- | ------------ | ---------------------------------- |
| **`epoll_ctl`**  | 输入参数（仅用于配置） | 用户→内核    | **期望监听的事件**（如 `EPOLLIN`） |
| **`epoll_wait`** | 输出参数（存储结果）   | 内核→用户    | **实际发生的事件**（如 `EPOLLIN`） |

其中上述两个函数中的events不一样，如下图中
epoll_ctl里面的

~~~cpp
// ====== epoll_ctl 使用 ====== 
struct epoll_event ctl_event;             // 用户构造配置 
ctl_event.events = EPOLLIN | EPOLLET;     // 设置监听事件（输入）
ctl_event.data.fd = sockfd;               // 关联socket 
epoll_ctl(epfd, EPOLL_CTL_ADD, sockfd, &ctl_event); // 提交配置 
 
// ====== epoll_wait 使用 ====== 
struct epoll_event wait_events[10];       // 预分配结果数组
int n = epoll_wait(epfd, wait_events, 10, 1000); // 接收事件（输出）
for (int i=0; i<n; i++) {
    // wait_events[i].events 含实际事件（如 EPOLLIN）
    // wait_events[i].data.fd 是就绪的socket fd 
}
~~~

**核心区别：**

`epoll_ctl` 主要就是将发生的**sokct fd**和**事件类型**放入到**events数组**中。(作为后期的监控标志)

而`epoll_wait` 则是只是用来判断是否**后期的行为**是否为**events数组**里面**存储事件类型**一模一样  (作为判断标志)

### epoll_ctl分析

以下是 **Linux 系统**调用 `epoll_ctl` 的代码声明及其核心要素分析：

```c
extern int epoll_ctl (int __epfd, int __op, int __fd, struct epoll_event *__event) __THROW;
```

**返回值含义**

- **0**：操作成功（**永不返回事件数/超时**❗）
- **-1**：操作失败（检查 `errno` 如 `EBADF`/`EEXIST`）

 **核心参数解析**

| **参数**  | **类型**              | **作用说明**                                                 | **典型值示例**                  |
| --------- | --------------------- | ------------------------------------------------------------ | ------------------------------- |
| `__epfd`  | `int`                 | **epoll 实例的文件描述符**（由 `epoll_create` 创建）         | `3`（表示已打开的 epoll 实例）  |
| `__op`    | `int`                 | 操作类型：添加、修改或删除监听事件                           | `EPOLL_CTL_ADD`（添加新事件）   |
| `__fd`    | `int`                 | 需要监听的**目标文件描述符**（如 **socket对应的文件描述符**、管道等） | `4`（某个 socket 描述符）       |
| `__event` | `struct epoll_event*` | 事件配置**结构体指针**，定义监听的事件类型和回调数据         | 指向自定义 `epoll_event` 的指针 |

**操作类型 `__op` 详解**   ——>     主要用于**监控具体哪一类事件**的发生（添加，修改，还是删除）

通过**宏定义**实现三种操作：

```c
#define EPOLL_CTL_ADD 1  // 添加新监听事件 
#define EPOLL_CTL_MOD 2  // 修改已有事件 更新 已注册fd 的监听事件（如从 EPOLLIN 改为 EPOLLOUT）
#define EPOLL_CTL_DEL 3  // 删除事件监听 
EPOLL_CTL_ADD：       	// 注册新的fd到epfd中；
EPOLL_CTL_MOD：       	// 修改已经注册的fd的监听事件；
EPOLL_CTL_DEL：       	// 从epfd中删除一个fd；
```

- 示例场景：
  - **新连接**接入 → `EPOLL_CTL_ADD`
  - **修改**监听事件（如从读切换到写）→ `EPOLL_CTL_MOD`    （modify)
  - **连接**关闭 → `EPOLL_CTL_DEL`

**事件结构体 `epoll_event`**

定义于 `sys/<epoll.h>`：

```c
typedef union epoll_data {
    void    *ptr;      // 用户自定义数据指针（常用）
    int      fd;       // 关联的文件描述符 
    uint32_t u32;
    uint64_t u64;
} epoll_data_t;
 
struct epoll_event {
    uint32_t     events;  // 事件掩码（EPOLLIN/EPOLLOUT 等）
    epoll_data_t data;    // 事件触发时的回调数据 
};
```

- 关键事件掩码：**(events)   指的是epoll_event里面的成员**
  - `EPOLLIN`：数据可读
  - `EPOLLOUT`：数据可写
  - `EPOLLERR`：错误发生
  - `EPOLLET`：边缘触发模式（默认水平触发）

**实际调用示例**

添加 socket 可读事件监听：

```c
int epfd = epoll_create1(0);  // 创建 epoll 实例
struct epoll_event ev;
ev.events = EPOLLIN;         // 监听读事件
ev.data.fd = sockfd;         // 关联 socket
 
// 将 socket 加入 epoll 监听    主要处理新增监听事件
if (epoll_ctl(epfd, EPOLL_CTL_ADD, sockfd, &ev) == -1) {
    perror("epoll_ctl failed");
    exit(EXIT_FAILURE);
}
```

### epoll_create分析

其中**EPoller.h**里面的**epollfd_**就是用**epoll_create**方法返回的epoll**句柄。**

变量 `epollfd_` 存储着访问和管理你通过 `epoll_create` 创建的那个特定 **epoll 事件监听中心**  (epoll维护的内核)   的钥匙（文件描述符）。后续所有对 **epoll 的操作** (`epoll_ctl`, `epoll_wait`) 都必须通过**这把钥匙**来指定你要**操作的是哪个中心**

- `epoll_create(int __size)`
  - 参数 `__size` 是一个历史遗留的**提示值**（内核 ≥ 2.6.8 后已忽略此参数），仅用于兼容性。
  - 必须传入 **大于 0** 的值（如 `1`），否则会返回 `EINVAL` 错误。
- `epoll_create1(int __flags)`
  - 移除了无用的 `__size` 参数。
  - 新增`__flags`参数，支持设置文件描述符标志：
    - **`EPOLL_CLOEXEC`**：在 **exec 时（下方有解释）自动关闭文件描述符**（避免泄漏到子进程）
    - `FD_CLOEXEC` 标志
      - 设置方式：
        - 通过 `fcntl(fd, F_SETFD, FD_CLOEXEC)` 手动设置。
        - 或使用 **创建时标记**（如 `epoll_create1(EPOLL_CLOEXEC)`）。
      - **作用机制**：
        当进程调用 `exec()` 时，内核自动关闭所有标记 `FD_CLOEXEC` 的文件描述符，确保新程序无法访问它们。
    - 若无需标志，可传 `0`。

~~~c
int main() {
    int epfd = epoll_create1(EPOLL_CLOEXEC);  // 父进程创建epoll 
    pid_t pid = fork();                       // 创建子进程 
    
    if (pid == 0) {                           // 子进程代码块 
        execl("/bin/ls", "ls", NULL);         //  关键点：执行程序替换 
        // 此处代码不会执行（除非 exec 失败）  	 
    }
    // 父进程继续运行...
    return 0;
}
~~~

2. **功能扩展**

- `epoll_create1` **额外支持 `EPOLL_CLOEXEC` 标志**：
  在多线程/多进程编程中，此标志能防止文件描述符意外泄漏到 exec 后的子进程，提升安全性。
  *示例*：调用 `epoll_create1(EPOLL_CLOEXEC)` 后，fork+exec 时描述符自动关闭。
- `epoll_create` **无标志控制**：
  创建的文件描述符默认无 `CLOEXEC`，需手动调用 `fcntl(fd, F_SETFD, FD_CLOEXEC)` 设置。

 `exec` 函数族详解：参数传递与环境变量处理

**核心作用**：所有 `exec` 函数均用于**替换当前进程的代码和数据**为新程序，但参数传递方式和环境变量处理存在显著差异。

(简单理解：**`execl` 类函数的作用是：让当前程序“灵魂出窍”，彻底变成另一个程序，但保留它的“身体”（进程ID和资源）。**)

### epoll_wait分析

~~~cpp
extern int epoll_wait (int __epfd, struct epoll_event *__events, 
                       int __maxevents, int __timeout);
~~~

| **参数**      | **作用**                                                     | **技术细节**                                                 |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `__epfd`      | epoll 实例的文件描述符（由 `epoll_create` 创建）             | 内核通过此标识符定位事件监控池                               |
| `__events`    | 输出参数，存储就绪事件的数组                                 | 需用户预分配内存，内核填充触发事件的详细信息                 |
| `__maxevents` | 期望返回的最大事件数量                                       | 必须 ≤ `__events` 数组长度，避免缓冲区溢出                   |
| `__timeout`   | 等待超时时间（毫秒）                                         | `-1`：阻塞等待；`0`：立即返回；`>0`：最长等待时间            |
| **返回值**    | `>0`：就绪事件数；`0`：超时无事件；`-1`：错误（需检查 `errno`） | 常见错误：`EBADF`（epfd 非法）、`EINTR`（被信号中断）、`EFAULT`（缓冲区不可访问） |

**返回值**

| **返回值** | **含义**                                                     | **后续操作**                                 |
| ---------- | ------------------------------------------------------------ | -------------------------------------------- |
| **`> 0`**  | **就绪事件数量** • 表示有 `N` 个 Socket 发生监听的事件 • `N` 最大不超过传入的 `__maxevents` 参数 | 需遍历 `events[0]` 到 `events[N-1]` 处理事件 |
| **`0`**    | **超时无事件** • 在 `__timeout` 毫秒内无任何事件触发         | 可继续调用 `epoll_wait` 等待或执行其他逻辑   |
| **`-1`**   | **发生错误** • 需通过 `errno` 获取错误码                     | 必须检查 `errno` 定位问题                    |

