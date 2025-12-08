// This file contains the main JavaScript functionality for the application.

// Function to handle the submission of internship applications
function submitApplication(offerId) {
    const applicationData = {
        offer_id: offerId,
        // Additional data can be added here
    };

    fetch(`/api/applications/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // CSRF token for security
        },
        body: JSON.stringify(applicationData),
    })
    .then(response => {
        if (response.ok) {
            alert('Application submitted successfully!');
            // Optionally redirect or update the UI
        } else {
            alert('Failed to submit application. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to initialize charts on the dashboard
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

// Example of fetching data for charts
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

// Call fetchChartData on page load for the dashboard
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('myChart')) {
        fetchChartData();
    }
});