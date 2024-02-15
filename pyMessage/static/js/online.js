const logged_in_user = JSON.parse(document.querySelector('#user_id').innerHTML);

const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + 'online/'
)

socket.onopen = function(e){
    console.log("CONNECTED TO ONLINE CONSUMER");

    socket.send(JSON.stringify({
        'user': logged_in_user,
        'type': 'online'
    }))
}

window.addEventListener("beforeunload", function(e){
    socket.send(JSON.stringify({
        'user': logged_in_user,
        'type': 'offline'
    }))
})

socket.onclose = function(e){
    console.log("DISCONNECTED FROM ONLINE CONSUMER")
}

socket.onmessage = function(e){
    var data = JSON.parse(e.data)
    console.log(data)
    if(data.user !== logged_in_user){
        console.log(data.user)
        var ball_status = document.querySelector(`#ball-status-${data.user}`);
        if(data.online_status === true){
            ball_status.style.color = 'green'
        }else{
            ball_status.style.color = 'grey'
        }
    }
}