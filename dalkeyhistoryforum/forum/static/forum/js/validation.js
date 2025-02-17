/*
 * Listen for click events on the submit button on the form for posting/editing
 * a comment. Make a call to the profanity API and block submission if found.
 */
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#postForm'); 
    const messageInput = document.querySelector('#id_content'); 
    const errorMessage = document.createElement('p');
    errorMessage.style.color = 'red';
    errorMessage.style.display = 'none';
    form.appendChild(errorMessage);
  
    form.addEventListener('submit', async function (event) {
      console.log("test");  
      event.preventDefault(); // This prevents the form from submitting
  
      const message = messageInput.value;
  
      try {
        const res = await fetch('https://vector.profanity.dev', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message }),
        });
  
        const data = await res.json();
  
        if (data.isProfanity) {
          errorMessage.textContent = 'Your message contains inappropriate language. Please remove it and try again.';
          errorMessage.style.display = 'block';
        } else {
          errorMessage.style.display = 'none';
          form.submit(); // This submits the form if no profanity is found
        }
      } catch (error) {
        console.error('Error:', error);
        errorMessage.textContent = 'An error occurred while checking the message. Please try again later.';
        errorMessage.style.display = 'block';
      }
    });
  });