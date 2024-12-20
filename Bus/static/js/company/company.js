document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.info-saide');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            const target = this.getAttribute('data-tab');


            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));


            this.classList.add('active');
            const targetTab = document.getElementById(target);
            if (targetTab) {
                targetTab.classList.add('active');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const otabs = document.querySelectorAll('.info-order');
    const orderCont = document.querySelectorAll('.order-content');
    
    otabs.forEach(tab =>{
        tab.addEventListener('click', function() {
            const target = this.getAttribute('data-tab');

            otabs.forEach(t => t.classList.remove('active'));
            orderCont.forEach(c => c.classList.remove('active'));

            this.classList.add('active');
            const orderTab = document.getElementById(target);
            if (orderTab) {
                orderTab.classList.add('active');
            }
        });
    });
});    



document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('add-bus-modal');
    const addBusBtn = document.getElementById('add-bus-btn');
    const closeModal = document.getElementById('close-modal');
 
    addBusBtn.addEventListener('click', () => {
        modal.style.display = 'block';
    });

    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});


document.addEventListener('DOMContentLoaded', () => {
    // Добавление модального окна для удаления автобуса
    const deleteButtons = document.querySelectorAll('.delete-bus');
    const deleteModal = document.getElementById('delete-bus-modal');
    const deleteForm = document.getElementById('delete-bus-form');
    const closeDeleteModal = document.getElementById('close-delete-modal');
    const cancelDelete = document.getElementById('cancel-delete');
    const deleteBusName = document.getElementById('delete-bus-name');

    deleteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const busElement = button.closest('.bus');
            const busId = busElement.dataset.id;
            const busName = busElement.querySelector('.bus-name').textContent;

            deleteBusName.textContent = `"${busName}"`;
            deleteForm.action = `/delete_bus/${busId}/`;
            deleteModal.style.display = 'block';
        });
    });

    closeDeleteModal.addEventListener('click', () => {
        deleteModal.style.display = 'none';
    });

    cancelDelete.addEventListener('click', () => {
        deleteModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === deleteModal) {
            deleteModal.style.display = 'none';
        }
    });


    const editButtons = document.querySelectorAll('.edit-info-bus');
    const editModal = document.getElementById('edit-bus-modal');
    const closeEditModal = document.getElementById('close-edit-modal');
    const editBusNameDisplay = document.getElementById('edit-bus-name-display');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const busElement = this.closest('.bus');
            const busId = busElement.dataset.id;
            const busName = busElement.querySelector('.bus-name').textContent;
            const busSeats = parseInt(busElement.querySelector('.bus-seats').textContent.replace(/\D/g, ''));
            const busPrice = parseFloat(busElement.querySelector('.bus-price').textContent.replace(/[^\d.]/g, ''));
            const busDesc = busElement.querySelector('.bus-desc').textContent;

            editBusNameDisplay.textContent = `"${busName}"`;
            document.getElementById('edit-bus-id').value = busId;
            document.getElementById('edit-bus-name').value = busName;
            document.getElementById('edit-bus-seats').value = busSeats;
            document.getElementById('edit-bus-price').value = busPrice;
            document.getElementById('edit-bus-description').value = busDesc;
            editModal.style.display = 'block';
        });
    });

    closeEditModal.addEventListener('click', () => {
        editModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
    });
});










