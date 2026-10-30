(function () {
  const grid = document.getElementById("basket-grid");
  if (!grid) return;

  const rows = Array.from(grid.querySelectorAll(".basket-row"));
  const chips = document.querySelectorAll(".basket-chips .chip");
  const search = document.getElementById("basket-search");
  const noMatch = document.getElementById("no-match");
  const countEl = document.getElementById("basket-count");
  const itemsEl = document.getElementById("panel-items");
  const totalEl = document.getElementById("panel-total");
  const fillEl = document.getElementById("budget-fill");
  const budgetText = document.getElementById("budget-text");
  const calcBtn = document.getElementById("calculate-btn");
  const budget = parseFloat(grid.dataset.budget) || 0;
  let activeCategory = "";
  const MAX_QUANTITY = 9999;

  const peso = (n) => "₱" + n.toFixed(2);

  function updateBasket() {
    let products = 0;
    let units = 0;
    let total = 0;
    itemsEl.textContent = "";

    rows.forEach((row) => {
      const input = row.querySelector(".qty-input");
      let quantity = parseInt(input.value, 10);
      if (Number.isNaN(quantity) || quantity < 0) quantity = 0;

      row.classList.toggle("selected", quantity > 0);

      const stepper = row.querySelector(".qty-stepper");
      stepper.querySelector('[data-step="-1"]').disabled = quantity <= 0;
      stepper.querySelector('[data-step="1"]').disabled = quantity >= MAX_QUANTITY;

      if (quantity > 0) {
        products += 1;
        units += quantity;
        total += quantity * (parseFloat(row.dataset.price) || 0);

        const li = document.createElement("li");
        const name = document.createElement("span");
        const qty = document.createElement("span");
        name.textContent = row.dataset.name;
        qty.textContent = "× " + quantity;
        li.append(name, qty);
        itemsEl.appendChild(li);
      }
    });

    if (products === 0) {
      countEl.textContent = "No items selected";
    } else {
      const itemWord = products === 1 ? "item" : "items";
      const unitWord = units === 1 ? "unit" : "units";
      countEl.textContent = `${products} ${itemWord} · ${units} ${unitWord} selected`;
    }

    totalEl.textContent = peso(total);

    const over = total > budget;
    const percent = budget > 0 ? Math.min(100, (total / budget) * 100) : 0;
    fillEl.style.width = percent + "%";
    fillEl.classList.toggle("over", over);
    budgetText.classList.toggle("over", over);
    budgetText.textContent = over
      ? `${peso(total - budget)} over budget`
      : `${peso(budget - total)} left of ${peso(budget)}`;

    calcBtn.disabled = products === 0;
  }

  function applyFilters() {
    const term = search.value.trim().toLowerCase();
    let shown = 0;

    rows.forEach((row) => {
      const matchCategory = !activeCategory || row.dataset.category === activeCategory;
      const matchText = !term || row.dataset.name.toLowerCase().includes(term);
      row.hidden = !(matchCategory && matchText);
      if (!row.hidden) shown += 1;
    });

    noMatch.hidden = shown !== 0;
  }

  grid.addEventListener("click", (event) => {
    const button = event.target.closest(".qty-btn");
    if (!button) return;

    const input = button.closest(".qty-stepper").querySelector(".qty-input");
    const step = parseInt(button.dataset.step, 10);
    let quantity = parseInt(input.value, 10);

    if (Number.isNaN(quantity)) quantity = 0;
    input.value = Math.min(MAX_QUANTITY, Math.max(0, quantity + step));
    updateBasket();
  });

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      chips.forEach((other) => {
        other.classList.toggle("active", other === chip);
        other.setAttribute("aria-pressed", other === chip ? "true" : "false");
      });
      activeCategory = chip.dataset.category;
      applyFilters();
    });
  });

  search.addEventListener("input", applyFilters);
  search.addEventListener("keydown", (event) => {
    if (event.key === "Enter") event.preventDefault();
  });

  updateBasket();

  const results = document.getElementById("results");
  if (results) {
    window.addEventListener("load", () => results.scrollIntoView(), { once: true });
  }
})();