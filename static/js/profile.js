document.addEventListener("DOMContentLoaded", async function () {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                }
            }
        }
        return cookieValue;
    }

    const profileBox = document.getElementById("profile");
    const ordersBox = document.getElementById("orders");

    // PROFILE
    const res = await fetch("/api/me/");
    const profile = await res.json();

    profileBox.innerHTML = `
        <p><b>Имя:</b> ${profile.full_name || ""}</p>
        <p><b>Телефон:</b> ${profile.phone || ""}</p>
        <p><b>Адрес:</b> ${profile.address || ""}</p>

        <button id="save" class="btn btn-primary">Сохранить</button>
    `;

    document.getElementById("save").addEventListener("click", async function () {

        await fetch("/api/me/", {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                full_name: "Тест",
                phone: "000",
                address: "Минск"
            })
        });

        alert("Сохранено");
    });

    // ORDERS
    const ordersRes = await fetch("/api/orders/");
    const orders = await ordersRes.json();

    ordersBox.innerHTML = orders.map(o => `
        <div class="card mt-2 p-2">
            <p>Заказ #${o.id}</p>
            <p>${o.total_price} BYN</p>
        </div>
    `).join("");
});