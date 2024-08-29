<template>
  <div class="home">
    <div class="col-md-6 mx-auto">
      <div class="form-group d-flex">
        <input
          class="form-control"
          v-model="todo"
          placeholder="Enter todo"
          type="text"
        />
        <button class="btn btn-success" @click="createTodo">Create</button>
      </div>
      <ul class="list-group mt-4">
        <li @click="updateTodo(todo.uuid, todo.is_completed)" v-for="todo in todos" :key="todo.uuid" class="list-group-item">
          <strike v-if="todo.is_completed">
            {{ todo.todo_name }}
          </strike>
          <p v-else> {{ todo.todo_name }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  data() {
    return {
      todo: "",
      todos: [], // Store fetched todos here
    };
  },
  created() {
    this.getTodos(); // Fetch the todos when the component is created
  },
  methods: {
    updateTodo(uuid, is_completed) {
  const token = localStorage.getItem("token");

  const requestOptions = {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`, // Correct authorization header
    },
    body: JSON.stringify({ uuid: uuid, is_completed: !is_completed }), // Toggle the completed state
  };

  fetch(`http://127.0.0.1:8000/api/todo/${uuid}/`, requestOptions) // Use uuid in URL for PATCH
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log("Updated todo:", data); // Log the updated todo data
      
      // Manually update the todo in the local `todos` array
      const index = this.todos.findIndex(todo => todo.uuid === uuid);
      if (index !== -1) {
        this.todos[index].is_completed = !is_completed; // Toggle the completed state in the UI
      }
    })
    .catch(error => {
      console.error("Error updating todo:", error); // Log any errors that occur
    });
},


    getTodos() {
      const token = localStorage.getItem("token");
      console.log("Token for GET request:", token); // Log the token to ensure it's correct

      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // Correct authorization header
        },
      };

      fetch("http://127.0.0.1:8000/api/todo/", requestOptions)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          this.todos = data.data || data; // Assign fetched todos to the todos array
          console.log("Fetched todos:", this.todos); // Log the fetched todos
        })
        .catch((error) => {
          console.error("Error fetching todos:", error);
        });
    },

    createTodo() {
      const token = localStorage.getItem("token");
      console.log("Token for POST request:", token); // Log the token to ensure it's correct

      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // Correct authorization header
        },
        body: JSON.stringify({ todo_name: this.todo }),
      };

      fetch("http://127.0.0.1:8000/api/todo/", requestOptions)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          console.log("Created todo:", data); // Log the created todo
          this.todos.push(data.data || data); // Add the new todo to the todos array
          this.todo = ""; // Clear the input field after creating the todo
        })
        .catch((error) => {
          console.error("Error creating todo:", error);
        });
    },
  },
};
</script>
