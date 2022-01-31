function copyFromInput(el) {
    el.focus()
    el.select()
    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
    } catch (err) {
    }
    let cpMsg = el.parentElement.querySelector('.adm-copy-success')
    cpMsg.classList.add('adm-copy-success_a')
    setTimeout(() => {
        cpMsg.classList.remove('adm-copy-success_a')
    }, 1000)
}