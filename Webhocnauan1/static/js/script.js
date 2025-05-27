document.addEventListener("DOMContentLoaded", function () {
    const expandBtn = document.querySelector(".expand-btn");
    const extraContent = document.querySelector(".extra-content");

    if (expandBtn && extraContent) {
        expandBtn.addEventListener("click", function () {
            // Toggle hiển thị nội dung
            if (extraContent.style.display === "none" || extraContent.style.display === "") {
                extraContent.style.display = "block";
                expandBtn.textContent = "Thu gọn";
            } else {
                extraContent.style.display = "none";
                expandBtn.textContent = "Xem thêm";
            }
        });
    }
});
document.addEventListener("DOMContentLoaded", function () {
    new Swiper(".swiper-container", {
        slidesPerView: 3, // Hiển thị 3 bài viết cùng lúc
        spaceBetween: 20, // Khoảng cách giữa các slide
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        loop: true, // Chạy liên tục
        autoplay: {
            delay: 3000, // Tự động trượt sau 3 giây
        },
    });
});

var featuredSwiper = new Swiper(".featured-recipes .swiper-container", {
    slidesPerView: 3,
    spaceBetween: 20,
    loop: true,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
    },
});

    async function sendMessage() {
        const input = document.getElementById("chat-input");
        const message = input.value.trim();
        const chatBox = document.getElementById("chat-box");

        if (!message) return;

        chatBox.innerHTML += `<div><strong>Bạn:</strong> ${message}</div>`;
        input.value = "";

        const res = await fetch("/chat_api", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await res.json();
        chatBox.innerHTML += `<div><strong>Chatbot:</strong> ${data.response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
