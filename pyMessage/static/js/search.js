function populateFriends(users_data) {
    const container = document.getElementById('container');

    container.innerHTML = '';

    users = JSON.parse(users_data)
    .forEach(user => {
        const friendContainer = document.createElement('div');
        friendContainer.className = 'friend-container';

        const userImageDiv = document.createElement('div');
        userImageDiv.className = 'user-image';
        const img = document.createElement('img');
        img.className = 'userImg';
        img.src = user.picture;
        img.alt = user.name;
        userImageDiv.appendChild(img);

        const userNameDiv = document.createElement('div');
        userNameDiv.className = 'user-image';
        const nameH3 = document.createElement('h3');
        nameH3.textContent = user.name;
        const messageP = document.createElement('p');
        messageP.className = 'message';
        messageP.textContent = user.lastMessage;
        userNameDiv.appendChild(nameH3);
        userNameDiv.appendChild(messageP);

        friendContainer.appendChild(userImageDiv);
        friendContainer.appendChild(userNameDiv);

        container.appendChild(friendContainer);
    });
}

const search_field = document.querySelector('#search')
console.log(search_field.value)

const search = async () => {
    let data = await fetch(`/api/search/${search_field.value}`)
    .then(response => response.json())
    .then(data => {
        populateFriends(data);
    })
}

search_field.addEventListener('input', async (e) => {
    console.log(search_field.value)
    await search();
})