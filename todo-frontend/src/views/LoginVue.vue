<template>
    <div class="about">
      <div class="col-6 mx-auto">
        <form @submit.prevent="submit">
          <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label">Username</label>
            <input
              type="text"
              v-model="username"
              class="form-control"
              id="exampleInputEmail1"
              aria-describedby="emailHelp"
            />
            {{ username }}
          </div>
          <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label">Password</label>
            <input
              type="password"
              v-model="password"
              class="form-control"
              id="exampleInputPassword1"
            />
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      async submit() {
        console.log(this.username);
        console.log(this.password);
  
        if (!this.username) {
          alert('Fill username');
          return;
        }
  
        if (!this.password) {
          alert('Fill password');
          return;
        }
  
        const requestOptions = {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username: this.username, password: this.password }),
        };
  
        try {
          const response = await fetch('http://127.0.0.1:8000/api/token/', requestOptions);
          if (!response.ok) {
            const errorMessage = `Network response was not ok: ${response.status} ${response.statusText}`;
            throw new Error(errorMessage);
          }
          const data = await response.json();
          console.log(data.access);
          localStorage.setItem('token', data.access);
          window.location.href = '/';
        } catch (error) {
          console.error('There was a problem with the fetch operation:', error);
          alert('Login failed. Please try again.');
        }
      },
    },
  };
  </script>
  