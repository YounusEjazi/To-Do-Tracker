<template>
  <div class="home container py-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">

        <!-- Header -->
        <div class="text-center mb-4">
          <h2 class="fw-bold text-primary">📝 My To-Do List</h2>
          <p class="text-muted mb-0">Stay organized. Stay productive.</p>
        </div>

        <!-- Input Section -->
        <div class="input-group shadow-sm mb-4">
          <input
              v-model="todo"
              type="text"
              class="form-control form-control-lg"
              placeholder="What needs to be done?"
          />
          <button class="btn btn-primary btn-lg" @click="createTodo">
            Add
          </button>
        </div>

        <!-- Task List -->
        <ul class="list-group shadow rounded overflow-hidden">
          <li
              v-for="todo in todos"
              :key="todo.uuid"
              class="list-group-item d-flex justify-content-between align-items-center"
              :class="{ 'text-muted text-decoration-line-through bg-light': todo.is_completed }"
              @click="updateTodo(todo.uuid, todo.is_completed)"
              style="cursor: pointer;"
          >
            <span class="flex-grow-1 me-3">
              {{ todo.todo_name }}
            </span>
            <span class="badge rounded-pill"
                  :class="todo.is_completed ? 'bg-success' : 'bg-warning text-dark'">
              {{ todo.is_completed ? 'Done' : 'Pending' }}
            </span>
          </li>
          <li
              v-if="todos.length === 0"
              class="list-group-item text-center text-muted bg-light"
          >
            No tasks yet. Start by adding one above!
          </li>
        </ul>
      </div>
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


<style scoped>
input::placeholder {
  opacity: 0.65;
}

.list-group-item {
  transition: background-color 0.2s ease-in-out;
}

.list-group-item:hover {
  background-color: #f8f9fa;
}
</style>

