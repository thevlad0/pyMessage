import { notify } from "./notifications.js";

const container = document.querySelector("#chat-box");
function createMessage(float_direction, color, message) {
    
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

export function blockOnPress(object) {
    let objects = document.querySelectorAll('.friendContainer li');
    objects.forEach(object => {
        object.classList.remove('bg-yellow-500');
        object.classList.add('bg-blue-500');
        object.disabled = false;
    });

    object.addEventListener('click', async () => {
        object.classList.remove('bg-blue-500');
        object.classList.add('bg-yellow-500');
        object.disabled = true;
    });
}

function clickNotificationBadge(object, user_id, receiver) {
    //Add notification badge here
    object.addEventListener('click', async () => {
        console.log('hello');
        notify.send(JSON.stringify({
            'user': user_id,
            'receiver': receiver,
            'type': 'read'
        }));
    });
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
            const ball_status = object.querySelector(`#ball-status-${receiver}`);
            up_part.innerHTML = name + " " + ball_status.outerHTML;

            clickNotificationBadge(object, id, receiver);

            container.innerHTML = '';
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

                const change_last_message = document.querySelector(`#last-message-${receiver}`);
                if(data.user === id) {
                    change_last_message.innerHTML = `You: ${data.message}`;
                } else {
                    change_last_message.innerHTML = `${data.message}`;
                }
            }

            const message_input = document.querySelector('#message-input');

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