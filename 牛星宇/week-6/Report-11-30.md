# 「众生之门」Unity Netcode 联机开发学习笔记周报
**核心主题**：「众生之门」项目局域网联机功能全流程开发（角色物理系统+多角色选择+联机通信）  
**适用场景**：3D多人联机游戏（局域网探测+角色操控+多角色切换）  
**技术栈**：Unity + Netcode for GameObjects（NGO）+ UDP广播 + 物理引擎  

## 一、开发背景与核心目标
### 1. 项目需求
- 核心功能：局域网内主机创建、客户端搜索连接、3种角色选择、角色移动/跳跃物理交互
- 关键要求：无角色半埋、跳跃正常（不上浮不卡顿）、多客户端稳定联机、角色正确生成

### 2. 基础环境配置
| 组件/工具 | 版本要求 | 核心作用 |
|----------|----------|----------|
| Unity | 2022 LTS 及以上 | 项目开发主引擎 |
| Netcode for GameObjects（NGO） | 1.8.x 稳定版 | 联机核心框架（角色同步、网络通信） |
| Unity Transport | 内置配套组件 | 网络传输层（端口管理、IP配置） |
| 物理组件 | CapsuleCollider + Rigidbody | 角色碰撞检测与物理运动 |

## 二、核心知识点拆解
### 模块1：角色物理系统（移动/跳跃/防半埋）
#### 1. 核心组件配置（必选参数）
| 组件 | 关键参数 | 配置原因 |
|------|----------|----------|
| CapsuleCollider | Radius=0.3、Height=1.5、Center=(0,0,0) | 避免半埋：中心Y=0让碰撞体底部贴合地形；尺寸适配角色模型 |
| Rigidbody | Use Gravity=true、Freeze Rotation(X/Y/Z)=true | 重力平衡跳跃力；防止角色旋转导致视角混乱 |
| PlayerController | moveSpeed=5f、jumpForce=3.5f、gravity=9.81f | 物理参数平衡：跳跃力与重力匹配，避免上浮/无法落地 |

#### 2. 关键逻辑实现
- **地面检测（跳跃触发前提）**：
  射线起点需匹配碰撞体位置（Center.Y=0时，起点=角色原点 - 碰撞体高度/2 + 0.1f），射线长度0.2f，仅检测Terrain层。
  ```csharp
  Vector3 rayStart = new Vector3(transform.position.x, transform.position.y - (capsuleCollider.height/2) + 0.1f, transform.position.z);
  isGrounded = Physics.Raycast(rayStart, Vector3.down, 0.2f, terrainLayerMask);
  ```
- **跳跃逻辑**：仅在`isGrounded=true`时触发，使用`ForceMode.Impulse`瞬间力，避免持续受力。
- **防半埋初始化**：SpawnPoint的Y坐标设为「地形高度+1.0f」，或代码强制抬高初始位置：
  ```csharp
  transform.position = new Vector3(transform.position.x, 1.0f, transform.position.z); // 地形Y=0时
  ```

### 模块2：Netcode 联机核心配置
#### 1. 核心组件（NetworkManager）必配项
| 配置项 | 正确设置 | 错误后果 |
|--------|----------|----------|
| Player Prefab | 设为None | 多角色场景下默认生成单个角色，冲突报错 |
| Network Prefabs Lists | 添加所有3种角色预制体 | 角色无法网络生成，客户端看不到其他玩家 |
| Unity Transport | 端口=7777（与广播端口区分） | 端口冲突，联机失败 |
| Connection Approval | response.Approved=true、CreatePlayerObject=false | 客户端被拒绝连接，或自动生成默认角色 |

#### 2. 角色预制体网络要求（必满足）
1. 根对象必须挂载`NetworkObject`组件（NGO识别网络预制体的唯一标识）；
2. 预制体需保存在「项目面板」（场景对象无法注册）；
3. 角色控制脚本需继承`NetworkBehaviour`（而非`MonoBehaviour`），确保网络同步；
4. 所有预制体需通过「编辑器手动添加」或「代码注册」到NetworkManager。

#### 3. 代码注册预制体（解决拖拽失败问题）
适配所有NGO版本的通用注册脚本，需在启动主机/客户端前调用：
```csharp
public class NetworkPrefabRegistry : MonoBehaviour
{
    public GameObject[] characterPrefabs; // 拖拽3种角色预制体
    public void RegisterBeforeStart()
    {
        if (NetworkManager.Singleton == null) return;
        foreach (var prefab in characterPrefabs)
        {
            if (prefab.GetComponent<NetworkObject>() != null)
                NetworkManager.Singleton.AddNetworkPrefab(prefab);
        }
    }
}
```

### 模块3：多角色选择联机实现
#### 1. 核心原理
- 客户端选择角色后，通过`ServerRpc`将选择索引同步到服务端；
- 服务端根据索引生成对应角色，并通过`SpawnAsPlayerObject(clientId)`绑定到客户端；
- 关键：服务端统一生成角色，确保所有客户端视角同步。

#### 2. 关键代码片段
```csharp
public class CharacterSelectManager : NetworkBehaviour
{
    public GameObject[] characterPrefabs; // 3种角色预制体
    private int selectedIndex = 0;

    // 客户端选择角色（UI调用）
    public void SelectCharacter(int index) => selectedIndex = index;

    // 客户端确认选择，发送RPC到服务端
    public void ConfirmSelection() => GenerateCharacterServerRpc(selectedIndex);

    // 服务端生成角色
    [ServerRpc(RequireOwnership = false)]
    private void GenerateCharacterServerRpc(int index, ServerRpcParams rpcParams)
    {
        ulong clientId = rpcParams.Receive.SenderClientId;
        Vector3 spawnPos = GameObject.Find("SpawnPoint").transform.position;
        GameObject character = Instantiate(characterPrefabs[index], spawnPos, Quaternion.identity);
        character.GetComponent<NetworkObject>().SpawnAsPlayerObject(clientId);
    }
}
```

### 模块4：局域网发现（LANDiscovery）
#### 1. 核心逻辑
- 主机：启动后通过UDP广播（端口7778）发送「密钥+IP+游戏端口（7777）」；
- 客户端：监听UDP广播，验证密钥后收集主机IP，去重后供用户选择；
- 关键：避免广播与游戏端口冲突，添加线程安全与异常处理。

#### 2. 避坑要点
- 广播前检查`NetworkManager.Singleton`是否初始化，避免空引用；
- 委托绑定需适配NGO版本（`OnServerStarted`需接收`bool`参数）；
- 关闭防火墙或放行7777/7778端口，否则广播无法接收。

### 模块5：联机流程控制（NGOLANManager）
串联UI面板与网络逻辑，核心流程：
1. 主菜单 → 点击「局域网联机」→ 显示联机面板；
2. 主机：点击「创建主机」→ 注册预制体 → 启动主机 → 角色选择 → 加载游戏场景；
3. 客户端：点击「加入游戏」→ 搜索主机 → 注册预制体 → 连接主机 → 角色选择 → 同步场景。

## 三、高频问题排查汇总
### 1. 编译错误（代码层面）
| 错误代码 | 错误描述 | 根本原因 | 解决方案 |
|----------|----------|----------|----------|
| CS1061 | “NetworkManager”未包含“AddNetworkPrefab”的定义 | NGO版本API差异 | 改用`NetworkManager.Singleton.AddNetworkPrefab`，移除`NetworkConfig`相关调用 |
| CS0246 | 未能找到“NetworkPrefabInfo” | 低版本NGO无该类型 | 放弃该类型，使用直接注册预制体方法 |
| CS1503 | 无法从“NetworkObject”转换为“GameObject” | 参数类型错误 | 传入预制体对象（GameObject），而非NetworkObject组件 |
| CS0117 | “NetworkManager”未包含“OnNetworkManagerCreated”的定义 | 该事件在低版本不存在 | 改用延迟检查（Update中验证`NetworkManager.Singleton`是否为空） |
| CS1593 | 委托“Action<bool>”未采用0个参数 | 委托签名不匹配 | 回调方法添加`bool`参数（如`OnServerStarted(bool success)`） |

### 2. 运行时错误（功能层面）
| 问题现象 | 常见原因 | 排查步骤 |
|----------|----------|----------|
| 角色半埋进地形 | 碰撞体位置与地形重叠；SpawnPointY坐标过低 | 1. 调整CapsuleCollider.Center=(0,0,0)；2. 抬高SpawnPointY=1.0f；3. 代码强制上移初始位置 |
| 跳跃后持续上浮 | 重力未启用；跳跃力过大 | 1. 勾选Rigidbody.UseGravity；2. 降低jumpForce=3.5f；3. 移除手动添加的额外重力 |
| 无法跳跃 | 地面检测射线未命中地形 | 1. 用`Debug.DrawRay`可视化射线；2. 调整射线起点/长度匹配碰撞体；3. 检查Terrain层是否正确 |
| 客户端无法发现主机 | UDP广播被拦截；广播逻辑未执行 | 1. 关闭防火墙；2. 验证`isHost`状态为true；3. 检查广播端口7778是否占用 |
| 客户端连接失败 | IP配置错误；预制体未注册 | 1. 客户端填写服务端局域网IP（非127.0.0.1）；2. 确认`NetworkPrefabRegistry`已调用；3. 检查NetworkManager的NetworkPrefabs是否包含所有角色 |
| 空引用异常（LANDiscovery） | `NetworkManager.Singleton`未初始化 | 1. 访问前加null检查；2. 延迟初始化逻辑；3. 确保NetworkManager在场景中存在 |

## 四、开发流程规范（避坑关键）
1. **预制体制作流程**：
   场景中创建角色 → 添加CapsuleCollider/Rigidbody/NetworkObject → 调整参数 → 拖到项目面板生成预制体 → 注册到NetworkManager。
2. **联机启动流程**：
   初始化NetworkManager → 注册预制体 → 启动主机/客户端 → 角色选择 → 服务端生成角色 → 加载游戏场景。
3. **调试技巧**：
   - 物理问题：用`Debug.DrawRay`可视化地面检测；
   - 网络问题：打印`isHost`、`isGrounded`、`DiscoveredHosts`等状态；
   - 预制体问题：检查`NetworkObject`是否在根对象，是否已注册。

## 五、核心开发经验总结
1. **版本兼容性优先**：NGO不同版本API差异大，优先使用通用基础API（如`AddNetworkPrefab`），避免高版本特有功能。
2. **物理与网络分离**：角色物理逻辑（移动/跳跃）在客户端执行，角色生成/同步由服务端控制，确保一致性。
3. **空值检查无处不在**：访问`NetworkManager.Singleton`、预制体、组件前必须加null判断，避免空引用崩溃。
4. **多角色核心原则**：清空默认PlayerPrefab，通过服务端RPC生成角色，确保所有客户端同步角色信息。
5. **网络环境排查**：联机失败先查防火墙/端口，再查IP配置，最后查预制体注册，按优先级排查。

## 六、后续优化计划
1. 角色状态同步：实现血量、道具等网络变量同步（`NetworkVariable`）；
2. 断线重连：添加断线检测与自动重连逻辑；
3. 广播优化：增加广播频率控制，避免网络拥堵；
4. 多客户端测试：验证3+客户端同时联机的稳定性；
5. 错误提示UI：将控制台日志转化为游戏内UI提示，提升用户体验。