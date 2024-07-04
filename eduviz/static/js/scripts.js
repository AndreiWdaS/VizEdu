/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('graph-form').addEventListener('submit', function(event) {
        var submitButton = document.getElementById('submit-button');
        var loadingButton = document.getElementById('loading-button');

        // Troca os botões
        submitButton.style.display = 'none';
        loadingButton.style.display = 'inline-block';

        // Opcional: Se o formulário estiver sendo enviado via AJAX
        // event.preventDefault(); // Impede o envio do formulário para teste
        // Simulação de uma ação assíncrona
        /*
        setTimeout(function() {
            // Reverter os botões após a ação ser concluída
            loadingButton.style.display = 'none';
            submitButton.style.display = 'inline-block';
        }, 3000); // Esconde o botão de carregamento após 3 segundos
        */
    });
});