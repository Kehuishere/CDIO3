async function ask(){

    const q = document.getElementById("q").value
    const chat = document.getElementById("chat-box")

    // user message
    const userMsg = document.createElement("div")
    userMsg.className = "message user"
    userMsg.innerText = q
    chat.appendChild(userMsg)

    document.getElementById("q").value=""

    // bot message
    const botMsg = document.createElement("div")
    botMsg.className = "message bot"
    chat.appendChild(botMsg)

    const res = await fetch("http://localhost:8000/ask",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            question:q
        })
    })

    const data = await res.json()

    typingEffect(botMsg, data.answer)

    chat.scrollTop = chat.scrollHeight
}


function typingEffect(element, text){

    text = text.replace(/\n/g,"<br>")

    let i = 0

    function type(){

        if(i >= text.length) return

        // nếu gặp <br> thì chèn luôn
        if(text.substring(i, i+4) === "<br>"){
            element.innerHTML += "<br>"
            i += 4
        }else{
            element.innerHTML += text.charAt(i)
            i++
        }

        setTimeout(type,20)
    }

    type()
}