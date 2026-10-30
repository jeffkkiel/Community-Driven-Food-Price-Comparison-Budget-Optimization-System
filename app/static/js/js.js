function updateHero() {
    const now = new Date();

    const dateText = now.toLocaleDateString("en-US", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
    });
    document.getElementById("hero-date").textContent = dateText;

    const hour = now.getHours();
    let greeting = "Good Evening!";
    if (hour < 12) greeting = "Good Morning!";
    else if (hour < 18) greeting = "Good Afternoon!";
    document.getElementById("greeting").textContent = greeting;
}

updateHero();                      
setInterval(updateHero, 60 * 1000); 

// auth html
const authCard = document.getElementById("auth-card");
const swapLink = document.querySelector("[data-swap]");

if (authCard && swapLink) {
  swapLink.addEventListener("click", (e) => {
    e.preventDefault();
    authCard.classList.toggle("register");
    authCard.classList.add("leaving");
    setTimeout(() => (window.location = swapLink.href), 500);
  });
}