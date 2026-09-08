# -*- coding: utf-8 -*-
"""
脚本名称: file_station_server.py (高并发极速传输优化版)
功能说明:
  Class-Widgets-2 官方最新发布与文件存放站
  性能优化:
    1. 升级为 ThreadedHTTPServer 多线程高并发架构，支持多用户、多线程并发下载;
    2. 开启 TCP_NODELAY，禁用 Nagle 算法，降低网络往返延迟;
    3. 暴力扩展 SO_SNDBUF 至 4MB (原系统默认仅 64KB)，彻底打破公网 BDP 窗口 500KB/s 瓶颈;
    4. 增大分块流式读取至 1MB，极大降低 CPU 切换开销与 I/O 阻塞;
    5. 完美适配 Range 响应，支持 IDM、ADM、迅雷等 8~16 线程并发拉满百兆上行宽带。
"""

import os
import sys
import json
import time
import socket
import socketserver
import shutil
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 19999
HOST = "0.0.0.0"
LAN_IP = "192.168.48.156"
WAN_IP = "223.72.8.19"

BASE_DIR = r"d:\PYTHON\classwiget"
STORAGE_DIR = os.path.join(BASE_DIR, "release_station", "files")
os.makedirs(STORAGE_DIR, exist_ok=True)


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def server_bind(self):
        super().server_bind()
        try:
            # 暴力调大发送缓冲区为 4MB (原 64KB，翻 64 倍)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4 * 1024 * 1024)
            # 禁用 Nagle 算法，有数据立即发送，彻底消除延迟等待
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except Exception as e:
            print("Socket tuning warning:", e)


def format_size(size_bytes):
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    elif size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} B"


def get_file_category(name):
    name_l = name.lower()
    if name_l.endswith(".zip") or name_l.endswith(".exe"):
        return ("核心软件包", "software", "#10B981")
    elif name_l.endswith(".docx") or name_l.endswith(".md") or name_l.endswith(".pdf"):
        return ("开发手册与规范", "document", "#3B82F6")
    elif name_l.endswith(".png") or name_l.endswith(".jpg") or name_l.endswith(".svg"):
        return ("4K 超清架构图", "image", "#8B5CF6")
    elif name_l.endswith(".bat") or name_l.endswith(".cmd") or name_l.endswith(".sh"):
        return ("便捷启动工具", "tool", "#F59E0B")
    else:
        return ("其他资源", "misc", "#6B7280")


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Class-Widgets-2 官方发布与文件存放站 (极速版)</title>
  <script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>
  <style>
    :root {
      --primary: #1E40AF;
      --primary-hover: #1D4ED8;
      --bg: #F8FAFC;
      --surface: #FFFFFF;
      --border: #E2E8F0;
      --text-main: #0F172A;
      --text-muted: #64748B;
      --radius: 14px;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 6px 16px -2px rgba(0,0,0,0.07);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft YaHei", sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      padding: 30px 20px;
      line-height: 1.6;
    }
    .container {
      max-width: 1100px;
      margin: 0 auto;
    }
    header {
      background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
      color: white;
      padding: 32px 30px;
      border-radius: var(--radius);
      box-shadow: var(--shadow-md);
      margin-bottom: 20px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
    }
    .header-info h1 {
      font-size: 25px;
      font-weight: 700;
      margin-bottom: 6px;
    }
    .header-info p {
      font-size: 13.5px;
      opacity: 0.92;
    }
    .network-badge-box {
      display: flex;
      flex-direction: column;
      gap: 6px;
      background: rgba(255, 255, 255, 0.16);
      padding: 12px 18px;
      border-radius: 10px;
      backdrop-filter: blur(8px);
      font-size: 13px;
    }
    .network-badge-box span {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .speed-tip-banner {
      background: #EFF6FF;
      border: 1px solid #BFDBFE;
      color: #1E40AF;
      padding: 12px 18px;
      border-radius: var(--radius);
      margin-bottom: 20px;
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr 310px;
      gap: 22px;
    }
    @media (max-width: 850px) {
      .grid { grid-template-columns: 1fr; }
    }
    .file-card-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .file-card {
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 16px 20px;
      border-radius: var(--radius);
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s ease;
      gap: 16px;
    }
    .file-card:hover {
      box-shadow: var(--shadow-md);
      border-color: #CBD5E1;
      transform: translateY(-1px);
    }
    .file-meta {
      display: flex;
      align-items: center;
      gap: 14px;
      flex: 1;
      min-width: 0;
    }
    .file-icon {
      width: 44px;
      height: 44px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      flex-shrink: 0;
    }
    .file-details {
      min-width: 0;
      flex: 1;
    }
    .file-name {
      font-weight: 600;
      font-size: 14.5px;
      color: var(--text-main);
      word-break: break-all;
      margin-bottom: 4px;
    }
    .file-sub {
      font-size: 12px;
      color: var(--text-muted);
      display: flex;
      gap: 12px;
    }
    .tag {
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 6px;
      font-weight: 600;
    }
    .btn-actions {
      display: flex;
      gap: 8px;
      flex-shrink: 0;
    }
    .btn-download {
      background-color: var(--primary);
      color: white;
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: background 0.15s;
    }
    .btn-download:hover {
      background-color: var(--primary-hover);
    }
    .btn-copy {
      background-color: #F1F5F9;
      color: #475569;
      border: 1px solid #CBD5E1;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 12px;
      cursor: pointer;
      font-weight: 500;
    }
    .btn-copy:hover {
      background-color: #E2E8F0;
    }
    .sidebar-panel {
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .panel-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 18px;
      box-shadow: var(--shadow-sm);
    }
    .panel-card h3 {
      font-size: 14.5px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-main);
    }
    #qrcode {
      display: flex;
      justify-content: center;
      margin: 10px 0;
    }
    .upload-area {
      border: 2px dashed #CBD5E1;
      border-radius: 10px;
      padding: 18px 10px;
      text-align: center;
      cursor: pointer;
      background: #F8FAFC;
      transition: all 0.2s;
    }
    .upload-area:hover {
      border-color: var(--primary);
      background: #EFF6FF;
    }
    .upload-area input {
      display: none;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="header-info">
        <h1>Class-Widgets-2 官方发布与文件存放站</h1>
        <p>Windows 桌面课表小组件 · 免安装绿色版、源码包与 4K 超清技术手册</p>
      </div>
      <div class="network-badge-box">
        <span>🌐 <strong>局域网地址</strong>: http://__LAN_IP__:__PORT__</span>
        <span>🌍 <strong>外网公网直连</strong>: http://__WAN_IP__:__PORT__</span>
        <span>⚡ <strong>引擎状态</strong>: 多线程并发 + 4MB TCP 缓冲极速优化</span>
      </div>
    </header>

    <div class="speed-tip-banner">
      <span style="font-size: 18px;">💡</span>
      <div>
        <strong>外网提速技巧</strong>：若在公网或手机流量下下载较慢，是因为手机浏览器单线程受运营商 QoS 限速。复制下载链接使用 <strong>手机 ADM / 迅雷 / 电脑 IDM</strong> 等多线程下载工具（开 8~16 线程并发），即可瞬间跑满百兆上行宽带！
      </div>
    </div>

    <div class="grid">
      <div class="main-content">
        <h2 style="font-size: 17px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
          📦 最新发布软件与核心文档清单 (<span id="file-count">__FILE_COUNT__</span>)
        </h2>
        <div class="file-card-list">
          __FILE_CARDS__
        </div>
      </div>

      <div class="sidebar-panel">
        <div class="panel-card">
          <h3>📱 手机扫码极速下载</h3>
          <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 6px;">同一 WiFi 下手机扫码即可直接访问并极速下载：</p>
          <div id="qrcode"></div>
          <p style="font-size: 11px; text-align: center; color: var(--text-muted); word-break: break-all;">http://__LAN_IP__:__PORT__</p>
        </div>

        <div class="panel-card">
          <h3>📤 存放站文件上传</h3>
          <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">上传新版本补丁包、课表数据或说明文件：</p>
          <form id="uploadForm" action="/upload" method="post" enctype="multipart/form-data">
            <label class="upload-area" for="fileInput">
              <div style="font-size: 26px;">☁️</div>
              <div style="font-size: 13px; font-weight: 600; margin-top: 4px;">点击或拖拽文件上传</div>
              <div style="font-size: 11.5px; color: var(--text-muted); margin-top: 4px;">支持任意格式</div>
              <input type="file" id="fileInput" name="file" onchange="document.getElementById('uploadForm').submit();">
            </label>
          </form>
        </div>

        <div class="panel-card" style="font-size: 12px; color: var(--text-muted);">
          <h3 style="font-size: 14px;">⚙️ 网络与传输参数</h3>
          <p style="margin-bottom: 5px;">• TCP 发送缓冲：<strong>4096 KB (优化级)</strong></p>
          <p style="margin-bottom: 5px;">• Nagle 延迟算法：<strong>已禁用 (TCP_NODELAY)</strong></p>
          <p style="margin-bottom: 5px;">• 分块传输颗粒度：<strong>1024 KB 流式推送</strong></p>
          <p style="margin-bottom: 5px;">• 断点续传：<strong>100% 完整支持 (HTTP 206)</strong></p>
        </div>
      </div>
    </div>
  </div>

  <script>
    window.addEventListener('DOMContentLoaded', function() {
      new QRCode(document.getElementById("qrcode"), {
        text: "http://__LAN_IP__:__PORT__",
        width: 160,
        height: 160,
        colorDark: "#1E3A8A",
        colorLight: "#FFFFFF",
        correctLevel: QRCode.CorrectLevel.M
      });
    });

    function copyLink(path) {
      const fullUrl = window.location.origin + path;
      navigator.clipboard.writeText(fullUrl).then(() => {
        alert('直链已复制到剪贴板！可直接粘贴至 IDM/迅雷/ADM 进行多线程极速下载：\\n' + fullUrl);
      }).catch(() => {
        prompt('请手动复制下载直链：', fullUrl);
      });
    }
  </script>
</body>
</html>
"""


class FileStationHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # 禁用标准终端刷屏，提高高并发大文件吞吐性能

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.serve_index()
        elif path.startswith("/download/"):
            file_name = urllib.parse.unquote(path[len("/download/"):])
            self.serve_download(file_name)
        elif path == "/api/files":
            self.serve_api_files()
        else:
            file_name = urllib.parse.unquote(path.lstrip("/"))
            file_path = os.path.join(STORAGE_DIR, file_name)
            if os.path.isfile(file_path):
                self.serve_download(file_name)
            else:
                self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == "/upload":
            try:
                content_type = self.headers.get("Content-Type", "")
                content_length = int(self.headers.get("Content-Length", 0))

                if "boundary=" in content_type and content_length > 0:
                    boundary = content_type.split("boundary=")[1].strip()
                    boundary_bytes = ("--" + boundary).encode("utf-8")
                    body_bytes = self.rfile.read(content_length)
                    parts = body_bytes.split(boundary_bytes)

                    for part in parts:
                        if b"filename=" in part:
                            header_part, file_data = part.split(b"\r\n\r\n", 1)
                            if file_data.endswith(b"\r\n"):
                                file_data = file_data[:-2]
                            elif file_data.endswith(b"\r\n--"):
                                file_data = file_data[:-4]

                            fn_idx = header_part.find(b'filename="')
                            if fn_idx != -1:
                                fn_end = header_part.find(b'"', fn_idx + 10)
                                filename = header_part[fn_idx + 10:fn_end].decode("utf-8", errors="ignore")
                            else:
                                filename = f"upload_{int(time.time())}.bin"

                            target_path = os.path.join(STORAGE_DIR, filename)
                            with open(target_path, "wb") as f:
                                f.write(file_data)
                            print(f"[UPLOAD] Received: {filename} ({len(file_data)} bytes)")

                self.send_response(303)
                self.send_header("Location", "/")
                self.end_headers()
            except Exception as e:
                print("Upload processing error:", e)
                self.send_error(500, f"Upload error: {e}")
        else:
            self.send_error(405, "Method Not Allowed")

    def serve_index(self):
        files = []
        if os.path.exists(STORAGE_DIR):
            for fname in os.listdir(STORAGE_DIR):
                fpath = os.path.join(STORAGE_DIR, fname)
                if os.path.isfile(fpath):
                    st = os.stat(fpath)
                    files.append({
                        "name": fname,
                        "size": st.st_size,
                        "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))
                    })

        def sort_key(item):
            n = item["name"].lower()
            if "latest" in n: return 0
            if "source" in n: return 1
            if ".docx" in n: return 2
            if ".md" in n: return 3
            if "架构图" in n: return 4
            return 5

        files.sort(key=sort_key)

        cards_html = []
        for f in files:
            cat_label, cat_type, cat_color = get_file_category(f["name"])
            icon = "📦"
            if cat_type == "document": icon = "📄"
            elif cat_type == "image": icon = "🖼️"
            elif cat_type == "tool": icon = "🛠️"

            dl_url = f"/download/{urllib.parse.quote(f['name'])}"
            size_str = format_size(f["size"])

            card = f"""
            <div class="file-card">
              <div class="file-meta">
                <div class="file-icon" style="background: {cat_color}15; color: {cat_color};">{icon}</div>
                <div class="file-details">
                  <div class="file-name">{f['name']}</div>
                  <div class="file-sub">
                    <span class="tag" style="background: {cat_color}18; color: {cat_color};">{cat_label}</span>
                    <span>💾 {size_str}</span>
                    <span>🕒 {f['mtime']}</span>
                  </div>
                </div>
              </div>
              <div class="btn-actions">
                <button class="btn-copy" onclick="copyLink('{dl_url}')" title="复制直链至 IDM/迅雷/ADM 多线程加速">📋 复制直链</button>
                <a href="{dl_url}" class="btn-download" download>⬇️ 下载</a>
              </div>
            </div>
            """
            cards_html.append(card)

        all_cards = "\n".join(cards_html) if cards_html else "<p style='color:#666;padding:20px;'>暂无文件，可通过右侧上传。</p>"

        html = HTML_TEMPLATE.replace("__LAN_IP__", LAN_IP) \
                             .replace("__WAN_IP__", WAN_IP) \
                             .replace("__PORT__", str(PORT)) \
                             .replace("__FILE_COUNT__", str(len(files))) \
                             .replace("__FILE_CARDS__", all_cards)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def serve_download(self, file_name):
        file_path = os.path.join(STORAGE_DIR, file_name)
        if not os.path.isfile(file_path):
            self.send_error(404, "File Not Found")
            return

        file_size = os.path.getsize(file_path)
        range_header = self.headers.get("Range")

        # 针对并发连接优化 socket 参数
        try:
            self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4 * 1024 * 1024)
            self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except Exception:
            pass

        # 1. 处理断点续传与多线程 Range 请求
        if range_header:
            try:
                ranges = range_header.replace("bytes=", "").split("-")
                start = int(ranges[0]) if ranges[0] else 0
                end = int(ranges[1]) if ranges[1] else file_size - 1
                length = end - start + 1

                self.send_response(206)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                self.send_header("Content-Length", str(length))
                self.send_header("Accept-Ranges", "bytes")
                safe_name = urllib.parse.quote(file_name)
                self.send_header("Content-Disposition", f"attachment; filename*=UTF-8''{safe_name}")
                self.end_headers()

                with open(file_path, "rb") as f:
                    f.seek(start)
                    chunk_size = 1024 * 1024  # 1MB 高速块
                    bytes_left = length
                    while bytes_left > 0:
                        chunk = f.read(min(chunk_size, bytes_left))
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                        bytes_left -= len(chunk)
                return
            except (ConnectionResetError, BrokenPipeError):
                return
            except Exception as e:
                print(f"Range download error for {file_name}:", e)
                return

        # 2. 全量极速流式下载
        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", str(file_size))
        self.send_header("Accept-Ranges", "bytes")
        safe_name = urllib.parse.quote(file_name)
        self.send_header("Content-Disposition", f"attachment; filename*=UTF-8''{safe_name}")
        self.end_headers()

        try:
            with open(file_path, "rb") as f:
                chunk_size = 1024 * 1024  # 1MB 高速大块
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
        except (ConnectionResetError, BrokenPipeError):
            return
        except Exception as e:
            print(f"Stream download error for {file_name}:", e)

    def serve_api_files(self):
        files = []
        if os.path.exists(STORAGE_DIR):
            for fname in os.listdir(STORAGE_DIR):
                fpath = os.path.join(STORAGE_DIR, fname)
                if os.path.isfile(fpath):
                    st = os.stat(fpath)
                    files.append({
                        "name": fname,
                        "size": st.st_size,
                        "mtime": st.st_mtime,
                        "download_url": f"/download/{urllib.parse.quote(fname)}"
                    })
        body = json.dumps(files, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server():
    server_address = (HOST, PORT)
    httpd = ThreadedHTTPServer(server_address, FileStationHandler)
    print(f"==================================================")
    print(f" Class-Widgets-2 极速文件存放站已启动!")
    print(f" 架构: ThreadedHTTPServer (多线程并发 + 4MB 缓冲)")
    print(f" 监听地址: http://0.0.0.0:{PORT}")
    print(f" 局域网地址: http://{LAN_IP}:{PORT}")
    print(f" 路由器外网映射: http://{WAN_IP}:{PORT}")
    print(f"==================================================")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
