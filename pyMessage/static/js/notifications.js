const logged_in_user = JSON.parse(document.querySelector('#user_id').innerHTML);

export const notification_count = (user) => {
    fetch(`/api/messages/get_notifications/${user}/`)
    .then(response => response.json())
    .then(data => {
        const parsed_data = JSON.parse(data);
        let count_badge = document.querySelector(`#notify-status-${user}`)
        if(parsed_data > 0){
            count_badge.style.visibility = "visible";
        } else {
            count_badge.style.visibility = "hidden";
        }
        count_badge.textContent = parsed_data
    })
}

export const notify = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + 'notify/'
)

notify.onopen = function(e){
    console.log("CONNECTED TO NOTIFICATION");
}


notify.onmessage = function(e){
    const data = JSON.parse(e.data)

    if(data.user !== logged_in_user){
        let count_badge = document.querySelector(`#notify-status-${data.user}`)
        
        if(data.count > 0){
            count_badge.style.visibility = "visible";
        } else {
            count_badge.style.visibility = "hidden";
        }

        count_badge.textContent = data.count
    }
}

notify.onclose = function(e){
    console.log("DISCONNECTED FROM NOTIFICATION");
}