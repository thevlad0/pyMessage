function populateBlocked(user_data) {
    const container = document.querySelector("#container");

    users = JSON.parse(user_data)
    .forEach(user => {
        const article = document.createElement('article');
        article.classList.add('flex', 'items-center', 'justify-between', 'my-2');

        const userSection = document.createElement('div');
        userSection.classList.add('flex', 'items-center', 'gap-4');

        const figure = document.createElement('figure');
        figure.classList.add('w-14', 'h-14');

        const img = document.createElement('img');
        img.classList.add('w-full', 'h-full', 'rounded-full');
        img.src = user.picture;
        img.alt = 'User Image';

        const userNameSection = document.createElement('div');
        userNameSection.classList.add('user-name');

        const userName = document.createElement('h3');
        userName.classList.add('text-xl');
        userName.textContent = user.name;

        const buttonSection = document.createElement('div');
        buttonSection.classList.add('flex');

        const removeButton = document.createElement('button');
        removeButton.type = 'button';
        removeButton.classList.add('btn', 'decline', 'bg-red-500', 'rounded-lg', 'px-4', 'py-1', 'mx-1');
        removeButton.textContent = 'Remove blocked';

        removeButton.addEventListener('click', async () => {
            let remove = await fetch(`/api/friends/remove_blocked/${request.id}/`)
            buttonSection.innerHTML = "";
            buttonSection.appendChild(document.createTextNode("Blocked user removed"));
        })

        container.appendChild(article);
        article.appendChild(userSection);
        userSection.appendChild(figure);
        figure.appendChild(img);
        userSection.appendChild(userNameSection);
        userNameSection.appendChild(userName);
        article.appendChild(buttonSection);
        buttonSection.appendChild(acceptButton);
        buttonSection.appendChild(declineButton);
    });
}

const load_users = async () => {
    let data = await fetch(`/api/friends/get_blocked/`)
    .then(response => response.json())
    .then(data => {
        populateBlocked(data);
    })
}

document.addEventListener('DOMContentLoaded', async () => {
    await load_users();
});