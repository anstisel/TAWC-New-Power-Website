<template>
  <form @submit.prevent="login">
    <h3>Login</h3>
    <div class="form-group">
      <label>Username</label>
      <input
        type="text"
        class="form-control"
        placeholder="username"
        v-model="this.username"
      />
    </div>
    <button class="btn btn-primary btn-block">Login</button>
  </form>
</template>

<script>
import { login_state } from "@/login_state.js";

const login = function () {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  };
  fetch("/api/user_id/" + this.username, requestOptions)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      login_state.username = this.username;
      login_state.user_id = data.id;
    });
  login_state.username = this.username;
  console.log(login_state.username);
  console.log(login_state.user_id);
};

export default {
  data() {
    return {
      username: "",
      login_state,
    };
  },
  methods: {
    login,
  },
  mounted() {
    console.log(login_state.username);
  },
};
</script>
