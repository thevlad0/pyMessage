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

function createImage(float_direction, image) {
    const flexDiv = document.createElement('div');
    flexDiv.classList.add('flex', 'items-end', 'mb-4', 'clear-both', float_direction);

    const nestedDiv = document.createElement('div');
    nestedDiv.classList.add('rounded-l-lg', 'rounded-tr-lg', 'px-4', 'py-2', 'text-white');

    const img = document.createElement('img');
    img.src = image;
    img.classList.add('w-40', 'h-40', 'rounded-lg');

    nestedDiv.appendChild(img);
    flexDiv.appendChild(nestedDiv);
    container.appendChild(flexDiv);
}

function clickNotificationBadge(object, user_id, receiver) {
    notify.send(JSON.stringify({
        'user': user_id,
        'receiver': receiver,
    }));
}

function scrollToBottom() {
    const container = document.querySelector('#chat-box');
    container.scrollTop = container.scrollHeight;
  }

export function addChatOption(object, user_id, name) {
    object.addEventListener('click', async () => {
        let id = Number(document.querySelector('#user_id').innerHTML);
        let receiver = user_id;
        await fetch(`/api/messages/${Number(receiver)}`)
        .then(response => response.json())
        .then(data => {
            let socket = new WebSocket(
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
                    if(message.image === '') {
                        createMessage('float-left', 'bg-yellow-500', message.message);
                    } else {
                        createImage('float-left', message.image);
                    }
                }else{
                    if(message.image === '') {
                        createMessage('float-right', 'bg-blue-500', message.message);
                    } else {
                        createImage('float-right', message.image);
                    }
                }
            })
            scrollToBottom();

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
                    if(data.type !== 'image') {
                        createMessage('float-right', 'bg-blue-500', data.message);
                    } else {
                        createImage('float-right', data.image);
                    }
                }else{
                    if(data.type !== 'image') {
                        createMessage('float-left', 'bg-yellow-500', data.message);
                    } else {
                        createImage('float-left', data.image);
                    }
                }

                const change_last_message = document.querySelector(`#last-message-${receiver}`);
                if(data.user === id) {
                    change_last_message.innerHTML = `You: ${data.message}`;
                } else {
                    change_last_message.innerHTML = `${data.message}`;
                }

                scrollToBottom();
            }

            const message_input = document.querySelector('#message-input');

            const fileInput = document.querySelector('#image-input');
            document.querySelector('#message-input-confirm').onclick = function(e){
                if (fileInput.files.length > 0) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const base64Image = e.target.result;

                        console.log(base64Image);
                        // Send the Base64 encoded string through WebSocket
                        socket.send(JSON.stringify({
                            'image': base64Image,
                            'user': id,
                            'receiver': receiver,
                            'type': 'image',
                        }));
                    };
                    reader.readAsDataURL(fileInput.files[0]);
                    fileInput.value = ''
            }

                const message = message_input.value;
                if(message === '') {
                    return;
                }
                socket.send(JSON.stringify({
                    'message': message,
                    'user': id,
                    'receiver': receiver,
                    'type': 'message'
                }));

                message_input.value = '';
            }

            document.querySelectorAll('.clickable.disabled').forEach(disabledItem => {
                disabledItem.classList.remove('disabled');
                disabledItem.classList.remove('bg-yellow-400');
            });
    
            // Then disable the clicked item
            object.classList.add('disabled');
            object.classList.add('bg-yellow-400');
            fileInput.value = ''

            let arr = document.querySelectorAll('.clickable')
            Array.from(arr).filter(item => item !== object).forEach(item => {                
                item.addEventListener('click', () => {
                    socket.close();
                });
            });

            object.addEventListener('click', () => {
                preventDefault();
                addChatOption(object, user_id, name);
            });
        })
    })
}