<script>
// use composition api
//import { ref } from "vue";
//import posts from "./posts.json";
import NavBar from "@/components/NavBar.vue";
import "@/assets/styles/style.css";
import { login_state } from "@/login_state.js";
import { useFetch } from "@/components/useFetch.vue";

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      isAuthenticated: this.$auth0.isAuthenticated,
      isLoading: this.$auth0.isLoading,
      auth0_user: this.$auth0.user,
      login_state,
      fetch_1: null,
    };
  },
  methods: {
    async getAccessToken() {
      let token;
      if (this.isAuthenticated) {
        token = await this.$auth0.getAccessTokenSilently();
        this.login_state.token = token;
        // console.log(token);
        const requestOptions = {
          method: "GET",
          headers: { "Content-Type": "application/json", Authorization: token },
        };
        fetch("/api/who_am_i", requestOptions)
          .then((response) => response.json())
          .then((data) => {
            // console.log(data);
            this.login_state.logged_in = true;
            this.login_state.username = data.username;
            this.login_state.user_id = data.user_id;
            this.login_state.admin = data.admin;
            this.login_state.avatar = data.avatar;
            console.log(login_state);
          });
      }
      //console.log(token);
      return token;
    },
    useFetch,
  },
  watch: {
    // whenever question changes, this function will run
    isLoading(newVal) {
      if (!newVal) {
        console.log("auth0 loaded");
        if (this.isAuthenticated) {
          this.login_state.logged_in = true;
          // the auth0 username will usually be correct, this just speeds up load
          this.login_state.username = this.auth0_user["nickname"];
          this.login_state.username = this.getAccessToken();
        }
      }
    },
  },
};
/*fetch("/api/v1/post/unnapproved")
  .then((response) => response.json())
  .then((data) => console.log(data));
    async logAccessToken() {
      let token;
      if (this.isAuthenticated) {
        token = await this.$auth0.getAccessTokenSilently();
      }
      console.log(token);
    },
  watch: {
    // whenever question changes, this function will run
    isLoading(newVal, oldVal) {
      console.log("loadstate" + String(this.isLoading));
      if (!newVal) {
        console.log("auth0 loaded");
        this.logAccessToken();
      }
    },
  },
  mounted() {
    console.log("Initialise auth0 load" + String(this.isLoading));
  },
        isAuthenticated: this.$auth0.isAuthenticated,
      isLoading: this.$auth0.isLoading,
*/
</script>

<template>
  <link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css"
    rel="stylesheet"
    integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT"
    crossorigin="anonymous"
  />
  <header>
    <nav-bar />
    <router-view />
  </header>
</template>
