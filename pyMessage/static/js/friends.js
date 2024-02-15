import { addChatOption } from './chat.js';

const display_last_message = async (object, user) => {
    await fetch(`/api/messages/get_last_message/${user}/`)
    .then(response => response.json())
    .then(data => {
        object.innerHTML = JSON.parse(data).message;
    })
}

export function populateFriends(users_data) {
    const container = document.querySelector('.friendContainer');

    container.innerHTML = '';

    JSON.parse(users_data)
    .forEach(user => {
        // Create li element
        var li = document.createElement("li");
        li.classList.add("flex", "items-center", "mb-4");

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
            p1.innerHTML += `   <i class="fa-solid fa-circle-dot" style="color: green" id="${user.id}-ball-status"></i>`;
        } else {
            p1.innerHTML += `   <i class="fa-solid fa-circle-dot" style="color: grey;" id="${user.id}-ball-status"></i>`;
        }

        // Create second paragraph element
        var p2 = document.createElement("p");
        p2.classList.add("text-blue-200", "text-sm");
        display_last_message(p2, user.id);

        // Append elements
        div.appendChild(p1);
        div.appendChild(p2);
        li.appendChild(img);
        li.appendChild(div);

        li.classList.add('bg-blue-800', 'text-white', 'py-2', 'px-4', 
        'rounded-lg', 'mt-4', 'w-full', 'hover:bg-yellow-400', 
        'focus:outline-none', 'focus:bg-blue-600');

        addChatOption(li, user.id, user.name);

        // Append the li to an existing ul or ol element with id "myList"
        container.appendChild(li);
    });
}