// Script principal para el Diario Emocional

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Animación para los botones de emoji
    const emojiButtons = document.querySelectorAll('.emoji-btn');
    if (emojiButtons) {
        emojiButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Añadir una pequeña animación al seleccionar
                this.classList.add('selected');
                setTimeout(() => {
                    this.classList.remove('selected');
                }, 300);
                
                // Mostrar feedback visual
                const feedbackText = document.getElementById('emoji-feedback');
                if (feedbackText) {
                    const emojiLabel = this.querySelector('.emoji-label').textContent;
                    feedbackText.textContent = `Has seleccionado: ${emojiLabel}`;
                    feedbackText.style.opacity = 1;
                    setTimeout(() => {
                        feedbackText.style.opacity = 0;
                    }, 2000);
                }
            });
        });
    }
    
    // Mejorar accesibilidad de formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const requiredInputs = form.querySelectorAll('[required]');
        requiredInputs.forEach(input => {
            input.addEventListener('invalid', function(e) {
                e.preventDefault();
                this.classList.add('is-invalid');
                
                // Crear mensaje de error si no existe
                let errorDiv = this.nextElementSibling;
                if (!errorDiv || !errorDiv.classList.contains('invalid-feedback')) {
                    errorDiv = document.createElement('div');
                    errorDiv.className = 'invalid-feedback';
                    errorDiv.textContent = 'Este campo es obligatorio';
                    this.parentNode.insertBefore(errorDiv, this.nextSibling);
                }
            });
            
            input.addEventListener('input', function() {
                if (this.validity.valid) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });
    });
    
    // Rotación de consejos para el bienestar
    const tips = [
        {
            icon: 'bi-brightness-high text-warning',
            text: 'Dedica 5 minutos al día para practicar la respiración consciente.'
        },
        {
            icon: 'bi-heart-pulse text-danger',
            text: 'El ejercicio físico libera endorfinas que mejoran tu estado de ánimo.'
        },
        {
            icon: 'bi-cup-hot text-success',
            text: 'Tómate un momento para ti mismo/a cada día, aunque sea breve.'
        },
        {
            icon: 'bi-chat-dots text-primary',
            text: 'Hablar sobre tus emociones con alguien de confianza puede ayudarte a procesarlas.'
        },
        {
            icon: 'bi-journal-text text-info',
            text: 'Escribir regularmente en tu diario te ayuda a entender mejor tus patrones emocionales.'
        },
        {
            icon: 'bi-music-note-beamed text-success',
            text: 'La música puede cambiar tu estado de ánimo. Crea una playlist con canciones que te hagan sentir bien.'
        },
        {
            icon: 'bi-tree text-success',
            text: 'Pasar tiempo en la naturaleza puede reducir el estrés y mejorar tu bienestar emocional.'
        },
        {
            icon: 'bi-book text-primary',
            text: 'La lectura es una excelente forma de desconectar y reducir la ansiedad.'
        }
    ];
    
    const tipCarousel = document.querySelector('.tip-carousel');
    if (tipCarousel) {
        let currentTip = 0;
        
        // Función para cambiar el consejo
        function rotateTip() {
            const tip = tips[currentTip];
            const tipHTML = `
                <div class="tip-item">
                    <i class="bi ${tip.icon}"></i>
                    <p>${tip.text}</p>
                </div>
            `;
            
            // Aplicar fade out
            tipCarousel.style.opacity = 0;
            
            // Cambiar el contenido después de la transición
            setTimeout(() => {
                tipCarousel.innerHTML = tipHTML;
                tipCarousel.style.opacity = 1;
                
                // Incrementar el índice para el próximo consejo
                currentTip = (currentTip + 1) % tips.length;
            }, 500);
        }
        
        // Iniciar la rotación de consejos
        setInterval(rotateTip, 8000);
        
        // Permitir cambio manual con botón
        const nextTipBtn = document.getElementById('nextTipBtn');
        if (nextTipBtn) {
            nextTipBtn.addEventListener('click', function() {
                currentTip = (currentTip + 1) % tips.length;
                rotateTip();
            });
        }
    }
    
    // Añadir animaciones de entrada
    const fadeElements = document.querySelectorAll('.fade-in');
    if (fadeElements.length > 0) {
        fadeElements.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add('visible');
            }, 100 * index);
        });
    }
    
    // Mejorar accesibilidad con teclas
    document.addEventListener('keydown', function(e) {
        // Presionar Alt+N para nueva entrada
        if (e.altKey && e.key === 'n') {
            const newEntryLink = document.querySelector('a[href*="new_entry"]');
            if (newEntryLink) newEntryLink.click();
        }
        
        // Presionar Alt+H para ir a inicio
        if (e.altKey && e.key === 'h') {
            const homeLink = document.querySelector('a[href*="dashboard"]');
            if (homeLink) homeLink.click();
        }
    });
});
