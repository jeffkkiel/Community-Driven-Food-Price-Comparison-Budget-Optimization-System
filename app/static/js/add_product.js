const storeSelect = document.getElementById("store-select");
const newStoreGroup = document.getElementById("new-store-group");

function toggleNewStore() {
  newStoreGroup.hidden = storeSelect.value !== "__new__";
}

storeSelect.addEventListener("change", toggleNewStore);
toggleNewStore();