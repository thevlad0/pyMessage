function searchFriends(users_data) {
    const container = document.querySelector('.friendContainer');

    container.innerHTML = '';

    JSON.parse(users_data)
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
        profilePicture.alt = '';

        // Create div for user details
        const userDetailsDiv = document.createElement('div');

        // Create user name
        const userName = document.createElement('p');
        userName.classList.add('text-white');
        userName.textContent = user.name;

        // Append elements for user details
        userDetailsDiv.appendChild(userName);

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
            console.log(send);
            buttonsDiv.innerHTML = ""
            buttonsDiv.appendChild(document.createTextNode("Request sent"))
        })

        blockButton.addEventListener('click', async () => {
            let block = await fetch(`/api/friends/add_blocked/${user.id}/`)
            console.log(block);
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

export const search_field = document.querySelector('#search')
export const search = async () => {
    await fetch(`/api/search/${search_field.value}`)
    .then(response => response.json())
    .then(data => {
        searchFriends(data);
    })
}