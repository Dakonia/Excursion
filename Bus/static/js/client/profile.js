const tabs = document.querySelectorAll('.info-saide');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
    
        tabs.forEach(t => t.classList.remove('active'));
        
        tab.classList.add('active');
    
        const activeTab = tab.getAttribute('data-tab');
        console.log(`Переход к ${activeTab}`);
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const otabs = document.querySelectorAll('.info-order');
    const orderCont = document.querySelectorAll('.order-content');

    otabs.forEach(tab => {
        tab.addEventListener('click', function () {
            const target = this.getAttribute('data-tab');
            console.log(`Клик по вкладке: ${target}`); 

            otabs.forEach(t => t.classList.remove('active'));
            orderCont.forEach(c => c.classList.remove('active'));

            this.classList.add('active');
            const orderTab = document.getElementById(target);
            console.log(orderTab); 

            if (orderTab) {
                orderTab.classList.add('active');
            }
        });
    });
});

const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const modal = document.getElementById('review-modal');
    const openModalButtons = document.querySelectorAll('.open-modal');
    const closeModalButton = document.querySelector('.close');

    openModalButtons.forEach(button => {
        button.addEventListener('click', function () {
            const orderId = button.getAttribute('data-order-id');
            document.getElementById('order-id').value = orderId;
            modal.style.display = 'block';
        });
    });

    closeModalButton.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    const reviewForm = document.getElementById('review-form');
    reviewForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(reviewForm);
        formData.append('csrfmiddlewaretoken', csrfToken);  

        fetch('/leave-review/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                modal.style.display = 'none';
                location.reload(); 
            } else {
                alert('Ошибка отправки отзыва');
            }
        })
        .catch(error => {
            alert('Ошибка отправки отзыва');
        });
    });


document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.info-saide');
    const tabContents = document.querySelectorAll('.tab-content');

    function showTab(tabId) {
        // Скрыть все вкладки
        tabContents.forEach(tab => {
            tab.style.display = 'none';
        });
        
       
        const activeTab = document.getElementById(tabId);
        if (activeTab) {
            activeTab.style.display = 'block'; 
        }
    }

   
    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            const tabId = this.getAttribute('data-tab');
            showTab(tabId);
        });
    });

    showTab('profile');
});

flatpickr("#datePicker", {
    // Настройка тем
    onReady: function(selectedDates, dateStr, instance) {
        const calendarContainer = instance.calendarContainer;

        // Примените ваши стили
        calendarContainer.style.backgroundColor = '#f0f0f0'; // Цвет фона
        calendarContainer.style.color = '#333'; // Цвет текста
    },
    // Можно добавить и другие параметры для стилизации
   
    locale: "ru",                 // Установка языка на русский
    firstDayOfWeek: 1,           // Установка начала недели с понедельника
    dateFormat: "Y-m-d",          // Формат даты
    allowInput: true              // Позволить ввод вручную
    });


document.querySelectorAll('.star').forEach(star => {
    star.addEventListener('click', function() {
        const value = this.getAttribute('data-value');
        
        // Обновляем значение скрытого инпута
        document.getElementById('stars-input').value = value;

        // Обновляем отображение звезд
        updateStars(value);
    });
});

function updateStars(selectedValue) {
    document.querySelectorAll('.star').forEach(star => {
        if (parseInt(star.getAttribute('data-value')) <= selectedValue) {
            star.classList.add('selected');
        } else {
            star.classList.remove('selected');
        }
    });
}

document.querySelector('.close').addEventListener('click', function() {
    document.querySelectorAll('.star').forEach(star => {
        star.classList.remove('selected');
    });
    document.getElementById('stars-input').value = '';  
});


function deleteAvatar() {
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = '';  
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    var csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    var deleteInput = document.createElement('input');
    deleteInput.type = 'hidden';
    deleteInput.name = 'delete-avatar';
    form.appendChild(deleteInput);

    document.body.appendChild(form);
    form.submit();
}