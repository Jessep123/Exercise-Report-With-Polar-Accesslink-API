from flask import Flask, request

app = Flask(__name__)

@app.route("/callback")
def callback():
    # This gets the authorization code from the URL
    code = request.args.get("code")
    return f"Authorization code received: {code}\nCopy this code for the next step!"

if __name__ == "__main__":
    app.run(port=8000)

    