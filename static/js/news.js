// Функция для создания карточки с постом
function createPostCard(post) {
    const card = document.createElement("div");
    card.classList.add("col-md-12", "mb-4");

    card.innerHTML = `
    <div class="card" style="width: 20rem;">
        <div class="card-body">
            <h5 class="card-title">${post.title}</h5>
            <h6 class="card-time">${post.date}</h6>
            <p class="card-text">${post.author}</p>
            <a href="/news/${post.id}" class="btn btn-primary">К новости</a>
        </div>
    </div>
    `;

    return card;
}

// Функция для загрузки постов и добавления карточек на страницу
function loadPosts() {
    const columnsContainer = document.getElementById("columnsContainer");
    fetch('/get-news/')
        .then(response => response.json())
        .then(posts => {
            const columns = Array.from({ length: 3 }, () => {
                const column = document.createElement("div");
                column.classList.add("col-md-4");
                return column;
            });

            let columnIndex = 0;

            posts.forEach(post => {
                columns[columnIndex].appendChild(createPostCard(post));
                columnIndex = (columnIndex + 1) % columns.length;
            });

            columns.forEach(column => columnsContainer.appendChild(column));
        })
        .catch(error => console.error('Ошибка при загрузке новостей:', error));
}

// Загрузка постов при загрузке страницы
window.onload = loadPosts;