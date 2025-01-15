const email = document.getElementById('email')
const password = document.querySelector('#password')

const handleLogin = async()=>{
    const res = await fetch('/login',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email.value,
            password: password.value
        })
    })
    const data = await res.json()
    if(data.status === 'ok'){
        window.location.href = '/home'
    }else{
        alert(data.message)
    }
}