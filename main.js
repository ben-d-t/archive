function loadSidebar() {
  fetch('sidebar.txt')
    .then(response => response.text())
    .then(data => {
      document.getElementById('sidebar').innerHTML = data;
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
loadSidebar();

function loadFooter() {
  fetch('footer.txt')
    .then(response => response.text())
    .then(data => {
      document.getElementById('footer_content').innerHTML = data;
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
loadFooter();
