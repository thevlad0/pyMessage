function searchFriends(users_data) {
    const container = document.querySelector('.friendContainer');

    container.innerHTML = '';

    users = JSON.parse(users_data)
    .forEach(user => {
        const listItem = document.createElement('li');
        listItem.classList.add('flex', 'items-center', 'justify-between', 'mb-4');

        // Create div for user information
        const userDiv = document.createElement('div');
        userDiv.classList.add('flex');

        // Create user profile picture
        const profilePicture = document.createElement('img');
        profilePicture.classList.add('rounded-full', 'h-10', 'w-10', 'mr-3');
        profilePicture.src = user.picture;
        profilePicture.alt = 'Profile picture of Richard Hendricks';

        // Create div for user details
        const userDetailsDiv = document.createElement('div');

        // Create user name
        const userName = document.createElement('p');
        userName.classList.add('text-white');
        userName.textContent = user.name;

        // Create message
        const message = document.createElement('p');
        message.classList.add('text-blue-200', 'text-sm');
        message.textContent = 'Sup man, wanna go out?';

        // Append elements for user details
        userDetailsDiv.appendChild(userName);
        userDetailsDiv.appendChild(message);

        // Append user details to user div
        userDiv.appendChild(profilePicture);
        userDiv.appendChild(userDetailsDiv);

        // Create div for buttons
        const buttonsDiv = document.createElement('div');

        // Create accept button
        const sendButton = document.createElement('button');
        sendButton.classList.add('text-lime-500');
        sendButton.innerHTML = `
            <svg class="h-5 w-5 text-green-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9 9V5a1 1 0 112 0v4h4a1 1 0 110 2h-4v4a1 1 0 11-2 0v-4H5a1 1 0 110-2h4z" clip-rule="evenodd" />
            </svg>
        `;

        // Create decline button
        const blockButton = document.createElement('button');
        blockButton.classList.add('text-white');
        blockButton.innerHTML = `
            <svg class="h-5 w-5 text-red-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM5.707 5.293a1 1 0 011.414 0l8 8a1 1 0 01-1.414 1.414l-8-8a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
        `;

        // Append buttons to buttons div
        buttonsDiv.appendChild(sendButton);
        buttonsDiv.appendChild(blockButton);

        sendButton.addEventListener('click', async () => {
            let send = await fetch(`/api/friends/send_request/${user.id}/`)
            buttonsDiv.innerHTML = ""
            buttonsDiv.appendChild(document.createTextNode("Request sent"))
        })

        blockButton.addEventListener('click', async () => {
            let block = await fetch(`/api/friends/add_blocked/${user.id}/`)
            buttonsDiv.innerHTML = ""
            buttonsDiv.appendChild(document.createTextNode("User blocked"))
        })

        // Append user div and buttons div to list item
        listItem.appendChild(userDiv);
        listItem.appendChild(buttonsDiv);

        // Append list item to the document
        container.appendChild(listItem);
    });
}

function populateFriends(users_data) {
    const container = document.querySelector('.friendContainer');

    container.innerHTML = '';

    users = JSON.parse(users_data)
    .forEach(user => {
        // Create li element
        var li = document.createElement("li");
        li.classList.add("flex", "items-center", "mb-4");
        li.id = "user-" + user.id;

        // Create img element
        var img = document.createElement("img");
        img.classList.add("rounded-full", "h-10", "w-10", "mr-3");
        img.src = user.picture;
        img.alt = "Profile picture of Richard Hendricks";

        // Create div element
        var div = document.createElement("div");

        // Create first paragraph element
        var p1 = document.createElement("p");
        p1.classList.add("text-white");
        p1.textContent = user.name;

        // Create second paragraph element
        var p2 = document.createElement("p");
        p2.classList.add("text-blue-200", "text-sm");
        p2.textContent = "Sup man, wanna go out?";

        // Append elements
        div.appendChild(p1);
        div.appendChild(p2);
        li.appendChild(img);
        li.appendChild(div);

        li.addEventListener('click', async () => {
            let data = await fetch(`/api/messages/${Number(user.id)}`)
            .then(response => response.json())
            .then(data => {
                const socket = new WebSocket(
                    'ws://'
                    + window.location.host
                    + '/ws/chat/'
                    + Number(user.id)
                    + '/'
                );

                const container = document.querySelector("#chat-box");

                function createMessage(float_direction, message) {
                    const flexDiv = document.createElement('div');
                    flexDiv.classList.add('flex', 'items-end', 'mb-4');

                    // Create nested div with bg-blue-500 and rounded classes
                    const nestedDiv = document.createElement('div');
                    nestedDiv.classList.add('bg-blue-500', 'rounded-l-lg', 'rounded-tr-lg', 'px-4', 'py-2', 'text-white', float_direction);

                    // Create paragraph element with Lorem Ipsum text
                    const paragraph = document.createElement('p');
                    paragraph.textContent = message;

                    // Append paragraph to nested div
                    nestedDiv.appendChild(paragraph);

                    // Append nested div to the main flex div
                    flexDiv.appendChild(nestedDiv);

                    // Append the main flex div to the document body
                    container.appendChild(flexDiv);
                }

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
                        createMessage('float-right', data.message);
                    }else{
                        createMessage('float-left', data.message);
                    }
                }

                document.querySelector('#chat-message-submit').onclick = function(e){
                    const message_input = document.querySelector('#message_input');
                    const message = message_input.value;

                    socket.send(JSON.stringify({
                        'message': message,
                        'user': id,
                        'receiver': receiver
                    }));

                    message_input.value = '';
                }

                const messageInput = document.querySelector('#message-input');
                console.log(messageInput)

                messageInput.addEventListener('keyup', function(event) {
                    if (event.key === 'Enter') {
                        
                        event.preventDefault();
                        
                    const message = messageInput.value.trim();

                    if(message !== ''){
                            socket.send(JSON.stringify({
                                'message': message,
                                'user': id,
                                'receiver': receiver
                            }))

                            messageInput.value = '';
                    }
                    }
                });
            })
        })

        // Append the li to an existing ul or ol element with id "myList"
        container.appendChild(li);
    });
}

const search_field = document.querySelector('#search')

const search = async () => {
    let data = await fetch(`/api/search/${search_field.value}`)
    .then(response => response.json())
    .then(data => {
        searchFriends(data);
    })
}

const load_friends = async () => {
    let data = await fetch(`/api/friends/`)
    .then(response => response.json())
    .then(data => {
        populateFriends(data);
    })
}

document.addEventListener('DOMContentLoaded', async () => {
    await load_friends();
});

search_field.addEventListener('input', async (e) => {
    if (search_field.value == '') {
        await load_friends();
        return;
    }

    await search();
});