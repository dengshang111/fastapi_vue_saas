# === 第一阶段：打包 Vue 管理后台 ===
FROM node:22-alpine AS build-admin
WORKDIR /app
# 注意路径：根据你的目录结构指向 web
COPY backend_admin/web/package*.json ./
RUN npm install
COPY backend_admin/web/ .
RUN npm run build

# === 第二阶段：打包 uni-app (H5端) ===
FROM node:22-alpine AS build-uniapp
WORKDIR /app
# 注意路径：指向 uniapp
COPY uniapp/package*.json ./
RUN npm install
COPY uniapp/ .
# 这里的构建命令根据你的 package.json 确认，通常是 build:h5
RUN npm run build:h5

# === 第三阶段：生产环境 Nginx ===
FROM nginx:alpine

# 1. 复制自定义 Nginx 配置
COPY deploy/nginx.conf /etc/nginx/nginx.conf

# 2. 复制管理后台产物到 /usr/share/nginx/html/admin
COPY --from=build-admin /app/dist /usr/share/nginx/html/admin

# 3. 复制 uni-app 产物到 /usr/share/nginx/html/mobile
# 注意：uniapp 默认构建路径通常是 dist/build/h5
COPY --from=build-uniapp /app/dist/build/h5 /usr/share/nginx/html/mobile

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]