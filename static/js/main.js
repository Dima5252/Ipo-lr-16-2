document.addEventListener("DOMContentLoaded", function () {

    const container = document.getElementById("products-container");
    const spinner = document.getElementById("spinner");

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function showAlert(message, type = "success") {
        const alertBox = document.createElement("div");
        alertBox.className = `alert alert-${type} mt-2`;
        alertBox.innerText = message;

        document.querySelector(".container").prepend(alertBox);

        setTimeout(() => {
            alertBox.remove();
        }, 3000);
    }

    async function loadProducts() {

        try {
            const response = await fetch("/api/products/");
            if (!response.ok) throw new Error("API error");

            const data = await response.json();

            spinner.style.display = "none";
            container.innerHTML = "";

            data.forEach(product => {

                const card = document.createElement("div");
                card.className = "col-md-4 mb-3";

                const image = product.image
                    ? product.image
                    : "https://via.placeholder.com/300x200";

                card.innerHTML = `
                    <div class="card h-100 shadow-sm">

                        <img src="${image}" class="card-img-top" alt="${product.name}">

                        <div class="card-body">

                            <h5 class="card-title">${product.name}</h5>

                            <p class="card-text">
                                ${product.price} BYN
                            </p>

                            <a href="/product/${product.id}/" class="btn btn-primary btn-sm">
                                Подробнее
                            </a>

                            <button class="btn btn-success btn-sm mt-2 add-to-cart" data-id="${product.id}">
                                В корзину
                            </button>

                        </div>

                    </div>
                `;

                container.appendChild(card);
            });

        } catch (error) {
            spinner.innerHTML = `
                <div class="alert alert-danger">
                    Ошибка загрузки товаров
                </div>
            `;
        }
    }

    async function addToCart(productId) {

        try {
            const response = await fetch(`/api/cart-items/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    product: productId,
                    quantity: 1
                })
            });

            if (!response.ok) {
                throw new Error("Add to cart failed");
            }

            showAlert("Товар добавлен в корзину", "success");

        } catch (error) {
            showAlert("Ошибка добавления в корзину", "danger");
        }
    }

    document.addEventListener("click", function (e) {
        if (e.target.classList.contains("add-to-cart")) {
            const productId = e.target.dataset.id;
            addToCart(productId);
        }
    });

    loadProducts();
});