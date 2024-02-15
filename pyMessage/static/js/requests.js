function populateRequests(user_data) {
    const container = document.querySelector("#container");

    requests = JSON.parse(user_data)
    .forEach(request => {
        const article = document.createElement('article');
        article.classList.add('flex', 'items-center', 'justify-between', 'my-2');

        const userSection = document.createElement('div');
        userSection.classList.add('flex', 'items-center', 'gap-4');

        const figure = document.createElement('figure');
        figure.classList.add('w-14', 'h-14');

        const img = document.createElement('img');
        img.classList.add('w-full', 'h-full', 'rounded-full');
        img.src = request.sender.picture;
        img.alt = 'User Image';

        const userNameSection = document.createElement('div');
        userNameSection.classList.add('user-name');

        const userName = document.createElement('h3');
        userName.classList.add('text-xl');
        userName.textContent = request.sender.name;

        const buttonSection = document.createElement('div');
        buttonSection.classList.add('flex');

        const acceptButton = document.createElement('button');
        acceptButton.type = 'button';
        acceptButton.classList.add('btn', 'accept', 'bg-green-500', 'rounded-lg', 'px-4', 'py-1', 'mx-1');
        acceptButton.textContent = 'Accept';

        const declineButton = document.createElement('button');
        declineButton.type = 'button';
        declineButton.classList.add('btn', 'decline', 'bg-red-500', 'rounded-lg', 'px-4', 'py-1', 'mx-1');
        declineButton.textContent = 'Decline';

        acceptButton.addEventListener('click', async () => {
            let accept = await fetch(`/api/friends/accept_request/${request.id}/`)
            console.log(accept);
            buttonSection.innerHTML = "";
            buttonSection.appendChild(document.createTextNode("Request Accepted"));
        })

        declineButton.addEventListener('click', async () => {
            let decline = await fetch(`/api/friends/decline_request/${request.id}/`)
            console.log(decline);
            buttonSection.innerHTML = "";
            buttonSection.appendChild(document.createTextNode("Request Declined"));
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

const load_requests = async () => {
    await fetch(`/api/friends/requests`)
    .then(response => response.json())
    .then(data => {
        populateRequests(data);
    })
}

document.addEventListener('DOMContentLoaded', async () => {
    await load_requests();
});