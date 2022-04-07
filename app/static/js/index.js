
const sse = new EventSource('/stream')
      
sse.addEventListener(
  'message',
  (e) => {
    var data = JSON.parse(e.data)
    let counter = document.querySelector("#counter")
    counter.innerText = data.count
    let status = document.querySelector("#control-status")
    // console.log(data.control)
    // console.log(status.innerText)
    status.innerText = data.control
    data.control == "stop" ? status.style.background = "red" : status.style.background = "green"
  },
  false
)

const start = () => {
  console.log("start")
  fetch('/start', {
    "method": "post"})
  .then(res => res.json())
  .then(data => console.log(data))
}

 const stop = () => {
  console.log("stop")
  fetch('/stop', {
    "method": "post"})
  .then(res => res.json())
  .then(data => console.log(data))
}

const increase = () => {
  console.log("increase")
  fetch('/increase', {
    "method": "post"})
  .then(res => res.json())
  .then(data => console.log(data))
}

const decrease = () => {
  console.log("decrease")
  fetch('/decrease', {
    "method": "post"})
  .then(res => res.json())
  .then(data => console.log(data))
}

const reset = () => {
  console.log("reset")
  const q = prompt('Reset Counter ?')
  if (!q) {
    alert(`Please enter "yes" to reset Counter:`)
    return
  }
  fetch('/reset', {
    "method": "post"})
  .then(res => res.json())
  .then(data => console.log(data))
}

const setCounter = () => {
  counter = prompt("set counter")
  if (!counter) {
    alter('Please enter your counter of exit')
    return
  }
  fetch(`/set/${counter}`, {
    "method": "post"})
  .then(res => res.json())
  .then(data => console.log(data))
 
}
