function createMessage(float_direction, color, message) {
    const container = document.querySelector("#chat-box");
    
    const flexDiv = document.createElement('div');
    flexDiv.classList.add('flex', 'items-end', 'mb-4', 'clear-both', float_direction);

    const nestedDiv = document.createElement('div');
    nestedDiv.classList.add(color, 'rounded-l-lg', 'rounded-tr-lg', 'px-4', 'py-2', 'text-white');

    const paragraph = document.createElement('p');
    paragraph.textContent = message;

    nestedDiv.appendChild(paragraph);
    flexDiv.appendChild(nestedDiv);
    container.appendChild(flexDiv);
}

export function addChatOption(object, user_id, name) {
    object.addEventListener('click', async () => {
        let id = Number(document.querySelector('#user_id').innerHTML);
        let receiver = user_id;
        await fetch(`/api/messages/${Number(receiver)}`)
        .then(response => response.json())
        .then(data => {
            const socket = new WebSocket(
                'ws://'
                + window.location.host
                + '/ws/chat/'
                + Number(receiver)
                + '/'
            );

            const up_part = document.querySelector('#chat-user');
            const ball_status = object.querySelector('p');
            up_part.innerHTML = ball_status.innerHTML;

            JSON.parse(data).forEach(message => {
                if(message.sender === receiver){
                    createMessage('float-left', 'bg-yellow-500', message.message);
                }else{
                    createMessage('float-right', 'bg-blue-500', message.message);
                }
            })

            socket.onopen = function(e) {
                console.log("CONNECTION ESTABLISHED");
            }

            socket.onclose = function(e) {
                console.log("CONNECTION LOST");
            }

            socket.onerror = function(e) {
                console.log("ERROR OCCURED");
            }

            socket.onmessage = function(e){
                const data = JSON.parse(e.data);
                if(data.user == id){
                    createMessage('float-right', 'bg-blue-500', data.message);
                }else{
                    createMessage('float-left', 'bg-yellow-500', data.message);
                }

                docu
            }

            const message_input = document.querySelector('#message-input');
            console.log(message_input);

            document.querySelector('#message-input-confirm').onclick = function(e){
                const message = message_input.value;

                socket.send(JSON.stringify({
                    'message': message,
                    'user': id,
                    'receiver': receiver
                }));

                message_input.value = '';
            }

            message_input.addEventListener('keyup', function(event) {
                if (event.key === 'Enter') {
                    
                    event.preventDefault();
                    
                    const message = message_input.value.trim();

                    if(message !== ''){
                            socket.send(JSON.stringify({
                                'message': message,
                                'user': id,
                                'receiver': receiver
                            }))

                            message_input.value = '';
                    }
                }
            });
        })
    })
}