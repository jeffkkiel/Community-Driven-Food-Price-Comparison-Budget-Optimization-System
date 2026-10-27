const storeSelect = document.getElementById("store-select");
const newStoreGroup = document.getElementById("new-store-group");

function toggleNewStore() {
  newStoreGroup.hidden = storeSelect.value !== "__new__";
}

storeSelect.addEventListener("change", toggleNewStore);
toggleNewStore();


const productSelect = document.getElementById("product_select");
const newProductGroup = document.getElementById("new-product-group");

function toggleNewProduct() {
  newProductGroup.hidden = productSelect.value !== "__new__";
}

productSelect.addEventListener("change", toggleNewProduct);
toggleNewProduct();

const quantityInput = document.getElementById("quantity");
const totalPriceInput = document.getElementById("total_price");
const pricePreview = document.getElementById("price-preview");

function updatePricePreview() {
  const quantity = parseInt(quantityInput.value, 10);
  const total = parseFloat(totalPriceInput.value);

  if (quantity > 0 && total >= 0) {
    pricePreview.textContent =
      "Price per item/package: ₱" + (total / quantity).toFixed(2);
  } else {
    pricePreview.textContent = "Price per item/package: ₱0.00";
  }
}

quantityInput.addEventListener("input", updatePricePreview);
totalPriceInput.addEventListener("input", updatePricePreview);
updatePricePreview(); 

function linkSelects(parentId, childId, key) {
  const parent = document.getElementById(parentId);
  const child = document.getElementById(childId);
  if (!parent || !child) return;

  const all = Array.from(child.options);
  const saved = child.value;            

  function filter() {
    child.innerHTML = "";
    all.forEach(function (opt) {
      const tag = opt.dataset[key]; 
      if (!tag || tag === parent.value) child.appendChild(opt.cloneNode(true));
    });
  }

  parent.addEventListener("change", function () {
    filter();
    child.value = "";
    child.dispatchEvent(new Event("change")); 
  });

  filter();
  child.value = saved;
}

linkSelects("category", "product_select", "category");
linkSelects("location", "store-select", "location");