from flask import Flask

app = Flask(__name__)

# 公式ドキュメントのQuickStartを実践
# https://flask.palletsprojects.com/en/3.0.x/quickstart/
# 実行はflask --app hello run
# flaskコマンドが使えなかったので、アンインストール後、再インストールした
# ログイン機能を実装してみたい!

# Turorialコースできそう...
# https://flask.palletsprojects.com/en/3.0.x/tutorial/

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"