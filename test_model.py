from flask import Flask, request, jsonify

from BACKEND.ibcy_engine import ask_ibcy


app = Flask(
    __name__,
    static_folder="FRONTEND",
    static_url_path=""
)


@app.route("/")
def home():

    return app.send_static_file(
        "index.html"
    )


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received."
        }), 400


    message = data.get(
        "message",
        ""
    ).strip()


    history = data.get(
        "history",
        []
    )


    if not message:

        return jsonify({
            "error": "Message cannot be empty."
        }), 400


    try:

        response = ask_ibcy(
            message,
            history
        )

        return jsonify({
            "response": response
        })


    except Exception as error:

        print("ERROR:", error)

        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":

    print()
    print("================================")
    print("        IBCY WEB SERVER")
    print("================================")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )