var socketio = io();

	const messages = document.getElementById("messages");

	const createMessage = (name, msg, time) => {
		const content = `
			<div class='text'>
				<span>
					<strong>${name}</strong>: ${msg}
				</span>
				<span class='muted'>
					${time}
				</span>
			</div>
		`;
		messages.innerHTML += content;
	};

	socketio.on("message", (data) => {
		createMessage(data.name, data.message, data.date);
	});
	const sendMessage = () => {
		const message = document.getElementById("message");
		if (message.value === "") return;
		socketio.emit("sendingMessage", { message: message.value });
		message.value = "";
	};

	document.getElementById("message").addEventListener("keyup", (event) => {
		if (event.keyCode === 13) {
			event.preventDefault();
			document.getElementById("send-btn").click();
		}
	});


    const newPpl = document.getElementById("meet-ppl")
    const waitingLabel = document.getElementById('waiting')
    newPpl.addEventListener('click', function() {
        waitingLabel.classList.remove('hidden')
    })