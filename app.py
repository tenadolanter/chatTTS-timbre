from utils import Utils
from utils.config import ROOT_DIR, WEB_ADDRESS, NAME, VERSION, LOGS_DIR
from flask import Flask, request, render_template, send_from_directory, make_response
from waitress import serve
import threading
import os
import datetime
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

# 配置日志
logLeve = logging.INFO
log = logging.getLogger("werkzeug")
log.handlers[:] = []
log.setLevel(logLeve)
root_log = logging.getLogger()
root_log.handlers = []
root_log.setLevel(logLeve)
file_handler = RotatingFileHandler(
    LOGS_DIR + f'/{datetime.datetime.now().strftime("%Y%m%d")}.log',
    maxBytes=1024 * 1024,
    backupCount=5,
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setLevel(logLeve)
file_handler.setFormatter(formatter)

app = Flask(
    __name__,
    static_folder=ROOT_DIR + "/static",
    static_url_path="/static",
    template_folder=ROOT_DIR + "/templates",
)
app.debug = True
app.use_reloader = True
# 调用日志
app.logger.setLevel(logLeve)
app.logger.addHandler(file_handler)
app.jinja_env.globals.update(enumerate=enumerate)


@app.route("/")
def index():
    return render_template("index.html", weburl=WEB_ADDRESS, name=NAME, version=VERSION)


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio_file" not in request.files:
        app.logger.warning("No audio file uploaded")
        return "No audio file uploaded", 400
    audio_file = request.files["audio_file"]
    if audio_file.filename == "":
        app.logger.warning("No audio file selected")
        return "No audio file selected", 400
    app.logger.info(f"[upload]{audio_file=}\n")
    try:
        # 创建 uploads 目录(如果不存在)
        uploads_dir = os.path.join(app.root_path, "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        # 保存上传的音频文件
        audio_path = os.path.join(app.root_path, "uploads", audio_file.filename)
        audio_file.save(audio_path)
        response = make_response(audio_path)
        response.headers["Content-Type"] = "text/plain"
        return response
    except Exception as e:
        print(f"Error: {e}")
        app.logger.error(f"Error upload timbre: {e}")
        return str(e), 500


@app.route("/generate", methods=["POST"])
def convert_audio():
    if "fileUrl" not in request.form:
        app.logger.warning("No audio file")
        return "No audio file", 400
    audio_path = request.form["fileUrl"]
    type = request.form["type"]
    app.logger.info(f"[generate]{audio_path=}\n{type=}\n")
    try:
        # 调用 Utils 中的方法进行音频转换
        timbre_path = Utils.generate_timbre(audio_path, type)
        # 构建包含本地主机地址的文件路径
        local_host = WEB_ADDRESS.lstrip("//")
        relative_path = os.path.relpath(timbre_path, ROOT_DIR)
        file_url = f"http://{local_host}/{relative_path}"
        response = make_response(file_url)
        response.headers["Content-Type"] = "text/plain"
        return response
    except Exception as e:
        print(f"Error: {e}")
        app.logger.error(f"Error generating timbre: {e}")
        return str(e), 500


try:
    host = WEB_ADDRESS.split(":")
    print(f"启动:{WEB_ADDRESS}")
    threading.Thread(target=Utils.openweb, args=(f"http://{WEB_ADDRESS}",)).start()
    serve(app, host=host[0], port=int(host[1]))
except Exception as e:
    print(e)
