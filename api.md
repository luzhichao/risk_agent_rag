# API接口文档

## 基础信息

- **服务地址**: http://127.0.0.1:8000
- **API版本**: v1
- **认证方式**: JWT Token
- **Token位置**: 请求头 `Authorization` 字段（不需要Bearer前缀）

---

## 认证接口

### 1. 用户注册

```
POST /api/v1/system/register
Content-Type: application/json
```

**请求体**:
```json
{
  "user_name": "testuser001",
  "phone": "13800138001",
  "email": "test001@example.com",
  "user_password": "Test123456"
}
```

**字段说明**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_name | string | 是 | 用户名(2-20位,仅英文字母和数字) |
| phone | string | 是 | 手机号(11位) |
| email | string | 是 | 邮箱 |
| user_password | string | 是 | 密码(6-20位) |

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "注册成功",
  "data": true
}
```

**失败响应**:
```json
{
  "status_code": 500,
  "msg": "用户名已存在",
  "data": null
}
```

---

### 2. 用户登录

```
POST /api/v1/system/login
Content-Type: application/json
```

**请求体**:
```json
{
  "user_name": "testuser001",
  "user_password": "Test123456"
}
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "登录成功",
  "data": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**失败响应**:
```json
{
  "status_code": 500,
  "msg": "账号或密码错误",
  "data": null
}
```

---

### 3. 获取用户信息

```
POST /api/v1/system/get_user_info
Authorization: {token}
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "操作成功",
  "data": {
    "user_id": 312387289013686272,
    "user_name": "testuser001"
  }
}
```

---

## 会话管理接口

### 4. 创建会话

```
POST /api/v1/session/create
Authorization: {token}
Content-Type: application/json
```

**请求体**: (string类型，纯文本)
```
安全隐患识别测试会话
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "会话创建成功",
  "data": "312389799828918272"
}
```

返回的 `data` 为会话ID (session_id)

---

### 5. 获取会话列表

```
POST /api/v1/session/list_user_sessions
Authorization: {token}
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "查询成功",
  "data": [
    {
      "session_id": "312389477584736256",
      "session_name": "安全隐患识别测试会话",
      "user_id": "312387289013686272"
    }
  ]
}
```

---

### 6. 更新会话标题

```
POST /api/v1/session/update
Authorization: {token}
Content-Type: application/json
```

**请求体**:
```json
{
  "session_id": "312389799828918272",
  "session_name": "新会话标题"
}
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "会话创建成功",
  "data": null
}
```

---

### 7. 获取会话历史

```
POST /api/v1/session/session_history
Authorization: {token}
Content-Type: application/json
```

**请求体**: (string类型，纯文本)
```
312389799828918272
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "查询成功",
  "data": [
    {
      "type": "human",
      "content": "Here is a summary of the conversation to date:\n\n## SESSION INTENT\n用户指出开放水域未设置护栏..."
    },
    {
      "type": "ai",
      "content": "{\n  \"name\": \"开放水域未设置护栏\",\n  \"sources\": [],\n  \"description\": \"开放水域未设置护栏，存在潜在溺水等安全事故风险。\",\n  \"according\": \"\",\n  \"solution\": \"\",\n  \"risk_type\": \"水灾\",\n  \"risk_level\": \"\",\n  \"risk_status\": \"\"\n}"
    }
  ]
}
```

---

### 8. 清空会话历史

```
DELETE /api/v1/session/clear_session_history
Authorization: {token}
Content-Type: application/json
```

**请求体**: (string类型，纯文本)
```
312389799828918272
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "清空成功",
  "data": null
}
```

---

## 智能问答接口

### 9. 发送问答消息

```
POST /api/v1/chat/ask
Authorization: {token}
Content-Type: application/json
```

**请求体**:
```json
{
  "session_id": "312389799828918272",
  "question": "开放水域未设置护栏",
  "image_urls": []
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| session_id | string | 是 | 会话ID |
| question | string | 是 | 问题内容 |
| image_urls | array | 否 | 图片URL列表 |

**响应**: 流式输出 (Server-Sent Events)

```
{"type": "think", "content": "## SESSION INTENT\n用户指出..."}
{"type": "output", "content": "{\n  \"name\": \"开放水域未设置护栏\",\n  \"sources\": [],\n  \"description\": \"开放水域未设置护栏，存在潜在溺水等安全事故风险。\",\n  \"according\": \"\",\n  \"solution\": \"\",\n  \"risk_type\": \"水灾\",\n  \"risk_level\": \"\",\n  \"risk_status\": \"\"\n}"}
```

---

## 文件上传接口

### 10. 上传风险图片

```
POST /api/v1/file/upload_risk_images
Authorization: {token}
Content-Type: multipart/form-data
```

**表单字段**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| files | File | 是 | 图片文件(支持jpg/png/jpeg) |

**限制**:
- 支持格式: jpg, png, jpeg
- 单文件最大: 5MB

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "上传成功",
  "data": [
    "https://k.sinaimg.cn/n/sinakd20260430s/405/w1080h925/20260430/9d08-8ede80edcd105e1d348a8073c097f9d8.jpg/w700d1q75cms.jpg",
    "https://q7.itc.cn/q_70/images03/20240617/e687d738f97145ad94f4eb13d440c497.jpeg"
  ]
}
```

**失败响应** (不支持的文件类型):
```json
{
  "status_code": 400,
  "msg": "不支持的文件类型。支持: {'image/jpeg': '.jpeg', 'image/png': '.png', 'image/jpg': '.jpg'}",
  "data": null
}
```

**失败响应** (无文件):
```json
{
  "status_code": 422,
  "detail": [{"type": "missing", "loc": ["body", "files"], "msg": "Field required", "input": null}]
}
```

---

### 11. 上传知识文档

```
POST /api/v1/file/upload_knowledge
Authorization: {token}
Content-Type: multipart/form-data
```

**表单字段**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | File | 是 | 文档文件 |

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "上传成功",
  "data": {
    "file_name": "test.md",
    "path": "",
    "url": "",
    "type": "md"
  }
}
```

---

## 知识库接口

### 12. 查询知识库列表

```
POST /api/v1/knowledge/list
Authorization: {token}
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "查询成功",
  "data": [
    {
      "doc_id": "",
      "knowledge_name": "",
      "type": "",
      "status": "",
      "path": "",
      "url": ""
    }
  ]
}
```

---

### 13. 新增知识库信息

```
POST /api/v1/knowledge/creat
Authorization: {token}
Content-Type: application/json
```

**请求体**:
```json
{
  "knowledge_name": "安全生产法",
  "type": "法律",
  "content": "..."
}
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "保存成功",
  "data": null
}
```

---

### 14. 更新知识库信息

```
POST /api/v1/knowledge/update
Authorization: {token}
Content-Type: application/json
```

**请求体**:
```json
{
  "doc_id": "文档ID",
  "knowledge_name": "新名称",
  "type": "法律",
  "content": "..."
}
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "更新成功",
  "data": null
}
```

---

### 15. 删除知识库信息

```
DELETE /api/v1/knowledge/delete
Authorization: {token}
Content-Type: application/json
```

**请求体**:
```json
{
  "doc_id": "文档ID"
}
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "删除成功",
  "data": null
}
```

---

### 16. 知识分块存储

```
POST /api/v1/knowledge/embedding
Authorization: {token}
Content-Type: application/json
```

**请求体**:
```json
{
  "doc_id": "文档ID"
}
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "知识库构建成功",
  "data": null
}
```

---

## 系统接口

### 17. 健康检查

```
GET /health
```

**成功响应**:
```json
{
  "status_code": 200,
  "msg": "操作成功",
  "data": "v1"
}
```

---

## 业务流程测试

### 完整问答流程

```bash
# 1. 登录获取Token
TOKEN=$(curl -s -X POST "http://127.0.0.1:8000/api/v1/system/login" \
  -H "Content-Type: application/json" \
  -d '{"user_name":"testuser001","user_password":"Test123456"}' | grep -o '"data":"[^"]*"' | cut -d'"' -f4)

# 2. 创建会话
SESSION_ID=$(curl -s -X POST "http://127.0.0.1:8000/api/v1/session/create" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '"安全隐患识别会话"' | grep -o '"data":"[^"]*"' | cut -d'"' -f4)

# 3. 发送问答
curl -s -X POST "http://127.0.0.1:8000/api/v1/chat/ask" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"$SESSION_ID\",\"question\":\"开放水域未设置护栏\"}"

# 4. 获取会话列表
curl -s -X POST "http://127.0.0.1:8000/api/v1/session/list_user_sessions" \
  -H "Authorization: $TOKEN"

# 5. 获取会话历史
curl -s -X POST "http://127.0.0.1:8000/api/v1/session/session_history" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "\"$SESSION_ID\""
```

---

## 错误码说明

| status_code | 说明 |
|-------------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权/登录失效 |
| 422 | 请求体验证失败 |
| 500 | 服务器内部错误 |

---

## 注意事项

1. **Token过期**: Token默认7天过期，过期后需重新登录
2. **会话历史参数**: `session_history` 和 `clear_session_history` 接口的Body参数为纯文本字符串，不是JSON对象
3. **流式响应**: 智能问答接口返回流式数据，需逐步解析
4. **图片上传**: 当前返回为测试图片URL，非实际上传结果
