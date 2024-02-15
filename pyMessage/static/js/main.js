import { populateFriends } from './friends.js'
import { search, search_field } from './search.js'

const load_friends = async () => {
    await fetch(`/api/friends/`)
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