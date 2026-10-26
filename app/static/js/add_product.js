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