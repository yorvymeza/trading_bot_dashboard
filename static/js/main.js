/*
 * Archivo: main.js
 * Descripción: Funciones JavaScript principales para la interfaz del Trading Bot.
 *
 * Este archivo gestionará interacciones del lado del cliente como:
 * 1. Actualización en tiempo real del estado.
 * 2. Manejo de notificaciones (toasts).
 * 3. Lógica compleja de formularios o gráficos (si se implementan).
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log("Trading Bot Dashboard - JavaScript cargado.");

    // ===============================================
    // 1. Manejo del Dropdown de Período en Historia
    // Esto asegura que el menú desplegable funcione sin Tailwind JS
    // ===============================================
    const periodoBtn = document.getElementById('periodo-btn');
    const periodoMenu = document.getElementById('periodo-menu');

    if (periodoBtn && periodoMenu) {
        periodoBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Evita que el click se propague al documento
            periodoMenu.classList.toggle('hidden');
        });

        // Ocultar el menú si se hace clic fuera
        document.addEventListener('click', (e) => {
            if (!periodoBtn.contains(e.target) && !periodoMenu.contains(e.target)) {
                periodoMenu.classList.add('hidden');
            }
        });
    }


    // ===============================================
    // 2. Función de Notificación (Simulada)
    // Para mostrar mensajes de éxito o error.
    // ===============================================

    /**
     * Muestra una notificación temporal (toast).
     * @param {string} message - El mensaje a mostrar.
     * @param {string} type - 'success' o 'error'.
     */
    function showNotification(message, type = 'success') {
        const notificationArea = document.querySelector('.notification-area') || document.createElement('div');
        if (!document.querySelector('.notification-area')) {
            notificationArea.className = 'notification-area fixed bottom-5 right-5 z-50 space-y-2';
            document.body.appendChild(notificationArea);
        }

        const toast = document.createElement('div');
        toast.textContent = message;
        toast.className = `p-4 rounded-lg shadow-xl text-white font-semibold transform transition-all duration-300 ease-out 
                           ${type === 'success' ? 'bg-green-600' : 'bg-red-600'}`;
        
        notificationArea.appendChild(toast);

        // Ocultar y remover después de 3 segundos
        setTimeout(() => {
            toast.classList.add('opacity-0', 'translate-x-full');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    // Ejemplo de uso (después de una operación manual exitosa)
    // showNotification("Entrada ejecutada con éxito.", "success");


    // ===============================================
    // 3. Simulación de Live Data/Polling
    // Esto se reemplazaría por una conexión WebSocket real, pero simula
    // una actualización periódica (ej. cada 5 segundos) para el balance.
    // ===============================================
    /*
    function pollBotData() {
        // En una aplicación real, esto haría una petición AJAX a una ruta de Flask
        // (ej. '/api/status') para obtener el balance, estado del bot, etc.
        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                // Actualizar elementos de la interfaz
                // document.getElementById('current-balance').textContent = data.balance;
                // ...
            })
            .catch(error => console.error('Error al obtener el estado del bot:', error));
    }
    
    // Iniciar el polling si el bot está activo (o siempre, para el balance)
    // setInterval(pollBotData, 5000);
    */
});