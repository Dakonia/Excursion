// Инициализация Flatpickr для выбора даты
flatpickr("#order-date", {
    locale: "ru",                // Локализация на русский
    dateFormat: "Y-m-d",         // Формат даты (год-месяц-день)
    allowInput: true,            // Разрешить ручной ввод
    defaultDate: new Date(),     // Текущая дата по умолчанию
    onChange: function (selectedDates, dateStr) {
        document.getElementById('order-date').value = dateStr;
    }
});

document.querySelectorAll('.book-bus').forEach(button => {
    button.addEventListener('click', function () {
        const busId = this.getAttribute('data-bus-id'); 
        document.getElementById('order-modal').style.display = 'block'; 

        
        fetch(`/bus_details/${busId}/`) 
            .then(response => response.json())
            .then(data => {                               
                document.getElementById('bus-name').textContent = data.name;

                
                const busImage = document.getElementById('bus-image');
                if (data.image_url) {
                   
                    if (data.image_url.startsWith('/')) {
                        busImage.src = data.image_url; 
                    } else {
                        busImage.src = `/media/${data.image_url}`; 
                    }
                    busImage.alt = data.name; 
                } else {
                   
                    busImage.src = '/media/static/media/company/bus.jpg';
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Не удалось загрузить данные о автобусе.');
            });

       
        document.getElementById('order-form').onsubmit = function (event) {
            event.preventDefault(); 

            const orderDate = document.getElementById('order-date').value;
            const description = document.getElementById('order-description').value;

           
            if (!orderDate) {
                alert("Пожалуйста, выберите дату заказа.");
                return;
            }

    
            fetch(`/calculate_cost/${busId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    order_date: orderDate,
                    description: description,
                }),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                document.getElementById('order-modal').style.display = 'none'; 
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при отправке данных.');
            });
        };
    });
});

document.getElementById('close-modal').addEventListener('click', () => {
    document.getElementById('order-modal').style.display = 'none';
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
