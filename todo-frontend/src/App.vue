<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">To-Do List</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link active" aria-current="page" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/about">About</router-link>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="true">
              Tasks
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="#">Completed Task</a></li>
              <li><a class="dropdown-item" href="#">Uncompleted Tasks</a></li>
            </ul>
          </li>
          <li class="nav-item">
            <a class="nav-link disabled" aria-disabled="false">Disabled</a>
          </li>
        </ul>
        <form class="d-flex" role="search">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
        <button v-if="isLoggedIn" class="btn btn-danger ms-3" @click="logout">Logout</button>
      </div>
    </div>
  </nav>
  <router-view/>
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: false  // Correctly return an object
    };
  },
  created() {
    if (localStorage.getItem('token')) {
      this.isLoggedIn = true;  // Use 'this' to refer to the data property
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.isLoggedIn = false;  // Update the state after logout
      this.$router.push('/login');  // Use Vue Router for navigation
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

nav a {
  font-weight: bold;
  color: #005ebc;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
