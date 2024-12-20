document.addEventListener("DOMContentLoaded", () => {
    const rangeMin = document.querySelector(".range-min");
    const rangeMax = document.querySelector(".range-max");
    const startPrice = document.querySelector(".start-price");
    const endPrice = document.querySelector(".end-price");
    const track = document.querySelector(".range-track");

    function updateRange() {
        const minValue = parseInt(rangeMin.value);
        const maxValue = parseInt(rangeMax.value);

        if (minValue >= maxValue) {
            rangeMin.value = maxValue - 100; 
        }
        if (maxValue <= minValue) {
            rangeMax.value = minValue + 100; 
        }

        startPrice.textContent = `${rangeMin.value} ₽`;
        endPrice.textContent = `${rangeMax.value} ₽`;

        const minPercent = ((rangeMin.value - 2000) / 28000) * 100;
        const maxPercent = ((rangeMax.value - 2000) / 28000) * 100;
        track.style.background = `linear-gradient(to right, #ddd ${minPercent}%, #007bff ${minPercent}%, #007bff ${maxPercent}%, #ddd ${maxPercent}%)`;
    }

    rangeMin.addEventListener("input", updateRange);
    rangeMax.addEventListener("input", updateRange);
    updateRange();
});



