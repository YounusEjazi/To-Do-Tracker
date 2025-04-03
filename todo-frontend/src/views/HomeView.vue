<template>
  <div class="home container py-5">
    <div class="row justify-content-center">
      <div class="col-md-10">

        <!-- Header -->
        <div class="text-center mb-5">
          <h2 class="fw-bold text-primary">📝 Smart To-Do List</h2>
          <p class="text-muted">Manage tasks with priorities, deadlines, tags, subtasks and more.</p>
        </div>

        <!-- Task Creation -->
        <div class="card mb-4 shadow">
          <div class="card-body">
            <div class="row g-2 align-items-center">
              <div class="col-md-4">
                <input v-model="todo" type="text" class="form-control" placeholder="Enter task..." />
              </div>
              <div class="col-md-2">
                <select v-model="priority" class="form-select">
                  <option disabled value="">Priority</option>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
              <div class="col-md-3">
                <input v-model="dueDate" type="date" class="form-control" />
              </div>
              <div class="col-md-3">
                <input v-model="tags" type="text" class="form-control" placeholder="Tags (comma-separated)" />
              </div>
            </div>
            <div class="mt-3">
              <textarea v-model="description" class="form-control" placeholder="Description (optional)"></textarea>
              <button class="btn btn-primary mt-2" @click="createTodo">Add</button>
            </div>
          </div>
        </div>

        <!-- Task List -->
        <div class="card shadow">
          <div class="card-header d-flex justify-content-between">
            <span class="fw-bold">Your Tasks</span>
            <span class="text-muted">Click to mark as complete</span>
          </div>
          <ul class="list-group list-group-flush">
            <li
              v-for="todo in todos"
              :key="todo.uuid"
              class="list-group-item"
              :class="{ 'text-decoration-line-through text-muted': todo.is_completed }"
            >
              <div class="d-flex justify-content-between align-items-start w-100">
                <div @click="() => updateTodo(todo)" style="cursor: pointer;" class="flex-grow-1">
                  <div class="fw-bold">{{ todo.todo_name }}</div>
                  <small v-if="todo.due_date">📅 {{ new Date(todo.due_date).toLocaleDateString() }}</small>
                  <div v-if="todo.description" class="text-muted small">{{ todo.description }}</div>
                </div>

                <div class="text-end ms-2">
                  <!-- Priority Badge -->
                  <span class="badge me-1" :class="{
                    'bg-danger': todo.priority === 'high',
                    'bg-warning text-dark': todo.priority === 'medium',
                    'bg-info text-dark': todo.priority === 'low'
                  }">
                    {{ todo.priority }}
                  </span>

                  <!-- Toggle Status -->
                  <span class="badge me-1" :class="{
                    'bg-success': todo.is_completed,
                    'bg-secondary': !todo.is_completed
                  }">
                    {{ todo.is_completed ? 'Done' : 'Pending' }}
                  </span>

                  <!-- Tags -->
                  <span
                    v-if="todo.tags?.length"
                    class="badge bg-secondary"
                  >{{ todo.tags.join(', ') }}</span>

                  <!-- Priority Edit -->
                  <select class="form-select form-select-sm d-inline-block w-auto ms-2"
                    v-model="todo.priority"
                    @change="changePriority(todo)"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>

                  <!-- Delete Button -->
                  <button class="btn btn-sm btn-outline-danger ms-2" @click="deleteTodo(todo.uuid)">
                    ❌
                  </button>
                </div>
              </div>
            </li>

            <li
              v-if="todos.length === 0"
              class="list-group-item text-center text-muted"
            >
              No tasks yet. Start by adding one!
            </li>
          </ul>
        </div>

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
      description: "",
      priority: "medium",
      dueDate: "",
      tags: "",
      todos: []
    };
  },
  created() {
    this.getTodos();
  },
  methods: {
    getAuthHeaders() {
      return {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`
      };
    },
    getTodos() {
      fetch("http://127.0.0.1:8000/api/todo/", {
        headers: this.getAuthHeaders()
      })
        .then(res => res.json())
        .then(res => {
          this.todos = res.data || [];
        })
        .catch(err => console.error(err));
    },
    createTodo() {
      if (!this.todo.trim()) return;
      fetch("http://127.0.0.1:8000/api/todo/", {
        method: "POST",
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          todo_name: this.todo,
          description: this.description,
          priority: this.priority,
          due_date: this.dueDate || null,
          tags: this.tags.split(',').map(t => t.trim()).filter(Boolean)
        })
      })
        .then(res => res.json())
        .then(res => {
          if (res.data) {
            this.todos.push(res.data);
            this.todo = "";
            this.description = "";
            this.priority = "medium";
            this.dueDate = "";
            this.tags = "";
          }
        })
        .catch(err => console.error(err));
    },
    updateTodo(todo) {
      fetch(`http://127.0.0.1:8000/api/todo/${todo.uuid}/`, {
        method: "PATCH",
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ is_completed: !todo.is_completed })
      })
        .then(() => {
          todo.is_completed = !todo.is_completed;
        })
        .catch(err => console.error(err));
    },
    changePriority(todo) {
      fetch(`http://127.0.0.1:8000/api/todo/${todo.uuid}/`, {
        method: "PATCH",
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ priority: todo.priority })
      }).catch(err => console.error(err));
    },
    deleteTodo(uuid) {
      if (!confirm("Delete this task?")) return;
      fetch(`http://127.0.0.1:8000/api/todo/${uuid}/`, {
        method: "DELETE",
        headers: this.getAuthHeaders()
      })
        .then(() => {
          this.todos = this.todos.filter(t => t.uuid !== uuid);
        })
        .catch(err => console.error(err));
    }
  }
};
</script>

<style scoped>
input::placeholder, textarea::placeholder {
  opacity: 0.65;
}
.list-group-item {
  transition: background-color 0.2s ease-in-out;
}
.list-group-item:hover {
  background-color: #f8f9fa;
}
</style>
