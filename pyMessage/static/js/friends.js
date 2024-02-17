import { addChatOption } from './chat.js';
import { notification_count } from './notifications.js';

const display_last_message = async (object, user) => {
    await fetch(`/api/messages/get_last_message/${user}/`)
    .then(response => response.json())
    .then(data => {
        const parsed_data = JSON.parse(data);
        if(parsed_data.sender !== user) {
            object.innerHTML = `You: ${parsed_data.message}`;
        } else {
            object.innerHTML = `${parsed_data.message}`;
        }
    })
}

export function populateFriends(users_data) {
    const container = document.querySelector('.friendContainer');

    container.innerHTML = '';

    JSON.parse(users_data)
    .forEach(user => {
        // Create li element
        var li = document.createElement("li");
        li.classList.add("flex", "items-center", "mb-4", "clickable");

        // Create img element
        var img = document.createElement("img");
        img.classList.add("rounded-full", "h-10", "w-10", "mr-3");
        img.src = user.picture;
        img.alt = "";

        // Create div element
        var div = document.createElement("div");

        // Create first paragraph element
        var p1 = document.createElement("p");
        p1.classList.add("text-white");
        p1.textContent = user.name;
        if(user.status === "online") {
            p1.innerHTML += `   <i class="fa-solid fa-circle-dot" style="color: green" id="ball-status-${user.id}"></i>`;
        } else {
            p1.innerHTML += `   <i class="fa-solid fa-circle-dot" style="color: grey;" id="ball-status-${user.id}"></i>`;
        }
        
        // Create second paragraph element
        var p2 = document.createElement("p");
        p2.classList.add("text-blue-200", "text-sm");
        p2.setAttribute('id', `last-message-${user.id}`)
        display_last_message(p2, user.id);

        // Append elements
        div.appendChild(p1);
        div.appendChild(p2);
        li.appendChild(img);
        li.appendChild(div);

        li.classList.add('bg-blue-800', 'text-white', 'py-2', 'px-4', 
        'rounded-lg', 'mt-4', 'w-full', 'hover:bg-yellow-400', 
        'focus:outline-none', 'focus:bg-blue-600', 'relative');

        let notify_count = document.createElement('button');
        notify_count.classList.add('bg-red-500', 'rounded-full', 'h-4', 'w-4', 'flex', 
        'items-center', 'justify-center', 'text-white', 'text-xs', 'absolute', '-top-1', '-right-1');
        notify_count.setAttribute('id', `notify-status-${user.id}`);
        notification_count(user.id);
        li.appendChild(notify_count);

        addChatOption(li, user.id, user.name);

        // Append the li to an existing ul or ol element with id "myList"
        container.appendChild(li);
    });
}