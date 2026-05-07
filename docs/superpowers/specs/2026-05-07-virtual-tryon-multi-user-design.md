# 虚拟试衣多用户系统 — 设计文档

> 状态: 已确认 | 日期: 2026-05-07

## 目标

将当前单页 Demo 升级为支持多用户的 Web 应用：注册登录、个人照片管理、衣物库管理、智能虚拟试穿。

## 技术栈

- **后端:** Python 3.12 + Flask 3.1 + Jinja2
- **认证:** Flask-Login + Flask-Bcrypt (Session-based)
- **数据库:** SQLite + Flask-SQLAlchemy ORM
- **图像处理:** Pillow, OpenCV, MediaPipe Pose
- **深度学习:** PyTorch 2.x + FashionCNN (现有模型)
- **前端:** 无框架，CSS 自定义属性 + Vanilla JS，Google Fonts

## 架构

Flask 工厂模式 + Blueprint 模块化。按功能拆分为 auth / main / wardrobe / tryon 四个 Blueprint，数据模型独立为 models/。虚拟试穿引擎抽象为接口，MediaPipe 方案为默认实现，架构预留深度学习方案替换空间。

---

## 数据模型

### User
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增主键 |
| username | String(80) unique | 用户名，不可重复 |
| email | String(120) unique | 邮箱，不可重复 |
| password_hash | String(128) | bcrypt 哈希 |
| email_verified | Boolean | 是否已验证邮箱，默认 False |
| verification_token | String(64) | 邮箱验证 token，可空 |
| reset_token | String(64) | 密码重置 token，可空 |
| reset_token_expiry | DateTime | 重置 token 过期时间 |
| created_at | DateTime | 注册时间 |

### Photo
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增主键 |
| user_id | Integer FK→User | 所属用户 |
| filename | String(255) | 存储文件名 |
| is_active | Boolean | 是否当前试穿底图，默认 False |
| uploaded_at | DateTime | 上传时间 |

- 约束：每个用户同时只能有一个 `is_active=True` 的照片

### Clothing
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增主键 |
| user_id | Integer FK→User | 所属用户 |
| filename | String(255) | 存储文件名 |
| category | String(50) | CNN 自动分类结果 |
| manual_category | String(50) | 用户手动修正的分类，可空 |
| uploaded_at | DateTime | 上传时间 |

- `display_category` 逻辑：`manual_category or category`

---

## 路由设计

### auth Blueprint (`/`)
| 路由 | 方法 | 说明 | 登录要求 |
|------|------|------|----------|
| /login | GET, POST | 登录 | 否 |
| /register | GET, POST | 注册 | 否 |
| /logout | GET | 退出登录 | 是 |
| /verify/<token> | GET | 邮箱验证 | 否 |
| /reset-password | GET, POST | 密码重置请求 | 否 |

### main Blueprint (`/`)
| 路由 | 方法 | 说明 | 登录要求 |
|------|------|------|----------|
| / | GET | 试穿主页 | 是 |
| /upload-photo | POST | 上传个人照片 | 是 |
| /set-photo/<id> | POST | 设为当前试穿底图 | 是 |
| /delete-photo/<id> | POST | 删除个人照片 | 是 |

### wardrobe Blueprint (`/wardrobe`)
| 路由 | 方法 | 说明 | 登录要求 |
|------|------|------|----------|
| /wardrobe | GET | 衣橱列表页 | 是 |
| /wardrobe/upload | POST | 上传衣物（触发 CNN 分类） | 是 |
| /wardrobe/<id>/edit | POST | 修改衣物分类 | 是 |
| /wardrobe/<id>/delete | POST | 删除衣物 | 是 |

### tryon Blueprint
| 路由 | 方法 | 说明 | 登录要求 |
|------|------|------|----------|
| /tryon/<clothing_id> | POST | 对指定衣物执行虚拟试穿 | 是 |

---

## 虚拟试穿引擎

### 接口
```python
class TryOnEngine(ABC):
    @abstractmethod
    def composite(self, user_photo: Image.Image, clothing: Image.Image,
                  category: str) -> Image.Image:
        """返回合成后的 RGBA 图片"""
```

### 实现

**SimpleEngine** — 保留现有 `region_mapping` 固定坐标逻辑，作为回退方案。

**MediaPipeEngine** — 使用 MediaPipe Pose 检测 33 个身体关键点，根据关键点动态计算衣物区域：
1. 肩部中点（11-12 关键点）→ 上衣上边界
2. 髋部（23-24 关键点）→ 上下衣分界
3. 踝部（27-28 关键点）→ 鞋区域
4. 对衣物图片做 `cv2.getAffineTransform` 适配目标区域
5. Alpha 合成到用户照片

引擎通过 Flask 配置项切换，默认使用 `MediaPipeEngine`。

---

## 前端页面

### base.html — 公共布局
- 导航栏：Logo + 试穿/衣橱 链接 + 用户下拉（我的照片/退出）
- Google Fonts: Playfair Display + DM Sans
- 保持现有的 CSS 设计系统 token

### login.html / register.html / reset_password.html
- 居中卡片式表单
- 表单验证反馈（Flask flash 消息）
- 链接互相跳转

### index.html（改造现有）
- 保留现有设计风格
- 上传区域拆分为两个 tab：上传照片 / 上传衣物
- 用户照片选择器：显示已上传的照片缩略图，点击切换
- 衣物选择器：从衣橱加载缩略图列表，点击选中
- "立即试衣"按钮 → POST /tryon/<clothing_id>
- 结果显示区保留

### wardrobe.html — 衣橱管理
- 衣物卡片网格展示
- 每张卡片显示：缩略图、分类标签、编辑/删除按钮
- 分类编辑为下拉选择（10 个 FashionMNIST 类别）
- 上传按钮触发 CNN 自动分类

---

## 邮件

开发阶段使用 Python `smtpd` 调试服务器或直接打印验证链接到控制台，不对接真实 SMTP。

---

## 安全约束

- 密码 bcrypt 哈希存储
- 所有表单 CSRF 保护（Flask-WTF 或手动 token）
- 文件上传仅允许 image/* MIME 类型
- 用户只能访问自己的照片和衣物（user_id 过滤）
- Session cookie 设置 `http_only=True`
- SQLAlchemy 参数化查询（防注入）

---

## 不包含的内容

- 生产级 SMTP 邮件服务
- 管理员后台
- 社交功能（分享/评论）
- 真实深度学习人体解析（仅做 MediaPipe 方案，预留接口）
