document.addEventListener('DOMContentLoaded', function () {

    // Lógica para o menu móvel (hambúrguer)
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Lógica para fechar as mensagens de notificação
    const closeButtons = document.querySelectorAll('.close-message');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.parentElement;
            message.style.display = 'none';
        });
    });

});
