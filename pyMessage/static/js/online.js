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
    console.log(data);
    if(data.user !== logged_in_user){
        var ball_status = document.querySelector(`#${data.user}-ball-status`)
        console.log(ball_status);
        if(data.online_status === true){
            ball_status.style.backgroundColor = 'green'
        }else{
            ball_status.style.backgroundColor = 'grey'
        }
    }
}