const chat = document.getElementById("chat");

const input = document.getElementById(
    "messageInput"
);

const sendButton = document.getElementById(
    "sendButton"
);

const loading = document.getElementById(
    "loading"
);


let history = [];


function addMessage(
    sender,
    text,
    type
) {

    const message =
        document.createElement("div");

    message.className =
        "message " + type;


    const senderElement =
        document.createElement("div");

    senderElement.className =
        "sender";

    senderElement.textContent =
        sender;


    const bubble =
        document.createElement("div");

    bubble.className =
        "bubble";

    bubble.textContent =
        text;


    message.appendChild(
        senderElement
    );

    message.appendChild(
        bubble
    );


    chat.appendChild(
        message
    );


    chat.scrollTop =
        chat.scrollHeight;
}


async function sendMessage() {

    const message =
        input.value.trim();


    if (!message) {
        return;
    }


    addMessage(
        "You",
        message,
        "user"
    );


    input.value = "";

    input.disabled = true;

    sendButton.disabled = true;

    loading.classList.remove(
        "hidden"
    );


    try {

        const response =
            await fetch(
                "/api/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message,
                        history: history
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Server error"
            );
        }


        const answer =
            data.response;


        addMessage(
            "IBCY",
            answer,
            "bot"
        );


        history.push({
            role: "user",
            content: message
        });


        history.push({
            role: "assistant",
            content: answer
        });


    } catch (error) {

        addMessage(
            "System",
            "Error: " + error.message,
            "bot"
        );

    } finally {

        input.disabled = false;

        sendButton.disabled = false;

        loading.classList.add(
            "hidden"
        );

        input.focus();
    }
}


sendButton.addEventListener(
    "click",
    sendMessage
);


input.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);