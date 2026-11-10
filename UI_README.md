# OrderFlow 深色工作台

本次新增原生 HTML / CSS / JavaScript 管理界面，无须 Node.js、npm、React 或额外前端服务。

## 本地运行

1. 将新版文件复制进原项目（如原项目已经有本地 `.env`，请保留原有 `.env`，不要覆盖）。
2. 安装原项目依赖：`pip install -r requirements.txt`。
3. 确保 PostgreSQL、MCP 及 LLM 等项目运行所需的服务已按原项目说明正确配置和启动。
4. 在项目根目录执行：`uvicorn main:app --reload`。
5. 打开 `http://127.0.0.1:8000/` 进入工作台；`http://127.0.0.1:8000/docs` 查看接口文档。

## 新增文件

- `static/index.html`：工作台及三个功能页面
- `static/styles.css`：深色主题、响应式布局
- `static/app.js`：调用真实后端接口和审批交互
- `main.py`：挂载静态资源、将 `/` 改为工作台首页；保留原 JSON 状态信息于 `/api/info`

## 功能与约束

- AI 智能客服：调用 `POST /chat`；如接口返回 `waiting_approval`，需通过 `POST /chat/resume` 同意或拒绝。
- 订单查询：调用 `GET /orders/{order_id}`，不制造虚假的订单数据。
- 系统连接：`GET /health` 只检查 API 健康状态，不保证外部 LLM、MCP 或数据库依赖全部可用。
- API 页面：提供 `/docs` 和 `/openapi.json` 入口。
- **注意**：原项目没有用户鉴权；切勿直接将含退款操作的服务无保护地暴露在互联网。
- 审批会话使用项目原有内存 checkpoint，服务重启或不同 worker 之间不保证能继续此前暂停的审批。

## 安全说明

为了减少敏感信息外泄，交付包已排除 `.env`、`.git` 历史和本地测试数据库、Chroma 持久化数据及缓存。`.env.example` 仍保留，填入自己的配置即可。

## 检查范围

已检查 HTML 解析、JS 语法与 Python 文件编译；未在当前环境进行真实 LangGraph / MCP / PostgreSQL 联调。
