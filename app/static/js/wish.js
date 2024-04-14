function Waves() {
    const waves = document.querySelectorAll(".wave");
    waves.forEach((wave) => {
        for (let i = 0; i < wave.children.length; i++)
            wave.children[i].style.transitionDelay = `${i * 0.1}s`;
    });
}

Waves();

const addButtom = document.getElementById('addButton');
addButtom.addEventListener('click', () => {
    const wishDataFormInputs = document.getElementById('addWish').getElementsByTagName("input");
    let wishData = {}
    for (let wish of wishDataFormInputs){
        wishData[wish.id] = wish.value
    }
    wishData['user_id'] = 470184649
    fetch('/api/v1/wish', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(wishData)
    })
    .then(response => {
        if (response.ok){
            showToast('Succesfully 😎')
        }
        else {
            showToast('Something went wrong. Please tell your partner what you want to do on your own 😞')
        }
    })

})

function showToast(msg) {
    let toastContainer = document.getElementById('toastContainer');
    toastContainer.textContent = msg;
    toastContainer.classList.add('show');

    setTimeout(function () {
        toastContainer.classList.remove('show');
    }, 2000);
 }
