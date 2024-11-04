// Log page view event on load
window.onload = () => {
    logEvent('page_view');
};

// Function to log events
function logEvent(eventType) {
    fetch('/log_event', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ page: window.location.pathname, eventType: eventType })
    }).then(response => response.json())
      .then(data => console.log(data));
}
