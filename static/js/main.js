
function submitApplication(offerId) {
    const applicationData = {
        offer_id: offerId,
    };

    fetch(`/api/applications/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), 
        },
        body: JSON.stringify(applicationData),
    })
    .then(response => {
        if (response.ok) {
            alert('Application submitted successfully!');
        } else {
            alert('Failed to submit application. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}

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

function initializeCharts(data) {
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: '# of Offers',
                data: data.values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function fetchChartData() {
    fetch('/api/dashboard/statistics/')
    .then(response => response.json())
    .then(data => {
        initializeCharts(data);
    })
    .catch(error => {
        console.error('Error fetching chart data:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('myChart')) {
        fetchChartData();
    }
});