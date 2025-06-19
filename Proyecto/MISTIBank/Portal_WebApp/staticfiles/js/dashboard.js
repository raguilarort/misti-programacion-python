document.addEventListener('DOMContentLoaded', function() {
    // Datos de ejemplo para el gráfico (simulados)
    const data = {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        datasets: [
            {
                label: 'Ingresos',
                data: [12000, 13500, 11000, 14000, 15000, 16000],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                tension: 0.3
            },
            {
                label: 'Gastos',
                data: [7000, 8500, 6000, 9000, 8000, 9500],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: true,
                tension: 0.3
            }
        ]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Resumen Mensual de Ingresos y Gastos'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Monto ($)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Mes'
                    }
                }
            }
        }
    };

    // Renderizar el gráfico
    const myChart = new Chart(
        document.getElementById('myFinancialChart'),
        config
    );

    // Aquí podrías agregar más lógica JavaScript para:
    // - Cargar datos reales de la cuenta del usuario vía AJAX (Django views)
    // - Manejar la interactividad de los menús (si no usas directamente la navegación)
    // - Actualizar las estadísticas en tiempo real (websockets si es necesario)
});