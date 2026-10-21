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