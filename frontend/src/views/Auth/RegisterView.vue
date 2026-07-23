<template>
    <h1>Register Page</h1>
    <p>Give your details to create an account...</p>

    <RouterLink to="/login">Already have an account? Login here!</RouterLink>
    <br>
    <RouterLink to="/">Back to Home</RouterLink>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>