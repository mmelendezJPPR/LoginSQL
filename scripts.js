// Add some interactive effects
        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.parentElement.style.transform = 'scale(1.02)';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.parentElement.style.transform = 'scale(1)';
            });
        });

        // Form submission handler
        document.querySelector('form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const button = document.querySelector('.login-button');
            const originalText = button.textContent;
            
            button.textContent = 'Iniciando...';
            button.style.background = '#95a5a6';
            
            setTimeout(() => {
                button.textContent = originalText;
                button.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                alert('Demo: Funcionalidad de login simulada');
            }, 2000);
        });

        // Create more floating particles dynamically
        const shapes = document.querySelector('.floating-shapes');
        for(let i = 0; i < 5; i++) {
            const shape = document.createElement('div');
            shape.style.left = Math.random() * 100 + '%';
            shape.style.width = (Math.random() * 60 + 40) + 'px';
            shape.style.height = shape.style.width;
            shape.style.animationDelay = -(Math.random() * 15) + 's';
            shape.style.animationDuration = (Math.random() * 10 + 10) + 's';
            shapes.appendChild(shape);
        }