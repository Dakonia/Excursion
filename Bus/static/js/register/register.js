const clientBut = document.getElementById('client-btn');
const companyBut = document.getElementById('company-btn');
const regClient = document.getElementById('client-form');
const regCompany = document.getElementById('company-form');


clientBut.addEventListener('click', function(){
    regClient.style.display = 'block';
    regCompany.style.display = 'none';
});

companyBut.addEventListener('click', function(){
    regClient.style.display ='none';
    regCompany.style.display = 'block';
});