document.addEventListener('DOMContentLoaded', function () {
    // Efecto hover en las tarjetas
    const cards = document.querySelectorAll('.dashboard-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
            card.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.12)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.08)';
        });
    });

    // 
    console.log("Dashboard cargado correctamente.");

    // canvas para gráficas, activar esto:
    /*
    const ctx = document.getElementById('myFinancialChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Seguro 1', 'Seguro 2'],
                datasets: [{
                    label: 'Costo',
                    data: [5000, 3000],
                    backgroundColor: ['#007bff', '#28a745']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' },
                    title: { display: true, text: 'Ejemplo de gráfica' }
                }
            }
        });
    }
    */
});
