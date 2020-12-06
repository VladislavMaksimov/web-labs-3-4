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

const setState = (id) => {
    const url = '/tasks/' + id;

    fetch(url, {
        method: 'PUT'
    })
    .catch((e) => {
        alert(e.message)
    })
}

const getComment = (id) => {
    const url = `https://jsonplaceholder.typicode.com/comments?postId=${id}`;

    fetch(url)
        .then(response => response.json())
        .then(json => {
            const comments = document.getElementById('comments');
            const comment = document.createElement('p');
            comment.innerText = json[0]['body'];
            comments.appendChild(comment);
        })
}