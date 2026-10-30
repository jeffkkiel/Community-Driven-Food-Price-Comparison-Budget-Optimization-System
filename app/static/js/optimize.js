(function () {
  const grid = document.getElementById("basket-grid");
  if (!grid) return;

  const countEl = document.getElementById("basket-count");
  const chips = document.querySelectorAll(".basket-chips .chip");
  const MAX_QUANTITY = 9999;

  function updateBasket() {
    let products = 0;
    let units = 0;

    grid.querySelectorAll(".qty-input").forEach((input) => {
      let quantity = parseInt(input.value, 10);
      if (Number.isNaN(quantity) || quantity < 0) quantity = 0;

      if (quantity > 0) {
        products += 1;
        units += quantity;
      }

      const card = input.closest(".basket-card");
      if (card) card.classList.toggle("selected", quantity > 0);

      const stepper = input.closest(".qty-stepper");
      if (stepper) {
        stepper.querySelector('[data-step="-1"]').disabled = quantity <= 0;
        stepper.querySelector('[data-step="1"]').disabled = quantity >= MAX_QUANTITY;
      }
    });

    if (countEl) {
      if (products === 0) {
        countEl.textContent = "No items selected";
      } else {
        const itemWord = products === 1 ? "item" : "items";
        const unitWord = units === 1 ? "unit" : "units";
        countEl.textContent = `${products} ${itemWord} · ${units} ${unitWord} selected`;
      }
    }
  }

  grid.addEventListener("click", (event) => {
    const button = event.target.closest(".qty-btn");
    if (!button) return;

    const stepper = button.closest(".qty-stepper");
    const input = stepper.querySelector(".qty-input");
    const step = parseInt(button.dataset.step, 10);
    let quantity = parseInt(input.value, 10);

    if (Number.isNaN(quantity)) quantity = 0;
    quantity = Math.min(MAX_QUANTITY, Math.max(0, quantity + step));
    input.value = quantity;
    updateBasket();
  });

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      chips.forEach((other) => {
        other.classList.toggle("active", other === chip);
        other.setAttribute("aria-pressed", other === chip ? "true" : "false");
      });

      const category = chip.dataset.category;
      grid.querySelectorAll(".basket-card").forEach((card) => {
        card.hidden = Boolean(category) && card.dataset.category !== category;
      });
    });
  });

  updateBasket();

  const results = document.getElementById("results");
  if (results) {
    window.addEventListener("load", () => results.scrollIntoView(), { once: true });
  }
})();
