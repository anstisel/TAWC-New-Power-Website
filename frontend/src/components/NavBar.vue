<template>
  <header>
    <b-navbar style="padding: 0px 12%" class="topnav" toggleable="sm">
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-navbar-brand href="https://theanimalwelfarecollaborative.org/">
        <img
          src="@/assets/TAWClogo.png"
          style="width: 112px; height: 56px"
          alt="TAWC Logo"
        />
      </b-navbar-brand>

      <b-collapse id="nav-collapse" is-nav class="space">
        <b-navbar-nav>
          <b-nav-item to="/">Homepage</b-nav-item>

          <b-nav-item to="/discussion-board">Discussion</b-nav-item>

          <b-nav-item v-if="login_state.admin" to="/admin">Admin</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav>
          <div v-if="isAuthenticated">
            <b-nav-item-dropdown
              id="my-nav-dropdown"
              :text="user.nickname"
              toggle-class="nav-link-custom"
            >
              <b-dropdown-item to="/profile-page">Profile</b-dropdown-item>

              <b-dropdown-item @click="logout">Logout</b-dropdown-item>
            </b-nav-item-dropdown>
          </div>
          <div v-else>
            <b-nav-item @click="login">Login</b-nav-item>
          </div>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </header>
</template>

<script>
import { login_state } from "@/login_state.js";

export default {
  data() {
    return {
      login_state,
      user: this.$auth0.user,
      isAuthenticated: this.$auth0.isAuthenticated,
    };
  },
  methods: {
    logout() {
      this.$auth0.logout({ returnTo: window.location.origin });
    },
    login() {
      this.$auth0.loginWithRedirect();
    },
  },
};
</script>
