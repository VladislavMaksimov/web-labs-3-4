const deleteTask = (id) => {
    const url = '/tasks/' + id;

    fetch(url, {
        method: 'DELETE'
    })
    .then(() => {
        const card = document.querySelector('.card#id_' + id);
        card.remove();
    })
    .catch((e) => {
        alert(e.message)
    })
}