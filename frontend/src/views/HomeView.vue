<script setup>
// import TheWelcome from '../components/TheWelcome.vue'
import { RouterLink } from 'vue-router'

function getBackendMessage() {
  alert('function is working on click')
  fetch('http://127.0.0.1:5000/api/greet')
    .then(response => response.json())
    .then(data => {
      document.getElementById('message').innerText = data.message;
    })
    .catch(error => {
      console.error('Error fetching message:', error);
    });
}

</script>

<template>
  <!-- <main>
    <TheWelcome />
  </main> -->
  <h1>Welcome to My Mad2 APP</h1>

  <div id="message">message will be shown here...</div>
  <button @click="getBackendMessage">Click to get message from backend!</button>

  <br><br>

  <RouterLink to="/about">View more About US</RouterLink>

  <br><br>

  <RouterLink to="/register">Create an Account!</RouterLink>
  <br>
  <RouterLink to="/login">Already have an account? Login here!</RouterLink>

</template>
