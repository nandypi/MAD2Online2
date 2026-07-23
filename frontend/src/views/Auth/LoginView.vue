<template>
    <h1>Login Page</h1>
    <p>Enter your credentials to log in...</p>

    <RouterLink to="/register">Don't have an account? Register here!</RouterLink>
    <br>
    <RouterLink to="/">Back to Home</RouterLink>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>